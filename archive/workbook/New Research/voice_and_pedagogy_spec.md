# Voice and Pedagogy Specification
## Romantasy Worldbuilding Workbook — Reference Guide for Claude Code

This spec is built from a full read of School of Plot's *Fantasy Worldbuilding Workbook*. It is meant to be loaded on every page-generation task so the voice stays consistent across hundreds of prompts. Where the spec recommends divergence from School of Plot, those sections are labelled **DIVERGE**.

---

## 1. Tone and Voice

### How School of Plot addresses the reader

The voice is the **encouraging pragmatic friend**. Not a coach (too motivational), not a teacher (too hierarchical), not a cheerleader (too emotional). It sits closer to a slightly-more-experienced writer friend giving you practical advice over coffee. Key markers:

- Second person throughout. "You" is constant. "I" barely appears (only in the Dear Writer letter and a few asides).
- Direct address without preamble. Sentences like *"You don't need a map"* or *"Think of a reason why all magic users aren't unstoppable gods"* start with the instruction, not with a warm-up.
- Occasional first-person plural ("Now that we've seen some examples...") to signal shared journey.
- Neutral register. Not formal, not slangy. No "hey writer!" energy. No professor energy either.

### How the "Dear Writer" opening lands

It's short — under 100 words. Four key moves:

1. **Congratulations you're doing the thing.** ("Congratulations on deciding to write a story!")
2. **Your words matter regardless of where you are.** ("Whether it's your first story or your 100th, and whether you started years ago or this morning, your words are valuable.")
3. **Doing is better than dreaming.** ("By committing to this project, you've already done better than anyone who's just dreaming about it.")
4. **Transparent small-business thank you.** ("I want to thank you from the bottom of my heart for supporting this small business (actually, a super small business...it's just 1 person!)")

It lands because it's not performatively wholesome. It's brief, specific, and ends on a quiet human note rather than a writing-career promise. It treats the reader as a peer, not an aspirant.

### Permission-giving language

This is the single most distinctive voice feature. It appears on roughly every third or fourth page and takes these forms:

- *"You can fill it in for fun, or skip it completely and delete the pages."*
- *"Feel free to delete these pages if you don't want to go into this level of detail - you really don't need to unless it's fun for you!"*
- *"Having said that, your setting name doesn't need to mean something if it's taking up too much of your energy."*
- *"You don't need a map."*
- *"It's not necessary."*
- *"Don't feel pressure to label your system if you don't want to."*
- *"You can choose to go into as much or as little detail as you like."*

Notice the pattern: **direct negation of obligation**, followed by a permission clause or a gentle reason. The voice is not apologetic about this — it's just stating the fact that some things are optional.

### Where the humour lives

Humour is **sparse and dry**. It does not try to be funny. When it works, it's because of:

- Parenthetical asides that undercut the seriousness. *"(actually, a super small business...it's just 1 person!)"*
- Dry practical observations. *"Don't get too tied up in realism, because nobody's going to check this stuff."*
- Gentle reality checks on writer anxiety. *"Creative people don't tend to like being restricted, so this idea is often unpopular with new writers."*

There are **no jokes**. No quips. No witty one-liners. The humour is situational and empathetic — laughing *with* the writer at the absurdity of overplanning, never *at* them.

### How they cite examples

Citations are frictionless and load-bearing. Patterns:

- **Pratchett** is quoted directly as an authority opener ("Here's some golden advice from Sir Terry Pratchett, a master of fantasy worldbuilding:") — this is the one extended quote in the whole workbook.
- **Avatar: The Last Airbender** is used as the go-to example for hard magic ("Avatar the Last Airbender is often given as an example of an understandable hard magic system (e.g. you know that a waterbender can't control fire).")
- **BBC's Merlin** is used for the "magic is illegal" example.
- **Harry Potter** is used for the "magic requires a tool" example ("E.g., Harry Potter's wizards are often useless without wands.")
- **Brandon Sanderson** is name-dropped as a literary comp for hard magic.

Pattern rules:
- Examples appear **only when they make a teaching point concrete**. They are never decorative.
- One example per concept. No lists of five comps.
- The reference is always followed by a one-line explanation of *what it illustrates* — assumes the reader may not know the work.
- **Romeo & Juliet** is referenced in lowercase as a concept ("this world's Romeo & Juliet"), suggesting the workbook is comfortable using cultural shorthand for famous-enough examples.

