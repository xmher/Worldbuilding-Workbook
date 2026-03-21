# Workbook PDF QA Framework

## The Workflow — READ THIS FIRST

The workbook creation pipeline has **three stages**. All three must happen every time. Do not skip Stage 3.

### Stage 1: AI Writes the JSON
The AI generates the structured JSON content for the workbook — all sections, text, exercises, tables, callout boxes, etc. During this stage, the AI should apply any **content-level rules** from this document (e.g., Issue 15 — don't write essay-length callout boxes; Issue 19 — include enough reference table rows to fill a page).

### Stage 2: Python Script Builds the PDF
The Python script takes the JSON, generates Typst, and outputs the PDF. All **RULE-type fixes** from this document should be encoded into the Python script and/or Typst templates so they are applied automatically every time. This includes spacing, margins, footer boundaries, table placement logic, column width proportions, page break rules. The goal is to automate as much as possible so the PDF comes out clean by default.

### Stage 3: AI Manually Reviews the PDF (QA Pass) — DO NOT SKIP
**After the PDF is generated, the AI must open and review the output.** The programmatic rules will catch most issues, but some problems require judgment that only a manual review can provide. During this pass, the AI should:

1. **Check every page** for visual issues the rules couldn't catch — awkward gaps, elements that technically fit but look bad, tables that could benefit from width adjustments, etc.
2. **Apply all MANUAL REVIEW fixes** from this document — expanding reference tables, judging answer box importance/sizing, filling white space with appropriate filler content, flagging oversized callout boxes, etc.
3. **Verify the RULE fixes actually worked** — confirm that no elements overlap the footer, tables aren't splitting when they shouldn't, spacing looks consistent, etc. Rules can have edge cases the script misses.
4. **Make corrections** by updating the JSON or Typst and regenerating, then review again until the output is clean.

**This is not optional.** The programmatic rules handle the predictable stuff. The manual QA pass catches everything else. Every PDF output must go through Stage 3 before being considered final.

---

## How to Use This Document

Each issue below is tagged with its fix type so you know where it belongs in the workflow:

- **`RULE`** → Encode into the Python script / JSON / Typst templates (Stage 2). These are applied automatically every build.
- **`MANUAL REVIEW`** → The AI checks for these during the QA pass (Stage 3). These require judgment and cannot be fully automated.
- **`BOTH`** → Has an automated component (Stage 2) AND requires a manual check (Stage 3) to verify or refine.

Each issue also has:
- **Description**: What the problem looks like
- **Fix Instructions**: Exactly what to do
- **Priority**: `HIGH` (affects readability or page count significantly), `MEDIUM` (noticeable quality issue), `LOW` (polish)

---

## SPACING & BREATHING ROOM

### Issue 1: Insufficient Spacing Between Paragraphs
- **Fix Type:** RULE
- **Priority:** HIGH
- **Description:** Paragraphs run directly into each other with no visible gap. Pages look cluttered and dense.
- **Fix:** Add consistent paragraph spacing (e.g., `0.6em–0.8em` below each paragraph). This applies globally to all body text paragraphs.

### Issue 2: No Spacing Before/After Lists
- **Fix Type:** RULE
- **Priority:** HIGH
- **Description:** Numbered and bulleted lists have no line break between the intro text and the first item, or between the last item and the following text. Everything runs together.
- **Fix:** Add spacing above and below list blocks (before first item, after last item). The intro sentence and list should feel like connected but visually separate elements.

### Issue 3: All Elements Need Breathing Room
- **Fix Type:** RULE
- **Priority:** HIGH
- **Description:** Not just paragraphs — every element type (callout boxes, tables, answer boxes, headers, questions) butts directly against the next element with no gap.
- **Fix:** Define a minimum vertical gap between ALL element types. Every block-level element should have consistent margin-top and margin-bottom so nothing ever touches the next thing directly.

### Issue 20: Header Spacing — More Above, Less Below
- **Fix Type:** RULE
- **Priority:** HIGH
- **Description:** Section headers (like "The Sensory World") appear too close to the text above them, making them look attached to the previous section. The gold divider line below the header floats too far from the header text.
- **Fix:** Headers should have a large top margin (to clearly separate from previous content) and a small bottom margin. The header + divider line are one visual unit — the divider should sit tight under the header. This applies to all header levels (H1, H2, subsection headers).

---

## TABLES — LAYOUT & SIZING

### Issue 4: Column Widths Should Be Proportional, Not Equal
- **Fix Type:** BOTH
- **Priority:** HIGH
- **Description:** All table columns are set to equal width. Columns with short labels waste horizontal space, while columns with longer text get squeezed and wrap to many lines, making rows taller than necessary.
- **Fix (Rule):** Default behavior should allocate more width to columns with longer content and less to label/short-answer columns. Never default to equal-width.
- **Fix (Manual Review):** AI should check whether adjusting column widths could reduce row heights enough to prevent a table from splitting across pages. The goal is to minimize overall table height.

### Issue 8: Tables Should Never Split If They Fit on One Page
- **Fix Type:** RULE
- **Priority:** HIGH
- **Description:** Tables that could fit on a single page are being split across two pages, creating ugly breaks.
- **Fix:** Before placing a table, check if it fits in the remaining page space. If not, push the entire table to the next page. Fill the white space left behind using the logic in Issue 6. Only split a table as a last resort when it's physically too tall for a full page.

### Issue 9: When Tables Must Split, Split Cleanly
- **Fix Type:** RULE
- **Priority:** MEDIUM
- **Description:** When a table is too large for one page and must split, the split happens at bad points (1 orphan row on the next page, uneven distribution).
- **Fix:** If a table must split: (a) repeat the header row on the continuation page, (b) split roughly evenly — never leave fewer than 3 rows on either side, (c) prefer splitting at logical grouping points if applicable. This should be a last resort — most tables should fit on one page.

### Issue 19: Reference Tables Should Be Expanded to Fill Pages
- **Fix Type:** MANUAL REVIEW
- **Priority:** MEDIUM
- **Description:** Reference/lookup tables (like name pattern tables) often don't fill their page, leaving dead white space. Unlike exercise tables, these can easily have more rows added.
- **Fix:** AI should detect reference tables (pre-filled examples, not user-fillable) and check if the page has unused space. If yes, generate additional relevant, accurate rows to fill the page. Each reference table should start on its own page to maximize available space. Ensure new entries are genuinely useful, not filler.

---

## FILLABLE ELEMENTS — ANSWER BOXES & EXERCISE TABLES

### Issue 5: Question + Explainer Must Stay With Their Fillable Element
- **Fix Type:** RULE
- **Priority:** HIGH
- **Description:** Questions and their helper/explainer text get separated from the table or answer box that the user fills in, split across pages.
- **Fix:** Treat question text + explainer text + the fillable element (answer box or table) as one atomic unit. They must always appear on the same page. If the unit doesn't fit on the current page, push the entire unit to the next page.

### Issue 6: Fill White Space by Expanding Fillable Elements
- **Fix Type:** BOTH
- **Priority:** HIGH
- **Description:** When elements get pushed to new pages (due to Issue 5, 8, 11, etc.), awkward white space gaps are left behind.
- **Fix (Rule):** After layout, check for significant white space gaps. If fillable elements (answer boxes, table rows) exist above the gap, expand them vertically to fill the remaining space. Distribute extra height equally across rows/boxes.
- **Fix (Manual Review):** AI should verify that expanded elements still look proportional and intentional, not awkwardly stretched.

### Issue 7: Maximum Three Answer Boxes Per Page
- **Fix Type:** BOTH
- **Priority:** MEDIUM
- **Description:** Pages with too many answer boxes feel overwhelming and give users too little writing space per question.
- **Fix (Rule):** Enforce a maximum of 3 answer boxes per page.
- **Fix (Manual Review):** When a page has only answer boxes, AI should judge whether all questions are equally important (make boxes equal height) or whether some deserve less space (make those shorter, give more room to important ones). This requires understanding the content.

---

## PAGE FLOW & BREAKS

### Issue 11: Don't Cram a New Subsection Below a Table If It Won't Fit
- **Fix Type:** RULE
- **Priority:** HIGH
- **Description:** After a table ends, the pipeline starts a new subsection (heading + content) in the remaining page space even when there isn't room for it to fit completely, causing the subsection to split immediately.
- **Fix:** After placing a table or major element, check remaining page space. If the next element (subsection heading + its first content block) cannot fit completely, don't start it. Instead, expand the table/elements above to fill the page (Issue 6) and start the new subsection on the next page.

### Issue 16: Elements Must Never Overlap the Footer
- **Fix Type:** RULE
- **Priority:** HIGH
- **Description:** Elements (answer boxes, callout boxes, tables) overflow past the page's safe area and overlap with the footer text and page number.
- **Fix:** Define a hard boundary above the footer. No element may start or extend past this boundary. If an element doesn't fit above the footer, push it to the next page entirely. This is a non-negotiable constraint that overrides all other layout decisions.

---

## CALLOUT BOXES (REMEMBER, COMMON MISTAKES, ETC.)

### Issue 13: Callout Boxes Need Internal Spacing
- **Fix Type:** RULE
- **Priority:** HIGH
- **Description:** Text inside callout boxes (especially Common Mistakes) is a wall of text with no paragraph breaks. The "FIX" label runs into the description above it.
- **Fix:** Add internal paragraph spacing within callout boxes. The "FIX" section should have clear visual separation from the mistake description (extra space above the FIX label, or a subtle internal divider).

### Issue 14: Callout Box Overflow at Page Bottoms
- **Fix Type:** RULE
- **Priority:** HIGH
- **Description:** Long callout boxes don't respect page boundaries — text runs over the footer and off the page instead of breaking or moving to the next page.
- **Fix:** Callout boxes must respect the same page boundary rules as all other elements (Issue 16). If a callout box doesn't fit, either push it entirely to the next page, or split it cleanly with a visual continuation indicator. Never let it overflow.

### Issue 15: Very Long Callout Boxes Should Be Reviewed
- **Fix Type:** MANUAL REVIEW
- **Priority:** MEDIUM
- **Description:** Some Common Mistakes boxes contain essay-length content that fills an entire page or more within a single box.
- **Fix:** AI should flag any callout box that exceeds approximately half a page in length. Review whether the content could be broken into shorter paragraphs with internal subheadings, split into multiple separate callout boxes, or restructured so it's not all inside one giant container. This is a content/design judgment call.

---

## WHITE SPACE & FILLER CONTENT

### Issue 12: Large White Space Gaps Should Be Filled
- **Fix Type:** MANUAL REVIEW
- **Priority:** MEDIUM
- **Description:** After applying all layout rules, some pages may still have significant white space that isn't absorbed by expanding existing elements.
- **Fix:** AI should assess whether the gap is small enough to be acceptable (a little breathing room is fine) or large enough to need filling. If filling is needed, select from these contextually appropriate filler types:

  **Filler Toolkit:**
  | Filler Type | Use For |
  |---|---|
  | **Tip** | Practical, actionable advice related to the section |
  | **Common Mistake** | A warning about what writers get wrong |
  | **Watch Out** | A subtle pitfall specific to the topic |
  | **Remember** | Reinforcing a key concept from the section |
  | **Try This** | A quick mini-prompt or thought exercise (not a full answer box) |
  | **In Practice** | A short real-book example showing the concept in action |
  | **Quick Check** | A yes/no or one-line reflection question |
  | **Pro Tip** | A more advanced or nuanced insight |
  | **What If...** | A speculative prompt to push the reader's thinking |
  | **Reader Experience** | How this element feels from the reader's perspective |
  | **Red Flag** | A warning sign that something's going wrong in their story |
  | **Romantasy Spotlight** | A brief genre-specific insight or trope connection |

  The AI must pick the right filler type based on the surrounding section's topic and content. Generic or irrelevant fillers are worse than white space.

---

## MARGINS & PAGE EFFICIENCY

### Issue 17: Left and Right Margins Are Too Wide
- **Fix Type:** RULE
- **Priority:** HIGH
- **Description:** Side margins appear oversized for a digital-only PDF. No print binding requires generous inner margins.
- **Fix:** Reduce left and right margins to reclaim horizontal space. For a digital workbook, 1.5–2cm side margins is usually sufficient (vs. the current ~2.5–3cm+). More horizontal space means less text wrapping, shorter table rows, and fewer pages overall. Test to ensure it doesn't feel cramped.

### Issue 18: Top and Bottom Margins Are Too Wide
- **Fix Type:** RULE
- **Priority:** HIGH
- **Description:** Vertical margins/padding above and below the content area waste space on every page. Large gaps between the page edge and where content starts/ends.
- **Fix:** Reduce top and bottom margins while keeping the footer readable. Even saving 1cm top and bottom reclaims significant vertical space per page, compounding across 1,600+ pages. The footer still needs breathing room, but the current spacing is designed for print, not digital.

---

## PRIORITY SUMMARY

### Do First (HIGH — biggest impact on quality and page count)
1. Issue 17 & 18: Reduce margins (massive page count reduction)
2. Issue 16: Hard footer boundary (prevents overflow/overlap)
3. Issue 1, 2, 3, 20: Global spacing rules (fixes cluttered feel)
4. Issue 4: Proportional column widths (reduces table height)
5. Issue 8: Keep tables on one page (prevents ugly splits)
6. Issue 5: Keep question + fillable together (prevents orphaning)
7. Issue 6: Expand fillable elements to absorb white space
8. Issue 11: Don't start subsections that won't fit
9. Issue 13: Internal callout box spacing
10. Issue 14: Callout box overflow fix

### Do Second (MEDIUM — quality polish)
11. Issue 9: Clean table splits when unavoidable
12. Issue 7: Max 3 answer boxes per page + height judgment
13. Issue 15: Flag oversized callout boxes
14. Issue 19: Expand reference tables with more rows
15. Issue 12: Fill remaining white space with contextual content
