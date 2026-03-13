#!/usr/bin/env python3
"""
Workbook Build Script
=====================
Reads JSON data files from data/ and generates Typst source files
in sections/, then compiles the full workbook to PDF.

Usage:
    python build.py              # generate .typ files + compile PDF
    python build.py --generate   # generate .typ files only
    python build.py --compile    # compile only (assumes .typ files exist)
"""

import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
SECTIONS_DIR = SCRIPT_DIR / "sections"
OUTPUT_DIR = SCRIPT_DIR / "output"


# ===========================================================
# Typst Code Generation
# ===========================================================

def escape_typst(text: str) -> str:
    """Escape special Typst characters in prose text (content mode)."""
    import re

    # Convert **bold** to Typst #strong[bold]
    text = re.sub(r'\*\*(.+?)\*\*', r'#strong[\1]', text)
    # Convert *italic* to Typst #emph[\1]
    text = re.sub(r'\*(.+?)\*', r'#emph[\1]', text)

    # Escape characters that are special in Typst markup
    # but NOT # since we use it for Typst commands above
    for char in ['$', '\\']:
        text = text.replace(char, '\\' + char)

    return text


def escape_typst_string(text: str) -> str:
    """Escape text for use inside Typst double-quoted strings."""
    text = text.replace('\\', '\\\\')
    text = text.replace('"', '\\"')
    return text


def gen_title_page(item: dict) -> str:
    title = item.get("title", "Untitled")
    # Replace literal \n with Typst linebreak
    title_escaped = escape_typst_string(title.replace("\n", "\\n"))
    tagline = item.get("tagline")
    tagline_arg = f'\n  tagline: "{escape_typst_string(tagline)}",' if tagline else ""
    return f'''#title-page(
  title: "{title_escaped}",{tagline_arg}
)
'''


def gen_section_title_page(section_number, title, intro) -> str:
    num_arg = f"\n  number: {section_number}," if section_number else ""
    intro_arg = f'\n  intro: [{escape_typst(intro)}],' if intro else ""
    return f'''#section-title-page({num_arg}
  title: "{escape_typst_string(title)}",{intro_arg}
)
'''


def gen_heading(level: int, text: str) -> str:
    prefix = "=" * level
    return f"\n{prefix} {text}\n"


def gen_prose(text: str) -> str:
    return f"\n{escape_typst(text)}\n"


def gen_lead_text(text: str) -> str:
    return f"\n#lead-text[{escape_typst(text)}]\n"


def gen_hint(text: str) -> str:
    return f"\n#hint[{escape_typst(text)}]\n"


def gen_divider() -> str:
    return "\n#divider()\n"


def gen_bullet_list(items: list) -> str:
    lines = []
    for item in items:
        lines.append(f"- {escape_typst(item)}")
    return "\n" + "\n".join(lines) + "\n"


def gen_anchor_card(item: dict) -> str:
    title = escape_typst_string(item.get("title", "Anchor Question"))
    question = escape_typst(item.get("question", ""))
    return f'''
#anchor-card(
  title: "{title}",
  question: [{question}],
)
'''


def gen_framework_box(item: dict) -> str:
    title = escape_typst_string(item.get("title", "Framework"))

    # Simple content (string)
    if "content" in item and isinstance(item["content"], str):
        content = escape_typst(item["content"])
        return f'''
#framework-box(title: "{title}")[
  {content}
]
'''

    # Complex content (content_blocks)
    if "content_blocks" in item:
        inner = []
        for block in item["content_blocks"]:
            btype = block.get("type")
            if btype == "hint":
                inner.append(f'  #hint[{escape_typst(block["text"])}]')
            elif btype == "prose":
                inner.append(f'  {escape_typst(block["text"])}')
            elif btype == "heading_inline":
                inner.append(f'\n  #strong[{escape_typst(block["text"])}]')
            elif btype == "bullet_list":
                for bi in block["items"]:
                    inner.append(f"  - {escape_typst(bi)}")
        return f'''
#framework-box(title: "{title}")[
{chr(10).join(inner)}
]
'''

    return f'#framework-box(title: "{title}")[]\n'


def gen_mistake_box(item: dict) -> str:
    title = escape_typst_string(item.get("title", "Common Mistake"))
    fix = item.get("fix")
    fix_arg = f'\n  fix: [{escape_typst(fix)}],' if fix else ""
    body = escape_typst(item.get("body", ""))
    return f'''
#mistake-box(
  title: "{title}",{fix_arg}
)[
  {body}
]
'''


def gen_writing_box(item: dict) -> str:
    label = item.get("label")
    height = item.get("height", "100pt")
    label_arg = f'\n  label: "{escape_typst_string(label)}",' if label else ""
    return f'''
#writing-box({label_arg}
  height: {height},
)
'''


def gen_writing_lines(item: dict) -> str:
    count = item.get("count", 3)
    return f"\n#writing-lines(count: {count})\n"


def gen_checklist(item: dict) -> str:
    items = item.get("items", [])
    args = ",\n  ".join(f'[{escape_typst(i)}]' for i in items)
    return f"\n#checklist(\n  {args},\n)\n"


def _format_cell(cell: str) -> str:
    """Format a table cell value."""
    escaped = escape_typst(cell)
    return f"[{escaped}]"


def gen_data_table(item: dict) -> str:
    headers = item.get("headers", [])
    rows = item.get("rows", [])

    header_args = ", ".join(f'"{h}"' for h in headers)
    row_lines = []
    for row in rows:
        cells = ", ".join(_format_cell(c) for c in row)
        row_lines.append(f"    ({cells}),")

    return f'''
#workbook-table(
  headers: ({header_args}),
  rows: (
{chr(10).join(row_lines)}
  ),
)
'''


