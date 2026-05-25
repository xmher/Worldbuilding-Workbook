#!/usr/bin/env python3
"""Universal Markdown → JSON converter for all workbook sections.

Reads from Updated Sections/*.md and writes to typst/data/*.json.

Usage:
    python convert_all.py                # convert all sections
    python convert_all.py section_name   # convert one section (partial match)
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SECTIONS_DIR = ROOT / "Updated Sections"
DATA_DIR = ROOT / "typst" / "data"

# ── Section mapping ──────────────────────────────────────────
# (filename_pattern, section_number, output_json_name, canonical_title)
SECTION_MAP = [
    ("01_Geography",          1,  "01_geography",          "Geography & Environment"),
    ("02_Flora_Fauna",        2,  "02_flora_fauna",        "Flora, Fauna & Ecosystems"),
    ("Culture_Customs",       3,  "03_culture",            "Culture, Customs & Daily Life"),
    ("Economy_Labour",        4,  "04_economy",            "Economy, Labour & Resources"),
    ("Government_Power",      5,  "05_government",         "Government, Power & Law"),
    ("religion-myth",         6,  "06_religion",           "Religion, Myth & Prophecy"),
    ("history-and-lore",      7,  "07_history",            "History & Lore"),
    ("magic-system",          8,  "08_magic",              "Building Your Magic System"),
    ("09_Technology",         9,  "09_technology",         "Technology & Infrastructure"),
    ("language-and-comm",    10,  "10_language",           "Language & Communication"),
    ("section13-pressure",   13,  "13_pressure_cooker",    "The Pressure Cooker"),
    ("section14_instit",     14,  "14_institutions",       "Institutions & Structures"),
    ("Designing_Your_Key",   15,  "15_locations",          "Designing Your Key Locations"),
    ("Web_of_Systems",       16,  "16_web_of_systems",     "The Web of Systems"),
    ("section17-consistency", 17, "17_consistency",        "The Consistency Check"),
    ("The-Agency-Check",     18,  "18_agency_check",       "The Agency Check"),
    ("Quick_Reference",      20,  "20_quick_reference",    "Quick Reference Sheets"),
    ("common-romantasy",     21,  "21_common_mistakes",    "Common Romantasy Worldbuilding Mistakes"),
]


def find_md_file(pattern):
    """Find the markdown file matching a pattern."""
    for f in SECTIONS_DIR.iterdir():
        if f.suffix == '.md' and pattern in f.name:
            return f
    return None


# ── Table parsing ────────────────────────────────────────────

def parse_table(lines):
    """Parse a markdown table into headers and rows."""
    if len(lines) < 2:
        return None, None
    headers = [cell.strip() for cell in lines[0].strip('|').split('|')]
    rows = []
    for line in lines[2:]:  # skip separator
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        rows.append(cells)
    return headers, rows


def is_italic_row(row):
    """Check if a row is an italic example row."""
    non_empty = [c for c in row if c.strip()]
    if not non_empty:
        return False
    first = non_empty[0].strip()
    return first.startswith('*') and first.endswith('*') and not first.startswith('**')


def strip_italic(text):
    """Remove surrounding italic markers."""
    text = text.strip()
    if text.startswith('*') and text.endswith('*') and not text.startswith('**') and len(text) > 2:
        return text[1:-1]
    return text


def is_empty_row(row):
    return all(c.strip() == '' for c in row)


def is_label_row(row):
    if len(row) < 2:
        return False
    first = row[0].strip()
    rest_empty = all(c.strip() == '' for c in row[1:])
    return first != '' and rest_empty


def classify_table(headers, rows):
    """Classify a table as data_table, structured_table, or open_table."""
    if not rows:
        return {"type": "data_table", "headers": headers, "rows": []}

    example_rows = []
    data_rows = []

    for row in rows:
        if is_italic_row(row):
            example_rows.append([strip_italic(c) for c in row])
        else:
            data_rows.append(row)

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
        return {
            "type": "structured_table",
            "headers": headers,
            "rows": data_rows,
            "row_height": "55pt",
        }

    if example_rows:
        if all_label:
            return {
                "type": "structured_table",
                "headers": headers,
                "example_rows": example_rows,
                "rows": data_rows,
                "row_height": "55pt",
            }
        else:
            return {
                "type": "open_table",
                "headers": headers,
                "example_rows": example_rows,
                "rows": data_rows,
                "row_height": "55pt",
                "fill_strategy": "wider_rows",
            }

    if all_empty:
        return {
            "type": "open_table",
            "headers": headers,
            "example_rows": [],
            "rows": [],
            "row_height": "55pt",
            "fill_strategy": "wider_rows",
        }

    # Mixed: check if structured-like
    structured_like = sum(1 for r in data_rows if is_label_row(r))
    if structured_like > len(data_rows) * 0.4:
        return {
            "type": "structured_table",
            "headers": headers,
            "example_rows": example_rows if example_rows else [],
            "rows": data_rows,
            "row_height": "55pt",
        }

    return {
        "type": "open_table",
        "headers": headers,
        "example_rows": example_rows if example_rows else [],
        "rows": data_rows,
        "row_height": "55pt",
        "fill_strategy": "wider_rows",
    }


# ── Block parsers ────────────────────────────────────────────

def parse_mistake(lines, start):
    """Parse a ### Mistake #N: ... block."""
    title_line = lines[start].strip().lstrip('#').strip()
    i = start + 1
    body_parts = []
    fix = ""

    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith('#') or stripped == '---':
            break
        if stripped == '':
            i += 1
            continue

        if stripped.startswith('**How to fix it:**') or stripped.startswith('**How to Fix It:**'):
            fix = re.sub(r'^\*\*How to [Ff]ix [Ii]t:\*\*\s*', '', stripped)
        elif stripped.startswith('**What it looks like:**') or stripped.startswith('**What It Looks Like:**'):
            body_parts.append(re.sub(r'^\*\*What [Ii]t [Ll]ooks [Ll]ike:\*\*\s*', '', stripped))
        elif stripped.startswith('**Why it hurts'):
            body_parts.append(re.sub(r'^\*\*Why it hurts[^*]*\*\*\s*', '', stripped))
        elif stripped.startswith('**Why It Hurts'):
            body_parts.append(re.sub(r'^\*\*Why It Hurts[^*]*\*\*\s*', '', stripped))
        elif stripped.startswith('**The fix:**') or stripped.startswith('**The Fix:**'):
            fix = re.sub(r'^\*\*The [Ff]ix:\*\*\s*', '', stripped)
        else:
            body_parts.append(stripped)
        i += 1

    return {
        "type": "mistake_box",
        "title": title_line,
        "body": " ".join(body_parts),
        "fix": fix,
    }, i


