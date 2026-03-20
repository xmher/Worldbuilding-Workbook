# Worldbuilding Workbook — Project Guide

## Project Overview

A romantasy worldbuilding workbook (PDF) generated via:
**Markdown source → JSON content → Python translator → Typst source → PDF output**

## Repository Structure

```
Updated Sections/             # *** SOURCE OF TRUTH *** — updated markdown for all sections
  01_Geography_Environment_UPDATED.md
  02_Flora_Fauna_Ecosystems_UPDATED.md
  Culture_Customs_Daily_Life_UPDATED.md
  Economy_Labour_Resources_UPDATED.md
  Government_Power_and_Law_-_final (1).md
  religion-myth-prophecy-final.md
  history-and-lore-updated.md
  magic-system-updated (1).md
  09_Technology_Infrastructure_UPDATED.md
  language-and-communication-updated (1).md
  section13-pressure-cooker-updated.md
  section14_institutions_and_structures (2).md
  Designing_Your_Key_Locations_-_exercise_audit_applied.md
  Web_of_Systems_exercises_updated.md
  section17-consistency-check_UPDATED.md
  The-Agency-Check_UPDATED.md
  Quick_Reference_Sheets_UPDATED.md
  common-romantasy-worldbuilding-mistakes_ASSEMBLED.md

typst/
  template.typ          # Typst component library (colors, fonts, all UI elements)
  build.py              # JSON → Typst generator + PDF compiler
  add_prose.py          # JSON enrichment script
  workbook.typ          # Main file (imports template, includes sections)
  data/                 # JSON content files (one per section)
    00_introduction.json
    01_geography.json
  sections/             # Generated Typst files (DO NOT edit manually)
  fonts/                # Libre Baskerville, Cormorant Garamond, Inter
  output/               # Compiled PDF output

convert_geography.py    # Markdown → JSON converter (Geography-specific)
LAYOUT_SYSTEM.md        # Full layout system specification
```

### Pipeline Flow

```
Updated Sections/*.md  →  convert to JSON  →  typst/data/*.json
                                                     ↓
                                              build.py --generate
                                                     ↓
                                              typst/sections/*.typ
                                                     ↓
                                              review.py (automated QA checks)
                                                     ↓
                                              build.py --compile
                                                     ↓
                                              typst/output/workbook.pdf
                                                     ↓
                                              AI REVIEW (Claude reads PDF page-by-page)
                                                     ↓
                                              Human final review
```

## Build Commands

```bash
cd typst
python build.py              # generate .typ + compile PDF
python build.py --generate   # generate .typ only
python build.py --compile    # compile only
python build.py --review     # full pipeline: generate + automated QA + compile (then AI reviews)
python review.py             # run automated QA checks standalone
python review.py 03_culture  # check one section only
```

## Layout System

See `LAYOUT_SYSTEM.md` for the full specification. Key principles:

1. **JSON defines intent** via optional `layout` field on any content block
2. **Typst handles execution** using `layout()` to measure real remaining space
3. **Python is a translator** — no height estimation, no layout decisions

### JSON Layout Fields (all optional)

| Field | Values | Purpose |
|-------|--------|---------|
| `page_behavior` | `flow`, `keep_together`, `start_new_page`, `keep_with_next` | Page break behavior |
| `fill_page` | `true` / `false` | Expand to fill remaining page space |
| `min_space` | `150`, `"quarter"`, `"third"`, `"half"` | Minimum space before rendering |
| `continuation` | `{"extra_pages": N}` | Multi-page tables |

Most blocks need zero layout fields — defaults are built into Typst components.

## Content Block Types

| Type | Purpose | Notes |
|------|---------|-------|
| `title_page` | Full-page title | `title` (supports `\n`), `tagline` |
| `section_title_page` | Section opener | Auto-generated from section metadata |
| `heading2/3/4` | Section headings | `text` field |
| `prose` | Body text | Supports `**bold**` and `*italic*` markdown |
| `lead_text` | Italic intro paragraph | |
| `hint` | Muted guidance text | |
| `divider` | Gold flourish separator | |
| `anchor_card` | Key question box | `title`, `question` |
| `framework_box` | Concept box | `title`, `content` or `content_blocks` |
| `mistake_box` | Error callout | `title`, `body`, `fix` |
| `writing_box` | Blank user input area | `label`, `height` |
| `writing_lines` | Ruled lines | `count` |
| `checklist` | Checkbox list | `items` array |
| `data_table` | Read-only reference table | `headers`, `rows` |
| `structured_table` | Pre-labeled user-fill table | `headers`, `rows`, `example_rows`, `row_height` |
| `open_table` | Page-filling blank table | `headers`, `example_rows`, `row_height`, `fill_strategy` |
| `cross_ref` | Section reference callout | `section`, `note` |
| `bullet_list` | Enumerated list | `items` array |
| `group` | Grouped content | `content` array, `full_page` bool |