### Tone adjustments for a romantasy audience — **DIVERGE**

Romantasy readers (and writers) arrive with a different baseline than generic fantasy readers:

- **They are often more experienced readers than writers.** They've read 40+ romantasy books. They know the tropes by name. Do not over-explain what a fated mate is.
- **They expect the voice to know what they're here for.** Pretending not to know what "shadow daddy" means reads as condescending. Use the vocabulary.
- **They are more emotionally invested in the fantasy.** A line like "don't get too tied up in realism, because nobody's going to check this stuff" needs to become "the spice scene doesn't need a physics paper — trust the fantasy." The *posture* is the same (permission to not over-think). The reference points change.
- **They are comfortable with adult content.** The voice can name sex, bonds, consent, dark themes without coyness. But it should not be *gratuitously* explicit — the workbook is a workbook, not erotica.
- **Warmth should tick up slightly.** School of Plot is pragmatic-friend. The romantasy version is pragmatic-friend who also knows your weird taste and doesn't judge you for it. A degree warmer, no more.

---

## 2. Prompt Style

### Typical prompt length and structure

Prompts are **short, grammatically simple, and cluster 2–4 per page**. Examples from the source:

- "Are there any important historical rulers whom people often mention? In which context are they mentioned?"
- "What does courting involve?"
- "How is alcohol regarded? Who can and can't drink?"
- "Who raises the child? The whole village? A nanny? The parents?"
- "At what age are children considered adults? What does that mean? Marriage? War?"

Patterns:
- **10–20 words per prompt on average.**
- Often a **main question + a clarifying follow-up or example** in parentheses or as a second sentence.
- Compound prompts (two linked questions) are common and welcome.
- Examples in parentheses are used as **scaffolding** — "(e.g. their mums, a holy book...)" — to unlock the reader without dictating the answer.

### Explanation before prompts

Very little. A typical "explanation page" is 2–5 short paragraphs of craft content, followed (often on a separate page) by 3–4 prompts that activate that content. The ratio is roughly:

- **1 page of explanation** → **1–3 pages of prompts**.

Explanation pages are mostly standalone and sit before the prompt pages rather than being mixed in with them.

### Do prompts stand alone or cluster?