def parse_mistake_alt(lines, start):
    """Parse mistake with ### subsections (What It Looks Like, etc.)."""
    title_line = lines[start].strip().lstrip('#').strip()
    i = start + 1
    body_parts = []
    fix = ""
    current_section = None

    while i < len(lines):
        stripped = lines[i].strip()
        # Stop at next ## heading or ---
        if stripped.startswith('## ') or stripped == '---':
            break
        # Stop at next mistake heading
        if re.match(r'^###\s+Mistake\s+#\d+', stripped):
            break
        if stripped == '':
            i += 1
            continue

        # Check for subsection headers
        if stripped.startswith('### '):
            sub = stripped[4:].strip()
            if 'What It Looks Like' in sub or 'What it looks like' in sub:
                current_section = 'body'
            elif 'Why It Hurts' in sub or 'Why it hurts' in sub:
                current_section = 'body'
            elif 'How to Fix' in sub or 'How to fix' in sub or 'The Fix' in sub:
                current_section = 'fix'
            else:
                # Some other ### under a mistake — probably not a mistake subsection
                break
            i += 1
            continue

        if current_section == 'fix':
            fix = stripped if not fix else fix + " " + stripped
        else:
            body_parts.append(stripped)
        i += 1

    return {
        "type": "mistake_box",
        "title": title_line,
        "body": " ".join(body_parts),
        "fix": fix,
    }, i


