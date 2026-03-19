# Formatting Rules — WIP

Rules discovered during PDF review. Each is classified as:
- **AUTO** — can be fixed in the pipeline (template.typ / build.py)
- **MANUAL** — requires hand-editing JSON or one-off fixes

---

## Active Rules

| # | Rule | Fix Type | Status |
|---|------|----------|--------|
| F1 | **Paragraph spacing**: visible line break between paragraphs. Before and after bullet lists there should be a clear line break separating them from surrounding prose. | AUTO | DONE |

---

## Rule Details

### F1: Paragraph & List Spacing
**Problem**: Paragraphs run together with no visual gap. Bullet lists butt directly against the preceding/following prose text.
**Fix**: Increase `par(spacing)` for paragraph gaps; increase `above`/`below` on bullet_list component.
**Where**: `template.typ` — `set par(spacing: ...)` and `gen_bullet_list` block spacing.
