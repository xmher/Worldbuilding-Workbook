#!/usr/bin/env python3
"""Convert updated geography markdown to JSON format for Typst rendering."""

import json
import re

def parse_table(lines):
    """Parse a markdown table into headers and rows."""
    if len(lines) < 2:
        return None, None
    # Parse header
    headers = [cell.strip() for cell in lines[0].strip('|').split('|')]
    # Skip separator line (line 1)
    rows = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        rows.append(cells)
    return headers, rows

def is_fillable_table(rows):
    """Check if a table has empty cells (fillable by user)."""
    for row in rows:
        for cell in row:
            if cell.strip() == '':
                return True
    return False

def table_to_json(headers, rows):
    """Convert a table to the appropriate JSON type."""
    fillable = is_fillable_table(rows)
    if fillable:
        # Check if it's a structured table (first column has labels, rest are empty)
        is_structured = all(
            row[0].strip() != '' and all(cell.strip() == '' for cell in row[1:])
            for row in rows if len(row) > 1
        )
        if is_structured:
            return {
                "type": "structured_table",
                "headers": headers,
                "rows": rows,
                "row_height": "55pt"
            }
        else:
            return {
                "type": "open_table",
                "headers": headers,
                "rows": rows,
                "fill_strategy": "wider_rows"
            }
    else:
        return {
            "type": "data_table",
            "headers": headers,
            "rows": rows
        }

def parse_mistake(title, paragraphs):
    """Parse a mistake section into a mistake_box."""
    body_parts = []
    fix = ""
    for p in paragraphs:
        if p.startswith("**What it looks like:**"):
            body_parts.append(p.replace("**What it looks like:** ", ""))
        elif p.startswith("**Why it hurts your romance:**"):
            body_parts.append(p.replace("**Why it hurts your romance:** ", ""))
        elif p.startswith("**How to fix it:**"):
            fix = p.replace("**How to fix it:** ", "")
    body = " ".join(body_parts) if body_parts else " ".join(paragraphs[:-1]) if paragraphs else ""
    if not fix and paragraphs:
        fix = paragraphs[-1]
    return {
        "type": "mistake_box",
        "title": title,
        "body": body,
        "fix": fix
    }