def parse_mistake_h2(lines, start):
    """Parse ## Mistake #N with ### subsections (common-mistakes format).

    In this format, the content is NOT prefixed with **What it looks like:** etc.
    Instead, paragraphs between ### headings are the content for that section.
    The flow is: prose paragraphs alternate between description, cause, and fix,
    separated by ### headings.
    """
    title_line = lines[start].strip().lstrip('#').strip()
    i = start + 1
    body_parts = []
    fix = ""
    current_section = 'body'

    while i < len(lines):
        stripped = lines[i].strip()
        # Stop at next ## or # heading or ---
        if stripped.startswith('## ') and not stripped.startswith('### '):
            break
        if stripped.startswith('# ') and not stripped.startswith('## '):
            break
        if stripped == '---':
            break
        if stripped == '':
            i += 1
            continue

        if stripped.startswith('### '):
            sub = stripped[4:].strip()
            if 'What It Looks Like' in sub or 'What it looks like' in sub:
                current_section = 'body'
            elif 'Why' in sub:
                current_section = 'body'
            elif 'How to Fix' in sub or 'How to fix' in sub or 'The Fix' in sub:
                current_section = 'fix'
            else:
                break
            i += 1
            continue

        if current_section == 'fix':
            fix = stripped if not fix else fix + " " + stripped
        else:
            body_parts.append(stripped)
        i += 1

    return {
        "type": "mistake_box",
        "title": title_line,
        "body": " ".join(body_parts),
        "fix": fix,
    }, i


def parse_blockquote(lines, start):
    """Parse a > blockquote."""
    parts = []
    i = start
    while i < len(lines) and lines[i].strip().startswith('>'):
        text = lines[i].strip().lstrip('>').strip()
        if text:
            parts.append(text)
        i += 1

    full_text = " ".join(parts)

    # Cross-reference: > **Continue in Section X**
    m = re.match(r'\*\*Continue in (Section \d+)\*\*', full_text)
    if m:
        section = m.group(1)
        note_parts = [p.strip('*').strip() for p in parts[1:] if p.strip('*').strip()]
        return {"type": "cross_ref", "section": section, "note": " ".join(note_parts)}, i

    # Final Thought blockquote
    if full_text.startswith('**Final Thought**'):
        note_parts = [p.strip('*').strip() for p in parts if not p.startswith('**Final Thought**') and p.strip('*').strip()]
        return {"type": "hint", "text": " ".join(note_parts)}, i

    return {"type": "prose", "text": full_text}, i


def count_underscore_lines(lines, start):
    """Count consecutive underscore lines and return (count, next_index)."""
    count = 0
    i = start
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith('_____'):
            count += 1
            i += 1
        elif s == '' and i + 1 < len(lines) and lines[i + 1].strip().startswith('_____'):
            i += 1  # skip blank between underscores
        else:
            break
    return count, i


def underscore_count_to_height(count):
    """Map underscore line count to writing_box height."""
    if count <= 1:
        return "80pt"
    elif count <= 2:
        return "100pt"
    elif count <= 3:
        return "145pt"
    else:
        return "200pt"


# ── Main parser ──────────────────────────────────────────────

def parse_section_header(lines):
    """Extract section number, title, and subtitle from the first lines."""
    title_line = lines[0].strip().lstrip('#').strip()

    # Try to extract section number: "SECTION 1:", "Section Two:", "Section 13:", etc.
    section_num = None
    title = title_line

    m = re.match(r'(?:SECTION|Section)\s+(\d+)\s*[:\-—]\s*(.*)', title_line)
    if m:
        section_num = int(m.group(1))
        title = m.group(2).strip()

    # Word numbers
    word_nums = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5,
                 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10}
    m = re.match(r'(?:SECTION|Section)\s+(\w+)\s*[:\-—]\s*(.*)', title_line)
    if m and m.group(1) in word_nums:
        section_num = word_nums[m.group(1)]
        title = m.group(2).strip()

    # Check for APPENDIX
    if title_line.startswith('APPENDIX:'):
        title = title_line.replace('APPENDIX:', '').strip()

    # Strip trailing subtitle markers
    title = re.sub(r'\s*[—\-]+\s*$', '', title).strip()

    # Check line 2 for bold subtitle
    subtitle = None
    next_content_line = 1
    if len(lines) > 1:
        line2 = lines[1].strip()
        if line2.startswith('**') and line2.endswith('**'):
            subtitle = line2.strip('*').strip()
            next_content_line = 2

    return section_num, title, subtitle, next_content_line


