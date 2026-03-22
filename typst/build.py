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
    for char in ['$', '\\', '_', '@']:
        text = text.replace(char, '\\' + char)

    # Escape # that aren't Typst function calls (#strong, #emph, etc.)
    # A lone # at start of text or after space needs escaping
    text = re.sub(r'(?<![a-zA-Z])#(?!(strong|emph|text|link)\[)', r'\#', text)

    # Escape stray * that weren't part of bold/italic pairs
    # Count remaining * — if odd, there's an unmatched one
    # Simple approach: escape * at start or end of text if unmatched
    star_count = text.count('*')
    if star_count % 2 == 1:
        # Escape the last * if it's at the end
        if text.endswith('*'):
            text = text[:-1] + '\\*'
        elif text.startswith('*'):
            text = '\\*' + text[1:]

    return text


def escape_typst_string(text: str) -> str:
    """Escape text for use inside Typst double-quoted strings."""
    text = text.replace('\\', '\\\\')
    text = text.replace('"', '\\"')
    return text


def gen_title_page(item: dict) -> str:
    title = item.get("title", "Untitled")
    tagline = item.get("tagline")
    tagline_arg = f'\n  tagline: "{escape_typst_string(tagline)}",' if tagline else ""
    # Pass title as content so line breaks render correctly
    # Split on \n and join with Typst linebreak
    title_lines = title.split("\n")
    if len(title_lines) > 1:
        title_content = " \\\n    ".join(escape_typst(line) for line in title_lines)
        return f'''#title-page(
  title: [{title_content}],{tagline_arg}
)
'''
    else:
        return f'''#title-page(
  title: "{escape_typst_string(title)}",{tagline_arg}
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
    # Escape underscores and other Typst-special chars in heading text
    escaped = escape_typst(text)
    return f"\n{prefix} {escaped}\n"


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
    height_str = item.get("height", "120pt")
    fill_page = item.get("fill_page", False)

    # R2: Enforce minimum 120pt height for writing boxes
    height_val = int(height_str.replace("pt", "")) if isinstance(height_str, str) else int(height_str)
    height_val = max(height_val, 120)
    height_str = f"{height_val}pt"

    label_arg = f'\n  label: "{escape_typst_string(label)}",' if label else ""
    fill_arg = "\n  fill-page: true," if fill_page else ""
    return f'''
#writing-box({label_arg}
  height: {height_str},{fill_arg}
)
'''


def gen_answer_box(item: dict) -> str:
    height_str = item.get("height", "180pt")
    return f"\n#answer-box(\n  height: {height_str},\n)\n"


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


def _format_row(row: list) -> str:
    """Format a table row as a Typst tuple, handling single-element rows."""
    cells = ", ".join(_format_cell(c) for c in row)
    # Single-element tuple needs trailing comma in Typst
    if len(row) == 1:
        return f"    ({cells},),"
    return f"    ({cells}),"


def gen_data_table(item: dict) -> str:
    headers = item.get("headers", [])
    rows = item.get("rows", [])
    col_widths = item.get("col_widths")

    header_args = ", ".join(f'"{escape_typst_string(h)}"' for h in headers)
    if len(headers) == 1:
        header_args += ","
    row_lines = []
    for row in rows:
        row_lines.append(_format_row(row))

    col_widths_arg = ""
    if col_widths:
        col_widths_arg = f"\n  col-widths: ({', '.join(col_widths)}),"

    return f'''
#workbook-table(
  headers: ({header_args}),{col_widths_arg}
  rows: (
{chr(10).join(row_lines)}
  ),
)
'''


def gen_structured_table(item: dict, preamble: str = "") -> str:
    """Structured table: pre-filled labels, user fills in cells. Breakable."""
    headers = item.get("headers", [])
    example_rows = item.get("example_rows", [])
    rows = item.get("rows", [])
    row_height = item.get("row_height", "55pt")

    # R3: Enforce minimum 60pt row height; auto-increase for rows with long text
    # Longer text in narrow columns (3+) needs even more height
    rh_val = int(row_height.replace("pt", ""))
    max_cell_len = max((len(c) for row in rows for c in row), default=0)
    col_count = len(headers)
    if max_cell_len > 90 and col_count >= 3:
        rh_val = max(rh_val, 90)
    elif max_cell_len > 80:
        rh_val = max(rh_val, 75)
    elif max_cell_len > 60:
        rh_val = max(rh_val, 65)
    else:
        rh_val = max(rh_val, 60)
    row_height = f"{rh_val}pt"

    header_args = ", ".join(f'"{escape_typst_string(h)}"' for h in headers)
    if len(headers) == 1:
        header_args += ","

    ex_lines = []
    for row in example_rows:
        ex_lines.append(_format_row(row))

    row_lines = []
    for row in rows:
        row_lines.append(_format_row(row))

    preamble_arg = f"\n  preamble: [{preamble}]," if preamble else ""

    return f'''