## Post-Build QA Checklist

Run this after every PDF generation.

### Critical Issues (must fix)

- [ ] Orphaned heading: h2/h3/h4 at bottom of page with content on next page
- [ ] Split box: framework_box, mistake_box, anchor_card, or writing_box breaking across pages
- [ ] Ghost row: table row partially visible / clipped at page break
- [ ] Missing section title page: section content starts without its title page

### Major Issues (should fix)

- [ ] Table starts too low: table begins in bottom third with only 1-2 rows visible
- [ ] Unfilled open table: open table has significant blank space instead of filling page
- [ ] Large mid-page whitespace: >2 inches of blank space mid-page
- [ ] Heading without content: heading visible but its content is on next page

### Minor Issues (nice to fix)

- [ ] Divider at page top: decorative divider as first element on a page
- [ ] Widowed line: single prose line alone at top of page
- [ ] Cramped table rows: content truncated or overlapping row borders
- [ ] Tiny writing box: writing box with less than ~1 inch of writable space

### Report Format

```
Page [N]: [CATEGORY] - [description]
  → Fix: [suggested fix]
```

Categories: SPACING, TABLE, BOX, FLOW

## Key Design Decisions

- **Color scheme**: Forest green (#065f46), gold (#e2c98a), warm cream (#fdfbf7)
- **Fonts**: Libre Baskerville (display), Cormorant Garamond (accent), Inter (body)
- **Page size**: 8.5in × 11in, margins ~1in
- **Double decorative border**: green outer (3pt), gold inner (1pt)
- **Table row height default**: 55pt for user-fill tables
- **Page capacity**: ~620pt usable height

## Rules for AI Assistants

1. **Never edit files in `typst/sections/`** — these are generated by `build.py`
2. **Content changes go in JSON** (`typst/data/*.json`), not Typst files
3. **Style changes go in `template.typ`**, not individual sections
4. **Run `python build.py --review`** after any JSON or template change to regenerate
5. **Layout overrides go in JSON `layout` field**, not in Python logic
6. **Don't add height estimation to Python** — let Typst handle layout
7. **Review the PDF output** using the AI Review Process below after each build

## AI Review Process

After every build, Claude must perform a manual review of the compiled PDF before
the human reviews it. This is a required pipeline step, not optional.

### How to review

1. Run `python build.py --review` (generates, runs automated checks, compiles)
2. Read the PDF at `typst/output/workbook.pdf` using the Read tool (page by page, ~20 pages at a time)
3. Check every page against the QA checklist below
4. Report all findings to the user in this format:

```
Page [N]: [SEVERITY] [CATEGORY] - [description]
  → Fix: [specific fix — which JSON file, which block, what to change]
```

Severity: CRITICAL (must fix), MAJOR (should fix), MINOR (nice to fix)

### What to look for (that scripts can't catch)

- **Orphaned headings**: heading visible at page bottom, its content on next page
- **Split boxes**: framework_box/mistake_box/anchor_card breaking across pages
- **Ghost rows**: table row partially clipped at page break
- **Awkward page breaks**: content that looks wrong split across pages even if technically valid
- **Wasted space**: large blank areas mid-page that could fit more content
- **Visual rhythm**: sections that feel cramped or too sparse compared to others
- **Reading flow**: content that's confusing to follow due to layout choices
- **Table legibility**: text overflowing cells, columns too narrow, rows too cramped
- **Writing box sizing**: boxes too small to be useful or too large relative to the prompt
- **Consistency**: similar elements looking different across sections

### Decision authority

Claude should make judgment calls and propose specific fixes for:
- Adding `layout` fields to JSON blocks to fix page break issues
- Adjusting `row_height` values when rows are cramped
- Adding `fill_page: true` to writing boxes that should expand
- Suggesting group restructuring when content should stay together
- Recommending `page_behavior: "start_new_page"` for elements that need breathing room

Report findings to the user. Fix critical/major issues directly if confident,
ask before fixing if the change is subjective.
