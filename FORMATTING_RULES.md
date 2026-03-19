# Formatting Rules — WIP

Rules discovered during PDF review. Each is classified as:
- **AUTO** — can be fixed in the pipeline (template.typ / build.py)
- **MANUAL** — requires hand-editing JSON or one-off decisions per table
- **DECISION** — needs human judgement case-by-case; cannot be fully automated

---

## Active Rules

| # | Rule | Fix Type | Status |
|---|------|----------|--------|
| F1 | **Paragraph spacing**: visible line break between paragraphs. Before and after bullet lists there should be a clear line break separating them from surrounding prose. | AUTO | DONE |
| F2 | **Structured table review**: For user-fill tables, decide per table: (a) remove unnecessary columns (e.g. "Does it apply?" yes/no columns waste space), (b) add blank rows for user ideas, (c) make rows taller for more writing room. Give writing space to the columns that need it. | DECISION | TODO |
| F3 | **Data table fragmentation**: Long reference tables (read-only) split across 2-3 pages look messy. Consider: consolidating sub-tables, keeping short tables on one page, or accepting clean page breaks with repeated headers. | DECISION | TODO |

---

## Rule Details

### F1: Paragraph & List Spacing
**Problem**: Paragraphs run together with no visual gap. Bullet lists butt directly against the preceding/following prose text.
**Fix**: Increase `par(spacing)` for paragraph gaps; increase `above`/`below` on bullet_list component.
**Where**: `template.typ` — `set par(spacing: ...)` and list show rule.
**Status**: DONE

### F2: Structured Table Column/Row Review
**Problem**: Some structured tables have columns that waste space (e.g. "Does it apply?" is a yes/no that doesn't need a full column). The writing columns end up cramped. Some tables need blank rows added so users can write in their own ideas.
**Example**: Trapping Type table (p14) — "Does it apply?" column could be removed, giving all that space to "How it works in your world". Could also add 1-2 blank rows for custom trapping types.
**Fix**: Review each structured table in the JSON files and decide:
1. Are all columns necessary? Remove or merge redundant ones.
2. Should blank rows be added for user entries?
3. Are rows tall enough for handwriting?
**Where**: `typst/data/*.json` — edit table definitions per section.
**Status**: TODO — requires going through each section's tables with the user.

### F3: Data Table Fragmentation
**Problem**: Long read-only reference tables (e.g. "Settings That Force Proximity" — 8 rows, "Geographic Barriers" — 8 rows, "Environmental Conditions" — 7 rows) split across multiple pages, looking fragmented even though headers repeat correctly.
**Example**: Geography section "Common Geographic Patterns" has 3 sub-tables spanning ~3.5 pages.
**Options**:
1. **Merge sub-tables** — combine "Settings That Force Proximity" + continuation into one table. Fewer headers = less visual noise.
2. **Start each sub-table on a new page** — cleaner but uses more paper.
3. **Accept the flow** — tables break naturally with repeated headers (current behavior). Just ensure H3 subheading always stays with at least 2 rows of its table.
4. **Convert to a different format** — some reference tables might work better as bullet lists or framework boxes if they're short.
**Where**: `typst/data/*.json` — per-section decisions about table structure.
**Status**: TODO — needs user decision on preferred approach per section.
