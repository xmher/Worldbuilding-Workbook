#!/usr/bin/env python3
"""Convert the updated geography markdown to JSON format for Typst rendering.

Source: Updated Sections/01_Geography_Environment_UPDATED.md
"""

import json
import re


def parse_table(lines):
    """Parse a markdown table into headers and rows."""
    if len(lines) < 2:
        return None, None
    headers = [cell.strip() for cell in lines[0].strip('|').split('|')]
    # Skip separator line (line 1)
    rows = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        rows.append(cells)
    return headers, rows


def is_italic_row(row):
    """Check if a row is an italic example row (cells wrapped in *...*) ."""
    non_empty = [c for c in row if c.strip()]
    if not non_empty:
        return False
    # First non-empty cell should start with * and end with *
    first = non_empty[0].strip()
    return first.startswith('*') and first.endswith('*')


def strip_italic(text):
    """Remove surrounding italic markers from text."""
    text = text.strip()
    if text.startswith('*') and text.endswith('*') and len(text) > 2:
        return text[1:-1]
    return text


def is_empty_row(row):
    """Check if all cells in a row are empty."""
    return all(c.strip() == '' for c in row)


def is_label_row(row):
    """Check if first cell has content and rest are empty (structured label row)."""
    if len(row) < 2:
        return False
    return row[0].strip() != '' and all(c.strip() == '' for c in row[1:])


def classify_table(headers, rows):
    """Classify a table and return the appropriate JSON structure.

    Types:
    - data_table: all rows have content (reference/read-only)
    - structured_table: label rows with empty fillable cells
    - open_table: has example rows + empty rows for user to fill
    """
    if not rows:
        return {"type": "data_table", "headers": headers, "rows": []}

    example_rows = []
    data_rows = []

    # Separate example rows (italic) from regular rows
    for row in rows:
        if is_italic_row(row):
            example_rows.append([strip_italic(c) for c in row])
        else:
            data_rows.append(row)

    # Check if remaining rows are all empty or label-only
    all_empty = all(is_empty_row(r) for r in data_rows)
    all_label = all(is_label_row(r) or is_empty_row(r) for r in data_rows) and any(
        not is_empty_row(r) for r in data_rows
    )
    all_data = all(
        not is_empty_row(r) and not is_label_row(r) for r in data_rows
    ) and not example_rows

    if all_data and not example_rows:
        return {"type": "data_table", "headers": headers, "rows": data_rows}

    if all_label and not example_rows:
        # Structured table with labels
        return {
            "type": "structured_table",
            "headers": headers,
            "rows": data_rows,
            "row_height": "55pt",
        }

    if example_rows:
        if all_label:
            # Structured table with examples
            return {
                "type": "structured_table",
                "headers": headers,
                "example_rows": example_rows,
                "rows": data_rows,
                "row_height": "55pt",
            }
        else:
            # Open table with examples + blank rows
            # Include empty rows as regular rows (don't use extra_rows)
            result = {
                "type": "open_table",
                "headers": headers,
                "example_rows": example_rows,
                "rows": data_rows,
                "row_height": "55pt",
                "fill_strategy": "wider_rows",
            }
            return result

    # Fallback: has empty rows but no examples and no labels
    if all_empty:
        return {
            "type": "open_table",
            "headers": headers,
            "example_rows": [],
            "rows": data_rows,
            "row_height": "55pt",
            "fill_strategy": "wider_rows",
        }

    # Mixed: some have content, some don't
    # Check if it looks structured (first col has content, others mostly empty)
    structured_like = sum(1 for r in data_rows if is_label_row(r))
    if structured_like > len(data_rows) * 0.5:
        return {
            "type": "structured_table",
            "headers": headers,
            "example_rows": example_rows if example_rows else [],
            "rows": data_rows,
            "row_height": "55pt",
        }

    # Default to open_table
    return {
        "type": "open_table",
        "headers": headers,
        "example_rows": example_rows if example_rows else [],
        "rows": data_rows,
        "row_height": "55pt",
        "fill_strategy": "wider_rows",
    }


def parse_mistake(lines, start):
    """Parse a mistake section starting at ### Mistake #N: ..."""
    title_line = lines[start].strip().lstrip('#').strip()
    i = start + 1
    body_parts = []
    fix = ""

    while i < len(lines):
        stripped = lines[i].strip()
        # Stop at next heading or divider
        if stripped.startswith('#') or stripped == '---':
            break
        if stripped == '':
            i += 1
            continue

        if stripped.startswith('**How to fix it:**'):
            fix = stripped.replace('**How to fix it:**', '').strip()
        elif stripped.startswith('**What it looks like:**'):
            body_parts.append(stripped.replace('**What it looks like:**', '').strip())
        elif stripped.startswith('**Why it hurts:**'):
            body_parts.append(stripped.replace('**Why it hurts:**', '').strip())
        elif stripped.startswith('**Why it hurts your romance:**'):
            body_parts.append(stripped.replace('**Why it hurts your romance:**', '').strip())
        else:
            body_parts.append(stripped)
        i += 1

    body = " ".join(body_parts)
    return {
        "type": "mistake_box",
        "title": title_line,
        "body": body,
        "fix": fix,
    }, i