def parse_markdown(md_text, section_number, canonical_title):
    """Parse full markdown text into JSON content blocks."""
    lines = md_text.split('\n')
    content = []

    # Parse header
    _, title_from_md, subtitle, start_line = parse_section_header(lines)
    title = canonical_title or title_from_md

    i = start_line

    # Skip blanks after header
    while i < len(lines) and lines[i].strip() == '':
        i += 1

    # Collect intro paragraphs (before first --- or ## heading)
    intro_paragraphs = []
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped == '---':
            break
        if stripped.startswith('## ') or stripped.startswith('# '):
            break
        if stripped:
            intro_paragraphs.append(stripped)
        i += 1

    # Build section_title_intro from first paragraph (or all intro if short)
    section_title_intro = intro_paragraphs[0] if intro_paragraphs else None

    # Remaining intro paragraphs as prose
    for p in intro_paragraphs[1:]:
        content.append({"type": "prose", "text": p})

    # Skip the ---
    if i < len(lines) and lines[i].strip() == '---':
        i += 1

    # Skip "In This Section" TOC
    j = i
    while j < len(lines) and lines[j].strip() == '':
        j += 1
    if j < len(lines) and 'In This Section' in lines[j].strip():
        while i < len(lines) and lines[i].strip() != '---':
            i += 1
        if i < len(lines):
            i += 1

    # ── Parse body ──
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

        # H1 in body (sub-parts of a section, e.g. "# PART TWO: ...")
        # Treat as heading2 since section title was already consumed
        if stripped.startswith('# ') and not stripped.startswith('## '):
            text = stripped[2:].strip()
            content.append({"type": "heading2", "text": text})
            i += 1
            continue

        # Heading 2
        if stripped.startswith('## ') and not stripped.startswith('### '):
            text = stripped[3:].strip()

            # Check for ## Mistake #N: pattern
            if re.match(r'Mistake\s+#\d+', text):
                # Look ahead for ### subsections
                j = i + 1
                uses_subsections = False
                while j < len(lines) and j < i + 15:
                    s = lines[j].strip()
                    if s.startswith('### What') or s.startswith('### How') or s.startswith('### Why') or s.startswith('### The'):
                        uses_subsections = True
                        break
                    if s.startswith('## ') or s.startswith('# ') or s == '---':
                        break
                    j += 1
                if uses_subsections:
                    item, i = parse_mistake_h2(lines, i)
                else:
                    item, i = parse_mistake(lines, i)
                content.append(item)
                continue

            content.append({"type": "heading2", "text": text})
            i += 1
            continue

        # Heading 3
        if stripped.startswith('### ') and not stripped.startswith('#### '):
            text = stripped[4:].strip()

            # Check for Mistake pattern (inline style)
            if re.match(r'Mistake\s+#\d+', text):
                # Look ahead: does it use ### subsections or inline **bold:** markers?
                j = i + 1
                uses_subsections = False
                while j < len(lines) and j < i + 15:
                    s = lines[j].strip()
                    if s.startswith('### What') or s.startswith('### How') or s.startswith('### Why') or s.startswith('### The'):
                        uses_subsections = True
                        break
                    if s.startswith('## ') or s == '---':
                        break
                    j += 1

                if uses_subsections:
                    item, i = parse_mistake_alt(lines, i)
                else:
                    item, i = parse_mistake(lines, i)
                content.append(item)
                continue

            content.append({"type": "heading3", "text": text})
            i += 1
            continue

        # Heading 4 — may be italic exercise prompt
        if stripped.startswith('#### '):
            text = stripped[5:].strip()
            # Strip surrounding italic markers if present
            if text.startswith('*') and text.endswith('*') and not text.startswith('**'):
                text = text[1:-1]
            content.append({"type": "heading4", "text": text})
            i += 1
            continue

        # Table
        if stripped.startswith('|') and i + 1 < len(lines) and '|' in lines[i + 1]:
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            headers, rows = parse_table(table_lines)
            if headers and rows is not None:
                content.append(classify_table(headers, rows))
            continue

        # Checklist with ☐ or [ ]
        if '☐' in stripped or re.match(r'^[-*]\s*\[[ ]\]', stripped):
            items = []
            while i < len(lines):
                s = lines[i].strip()
                if '☐' in s:
                    # Extract text after ☐
                    parts = s.split('☐')
                    for p in parts[1:]:
                        clean = p.strip().strip('☐').strip()
                        if clean:
                            items.append(clean)
                    i += 1
                elif re.match(r'^[-*]\s*\[[ ]\]', s):
                    items.append(re.sub(r'^[-*]\s*\[[ ]\]\s*', '', s))
                    i += 1
                elif s == '':
                    # Check if next line continues the checklist
                    if i + 1 < len(lines) and ('☐' in lines[i + 1] or re.match(r'^[-*]\s*\[[ ]\]', lines[i + 1].strip())):
                        i += 1
                    else:
                        break
                else:
                    break
            if items:
                content.append({"type": "checklist", "items": items})
            continue

        # Bullet list
        if stripped.startswith('- ') or stripped.startswith('* '):
            marker = stripped[0]
            items = []
            while i < len(lines):
                s = lines[i].strip()
                if s.startswith(f'{marker} '):
                    items.append(s[2:])
                    i += 1
                elif s == '':
                    # Check if list continues after blank
                    if i + 1 < len(lines) and lines[i + 1].strip().startswith(f'{marker} '):
                        i += 1
                    else:
                        break
                else:
                    break
            content.append({"type": "bullet_list", "items": items})
            continue

        # Numbered list that's just fill-in blanks (1. ____)
        if re.match(r'^\d+\.\s+_____', stripped):
            count = 0
            while i < len(lines) and re.match(r'^\d+\.\s+_____', lines[i].strip()):
                count += 1
                i += 1
            # Skip blanks between
            while i < len(lines) and lines[i].strip() == '':
                if i + 1 < len(lines) and re.match(r'^\d+\.\s+_____', lines[i + 1].strip()):
                    i += 1
                else:
                    break
            content.append({
                "type": "writing_lines",
                "count": count,
            })
            continue

        # Underscore lines (writing boxes)
        if stripped.startswith('_____'):
            count, i = count_underscore_lines(lines, i)
            height = underscore_count_to_height(count)
            # Check if previous item was a bold question — use it as label
            label = "Your Answer"
            if content and content[-1].get("type") == "prose":
                prev_text = content[-1].get("text", "")
                # Bold question followed by underscores → convert to heading4 + writing_box
                if prev_text.startswith("**") and prev_text.endswith("**"):
                    label = prev_text.strip('*').strip()
                    content[-1] = {"type": "heading4", "text": label}
            content.append({"type": "writing_box", "label": label, "height": height})
            continue

        # Bold label + underscores on same line: **Label:** ___
        m = re.match(r'^\*\*(.+?):\*\*\s*_+', stripped)
        if m:
            label = m.group(1).strip()
            content.append({"type": "writing_box", "label": label, "height": "55pt"})
            i += 1
            continue

        # Label + underscores: "Primary subtype: ___"
        m = re.match(r'^(.+?):\s*_____+', stripped)
        if m and not stripped.startswith('*') and not stripped.startswith('#'):
            label = m.group(1).strip()
            # Clean up bold markers in label
            label = label.replace('**', '')
            content.append({"type": "writing_box", "label": label, "height": "55pt"})
            i += 1
            continue

        # Standalone italic line → hint
        if re.match(r'^\*[^*]+\*$', stripped):
            text = stripped.strip('*')
            content.append({"type": "hint", "text": text})
            i += 1
            continue

        # Multi-line italic (starts with * but continues)
        if stripped.startswith('*') and not stripped.startswith('**') and not stripped.endswith('*'):
            # Collect until closing *
            parts = [stripped]
            i += 1
            while i < len(lines):
                s = lines[i].strip()
                if s == '':
                    break
                parts.append(s)
                if s.endswith('*'):
                    i += 1
                    break
                i += 1
            full = ' '.join(parts)
            if full.startswith('*') and full.endswith('*'):
                full = full[1:-1]
            content.append({"type": "hint", "text": full})
            continue

        # Reference line: (Reference: Section X — Title)
        if stripped.startswith('(Reference:') or stripped.startswith('(reference:'):
            # Extract section reference
            m = re.search(r'Section\s+(\d+)\s*[—\-]\s*(.+?)\)', stripped)
            if m:
                content.append({
                    "type": "cross_ref",
                    "section": f"Section {m.group(1)}",
                    "note": m.group(2).strip(),
                })
            else:
                content.append({"type": "hint", "text": stripped.strip('()')})
            i += 1
            continue

        # Skip navigation links like [Back to Contents](#)
        if re.match(r'^\[.+\]\(#.*\)$', stripped):
            i += 1
            continue

        # Regular prose paragraph
        content.append({"type": "prose", "text": stripped})
        i += 1

    return {
        "section_number": section_number,
        "title": title,
        "section_title_intro": section_title_intro,
        "content": content,
    }