def gen_input_table(item: dict) -> str:
    headers = item.get("headers", [])
    example_rows = item.get("example_rows", [])
    rows = item.get("rows", [])
    blank_rows = item.get("blank_rows", 0)
    row_height = item.get("row_height", "55pt")

    header_args = ", ".join(f'"{h}"' for h in headers)

    ex_lines = []
    for row in example_rows:
        cells = ", ".join(_format_cell(c) for c in row)
        ex_lines.append(f"    ({cells}),")

    row_lines = []
    for row in rows:
        cells = ", ".join(_format_cell(c) for c in row)
        row_lines.append(f"    ({cells}),")

    # Add blank rows
    col_count = len(headers)
    for _ in range(blank_rows):
        cells = ", ".join(["[]"] * col_count)
        row_lines.append(f"    ({cells}),")

    return f'''
#input-table(
  headers: ({header_args}),
  example-rows: (
{chr(10).join(ex_lines)}
  ),
  rows: (
{chr(10).join(row_lines)}
  ),
  row-height: {row_height},
)
'''


def gen_cross_ref(item: dict) -> str:
    section = escape_typst_string(item.get("section", ""))
    note = escape_typst(item.get("note", ""))
    return f'''
#cross-ref(
  section: "{section}",
  note: [{note}],
)
'''


# ===========================================================
# Content Block Router
# ===========================================================

GENERATORS = {
    "title_page": gen_title_page,
    "heading2": lambda item: gen_heading(2, item["text"]),
    "heading3": lambda item: gen_heading(3, item["text"]),
    "heading4": lambda item: gen_heading(4, item["text"]),
    "prose": lambda item: gen_prose(item["text"]),
    "lead_text": lambda item: gen_lead_text(item["text"]),
    "hint": lambda item: gen_hint(item["text"]),
    "divider": lambda _: gen_divider(),
    "bullet_list": lambda item: gen_bullet_list(item["items"]),
    "anchor_card": gen_anchor_card,
    "framework_box": gen_framework_box,
    "mistake_box": gen_mistake_box,
    "writing_box": gen_writing_box,
    "writing_lines": gen_writing_lines,
    "checklist": gen_checklist,
    "data_table": gen_data_table,
    "input_table": gen_input_table,
    "cross_ref": gen_cross_ref,
}


def generate_section(data: dict, standalone: bool = False) -> str:
    """Convert a section's JSON data to a Typst source string.

    If standalone=True, includes template import and show rule
    so the section can be compiled on its own.
    """
    parts = []

    # Always import template (needed for component functions)
    parts.append('#import "../template.typ": *\n')

    if standalone:
        parts.append("#show: workbook-setup\n")

    section_num = data.get("section_number")
    title = data.get("title", "Untitled")
    intro = data.get("section_title_intro")

    # Auto-generate section title page if intro is provided
    # and there's no explicit section_title_page in the content
    content = data.get("content", [])
    has_title_page = any(
        i.get("type") in ("section_title_page", "title_page")
        for i in content
    )
    if not has_title_page and intro:
        parts.append(gen_section_title_page(section_num, title, intro))

    for item in content:
        item_type = item.get("type", "")

        # Special handling for section title page vs title page
        if item_type == "title_page":
            parts.append(gen_title_page(item))
            continue

        if item_type == "section_title_page":
            parts.append(gen_section_title_page(
                item.get("number", section_num),
                item.get("title", title),
                item.get("intro", intro),
            ))
            continue

        gen = GENERATORS.get(item_type)
        if gen:
            parts.append(gen(item))
        else:
            parts.append(f"\n// WARNING: unknown type \"{item_type}\"\n")

    return "\n".join(parts)


# ===========================================================
# Main
# ===========================================================

def build():
    mode = sys.argv[1] if len(sys.argv) > 1 else None

    SECTIONS_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    section_files = []

    if mode != "--compile":
        # --- Generate .typ files from JSON ---
        json_files = sorted(DATA_DIR.glob("*.json"))
        if not json_files:
            print("No JSON files found in data/")
            sys.exit(1)

        for jf in json_files:
            print(f"  Converting {jf.name} ...")
            with open(jf) as f:
                data = json.load(f)

            typ_content = generate_section(data)
            typ_name = jf.stem + ".typ"
            typ_path = SECTIONS_DIR / typ_name
            with open(typ_path, "w") as f:
                f.write(typ_content)

            section_files.append(typ_name)
            print(f"    -> sections/{typ_name}")

        # --- Generate main workbook.typ ---
        main_content = ['#import "template.typ": *\n', "#show: workbook-setup\n"]
        for sf in section_files:
            main_content.append(f'#include "sections/{sf}"\n')

        main_path = SCRIPT_DIR / "workbook.typ"
        with open(main_path, "w") as f:
            f.write("\n".join(main_content))
        print(f"\n  Generated workbook.typ with {len(section_files)} sections")

    if mode != "--generate":
        # --- Compile PDF ---
        print("\n  Compiling PDF ...")
        result = subprocess.run(
            ["typst", "compile", "--font-path", "fonts", "workbook.typ", "output/workbook.pdf"],
            cwd=str(SCRIPT_DIR),
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"  Compilation failed:\n{result.stderr}")
            sys.exit(1)
        else:
            print(f"  -> output/workbook.pdf")
            if result.stderr:
                print(f"  Warnings:\n{result.stderr}")

    print("\n  Done!")


if __name__ == "__main__":
    build()