def parse_blockquote(lines, start):
    """Parse a blockquote starting at > ..."""
    parts = []
    i = start
    while i < len(lines) and lines[i].strip().startswith('>'):
        text = lines[i].strip().lstrip('>').strip()
        if text:
            parts.append(text)
        i += 1

    full_text = " ".join(parts)

    # Check for cross-reference: > **Continue in Section X**
    m = re.match(r'\*\*Continue in (Section \d+)\*\*', full_text)
    if m:
        section = m.group(1)
        # Get the note (remaining text after the section reference)
        note_parts = []
        for p in parts[1:]:  # skip the first "Continue in Section X" line
            # Strip italic markers
            clean = p.strip('*').strip()
            if clean:
                note_parts.append(clean)
        note = " ".join(note_parts) if note_parts else ""
        return {
            "type": "cross_ref",
            "section": section,
            "note": note,
        }, i

    # Check for "Final Thought" blockquote
    if full_text.startswith('**Final Thought**'):
        # Extract content after "Final Thought"
        note_parts = []
        for p in parts:
            if p.startswith('**Final Thought**'):
                continue
            clean = p.strip('*').strip()
            if clean:
                note_parts.append(clean)
        return {
            "type": "hint",
            "text": " ".join(note_parts),
        }, i

    # Generic blockquote → prose
    return {"type": "prose", "text": full_text}, i


def build_json():
    with open("/tmp/01_geo_updated.md", "r") as f:
        md = f.read()

    lines = md.split('\n')
    content = []
    i = 0

    # Line 0: # SECTION 1: Geography & Environment
    i = 1

    # Skip blanks
    while i < len(lines) and lines[i].strip() == '':
        i += 1

    # Grab intro paragraphs (before first ---)
    intro_paragraphs = []
    while i < len(lines) and lines[i].strip() != '---':
        stripped = lines[i].strip()
        if stripped:
            intro_paragraphs.append(stripped)
        i += 1

    # First paragraph is the section title intro
    section_title_intro = intro_paragraphs[0] if intro_paragraphs else ""

    # Remaining intro paragraphs go as prose
    for p in intro_paragraphs[1:]:
        content.append({"type": "prose", "text": p})

    # Skip the first ---
    if i < len(lines) and lines[i].strip() == '---':
        i += 1

    # Skip "In This Section" TOC block (until next ---)
    # This is a navigation aid, not content for the workbook
    if i < len(lines):
        # Check if next non-blank line is "## In This Section"
        j = i
        while j < len(lines) and lines[j].strip() == '':
            j += 1
        if j < len(lines) and lines[j].strip() == '## In This Section':
            # Skip until next ---
            while i < len(lines) and lines[i].strip() != '---':
                i += 1
            if i < len(lines):
                i += 1  # skip the ---

    # Now parse the rest of the document
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Empty line
        if stripped == '':
            i += 1
            continue

        # Divider
        if stripped == '---':
            content.append({"type": "divider"})
            i += 1
            continue

        # Blockquote
        if stripped.startswith('>'):
            item, i = parse_blockquote(lines, i)
            content.append(item)
            continue

        # Heading 2
        if stripped.startswith('## ') and not stripped.startswith('### '):
            text = stripped[3:].strip()
            content.append({"type": "heading2", "text": text})
            i += 1
            continue

        # Heading 3 - check for mistake pattern
        if stripped.startswith('### ') and not stripped.startswith('#### '):
            text = stripped[4:].strip()
            if re.match(r'Mistake #\d+:', text):
                item, i = parse_mistake(lines, i)
                content.append(item)
                continue
            else:
                content.append({"type": "heading3", "text": text})
                i += 1
                continue

        # Heading 4
        if stripped.startswith('#### '):
            text = stripped[5:].strip()
            content.append({"type": "heading4", "text": text})
            i += 1
            continue

        # Table
        if stripped.startswith('|') and i + 1 < len(lines) and lines[i + 1].strip().startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            headers, rows = parse_table(table_lines)
            if headers and rows is not None:
                content.append(classify_table(headers, rows))
            continue

        # Bullet list
        if stripped.startswith('- '):
            items = []
            while i < len(lines) and lines[i].strip().startswith('- '):
                items.append(lines[i].strip()[2:])
                i += 1
            content.append({"type": "bullet_list", "items": items})
            continue

        # Writing lines (underscores)
        if stripped.startswith('_____'):
            line_count = 0
            while i < len(lines):
                s = lines[i].strip()
                if s.startswith('_____'):
                    line_count += 1
                    i += 1
                elif s == '' and i + 1 < len(lines) and lines[i + 1].strip().startswith('_____'):
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

        # Standalone italic line (not bold-italic) → hint
        if re.match(r'^\*[^*]+\*$', stripped):
            text = stripped.strip('*')
            content.append({"type": "hint", "text": text})
            i += 1
            continue

        # Regular prose paragraph
        content.append({"type": "prose", "text": stripped})
        i += 1

    # Build the final JSON structure
    result = {
        "section_number": 1,
        "title": "Geography & Environment",
        "section_title_intro": section_title_intro,
        "content": content,
    }

    return result


def post_process(data):
    """Apply post-processing rules to improve the JSON output."""
    content = data["content"]
    new_content = []

    i = 0
    while i < len(content):
        item = content[i]

        # Convert certain prose items to hints based on context
        if item["type"] == "prose":
            text = item["text"]
            # Prose right after heading4 that's instructional → hint
            if new_content and new_content[-1].get("type") == "heading4":
                item = {"type": "hint", "text": text}

        new_content.append(item)
        i += 1

    data["content"] = new_content

    # Second pass: remove duplicate dividers
    filtered = []
    for i, item in enumerate(data["content"]):
        if item["type"] == "divider" and i > 0 and filtered and filtered[-1]["type"] == "divider":
            continue
        filtered.append(item)
    data["content"] = filtered

    # Third pass: remove dividers immediately before a heading2 that repeats
    # (the "prose section then worksheet section" pattern)
    # Actually, keep the dividers - build.py handles skipping dividers before headings

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
