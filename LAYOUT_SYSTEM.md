# Workbook Layout System

> Formatting and layout specification for the Markdown → JSON → Python → Typst → PDF pipeline.
> Goal: JSON defines layout **intent**, Typst handles layout **execution**, Python is a dumb translator.

## Source Content

All section content lives in `Updated Sections/` as markdown files. These are the **source of truth**.

The markdown uses consistent patterns that the converter must handle:
- `# Section Title` with subtitle on next line as bold text
- `## Heading` for major sections
- `### Heading` for subsections
- `#### *Italic exercise prompt*` for exercise introductions
- `### Mistake #N: Title` pattern for mistake boxes (with **What it looks like:** / **Why it hurts:** / **How to fix it:** structure)
- Tables with `| header | header |` format — may contain:
  - All-filled rows (→ `data_table`)
  - Label + empty cells (→ `structured_table`)
  - Italic example rows + empty rows (→ `open_table`)
- `---` horizontal rules as section dividers
- Bullet lists with bold lead items
- Blockquotes for cross-references or hints

---

## 1. JSON Layout Schema

### Design Principles

- Fields express **intent**, not rendering instructions
- Only add layout fields when the default behavior is wrong
- Most blocks need zero layout fields — sensible defaults handle them
- The schema is additive: omitted fields = default behavior

### Layout Fields

#### `page_behavior`

Controls how a block relates to page boundaries.

| Value | Meaning | Default for |
|-------|---------|-------------|
| `"flow"` | Normal flow, Typst decides breaks | All blocks (default) |
| `"keep_together"` | Don't split this block across pages | `framework_box`, `mistake_box`, `anchor_card`, `checklist`, `writing_box` |
| `"start_new_page"` | Force a page break before this block | `title_page`, `section_title_page` |
| `"keep_with_next"` | Keep this block on the same page as the following block | `heading2`, `heading3`, `heading4`, `hint` (when before a table) |

**Which block types use it:**
- Headings: `"keep_with_next"` (default, rarely needs override)
- Boxes (framework, mistake, anchor, writing): `"keep_together"` (default)
- Tables: `"flow"` (default — large tables should break naturally)
- Groups: `"keep_together"` if content is short, `"flow"` if tall

**JSON example:**
```json
{
  "type": "framework_box",
  "title": "The Pressure Cooker",
  "content": "...",
  "layout": {
    "page_behavior": "keep_together"
  }
}
```

#### `fill_page`

Whether a block should expand to consume remaining vertical space on the current page.

| Value | Meaning | Default for |
|-------|---------|-------------|
| `false` | Use natural/specified height | Everything (default) |
| `true` | Expand to fill remaining page space | `open_table`, `writing_box` (when explicitly desired) |

**Which block types use it:**
- `open_table`: `true` (default for this type — fill with blank rows)
- `writing_box`: `false` (default), set `true` for boxes that should expand
- All others: `false` always

**JSON example:**
```json
{
  "type": "open_table",
  "headers": ["Setting", "Why It Works", "Examples"],
  "example_rows": [["The Academy", "Trapped together", "Fourth Wing"]],
  "rows": [],
  "layout": {
    "fill_page": true
  }
}
```

#### `min_space`

Minimum remaining page space (in pt) required before rendering this block. If less space remains, the block moves to the next page. This replaces Python's height estimation.

| Value | Meaning |
|-------|---------|
| `null` / omitted | Typst decides (no minimum enforced) |
| `150` | At least 150pt of space must remain |
| `"quarter"` | At least 25% of page height must remain |
| `"third"` | At least 33% of page height must remain |
| `"half"` | At least 50% of page height must remain |