#structured-table(
  headers: ({header_args}),
  example-rows: (
{chr(10).join(ex_lines)}
  ),
  rows: (
{chr(10).join(row_lines)}
  ),
  row-height: {row_height},{preamble_arg}
)
'''


def gen_open_table(item: dict, preamble: str = "") -> str:
    """Open-ended table: example + labeled rows + blank rows filling page."""
    headers = item.get("headers", [])
    example_rows = item.get("example_rows", [])
    rows = item.get("rows", [])
    row_height = item.get("row_height", "55pt")
    extra_rows = item.get("extra_rows", 0)

    # R3: Enforce minimum 60pt row height; auto-increase for long text
    rh_val = int(row_height.replace("pt", ""))
    all_table_rows = rows + example_rows
    max_cell_len = max((len(c) for row in all_table_rows for c in row), default=0)
    col_count = len(headers)
    if max_cell_len > 90 and col_count >= 3:
        rh_val = max(rh_val, 90)
    elif max_cell_len > 80:
        rh_val = max(rh_val, 75)
    elif max_cell_len > 60:
        rh_val = max(rh_val, 65)
    else:
        rh_val = max(rh_val, 60)
    row_height = f"{rh_val}pt"

    header_args = ", ".join(f'"{escape_typst_string(h)}"' for h in headers)
    if len(headers) == 1:
        header_args += ","

    ex_lines = []
    for row in example_rows:
        ex_lines.append(_format_row(row))

    row_lines = []
    for row in rows:
        row_lines.append(_format_row(row))

    extra_arg = f"\n  extra-rows: {extra_rows}," if extra_rows > 0 else ""
    rows_arg = f"\n  rows: (\n{chr(10).join(row_lines)}\n  )," if rows else ""
    preamble_arg = f"\n  preamble: [{preamble}]," if preamble else ""
    fill_strategy = item.get("fill_strategy", "auto")
    fill_arg = f'\n  fill-strategy: "{fill_strategy}",' if fill_strategy != "auto" else ""

    return f'''
