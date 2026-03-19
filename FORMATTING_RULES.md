# Formatting Rules — WIP

## Workflow

The build process has three phases:

1. **BUILD** — `build.py` runs, applying all **AUTO** rules automatically
2. **AI REVIEW** — AI reviews the PDF output, applies **REVIEW** rules (makes decisions about dead space, table layout, etc.), edits JSON, rebuilds
3. **USER REVIEW** — user reviews the final PDF

Rule classifications:
- **AUTO** — baked into the pipeline (template.typ / build.py). Applied every build.
- **REVIEW** — AI makes the call during post-build review. Involves editing JSON data files based on context and judgement.

---

## Active Rules

| # | Rule | Fix Type | Status |
|---|------|----------|--------|
| F1 | **Paragraph spacing**: visible line break between paragraphs. Before and after bullet lists, clear separation from surrounding prose. | AUTO | DONE |
| F2 | **Structured table review**: For user-fill tables, decide per table: remove unnecessary columns, add blank rows for user ideas, adjust row heights. Give writing space to the columns that need it. | REVIEW | TODO |
| F3 | **Data table fragmentation**: Long reference tables split across 2-3 pages look messy. Decide: merge sub-tables, start on new page, accept flow, or convert format. | REVIEW | TODO |
| F4 | **Dead space fillers**: When >30% of a page is blank at the bottom, fill it with contextually relevant content from the filler menu. | REVIEW | TODO |

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
**AI Review Action**: For each structured/open table in the JSON, decide:
1. Are all columns necessary? Remove or merge redundant ones.
2. Should blank rows be added for user entries?
3. Are rows tall enough for handwriting?
**Where**: `typst/data/*.json` — edit table definitions per section.

### F3: Data Table Fragmentation
**Problem**: Long read-only reference tables split across multiple pages look fragmented.
**Example**: Geography section "Common Geographic Patterns" has 3 sub-tables spanning ~3.5 pages.
**AI Review Action**: For each data table, decide:
1. **Merge sub-tables** — combine related tables. Fewer headers = less noise.
2. **Start on new page** — cleaner but more paper.
3. **Accept the flow** — tables break naturally with repeated headers.
4. **Convert format** — some tables work better as bullet lists or framework boxes.
**Where**: `typst/data/*.json` — per-section decisions about table structure.

### F4: Dead Space Fillers
**Problem**: Pages with content ending early leave large blank areas (>30% of page). Looks unfinished and wastes space.
**Example**: Page 20 — Mistake #3 box + divider ends mid-page with ~50% blank.
**AI Review Action**: When a page has >30% dead space at the bottom, insert a filler element from this menu:

| Filler Type | Size | Use When |
|---|---|---|
| **Quick Tip** | ~80-150pt | Small gap. A one-liner practical tip relevant to the section. Styled box. |
| **Inspirational Quote** | ~80-150pt | Small-medium gap. A craft quote from a published author. Centered, italic. |
| **Reflection Prompt** | ~150-250pt | Medium gap. A thought-provoking question + 3-4 writing lines. |
| **Watch Out** | ~150-250pt | Medium gap. A common pitfall warning related to the current topic. |
| **Try This** | ~250pt+ | Large gap. A mini creative exercise with a writing box. |

**Selection criteria**:
- Match the filler to the section topic (e.g. geography tips for geography section)
- Don't repeat the same filler type on consecutive pages
- Prefer interactive fillers (reflection prompt, try this) over passive ones (quote, tip)
- The filler content must add genuine value, not just fill space

**Where**: `typst/data/*.json` — add filler blocks at appropriate positions.