**Which block types use it:**
- `structured_table`: `"quarter"` (default — don't start a table in the last quarter of a page)
- `open_table`: `"third"` (default — need meaningful space to fill)
- `data_table`: `"quarter"` (default)
- `writing_box`: `150` (default — need at least some visible space)
- Headings: handled by `keep_with_next` instead, no min_space needed

**JSON example:**
```json
{
  "type": "structured_table",
  "headers": ["Element", "Description"],
  "rows": [["Mountains", ""], ["Rivers", ""]],
  "layout": {
    "min_space": "half"
  }
}
```

#### `continuation`

For tables that need to span multiple pages intentionally.

| Value | Meaning |
|-------|---------|
| `null` / omitted | Single page (default) |
| `{ "extra_pages": 1 }` | Add 1 extra page of blank rows after the initial page |

**Which block types use it:**
- `open_table`: when you want blank rows to continue onto a second page
- `structured_table`: when the table is genuinely too long for one page

**JSON example:**
```json
{
  "type": "open_table",
  "headers": ["Character", "Connection to Place", "Emotional Meaning"],
  "rows": [],
  "layout": {
    "fill_page": true,
    "continuation": { "extra_pages": 1 }
  }
}
```

### Summary of Defaults by Block Type

| Block Type | `page_behavior` | `fill_page` | `min_space` | `continuation` |
|------------|-----------------|-------------|-------------|----------------|
| `title_page` | `start_new_page` | — | — | — |
| `section_title_page` | `start_new_page` | — | — | — |
| `heading2` | `keep_with_next` | — | — | — |
| `heading3` | `keep_with_next` | — | — | — |
| `heading4` | `keep_with_next` | — | — | — |
| `prose` | `flow` | `false` | — | — |
| `lead_text` | `flow` | `false` | — | — |
| `hint` | `flow` | `false` | — | — |
| `divider` | `flow` | — | — | — |
| `anchor_card` | `keep_together` | `false` | — | — |
| `framework_box` | `keep_together` | `false` | — | — |
| `mistake_box` | `keep_together` | `false` | — | — |
| `writing_box` | `keep_together` | `false` | `150` | — |
| `checklist` | `keep_together` | `false` | — | — |
| `data_table` | `flow` | `false` | `"quarter"` | — |
| `structured_table` | `flow` | `false` | `"quarter"` | — |
| `open_table` | `flow` | `true` | `"third"` | — |
| `cross_ref` | `keep_together` | `false` | — | — |
| `bullet_list` | `flow` | `false` | — | — |
| `group` | auto (by height) | `false` | — | — |

### When to Override Defaults

Only add a `"layout"` object to a JSON block when you need non-default behavior:

1. **A writing box should fill the rest of the page** → add `"fill_page": true`
2. **A short table should never split** → add `"page_behavior": "keep_together"`
3. **A large table needs extra space** → add `"min_space": "half"`
4. **An open table needs a second page** → add `"continuation": {"extra_pages": 1}`
5. **A section should always start fresh** → add `"page_behavior": "start_new_page"`

Most blocks will have **no layout object at all**.

---

## 2. Typst Layout Rules

### Principle: Let Typst Measure, Not Python

The current system has Python estimate heights in points. This is inherently unreliable because Python doesn't know actual text wrapping, font metrics, or current page position. Instead, all layout decisions should happen in Typst using `layout(size => ...)` and `context { ... }` to query real remaining space.

### Rule Implementation

#### Rule 1: `page_behavior`

**`"keep_together"`** — Wrap content in `#block(breakable: false)[...]`
```typst
// Already how framework_box, mistake_box, etc. work
block(breakable: false)[
  // ... content
]
```

**`"start_new_page"`** — Insert `#pagebreak(weak: true)` before the block
```typst
pagebreak(weak: true)
// ... content
```

**`"keep_with_next"`** — Use Typst's native heading orphan prevention. Headings already have `break-after: avoid` behavior via show rules. For additional protection when a heading leads into a table, the preamble-into-table injection pattern (already in use) handles this.

No new Typst code needed — this maps to existing behavior. The key change is that Python no longer *decides* whether to group; it just passes the intent through.

**`"flow"`** — No special wrapping. Content flows naturally with Typst's paragraph and page-break logic.

#### Rule 2: `fill_page`

Replace the current open-table `layout()` logic with a cleaner version that any block type can use:

```typst
// New template function: fill-remaining
#let fill-remaining(body) = {
  layout(size => {
    let remaining = size.height
    block(height: remaining)[#body]
  })
}
```

For **open tables**, the existing `layout(size => ...)` already does this correctly. The change is that `fill_page: true` is the *only* trigger — no Python estimation needed.

For **writing boxes**, add a variant:

```typst
#let writing-box(
  label: none,
  height: 100pt,
  fill-page: false,  // NEW parameter
) = {
  if fill-page {
    layout(size => {
      let label-h = if label != none { 30 } else { 0 }
      let remaining = size.height / 1pt - label-h - 40  // padding
      let actual-h = calc.max(height / 1pt, remaining) * 1pt
      block(width: 100%, inset: (x: 20pt, y: 15pt), stroke: 1pt + color-noir, fill: white)[
        #if label != none {
          text(font: font-display, size: 0.65em, tracking: 2pt, fill: color-theme)[#upper(label)]
          v(0.5em)
        }
        #v(actual-h)
      ]
    })
  } else {
    // existing writing-box code unchanged
  }
}
```

#### Rule 3: `min_space`

New Typst helper that checks remaining space and inserts a page break if needed:

```typst
// Resolve min-space value to points
#let resolve-min-space(value) = {
  if value == none { return 0pt }
  if type(value) == length { return value }
  // Named fractions of usable page height (~620pt)
  if value == "quarter" { return 155pt }
  if value == "third" { return 207pt }
  if value == "half" { return 310pt }
  return 0pt
}

// Ensure minimum space before rendering content
#let ensure-space(min-space, body) = {
  layout(size => {
    let threshold = resolve-min-space(min-space)
    if size.height < threshold {
      pagebreak(weak: true)
    }
    body
  })
}
```

**Usage in generated Typst:**
```typst
// Python generates this when min_space is specified:
#ensure-space(155pt)[
  #structured-table(...)
]

// When using named values:
#ensure-space("third")[
  #open-table(...)
]
```

**For default min_space values**, the check is built into the component itself. Tables already have height-checking logic — the change is to use `layout()` instead of the Python-estimated `620` constant:

```typst
// Inside structured-table, replace the current height estimation with:
#let structured-table(
  // ... existing params ...
  min-space: 155pt,  // NEW: default quarter-page
) = {
  layout(size => {
    if size.height < min-space {
      pagebreak(weak: true)
    }
    // ... rest of existing table rendering ...
  })
}
```

#### Rule 4: `continuation`

Already implemented as `extra-rows` in `open-table`. The JSON field maps directly:

```
"continuation": {"extra_pages": 1}  →  extra-rows: <calculated from page height>
```

The Typst `open-table` already handles continuation pages. The change is that the number of extra rows is calculated *in Typst* using `layout()`, not pre-calculated in Python.

### Auto-Grouping: Move to Typst

The current Python auto-grouping logic (heading2 + preamble + table → wrapped in `block(breakable: false)`) should move to a Typst component:

```typst
// Content group: keeps heading + preamble + first content block together
// if they fit. Otherwise flows normally.
#let content-group(body) = {
  layout(size => {
    // If content fits in remaining space, keep together
    // Typst measures the actual rendered height
    let measured = measure(body)
    if measured.height <= size.height {
      block(breakable: false)[#body]
    } else {
      body
    }
  })
}
```

Python would simply emit `#content-group[...]` whenever it encounters a `"group"` type in JSON, with zero height estimation.

### Modified Template Functions Summary

| Function | Change |
|----------|--------|
| `writing-box` | Add `fill-page` parameter |
| `structured-table` | Add `min-space` parameter, use `layout()` instead of hardcoded 620 |
| `open-table` | Add `min-space` parameter, keep existing `layout()` logic |
| NEW: `ensure-space` | Generic min-space check for any block |
| NEW: `content-group` | Auto-fit grouping via `layout()` + `measure()` |

---

## 3. Python Simplification Plan

### What to Remove

1. **All height estimation logic** (lines 435-450, 529-545 in `build.py`)
   - `estimated_height = 80` and all the `+= 50`, `+= 30`, `+= 44 + ...` calculations
   - The `620` threshold constant
   - The `if estimated_height < 620:` branching

2. **Auto-grouping lookahead** (lines 399-481, 483-521)
   - The heading2 + preamble collector
   - The heading4 + hint/prose collector
   - The preamble-into-table injection
   - The `consumed` set tracking

3. **The `group` type's height-based wrapping** (lines 525-563)
   - Replace with simple pass-through to `#content-group[...]`

### What to Keep

1. **All content generators** (`gen_prose`, `gen_heading`, `gen_framework_box`, etc.) — these stay exactly as-is
2. **The GENERATORS router dict** — stays as-is
3. **Escape functions** — stay as-is
4. **Section/workbook file generation** — stays as-is
5. **Compilation step** — stays as-is

### What Changes

#### 3a. Layout Field Pass-Through

Add a small helper that reads `layout` from a JSON item and generates the appropriate Typst wrapper:

```python
def get_layout(item: dict) -> dict:
    """Extract layout fields from a JSON item, or return empty dict."""
    return item.get("layout", {})


def wrap_with_layout(typst_code: str, item: dict) -> str:
    """Wrap generated Typst code with layout directives from JSON."""
    layout = get_layout(item)

    # page_behavior
    behavior = layout.get("page_behavior")
    if behavior == "start_new_page":
        typst_code = "\n#pagebreak(weak: true)\n" + typst_code
    elif behavior == "keep_together":
        typst_code = f"\n#block(breakable: false)[{typst_code}\n]\n"
    # "keep_with_next" and "flow" need no wrapping

    # min_space
    min_space = layout.get("min_space")
    if min_space is not None:
        if isinstance(min_space, int):
            typst_code = f'\n#ensure-space({min_space}pt)[{typst_code}\n]\n'
        else:
            typst_code = f'\n#ensure-space("{min_space}")[{typst_code}\n]\n'

    # fill_page — passed as parameter to the component, not a wrapper
    # (handled in generator functions)

    return typst_code
```

#### 3b. Simplified generate_section

The main loop becomes a straight pass-through:

```python
def generate_section(data: dict, standalone: bool = False) -> str:
    parts = []
    parts.append('#import "../template.typ": *\n')
    if standalone:
        parts.append("#show: workbook-setup\n")

    # Section title page (same as before)
    section_num = data.get("section_number")
    title = data.get("title", "Untitled")
    intro = data.get("section_title_intro")
    content = data.get("content", [])

    has_title_page = any(
        i.get("type") in ("section_title_page", "title_page")
        for i in content
    )
    if not has_title_page and intro:
        parts.append(gen_section_title_page(section_num, title, intro))

    for item in content:
        item_type = item.get("type", "")

        # Group type → content-group wrapper
        if item_type == "group":
            children = item.get("content", [])
            child_parts = []
            for child in children:
                child_gen = GENERATORS.get(child.get("type", ""))
                if child_gen:
                    child_parts.append(child_gen(child))
            inner = "".join(child_parts)
            if item.get("full_page"):
                parts.append("\n#pagebreak(weak: true)\n")
            parts.append(f"\n#content-group[{inner}\n]\n")
            continue

        gen = GENERATORS.get(item_type)
        if gen:
            typst_code = gen(item)
            typst_code = wrap_with_layout(typst_code, item)
            parts.append(typst_code)
        else:
            parts.append(f'\n// WARNING: unknown type "{item_type}"\n')

    return "\n".join(parts)
```

**Key differences from current code:**
- No `consumed` set
- No lookahead
- No height estimation
- No preamble collection
- Layout wrapping is driven entirely by the JSON `layout` field
- Groups use `#content-group[...]` instead of Python-estimated `block(breakable: false)`

#### 3c. Pass fill_page to Components

Update table/writing-box generators to forward the `fill_page` flag:

```python
def gen_writing_box(item: dict) -> str:
    label = item.get("label")
    height = item.get("height", "100pt")
    fill_page = item.get("layout", {}).get("fill_page", False)
    label_arg = f'\n  label: "{escape_typst_string(label)}",' if label else ""
    fill_arg = f'\n  fill-page: true,' if fill_page else ""
    return f'''
#writing-box({label_arg}
  height: {height},{fill_arg}
)
'''

def gen_open_table(item: dict, preamble: str = "") -> str:
    # ... existing code ...
    fill_page = item.get("layout", {}).get("fill_page", True)  # default true for open tables
    fill_arg = f'\n  fill-page: {str(fill_page).lower()},'
    # ... rest of existing generation ...
```

#### 3d. What About Preamble-into-Table?

The current system injects heading+hint content *into* a table's preamble parameter so they stay visually connected. This is a **content structure** decision, not a layout decision.

**Recommendation:** Move this to the JSON level. When generating JSON (in `convert_geography.py` or AI content generation), explicitly structure heading-table relationships:

```json
{
  "type": "structured_table",
  "headers": ["Friction Type", "How It Shows Up"],
  "rows": [...],
  "preamble": [
    {"type": "heading4", "text": "Geographic Friction Types"},
    {"type": "hint", "text": "Think about which types apply..."}
  ]
}
```

This way the *content* JSON encodes the relationship, not the layout system. Python just translates preamble blocks into Typst content.

### Migration Path

1. **Phase 1:** Add `ensure-space`, `content-group`, and `fill-page` parameter to `template.typ`
2. **Phase 2:** Update `build.py` to use `wrap_with_layout()` and simplified loop
3. **Phase 3:** Regenerate Geography section, compare PDF output
4. **Phase 4:** Remove old height estimation code
5. **Phase 5:** Update `convert_geography.py` / AI prompts to emit `"preamble"` fields in JSON

---

## 4. Post-Build QA Checklist

This checklist should be run after every PDF generation. It's designed to be used by a human reviewer or an AI assistant reviewing the output.

### Page-by-Page Review

For each page in the generated PDF, check:

#### Spacing Issues
- [ ] **Orphaned heading**: A heading (h2/h3/h4) appears in the last 2 lines of a page with its content starting on the next page
- [ ] **Widowed content**: A single line of prose appears alone at the top of a page, separated from its paragraph
- [ ] **Large whitespace gap**: More than ~2 inches of blank space appears mid-page (not at bottom of a page before a page break)
- [ ] **Table starts too low**: A table begins in the bottom third of a page with only 1-2 rows visible before the break

#### Table Issues
- [ ] **Unfilled open table**: An open table has significant blank space below its last row instead of filling the page
- [ ] **Ghost row**: A table row is partially visible (clipped) at a page break
- [ ] **Missing header repeat**: A table that breaks across pages doesn't show headers on the continuation page
- [ ] **Cramped rows**: Table row content is visibly truncated or overlapping the row border

#### Box & Card Issues
- [ ] **Split box**: A framework_box, mistake_box, anchor_card, or writing_box splits across a page break (these should always be kept together)
- [ ] **Tiny writing box**: A writing box appears with less than ~1 inch of writable space

#### Content Flow Issues
- [ ] **Divider at page top**: A decorative divider (◆) appears as the first element on a page
- [ ] **Heading without content**: A section heading appears but its first content block is on the next page
- [ ] **Back-to-back page breaks**: Two consecutive page breaks creating a blank page

### Section-Level Review

For each section:
- [ ] Section title page renders on its own page
- [ ] No content appears on the section title page below the intro text
- [ ] Part One / Part Two dividers are visually distinct
- [ ] Cross-references are legible and not split

### Report Format

When reporting issues, use this format:

```
## QA Report: [Section Name]
Generated: [date]

### Issues Found

Page 3:
- SPACING: Heading "The Pressure Cooker Principle" orphaned at bottom
  → Fix: Add min_space to heading group, or restructure as group with keep_with_next

Page 7:
- TABLE: Open table "Geographic Settings" only fills 60% of page
  → Fix: Check fill_page is true, verify layout() calculation

Page 12:
- BOX: Framework box "Culture as Constraint" split across pages 12-13
  → Fix: Ensure page_behavior is keep_together (should be default)

### Summary
- Total pages: 28
- Issues found: 3
- Critical (split boxes, orphaned headings): 1
- Minor (spacing, unfilled tables): 2
```

### Automated Checks (Future)

These checks could potentially be automated by inspecting the generated Typst or PDF:

1. **Typst source scan**: Grep for `block(breakable: true)` on box types that should be `breakable: false`
2. **PDF page analysis**: Use a PDF library to check for pages with very little content (< 20% filled)
3. **JSON validation**: Verify all `layout` fields use valid values from the schema
4. **Consistency check**: Ensure all `open_table` blocks have `fill_page: true` unless explicitly overridden