def build_json():
    with open("/home/user/Worldbuilding-Workbook/Completed section1_geography_v5.md", "r") as f:
        md = f.read()

    lines = md.split('\n')
    content = []
    i = 0

    # Skip the title line "# SECTION 1: Geography & Environment"
    # and get the intro text
    section_title_intro = ""

    # Skip line 0 (title)
    i = 1
    # Skip blank line
    while i < len(lines) and lines[i].strip() == '':
        i += 1

    # Grab intro paragraph
    if i < len(lines):
        section_title_intro = lines[i].strip()
        i += 1

    # Skip blank line after intro
    while i < len(lines) and lines[i].strip() == '':
        i += 1

    # Now parse "This section is divided into two parts:" and the part descriptions
    # These go as hint + prose blocks
    intro_blocks = []
    while i < len(lines) and not lines[i].startswith('---'):
        line = lines[i].strip()
        if line:
            intro_blocks.append(line)
        i += 1

    # Add intro blocks
    if intro_blocks:
        content.append({"type": "hint", "text": intro_blocks[0]})
        for block in intro_blocks[1:]:
            content.append({"type": "prose", "text": block})

    # Now process the rest of the document
    # Track if we're in a mistake section
    current_mistake_title = None
    current_mistake_paragraphs = []

    def flush_mistake():
        nonlocal current_mistake_title, current_mistake_paragraphs
        if current_mistake_title:
            content.append(parse_mistake(current_mistake_title, current_mistake_paragraphs))
            current_mistake_title = None
            current_mistake_paragraphs = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Divider
        if stripped == '---':
            flush_mistake()
            content.append({"type": "divider"})
            i += 1
            continue

        # Part header (# Section 1 · Part ...)
        if stripped.startswith('# Section 1') or stripped.startswith('# SECTION 1'):
            flush_mistake()
            # Convert to heading2
            part_text = stripped.lstrip('#').strip()
            # Map "Section 1 · Part One — The Foundation" to "Part One — The Foundation"
            if '·' in part_text:
                part_text = part_text.split('·', 1)[1].strip()
            content.append({"type": "heading2", "text": part_text})
            i += 1
            continue

        # Heading 2
        if stripped.startswith('## ') and not stripped.startswith('### '):
            flush_mistake()
            text = stripped[3:].strip()
            content.append({"type": "heading2", "text": text})
            i += 1
            continue

        # Heading 3 - check for mistake pattern
        if stripped.startswith('### '):
            flush_mistake()
            text = stripped[4:].strip()
            if re.match(r'Mistake #\d+:', text):
                current_mistake_title = text
                current_mistake_paragraphs = []
                i += 1
                continue
            else:
                content.append({"type": "heading3", "text": text})
                i += 1
                continue

        # Empty line
        if stripped == '':
            i += 1
            continue

        # Table
        if stripped.startswith('|') and i + 1 < len(lines) and lines[i+1].strip().startswith('|'):
            flush_mistake()
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            headers, rows = parse_table(table_lines)
            if headers and rows:
                content.append(table_to_json(headers, rows))
            continue

        # Bullet list
        if stripped.startswith('- '):
            flush_mistake()
            items = []
            while i < len(lines) and lines[i].strip().startswith('- '):
                items.append(lines[i].strip()[2:])
                i += 1
            content.append({"type": "bullet_list", "items": items})
            continue

        # Writing lines (underscores for fill-in)
        if stripped.startswith('_____'):
            flush_mistake()
            # Count underscore lines, skipping blank lines between them
            line_count = 0
            while i < len(lines):
                s = lines[i].strip()
                if s.startswith('_____'):
                    line_count += 1
                    i += 1
                elif s == '' and i + 1 < len(lines) and lines[i+1].strip().startswith('_____'):
                    i += 1  # skip blank line between underscore lines
                else:
                    break
            # Map line count to height
            if line_count <= 1:
                height = "80pt"
            elif line_count <= 2:
                height = "100pt"
            elif line_count <= 3:
                height = "145pt"
            else:
                height = "200pt"
            content.append({"type": "writing_box", "label": "Your Answer", "height": height})
            continue

        # Bold-only line that's a question -> heading4
        if re.match(r'^\*\*[^*]+\*\*$', stripped):
            flush_mistake()
            question_text = stripped.strip('*')
            content.append({"type": "heading4", "text": question_text})
            i += 1
            continue

        # If in a mistake section, collect paragraphs
        if current_mistake_title:
            current_mistake_paragraphs.append(stripped)
            i += 1
            continue

        # Regular prose paragraph
        content.append({"type": "prose", "text": stripped})
        i += 1

    flush_mistake()

    # Build the final JSON structure
    result = {
        "section_number": 1,
        "title": "Geography & Environment",
        "section_title_intro": section_title_intro,
        "content": content
    }

    return result

def post_process(data):
    """Apply post-processing rules to improve the JSON output."""
    content = data["content"]
    new_content = []

    for i, item in enumerate(content):
        # Convert certain prose items to hints based on patterns
        if item["type"] == "prose":
            text = item["text"]
            # Short advice/instruction paragraphs after questions become hints
            if i > 0 and new_content and new_content[-1].get("type") == "heading4":
                # This is a hint following a question
                item = {"type": "hint", "text": text}
            # Paragraphs that are clearly instructional/tips
            elif text.startswith("**How to write it:**"):
                item = {"type": "hint", "text": text}

        new_content.append(item)

    data["content"] = new_content
    return data

if __name__ == "__main__":
    result = build_json()
    result = post_process(result)

    output_path = "/home/user/Worldbuilding-Workbook/typst/data/01_geography.json"
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # Validate
    with open(output_path) as f:
        data = json.load(f)

    print(f"Valid JSON written to {output_path}")
    print(f"Content items: {len(data['content'])}")
    types = {}
    for item in data['content']:
        t = item.get('type', '?')
        types[t] = types.get(t, 0) + 1
    for t, c in sorted(types.items()):
        print(f"  {t}: {c}")
