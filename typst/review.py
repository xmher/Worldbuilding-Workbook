#!/usr/bin/env python3
"""
Automated QA Review Script
============================
Analyzes generated .typ files and source JSON for layout and formatting
issues before manual review. Runs after build.py --generate and before
PDF compilation to catch problems early.

Usage:
    python review.py                  # review all sections
    python review.py 03_culture       # review one section
    python review.py --json-only      # validate JSON only
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
SECTIONS_DIR = SCRIPT_DIR / "sections"

# Layout constants (must match template.typ)
USABLE_PAGE_HEIGHT = 620  # pt
MIN_WRITING_BOX_HEIGHT = 120  # pt
MIN_ROW_HEIGHT = 60  # pt

# Valid block types (must match GENERATORS in build.py)
VALID_TYPES = {
    "title_page", "section_title_page",
    "heading2", "heading3", "heading4",
    "prose", "lead_text", "hint", "divider",
    "bullet_list", "anchor_card", "framework_box", "mistake_box",
    "writing_box", "writing_lines", "checklist",
    "data_table", "input_table", "structured_table", "open_table",
    "cross_ref", "group",
}

# Types that can appear inside framework_box content_blocks
VALID_CONTENT_BLOCK_TYPES = {"hint", "prose", "heading_inline", "bullet_list"}


class Issue:
    CRITICAL = "CRITICAL"
    MAJOR = "MAJOR"
    MINOR = "MINOR"

    def __init__(self, severity, category, message, location="", fix=""):
        self.severity = severity
        self.category = category
        self.message = message
        self.location = location  # e.g., "03_culture.json, block 12"
        self.fix = fix

    def __str__(self):
        loc = f" [{self.location}]" if self.location else ""
        fix = f"\n  → Fix: {self.fix}" if self.fix else ""
        return f"  {self.severity}: {self.category} - {self.message}{loc}{fix}"


def review_json(filepath: Path) -> list[Issue]:
    """Validate a single JSON data file for structural and content issues."""
    issues = []
    loc_prefix = filepath.name

    with open(filepath) as f:
        data = json.load(f)

    # Check required top-level fields
    if "title" not in data:
        issues.append(Issue(Issue.MAJOR, "JSON", "Missing 'title' field", loc_prefix))
    if "content" not in data:
        issues.append(Issue(Issue.CRITICAL, "JSON", "Missing 'content' array", loc_prefix))
        return issues

    content = data["content"]
    if not isinstance(content, list):
        issues.append(Issue(Issue.CRITICAL, "JSON", "'content' is not an array", loc_prefix))
        return issues

    # Check for section title page
    has_title = any(
        b.get("type") in ("title_page", "section_title_page")
        for b in content
    )
    has_intro = data.get("section_title_intro") is not None
    if not has_title and not has_intro and data.get("section_number", 0) > 0:
        issues.append(Issue(
            Issue.MAJOR, "FLOW",
            "No section title page and no section_title_intro — section will start abruptly",
            loc_prefix,
            "Add 'section_title_intro' to the JSON or add a section_title_page block"
        ))

    for idx, block in enumerate(content):
        bloc_loc = f"{loc_prefix}, block {idx}"
        btype = block.get("type", "")

        # Unknown type
        if btype not in VALID_TYPES:
            issues.append(Issue(
                Issue.CRITICAL, "JSON",
                f"Unknown block type '{btype}'",
                bloc_loc,
                f"Valid types: {', '.join(sorted(VALID_TYPES))}"
            ))
            continue

        # Type-specific validation
        if btype in ("heading2", "heading3", "heading4", "prose", "lead_text", "hint"):
            if "text" not in block:
                issues.append(Issue(Issue.CRITICAL, "JSON", f"'{btype}' missing 'text' field", bloc_loc))
            elif not block["text"].strip():
                issues.append(Issue(Issue.MINOR, "JSON", f"'{btype}' has empty text", bloc_loc))

        elif btype == "bullet_list":
            if "items" not in block or not block["items"]:
                issues.append(Issue(Issue.MAJOR, "JSON", "bullet_list has no items", bloc_loc))

        elif btype == "checklist":
            if "items" not in block or not block["items"]:
                issues.append(Issue(Issue.MAJOR, "JSON", "checklist has no items", bloc_loc))

        elif btype in ("data_table", "structured_table", "open_table"):
            if "headers" not in block or not block["headers"]:
                issues.append(Issue(Issue.CRITICAL, "JSON", f"{btype} missing headers", bloc_loc))
            headers = block.get("headers", [])
            for row_key in ("rows", "example_rows"):
                for ri, row in enumerate(block.get(row_key, [])):
                    if len(row) != len(headers):
                        issues.append(Issue(
                            Issue.MAJOR, "TABLE",
                            f"{btype} {row_key}[{ri}] has {len(row)} cells but {len(headers)} headers",
                            bloc_loc,
                            "Ensure every row has the same number of cells as headers"
                        ))

        elif btype == "writing_box":
            height = block.get("height", "120pt")
            try:
                int(str(height).replace("pt", ""))
            except ValueError:
                issues.append(Issue(Issue.MAJOR, "JSON", f"Invalid writing_box height: '{height}'", bloc_loc))

        elif btype == "framework_box":
            if "content" not in block and "content_blocks" not in block:
                issues.append(Issue(Issue.MINOR, "JSON", "framework_box has no content or content_blocks", bloc_loc))
            if "content_blocks" in block:
                for ci, cb in enumerate(block["content_blocks"]):
                    cb_type = cb.get("type", "")
                    if cb_type not in VALID_CONTENT_BLOCK_TYPES:
                        issues.append(Issue(
                            Issue.MAJOR, "JSON",
                            f"framework_box content_block[{ci}] has unknown type '{cb_type}'",
                            bloc_loc
                        ))

        elif btype == "anchor_card":
            if "question" not in block:
                issues.append(Issue(Issue.MAJOR, "JSON", "anchor_card missing 'question'", bloc_loc))

        elif btype == "cross_ref":
            if "section" not in block:
                issues.append(Issue(Issue.MAJOR, "JSON", "cross_ref missing 'section'", bloc_loc))

        elif btype == "group":
            children = block.get("content", [])
            if not children:
                issues.append(Issue(Issue.MINOR, "JSON", "group has no content", bloc_loc))
            for ci, child in enumerate(children):
                ctype = child.get("type", "")
                if ctype not in VALID_TYPES:
                    issues.append(Issue(
                        Issue.MAJOR, "JSON",
                        f"group child[{ci}] has unknown type '{ctype}'",
                        bloc_loc
                    ))

        # Check for invalid layout fields
        layout = block.get("layout", {})
        if layout:
            valid_layout_keys = {"page_behavior", "fill_page", "min_space", "continuation"}
            for key in layout:
                if key not in valid_layout_keys:
                    issues.append(Issue(
                        Issue.MINOR, "JSON",
                        f"Unknown layout field '{key}'",
                        bloc_loc
                    ))

    # Sequence checks
    _check_sequences(content, loc_prefix, issues)

    return issues


def _check_sequences(content: list, loc_prefix: str, issues: list):
    """Check for problematic block sequences in JSON content."""

    for idx in range(len(content)):
        btype = content[idx].get("type", "")
        next_type = content[idx + 1].get("type", "") if idx + 1 < len(content) else ""
        prev_type = content[idx - 1].get("type", "") if idx > 0 else ""

        # Consecutive dividers
        if btype == "divider" and next_type == "divider":
            issues.append(Issue(
                Issue.MINOR, "FLOW",
                "Consecutive dividers",
                f"{loc_prefix}, block {idx}",
                "Remove one of the dividers"
            ))

        # Heading at end of content (potential orphan)
        if btype in ("heading2", "heading3", "heading4") and idx == len(content) - 1:
            issues.append(Issue(
                Issue.CRITICAL, "FLOW",
                f"Section ends with a {btype} and no following content",
                f"{loc_prefix}, block {idx}",
                "Add content after the heading or remove it"
            ))

        # Empty prose between headings (useless whitespace)
        if btype == "prose" and not content[idx].get("text", "").strip():
            issues.append(Issue(
                Issue.MINOR, "FLOW",
                "Empty prose block",
                f"{loc_prefix}, block {idx}"
            ))

        # Heading immediately followed by another heading of same or higher level
        if btype == "heading2" and next_type == "heading2":
            issues.append(Issue(
                Issue.MAJOR, "FLOW",
                "Two consecutive heading2 blocks with no content between them",
                f"{loc_prefix}, block {idx}",
                "Add introductory prose or remove one heading"
            ))


def review_typ(filepath: Path) -> list[Issue]:
    """Analyze a generated .typ file for potential layout issues."""
    issues = []
    loc_prefix = filepath.name
    text = filepath.read_text()
    lines = text.split("\n")

    # Check for WARNING comments from build.py (unknown types)
    for i, line in enumerate(lines):
        if "// WARNING: unknown type" in line:
            issues.append(Issue(
                Issue.CRITICAL, "BUILD",
                f"Build warning: {line.strip()}",
                f"{loc_prefix}, line {i+1}"
            ))

    # Check for unescaped # that would cause Typst compilation errors
    # Only flag # that appear in plain text content (inside [] brackets)
    # Skip lines that are Typst function calls, comments, or imports
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith("//") or stripped.startswith("#"):
            continue
        # Only check lines that look like plain text content (not inside function args)
        # A raw # in prose text (not preceded by \ and not followed by a letter) is suspect
        raw_hashes = re.findall(r'(?<!\\)#(?![a-zA-Z("])', stripped)
        if raw_hashes:
            issues.append(Issue(
                Issue.MINOR, "ESCAPE",
                f"Possibly unescaped '#' in content text",
                f"{loc_prefix}, line {i+1}",
                "Escape as \\# if this is literal text"
            ))

    # Check for very long non-breakable blocks (might overflow page)
    block_pattern = re.compile(r'#block\(breakable: false\)\[')
    in_block = False
    block_start = 0
    bracket_depth = 0
    for i, line in enumerate(lines):
        if not in_block:
            if '#block(breakable: false)[' in line:
                in_block = True
                block_start = i
                bracket_depth = line.count('[') - line.count(']')
        else:
            bracket_depth += line.count('[') - line.count(']')
            if bracket_depth <= 0:
                block_len = i - block_start
                if block_len > 80:
                    issues.append(Issue(
                        Issue.MAJOR, "SPACING",
                        f"Non-breakable block spans {block_len} lines — may overflow page",
                        f"{loc_prefix}, lines {block_start+1}-{i+1}",
                        "Consider allowing this block to break or splitting it"
                    ))
                in_block = False

    # Check for structured/open tables with row-height below minimum
    for i, line in enumerate(lines):
        match = re.search(r'row-height:\s*(\d+)pt', line)
        if match:
            rh = int(match.group(1))
            if rh < MIN_ROW_HEIGHT:
                issues.append(Issue(
                    Issue.MINOR, "TABLE",
                    f"Table row-height {rh}pt is below minimum {MIN_ROW_HEIGHT}pt",
                    f"{loc_prefix}, line {i+1}"
                ))

    return issues


def review_cross_section(data_dir: Path) -> list[Issue]:
    """Check cross-section concerns across all JSON files."""
    issues = []

    json_files = sorted(data_dir.glob("*.json"))
    all_sections = {}
    for jf in json_files:
        with open(jf) as f:
            data = json.load(f)
        all_sections[jf.stem] = data

    # Check cross_ref targets exist
    section_titles = {d["title"] for d in all_sections.values() if "title" in d}
    for name, data in all_sections.items():
        for idx, block in enumerate(data.get("content", [])):
            if block.get("type") == "cross_ref":
                ref_section = block.get("section", "")
                # Fuzzy check — cross_ref section names may not exactly match titles
                if ref_section and not any(ref_section.lower() in t.lower() for t in section_titles):
                    issues.append(Issue(
                        Issue.MINOR, "FLOW",
                        f"cross_ref to '{ref_section}' — no matching section title found",
                        f"{name}.json, block {idx}",
                        "Verify the section name matches an actual section title"
                    ))

    # Check section numbering gaps
    numbers = sorted(
        d.get("section_number", 0)
        for d in all_sections.values()
        if d.get("section_number") is not None and d.get("section_number", 0) > 0
    )
    if numbers:
        for i in range(len(numbers) - 1):
            gap = numbers[i + 1] - numbers[i]
            if gap > 1:
                issues.append(Issue(
                    Issue.MINOR, "FLOW",
                    f"Section numbering gap: {numbers[i]} → {numbers[i+1]}",
                    "cross-section",
                    "This may be intentional, but verify no section is missing"
                ))

    return issues


def format_report(all_issues: dict[str, list[Issue]], cross_issues: list[Issue]) -> str:
    """Format the full review report."""
    lines = []
    lines.append("=" * 60)
    lines.append("  AUTOMATED QA REVIEW REPORT")
    lines.append("=" * 60)

    total = sum(len(v) for v in all_issues.values()) + len(cross_issues)
    critical = sum(1 for v in all_issues.values() for i in v if i.severity == Issue.CRITICAL)
    critical += sum(1 for i in cross_issues if i.severity == Issue.CRITICAL)
    major = sum(1 for v in all_issues.values() for i in v if i.severity == Issue.MAJOR)
    major += sum(1 for i in cross_issues if i.severity == Issue.MAJOR)
    minor = total - critical - major

    lines.append(f"\n  Total issues: {total}  (CRITICAL: {critical}, MAJOR: {major}, MINOR: {minor})")

    if critical > 0:
        lines.append("\n  ⛔ CRITICAL issues found — must fix before compiling!")
    elif major > 0:
        lines.append("\n  ⚠ MAJOR issues found — should fix before final review.")
    elif minor > 0:
        lines.append("\n  ℹ Only minor issues found — review at your discretion.")
    else:
        lines.append("\n  ✓ No issues found — looking good!")

    # Per-section output
    for section_name in sorted(all_issues.keys()):
        section_issues = all_issues[section_name]
        if not section_issues:
            continue
        lines.append(f"\n{'─' * 50}")
        lines.append(f"  {section_name}")
        lines.append(f"{'─' * 50}")
        for severity in (Issue.CRITICAL, Issue.MAJOR, Issue.MINOR):
            severity_issues = [i for i in section_issues if i.severity == severity]
            for issue in severity_issues:
                lines.append(str(issue))

    # Cross-section issues
    if cross_issues:
        lines.append(f"\n{'─' * 50}")
        lines.append("  Cross-Section Issues")
        lines.append(f"{'─' * 50}")
        for issue in cross_issues:
            lines.append(str(issue))

    lines.append(f"\n{'=' * 60}")
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    json_only = "--json-only" in args
    args = [a for a in args if not a.startswith("--")]

    # Determine which sections to review
    if args:
        target = args[0]
        json_files = [DATA_DIR / f"{target}.json"]
        typ_files = [SECTIONS_DIR / f"{target}.typ"]
    else:
        json_files = sorted(DATA_DIR.glob("*.json"))
        typ_files = sorted(SECTIONS_DIR.glob("*.typ"))

    all_issues: dict[str, list[Issue]] = {}

    # JSON validation
    for jf in json_files:
        if not jf.exists():
            print(f"  Warning: {jf} not found, skipping")
            continue
        section_name = jf.stem
        issues = review_json(jf)
        all_issues.setdefault(section_name, []).extend(issues)

    # Typst analysis (unless json-only)
    if not json_only:
        for tf in typ_files:
            if not tf.exists():
                continue
            section_name = tf.stem
            issues = review_typ(tf)
            all_issues.setdefault(section_name, []).extend(issues)

    # Cross-section checks
    cross_issues = review_cross_section(DATA_DIR)

    # Output report
    report = format_report(all_issues, cross_issues)
    print(report)

    # Exit code: 2 for critical, 1 for major, 0 for minor/none
    if any(i.severity == Issue.CRITICAL for v in all_issues.values() for i in v):
        sys.exit(2)
    if any(i.severity == Issue.MAJOR for v in all_issues.values() for i in v):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