**Cluster.** Each page holds a themed set of 2–4 prompts under one header (e.g. MARRIAGE, CHILDREN, FOOD, CLASS). Pages are modular — a writer can tear one out, skip one, or fill one at a time. Prompts within a page are related but not sequential (you don't need to answer #1 to answer #2).

### Grammatical phrasing

**Mostly interrogative.** "What does...", "How does...", "Are there...", "Who raises...", "Is it common...". Imperatives appear in the explanation pages ("Think of a reason why...", "Note down any notable pieces...") but the fillable prompts themselves are overwhelmingly questions.

Mixed phrasing within a cluster is fine and actually good — it keeps the rhythm varied.

### Implied fillable space

From the source, implied space per prompt is roughly:

- **Short prompts (one-line answers):** 2–3 blank lines. These are the "Who raises the child?" type.
- **Medium prompts (paragraph answers):** 4–6 blank lines. "Describe your civilisation's culture and its values."
- **Tables:** 4–8 rows with 3–4 columns for things like gods, place names, currency.
- **Overview sheets (country overview):** 12–15 fields at 1 line each, packed into a single page.

Plan the layout before writing prompts — the amount of space says almost as much as the prompt itself.

---

## 3. Explanatory Content

### How much craft theory before prompts?

Just enough. School of Plot delivers theory in **bite-size, single-concept pages**. No page teaches more than one idea. A magic system explainer looks like:

- Page 1: Why magic needs rules (the concept).
- Page 2: Soft vs hard magic (the distinction).
- Page 3: Soft vs hard comparison table (the reference).
- Page 4: Types of magic systems, part 1 (the options).
- Page 5: Types of magic systems, part 2 (more options).
- Pages 6–8: Prompts.

Theory is **instrumental, not academic**. No history of the form. No "the debate over magic systems dates back to Tolkien". Just: here's the concept, here's why it matters, here are your choices, now answer some questions.

### Cheat sheets and reference tables

Used heavily. Patterns:

- **Naming tables** (prefixes/suffixes for place names).
- **Comparison tables** (hard vs soft magic).
- **Lists as tables** (natural resources and their cultural implications).
- **Fillable tables** (gods, spells, countries).

Tables serve two purposes: (1) they give the reader raw material to steal from, and (2) they break up the prose-heavy pages and give the workbook a practical-toolkit feel. A good workbook has a table every 4–6 pages.

### Name-dropping real examples

Already covered in §1 above. Rules in summary:

- Pratchett, Sanderson, Avatar, Merlin, Harry Potter.
- **Always load-bearing.** The example illustrates a concept.
- **Always a mini-explanation attached** — assume the reader may not know the comp.
- **Never a list of three comps**. One example per concept.

### Where they give permission to skip

Permission to skip is most dense around **effort-intensive optional content**:

- Fictional currency design ("Feel free to delete these pages if you don't want to go into this level of detail")
- Map-making ("You don't need a map")
- Language invention ("It's not necessary")
- Place-name etymology ("your setting name doesn't need to mean something if it's taking up too much of your energy")

**Pattern:** Permission to skip arrives at the *opening* of an ambitious section, not at the end. The writer is told they can skip before they've invested any effort in reading the page.

---

## 4. Structural Patterns

### Section organisation

The workbook is organised by **worldbuilding domain**, not by writing stage. Each major part is a domain:

1. Cities & Lands
2. History & Politics
3. Magic System
4. Culture
5. Religion
6. (plus Fashion, Language, Timekeeping threaded in)

Within each part, the structure is almost always:

1. **Part opener** — single page with the domain name, no content.
2. **Concept page(s)** — "Why write a world history?", "How to write magic", etc.
3. **Options/cheat-sheet pages** — "Types of magic", "Types of government".
4. **Fillable prompt pages** — clusters of questions.
5. **Reference tables to fill in** — "Keep track of your deities", "Magic spells or powers".

### Page modularity

**Extremely modular.** Every page is structured to work if the reader skipped the previous page. There are almost no "as we discussed above" references. Each page header re-anchors the topic.

**Rule for Claude Code:** Every page should work if the writer opened it at random. Header, brief context, content. Don't rely on what came before.

### Transitions between topics

There are almost no prose transitions. The structure transitions for you:

- Part opener full-page break.
- Section header page with the topic name.
- Next page just starts on the new content.

The only bridging sentences are things like "Now that we've seen some examples, on the next page you can make your own prefixes and suffixes..." These are rare and purely functional (telling the reader what happens next), not voicey.

### Part openers, section openers, page headers

- **Part openers:** Single page, all caps, centred. "CITIES & LANDS", "HISTORY & POLITICS", "MAGIC SYSTEM", "CULTURE", "RELIGION". No subtitle. No prose. Just the domain name.
- **Section openers:** Page header with a concept — "HOW TO WRITE MAGIC", "SOFT VS. HARD MAGIC", "WHAT IS CULTURE?". Usually a how-to or what-is.
- **Page headers:** Topic name — "MAGIC", "FASHION", "FOOD", "CLASS". When a prompt page sits under a section, the header repeats the domain name.

Footer pattern: every page carries "@SCHOOLOFPLOT" and "SCHOOLOFPLOT.COM". Your equivalent will be your brand footer on every page.

---

## 5. Permission Language

### Catalogue of "you don't need to" patterns

Direct from the source:

1. *"You don't need a map."*
2. *"You don't need to know every single thing about your world before you begin."* (paraphrased from "Some authors like to know every single thing... Some don't, and that's fine!")
3. *"It's not necessary."* (on invented languages)
4. *"This doesn't mean you need to plan every single detail."*
5. *"Your setting name doesn't need to mean something if it's taking up too much of your energy."*
6. *"You really don't need to unless it's fun for you!"*
7. *"Don't feel pressure to label your system if you don't want to."*
8. *"You can choose to go into as much or as little detail as you like."*
9. *"This doesn't mean you have to spend 7 paragraphs explaining origins of grain tax."*
10. *"Feel free to delete these pages if you don't want to go into this level of detail."*
11. *"Feel free to leave any fields blank."*
12. *"You can fill this in at the end if you like."*

**The underlying pattern has three forms:**

- **Pure negation:** "You don't need X."
- **Conditional permission:** "You can do X if [it's fun / you want to / it suits your story]."
- **Anti-guilt closure:** "[Pressure-releasing phrase] if it's taking up too much of your energy."

All three forms share a posture: **the reader's time and energy are the scarce resource, not the completeness of the workbook.**

### How they prevent reader overwhelm

Four main techniques:

1. **Permission to skip** (above).
2. **Scoping the effort upfront.** "This is just for quick reference." "This is a ballpark estimate." "This is optional."
3. **Pre-empting perfectionism.** "Nobody's going to check this stuff."
4. **Framing optional content as play, not work.** "You can fill it in for fun." "You really don't need to unless it's fun for you!"

### How they respect the writer's time

- Short pages. Almost no page has more than ~150 words of prose.
- No filler. Explanation pages make their teaching point and end.
- No recaps. The workbook never repeats itself.
- No "before we continue, let's remember...". The reader's memory is trusted.

---

## 6. Romantasy-Specific Voice Adjustments

### How explicit can you be about sex, bonds, consent, dark content?

**More explicit than School of Plot, but still functionally clinical when teaching.** The voice should:

- **Name things directly.** "The sex scene." "The mating bond." "The dubcon moment." Not "the intimate moment" or "the romantic culmination." Coyness reads as embarrassed and breaks trust with the reader.
- **Stay craft-focused in prose explanations.** When explaining a concept, treat sex and bonds as craft problems the way School of Plot treats magic systems. *"A mating bond that activates on first sight removes most of the tension. Consider what your bond requires besides proximity."* That's the register.
- **Allow visceral language in prompt framings and romance-leverage call-outs.** Prompts can say "When he touches her for the first time, what does the bond do to her body?" That's the romantasy reader's expectation.
- **Handle dark content with the same permission-giving posture.** "If your book has dubcon, make sure you know where the line of your personal comfort is and where your reader's comfort likely sits. You don't owe anyone a content warning inside the worldbuilding — but you owe yourself clarity on what you're writing."

**What to avoid:** Purple, breathless, or euphemistic language. The voice is still pragmatic. It just knows what it's talking about.

### Romantasy craft terminology

**Use it without flinching, but define it once.** The workbook is the reader's trusted friend — the one who already knows the vocabulary. Definitions can appear:

- The first time a term is used in the workbook, in a short parenthetical. *"A fated mate bond (the trope where two characters are supernaturally destined for each other) comes with a built-in problem..."*
- In a one-page glossary at the back for quick reference.

Terms to use without embarrassment: fated mates, mating bond, bond sickness, shadow daddy, morally grey, dubcon, non-con, spice level, fade to black, open door, slow burn, instalove, touch her and die, only one bed, enemies to lovers, dark romance, why choose.

**Omegaverse is a special case.** Include it (fae and paranormal workbooks may need it), but flag upfront — this is a subgenre with its own conventions, and the workbook should signal awareness without pretending it's mainstream.

### Warmly coachy (Abbie Emmons) vs pragmatic (School of Plot)?

**Mostly School of Plot, one degree warmer.** Your differentiation isn't in becoming Abbie Emmons — that voice is crowded and doesn't match the romantasy Etsy buyer, who is often a more experienced reader than writer. You want:

- School of Plot's **economy** (no wasted words).
- School of Plot's **permission-giving posture** (you can skip this).
- School of Plot's **instrumental examples** (comps that earn their place).
- **Plus** a touch more warmth at section openers. Where School of Plot says "Here are some things you can choose to include in your map," you might say "Here's what tends to earn its place on a romantasy map — fountains and gardens read differently than crypts and thorn hedges."
- **Plus** explicit romance-leverage callouts (see §8).

### BookTok-awareness

**Referenced but above the fray.** The workbook should *know* BookTok exists (tropes named on TikTok can be named here), but should not chase it. Don't reference specific creators. Don't use the word "viral." Don't mention bookish aesthetics by name.

What BookTok-awareness *does* give you:
- A shared vocabulary with the reader (tropes, archetypes).
- Permission to list tropes as legitimate craft elements.
- An understanding that the reader has likely seen *many* comps and doesn't need your help discovering them.

What BookTok-awareness should *not* do:
- Make the voice feel trendy. Trends age. This workbook should read the same in three years.

---

## 7. Differentiation Strategy

### Where your voice should diverge

School of Plot's voice is **generic-fantasy pragmatic**. Your voice is **romantasy pragmatic with romance-first eyes**. The three most important divergence points:

1. **Everything ties to the romance.** School of Plot asks "What is the currency?" You ask "What is the currency, and when does your heroine realise she can't afford something that would save him?" The worldbuilding question is still there, but the romance hook is baked in.

2. **Beginner scaffolding is higher.** School of Plot assumes a reader who can take a prompt and run. You assume a reader who wants one more worked example, one more "here's how to think about this," one more "if you're stuck, try..." before they hit the blank page.

3. **The romance is the engine, not the garnish.** School of Plot treats romance as one element of worldbuilding (see the "Romeo & Juliet" question, which is one prompt among many about history). You treat the romance as *the* throughline that every worldbuilding decision feeds.

### Two or three voice signatures that will make the workbook yours

Pick **two or three** and repeat them across hundreds of pages. These become the reader's recognition cues:

**SIGNATURE 1: The "Romance Leverage" callout.**
A recurring, visually distinct element at the bottom of many worldbuilding pages that pulls the worldbuilding idea into the romance. One sentence, one question. This is the single biggest voice differentiator. Example: *"**Romance Leverage:** What's the one religious rule your couple can't break without consequence? That's your midpoint."*

**SIGNATURE 2: Worked mini-examples that name romantasy comps.**
Where School of Plot says "e.g. Harry Potter wizards are useless without wands," you say "e.g. the bargains in *A Court of Thorns and Roses* have magical teeth — break one and your body pays." One comp per concept. Always load-bearing. Always romantasy.

**SIGNATURE 3: The "if you're stuck, try..." scaffolding line.**
Appears before difficult prompts as a low-key safety net. "If you're stuck, try this: list three things your protagonist would die for, then ask which one is here." School of Plot doesn't do this. It's your hand-holding layer, and it's optional — the writer who doesn't need it can skim past.

---

## 8. Specific Style Rules

Concrete rules Claude Code can follow without interpretation.

### Sentence length

- **Target:** 12–22 words average.
- **Range:** 6–30 words. Hit a short one (under 10) at least once per paragraph for rhythm.
- **Never more than two long sentences (25+ words) in a row.**
- Paragraphs are 2–4 sentences. Single-sentence paragraphs are allowed for emphasis.

### British vs American English

**British English throughout.** The competitor is British ("civilisation", "colour", "behaviour", "realised", "honoured"). The romantasy market is global, but British spelling doesn't alienate American readers, and American spelling mildly irritates British ones. Match the competitor.

Specific spellings to enforce:
- -ise not -ize (realise, recognise, organise — but note *capsize*, *prize*, *size* are -ize in British too)
- colour, flavour, honour, behaviour, armour
- grey not gray
- travelled, cancelled (double-l)
- dialogue not dialog
- centre not center
- defence not defense

### Contractions

**Yes — freely.** "You don't", "it's", "they're", "won't", "doesn't". The voice is conversational, not formal. No contractions reads as stiff. Avoid the uncommon ones (shan't, ain't).

### Em dashes, semicolons, parentheticals

- **Em dashes:** Use sparingly — one per paragraph maximum, often zero. Overuse makes the voice feel dashed-off and AI-ish. When used, they work best for a mid-sentence aside or a dramatic reveal at the end of a sentence.
- **Semicolons:** Almost never. The voice is direct. If you're reaching for a semicolon, you're reaching for a full stop.
- **Parentheticals:** Yes, frequently. This is a core voice feature. *"(actually, a super small business...it's just 1 person!)"*, *"(e.g. their mums, a holy book...)"*. Use for examples, clarifications, and dry asides.

### How to introduce a concept

Two-sentence pattern. First sentence states the concept plainly. Second sentence says why it matters *for this book*.

Example: *"A mating bond is a supernatural link between two characters that locks them together in some way. It's your most powerful romance engine and your biggest craft problem, because once the bond is sealed you've spent most of your tension."*

No history of the trope. No academic framing. Just: this is what it is, this is why it matters here.

### How to give permission to skip

Use one of three templates:

1. **Upfront:** *"You don't need to [X]. If you want to, here's how — but you can skip this page without losing anything."*
2. **Inline:** *"Leave any fields blank if they don't apply to your world."*
3. **At section open:** *"This section is for writers who want to [deep-dive on X]. If that's not you, turn the page."*

Always **before** the effort, never after. Always **direct**, never hedging.

### How to name-drop comp titles

- **Italicise book titles.** *A Court of Thorns and Roses*, *Fourth Wing*, *From Blood and Ash*, *The Serpent and the Wings of Night*, *Crescent City*.
- **One comp per concept.** Never a list of three.
- **Always explain what the comp illustrates in one short clause.** *"The bargains in A Court of Thorns and Roses have magical teeth — break one and your body pays."*
- **Don't rank comps.** No "the best example of this is..." Just "one example is..." or "in [book], this shows up as..."
- **Comps should be famous enough that a romantasy reader has likely heard of them.** Don't reach for obscure titles.
- **When citing TV, film, or classical references** (Avatar, Merlin, Romeo & Juliet), treat the same way — italicise, one-line explanation.

### How to handle content warnings

The workbook itself doesn't need blanket content warnings — it's a craft tool, not a piece of dark romance. But:

- **In sections on dark content** (dubcon, violence, trauma): open with a calm acknowledgement. *"This section covers writing sexual coercion and consent. Skip freely if it's not part of your book."*
- **Don't moralise.** Don't say "handle with care" or "be responsible." The reader is an adult.
- **Give permission to skip**, as with any effortful section.

### How to handle "Romance Leverage" call-outs

This is a signature element. Rules:

- **Visual:** Set apart from the rest of the page. Bold label "**Romance Leverage:**" followed by one or two sentences.
- **Length:** 15–40 words. Short.
- **Form:** Always a question or a directive that *takes the worldbuilding decision and points it at the romance*.
- **Frequency:** One per page on content pages. Zero on pure reference pages (tables, overview sheets).
- **Voice:** Same register as the rest of the workbook. Not hypey. Not winky. Just pragmatic.

**Templates:**

- *"**Romance Leverage:** What would [worldbuilding element] cost your couple if they chose each other?"*
- *"**Romance Leverage:** Which of these rules is the one your lovers will break? That's your act break."*
- *"**Romance Leverage:** What does [worldbuilding element] reveal about [love interest] the first time your protagonist sees it in action?"*

---

## 9. Things to Explicitly NOT Do

Tonal mistakes to avoid, based on what the competitor's strengths reveal by contrast:

1. **Do not write a "Dear Writer" letter that promises the reader a writing career.** School of Plot's letter is under 100 words and promises nothing. Don't write a 400-word manifesto about finding your voice.

2. **Do not use motivational language.** No "you've got this!", no "trust yourself!", no "your story matters!" The competitor achieves warmth through brevity and respect, not affirmation. Romantasy readers are not here for a pep talk.

3. **Do not over-explain craft theory.** Each concept gets one page. If you need more than one page to explain something, you're teaching a class, not building a workbook.

4. **Do not moralise about dark content.** The reader chose to write romantasy, knows the genre, and doesn't need a lecture on responsible representation. Trust them.

5. **Do not stack comp references.** One per concept. Ever.

6. **Do not reference creators, influencers, or BookTok personalities by name.** The workbook should age well.

7. **Do not use emoji, exclamation marks in prose (one or two in the whole workbook, reserved for genuine enthusiasm), or "!!!" energy.** The voice is pragmatic, not bubbly.

8. **Do not apologise for the workbook's structure.** "I know this might seem overwhelming, but..." No. State the thing. The reader can handle it.

9. **Do not use the word "journey."** No "your worldbuilding journey." Worldbuilding is a task, not a journey.

10. **Do not pad prompts with qualifiers.** "What might perhaps possibly be the sort of thing that..." No. "What is [X]?"

11. **Do not assume a gender for the reader, protagonist, or love interest by default.** Use "your protagonist", "your love interest", "they" unless the context genuinely demands otherwise.

12. **Do not pretend the workbook is more than it is.** It's a worldbuilding workbook. It will not write the book. It will not fix the book. It is a tool. The competitor's confidence comes partly from not overselling.

13. **Do not use em dashes more than once per paragraph.** It reads as AI-generated.

14. **Do not use "delve", "intricate", "tapestry", "weave", "rich"** or other LLM-signature words. They're markers of AI-generated prose and romantasy readers are alert to them.

15. **Do not write prompts that could apply to any genre.** If a prompt would work in a generic fantasy workbook verbatim, either cut it or add the romantasy hook. Your differentiation is in the specificity.

---

## 10. Sample Paragraphs

Five sample paragraphs in the target voice, calibrated to the spec above.

### Sample 1: An opening-of-section explanation (Magic Systems)

> **How to Write Magic in Romantasy**
>
> Magic is rarely just magic in a romantasy. It's the thing that makes one of your leads powerful, dangerous, or marked — and it's almost always how they end up near each other. Before you design a single spell, work out what the magic is *doing for the love story*. Is it the barrier keeping them apart? The secret one of them is hiding? The force that binds them to each other whether they like it or not? Your magic system doesn't need a hundred rules. It needs one rule that the romance can break.
>
> **Romance Leverage:** Which limit of your magic is the one your lovers will cross for each other? That's your climax.

### Sample 2: A permission-to-skip passage (Currency)

> **Designing Your World's Currency**
>
> You don't need to invent a currency. Nobody reads a romantasy for the exchange rates. If coin never affects your plot — if your protagonist isn't counting it, scheming for it, or noticing the love interest has more of it than she does — skip this page. Tear it out if you want.
>
> If currency *does* matter (a court heroine marrying for money, a mercenary who can be bought, a magical debt paid in something rarer than gold), a few pages of thought now will save you from contradictions later. Fill in as much as you need. Leave the rest blank.

### Sample 3: A prompt cluster with brief intro (Courting)

> **Courting and Romance Customs**
>
> Every culture has rules about how people fall in love in public. Your world's rules tell the reader what's expected — and make it more interesting when your couple breaks them.
>
> *What does courting involve in your world? Who initiates it?*
>
> *Is it common to marry for love, or is marriage usually arranged?*
>
> *What gesture, gift, or word constitutes a declaration of intent?*
>
> *What would make a courtship scandalous? Who decides?*
>
> **Romance Leverage:** Which of these rules does your couple break, and what does it cost them socially?

### Sample 4: A "Romance Leverage" callout (standalone, from the History page)

> **Romance Leverage:** Is there a historical pair of lovers in your world — their Romeo and Juliet, their Orpheus and Eurydice? What do ordinary people *believe* happened to them? Your couple will be compared to these two, fairly or not. Decide now which parallel you want the reader to notice.

### Sample 5: A worked example referencing a comp title (Magic Limitations)

> **Why Your Magic Needs a Price**
>
> Romantasy magic without a cost is romantasy without stakes. In *Fourth Wing*, riders bond with dragons who can kill them in the bonding itself — the magic is beautiful and the price is a death sentence half the class doesn't survive. The cost isn't a side-effect. It's the whole reason the first act works.
>
> Think about what your magic costs. It can be physical (bond sickness, burned-out power, a body that breaks), social (magic users are hunted, exiled, enslaved), or personal (every use takes something from the user that matters to the romance). Pick one. Write it down. Apply it every time magic gets used from here on.

---

## Closing Notes for Claude Code

When generating any page, reach for these in order:

1. **Is this page on-voice?** Second person, short sentences, British spelling, no motivational language, no AI-signature words.
2. **Has permission to skip appeared if the section is effortful?** Upfront, one of the three templates.
3. **Does a comp reference earn its place?** If yes, one comp, italicised, with a one-line explanation.
4. **Does the Romance Leverage callout land?** On content pages, not reference pages. 15–40 words.
5. **Does the page stand alone?** Does it work if the reader opened the workbook here at random?

The voice is **pragmatic friend who knows the genre**. Not coach, not teacher, not cheerleader. One degree warmer than School of Plot, specifically at section openers and in the Romance Leverage callouts. Everywhere else, match the source.