# ── Post-processing ──────────────────────────────────────────

def post_process(data):
    """Clean up the parsed content."""
    content = data["content"]
    new_content = []

    for i, item in enumerate(content):
        # Convert prose after heading4 to hint if it looks instructional
        if item["type"] == "hint" and new_content and new_content[-1].get("type") == "heading4":
            # Already a hint, keep it
            pass
        elif item["type"] == "prose" and new_content and new_content[-1].get("type") == "heading4":
            # Check if it's italicized guidance text
            text = item["text"]
            if text.startswith('*') and text.endswith('*') and not text.startswith('**'):
                item = {"type": "hint", "text": text.strip('*')}

        new_content.append(item)

    data["content"] = new_content

    # Remove consecutive duplicate dividers
    filtered = []
    for item in data["content"]:
        if item["type"] == "divider" and filtered and filtered[-1]["type"] == "divider":
            continue
        filtered.append(item)
    data["content"] = filtered

    # Remove leading/trailing dividers
    while data["content"] and data["content"][0]["type"] == "divider":
        data["content"].pop(0)
    while data["content"] and data["content"][-1]["type"] == "divider":
        data["content"].pop()

    return data


# ── Main ─────────────────────────────────────────────────────

def convert_section(pattern, section_number, output_name, canonical_title):
    """Convert a single section."""
    md_file = find_md_file(pattern)
    if not md_file:
        print(f"  SKIP: No file matching '{pattern}'")
        return False

    with open(md_file, 'r') as f:
        md_text = f.read()

    data = parse_markdown(md_text, section_number, canonical_title)
    data = post_process(data)

    output_path = DATA_DIR / f"{output_name}.json"
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Stats
    types = {}
    for item in data['content']:
        t = item.get('type', '?')
        types[t] = types.get(t, 0) + 1

    total = len(data['content'])
    type_summary = ", ".join(f"{t}:{c}" for t, c in sorted(types.items()))
    print(f"  {output_name}.json — {total} blocks ({type_summary})")
    return True


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    filter_arg = sys.argv[1] if len(sys.argv) > 1 else None

    converted = 0
    for pattern, num, output_name, title in SECTION_MAP:
        if filter_arg and filter_arg.lower() not in pattern.lower() and filter_arg != str(num):
            continue
        if convert_section(pattern, num, output_name, title):
            converted += 1

    print(f"\nConverted {converted} sections to typst/data/")


if __name__ == "__main__":
    main()