#open-table(
  headers: ({header_args}),
  example-rows: (
{chr(10).join(ex_lines)}
  ),{rows_arg}
  row-height: {row_height},{extra_arg}{fill_arg}{preamble_arg}
)
'''


def gen_input_table(item: dict) -> str:
    """Legacy: routes to structured or open table based on content."""
    if item.get("rows"):
        return gen_structured_table(item)
    return gen_open_table(item)


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
    "answer_box": gen_answer_box,
    "writing_lines": gen_writing_lines,
    "checklist": gen_checklist,
    "data_table": gen_data_table,
    "input_table": gen_input_table,
    "structured_table": gen_structured_table,
    "open_table": gen_open_table,
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

    # R2: Pre-scan to mark writing boxes that should fill remaining page space.
    # A writing_box is "page-filling" if the next non-trivial element is a
    # heading2, divider, group, or end-of-section (i.e., it's the last
    # interactive element before a visual break).
    fill_page_indices = set()
    for idx, item in enumerate(content):
        if item.get("type") == "writing_box":
            # Look ahead to see what follows
            j = idx + 1
            while j < len(content) and content[j].get("type") in ("divider", "hint"):
                j += 1
            if j >= len(content):
                # Last writing box in section
                fill_page_indices.add(idx)
            elif content[j].get("type") in ("heading2", "group"):
                # Writing box before a major section break
                fill_page_indices.add(idx)

    # Track which items have been consumed by lookahead grouping
    consumed = set()

    for idx, item in enumerate(content):
        if idx in consumed:
            continue

        item_type = item.get("type", "")

        # Skip dividers before headings/groups — the heading provides enough separation
        if item_type == "divider":
            next_type = content[idx + 1].get("type", "") if idx + 1 < len(content) else ""
            if next_type in ("heading2", "group"):
                continue

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

        # Auto-group: heading2 + following preamble items
        # If a table/group/writing_box follows, keep heading with it.
        # Otherwise, let content flow naturally (no non-breakable wrapping).
        if item_type == "heading2":
            preamble_types = {"heading2", "heading3", "heading4", "hint", "prose", "lead_text", "body"}
            table_types = {"structured_table", "open_table"}
            preamble_parts = [gen_heading(2, item["text"])]
            j = idx + 1
            has_prose = False
            while j < len(content) and content[j].get("type", "") in preamble_types:
                child = content[j]
                if child.get("type") == "prose":
                    has_prose = True
                child_gen = GENERATORS.get(child["type"])
                if child_gen:
                    preamble_parts.append(child_gen(child))
                consumed.add(j)
                j += 1
            # If a table follows, pass preamble into table and consume it.
            # But if preamble contains prose paragraphs, the preamble is too large
            # to fit inside the table header — output normally instead, letting
            # the heading4 auto-grouper handle table attachment.
            next_type = content[j].get("type", "") if j < len(content) else ""
            if next_type in table_types and not has_prose:
                preamble_text = "".join(preamble_parts)
                table_item = content[j]
                if next_type == "structured_table":
                    parts.append(gen_structured_table(table_item, preamble=preamble_text))
                elif next_type == "open_table":
                    parts.append(gen_open_table(table_item, preamble=preamble_text))
                consumed.add(j)
            elif next_type == "group" and not has_prose:
                # heading2 + group: estimate combined height
                group_item = content[j]
                full_page = group_item.get("full_page", False)
                children = group_item.get("content", [])
                all_group_parts = list(preamble_parts)
                estimated_height = 80  # heading2 preamble
                for child in children:
                    child_type = child.get("type", "")
                    child_gen = GENERATORS.get(child_type)
                    if child_gen:
                        all_group_parts.append(child_gen(child))
                    if child_type in ("heading3", "heading4"):
                        estimated_height += 50
                    elif child_type == "hint":
                        estimated_height += 30
                    elif child_type == "data_table":
                        estimated_height += 44 + len(child.get("rows", [])) * 36
                    elif child_type in ("structured_table", "open_table"):
                        row_h = int(child.get("row_height", "55").replace("pt", ""))
                        n_rows = len(child.get("rows", [])) + len(child.get("example_rows", []))
                        estimated_height += 44 + n_rows * (row_h + 24)

                if full_page:
                    parts.append("\n#pagebreak(weak: true)\n")
                    parts.append(
                        f"\n#block(breakable: false)["
                        f"\n{''.join(all_group_parts)}\n]\n"
                    )
                elif estimated_height < 620:
                    parts.append(
                        f"\n#block(breakable: false)["
                        f"\n{''.join(all_group_parts)}\n]\n"
                    )
                else:
                    for p in all_group_parts:
                        parts.append(p)
                consumed.add(j)
            elif next_type == "writing_box":
                # Group heading2 preamble + writing_box together
                wb_gen = GENERATORS.get("writing_box")
                if wb_gen:
                    preamble_parts.append(wb_gen(content[j]))
                parts.append(
                    f"\n#block(breakable: false)["
                    f"\n{''.join(preamble_parts)}\n]\n"
                )
                consumed.add(j)
            else:
                # No table/group/writing_box follows — output normally
                for p in preamble_parts:
                    parts.append(p)
            continue

        # Auto-group: heading4 + following hint/prose
        # If a table follows, pass preamble INTO the table so they stay together.
        if item_type == "heading4":
            preamble_types = {"heading4", "hint", "prose"}
            table_types = {"structured_table", "open_table"}
            preamble_parts = [gen_heading(4, item["text"])]
            j = idx + 1
            while j < len(content) and content[j].get("type", "") in preamble_types:
                child = content[j]
                child_gen = GENERATORS.get(child["type"])
                if child_gen:
                    preamble_parts.append(child_gen(child))
                consumed.add(j)
                j += 1
            # If a table follows, pass preamble into table and consume it
            next_type = content[j].get("type", "") if j < len(content) else ""
            if next_type in table_types:
                preamble_text = "".join(preamble_parts)
                table_item = content[j]
                if next_type == "structured_table":
                    parts.append(gen_structured_table(table_item, preamble=preamble_text))
                elif next_type == "open_table":
                    parts.append(gen_open_table(table_item, preamble=preamble_text))
                consumed.add(j)
            elif next_type == "writing_box":
                # Group heading4+hint+writing_box together
                wb_gen = GENERATORS.get("writing_box")
                if wb_gen:
                    preamble_parts.append(wb_gen(content[j]))
                parts.append(
                    f"\n#block(breakable: false)["
                    f"\n{''.join(preamble_parts)}\n]\n"
                )
                consumed.add(j)
            else:
                # No table follows — output normally
                for p in preamble_parts:
                    parts.append(p)
            continue

        # Group: estimate height. If it fits on one page, wrap in non-breakable
        # block so the heading+table stay together. Otherwise render normally.
        if item_type == "group":
            children = item.get("content", [])
            full_page = item.get("full_page", False)
            all_child_parts = []
            estimated_height = 0
            for child in children:
                child_type = child.get("type", "")
                child_gen = GENERATORS.get(child_type)
                if child_gen:
                    all_child_parts.append(child_gen(child))
                # Rough height estimates (in pt)
                if child_type in ("heading3", "heading4"):
                    estimated_height += 50
                elif child_type == "hint":
                    estimated_height += 30
                elif child_type == "data_table":
                    estimated_height += 44 + len(child.get("rows", [])) * 36
                elif child_type in ("structured_table", "open_table"):
                    row_h = int(child.get("row_height", "55").replace("pt", ""))
                    n_rows = len(child.get("rows", [])) + len(child.get("example_rows", []))
                    estimated_height += 44 + n_rows * (row_h + 24)

            if full_page:
                # Force page break before and render as non-breakable block
                parts.append("\n#pagebreak(weak: true)\n")
                parts.append(
                    f"\n#block(breakable: false)["
                    f"\n{''.join(all_child_parts)}\n]\n"
                )
            elif estimated_height < 620:
                parts.append(
                    f"\n#block(breakable: false)["
                    f"\n{''.join(all_child_parts)}\n]\n"
                )
            else:
                # Too tall — render normally, Typst headings prevent orphaning
                for p in all_child_parts:
                    parts.append(p)
            continue

        # R2: If this writing_box should fill the page, inject fill_page flag
        if item_type == "writing_box" and idx in fill_page_indices:
            item = dict(item)  # copy to avoid mutating original
            item["fill_page"] = True

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
