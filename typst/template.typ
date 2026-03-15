// ============================================================
// Romantasy Worldbuilding Workbook — Typst Template
// ============================================================
// Reusable layout components matching the workbook's visual
// language: forest green + gold + warm cream, double border,
// serif display + elegant accent + clean body type.
// ============================================================

// --- Color Palette ---
#let color-theme     = rgb("#065f46")   // forest green
#let color-theme-light = rgb("#065f46").lighten(90%)
#let color-bg        = rgb("#fdfbf7")   // warm cream
#let color-noir      = rgb("#1a1515")   // near-black
#let color-accent    = rgb("#e2c98a")   // gold
#let color-danger    = rgb("#9f1239")   // deep red
#let color-text-main = rgb("#121212")
#let color-text-sub  = rgb("#444444")
#let color-text-muted = rgb("#888888")

// --- Font Stacks ---
#let font-display = "Libre Baskerville"
#let font-accent  = "Cormorant Garamond"
#let font-body    = "Inter"

// ============================================================
// Document Setup
// ============================================================

#let workbook-setup(
  title: "The Romantasy Worldbuilding Workbook",
  body,
) = {
  set document(title: title)

  // Page geometry — 8.5 × 11 in, generous margins
  set page(
    width: 8.5in,
    height: 11in,
    margin: (top: 1in, bottom: 1.25in, left: 1.1in, right: 1.1in),
    fill: white,

    // Double decorative border on every page
    background: {
      // Outer green border
      place(
        dx: 15pt, dy: 15pt,
        rect(
          width: 100% - 30pt,
          height: 100% - 30pt,
          stroke: 3pt + color-theme,
          fill: none,
          radius: 0pt,
        ),
      )
      // Inner gold border
      place(
        dx: 22pt, dy: 22pt,
        rect(
          width: 100% - 44pt,
          height: 100% - 44pt,
          stroke: 1pt + color-accent,
          fill: none,
          radius: 0pt,
        ),
      )
    },

    // Footer: section name (left) + page number (center)
    footer: context {
      let page-num = counter(page).get().first()
      // suppress footer on first page
      if page-num > 1 {
        set text(font: font-display)
        grid(
          columns: (2fr, 1fr, 1fr),
          align: (left, center, right),
          text(
            size: 0.6em,
            tracking: 1pt,
            fill: color-text-muted,
            upper(title),
          ),
          text(
            size: 0.7em,
            weight: "bold",
            fill: color-theme,
            str(page-num),
          ),
          [],
        )
      }
    },
  )

  // Base typography
  set text(
    font: font-body,
    size: 11pt,
    fill: color-text-main,
    hyphenate: false,
  )
  set par(
    leading: 0.65em * 1.6,
    justify: true,
    first-line-indent: 0pt,
  )

  // Heading styles
  show heading.where(level: 1): it => {
    set text(
      font: font-display,
      size: 2em,
      weight: "bold",
      fill: color-noir,
      tracking: 3pt,
    )
    block(above: 2em, below: 1.5em)[
      #upper(it.body)
    ]
  }

  show heading.where(level: 2): it => {
    set text(
      font: font-display,
      size: 1.4em,
      weight: "bold",
      fill: color-noir,
    )
    block(
      above: 2em,
      below: 1em,
    )[
      #it.body
      #v(0.5em)
      #line(length: 100%, stroke: 2pt + color-accent)
    ]
  }

  show heading.where(level: 3): it => {
    set text(
      font: font-display,
      size: 1.1em,
      weight: "bold",
      fill: color-theme,
    )
    block(above: 1.5em, below: 0.75em, it.body)
  }

  show heading.where(level: 4): it => {
    set text(
      font: font-accent,
      size: 1.1em,
      weight: "semibold",
      style: "italic",
      fill: color-text-sub,
    )
    block(above: 1.25em, below: 0.5em, it.body)
  }

  body
}


// --- Number-to-Word Mapping ---
#let number-words = (
  "Zero", "One", "Two", "Three", "Four", "Five",
  "Six", "Seven", "Eight", "Nine", "Ten",
  "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen",
  "Sixteen", "Seventeen", "Eighteen", "Nineteen", "Twenty",
  "Twenty-One",
)

#let number-to-word(n) = {
  if n >= 0 and n < number-words.len() {
    number-words.at(n)
  } else {
    str(n)
  }
}

// ============================================================
// COMPONENTS
// ============================================================

// --- Title Page ---
#let title-page(
  title: "The Romantasy Worldbuilding Workbook",
  tagline: none,
) = {
  page(
    footer: none,
  )[
    // Green banner at top
    #v(1em)
    #align(center)[
      #block(
        fill: color-theme,
        inset: (x: 2em, y: 0.6em),
        radius: 2pt,
      )[
        #set text(
          font: font-display,
          size: 1em,
          weight: "bold",
          tracking: 3pt,
          fill: white,
        )
        #upper[A Plotbrew Writing Workbook]
      ]
    ]

    #v(1fr)

    // Title
    #align(center)[
      #text(
        font: font-display,
        size: 2.5em,
        weight: "bold",
        tracking: 2pt,
        fill: color-noir,
      )[#upper(title)]
    ]

    #v(0.8em)

    // Decorative gold flourish with rule
    #align(center)[
      #grid(
        columns: (80pt, 12pt, auto, 12pt, 80pt),
        align: (horizon, horizon, horizon, horizon, horizon),
        line(length: 100%, stroke: 1.5pt + color-accent),
        [],
        text(fill: color-accent, size: 2.5em)[✦],
        [],
        line(length: 100%, stroke: 1.5pt + color-accent),
      )
    ]

    #v(0.8em)

    // Tagline
    #if tagline != none {
      align(center)[
        #text(
          font: font-accent,
          size: 1.8em,
          style: "italic",
          weight: "semibold",
          tracking: 0pt,
          fill: color-theme,
        )[#tagline]
      ]
    }

    #v(2fr)
  ]
}


// --- Section Title Page ---
#let section-title-page(
  number: none,
  title: "",
  intro: none,
) = {
  pagebreak(weak: true)
  page(footer: none)[
    #set align(left + horizon)
    #block(width: 100%)[
      #if number != none {
        text(
          font: font-display,
          size: 0.75em,
          tracking: 5pt,
          fill: color-theme,
        )[#upper("Section " + number-to-word(number))]
        v(1em)
      }

      #text(
        font: font-display,
        size: 2.2em,
        weight: "bold",
        tracking: 3pt,
        fill: color-noir,
      )[#upper(title)]

      #if intro != none {
        v(1.5em)
        text(
          font: font-accent,
          size: 1.15em,
          style: "italic",
          fill: color-text-sub,
        )[#intro]
      }

    ]
  ]
}


// --- Lead Text (italic intro paragraphs) ---
#let lead-text(body) = {
  block(below: 1.5em)[
    #text(
      font: font-accent,
      size: 1.15em,
      style: "italic",
      fill: color-text-sub,
    )[#body]
  ]
}


// --- Hint Text (muted guidance) ---
#let hint(body) = {
  block(above: -0.3em, below: 1em)[
    #text(
      font: font-accent,
      style: "italic",
      fill: color-text-muted,
      size: 0.95em,
    )[#body]
  ]
}


// --- Divider Flourish ---
#let divider() = {
  v(1em)
  align(center)[
    #box(width: 80pt, line(length: 100%, stroke: 2pt + color-accent))
    #h(8pt)
    #text(fill: color-accent, size: 1.2em)[◆]
    #h(8pt)
    #box(width: 80pt, line(length: 100%, stroke: 2pt + color-accent))
  ]
  v(1em)
}


// --- Anchor Card (key questions / principles) ---
#let anchor-card(
  title: "Anchor Question",
  question: "",
) = {
  block(
    width: 100%,
    inset: 25pt,
    stroke: 2pt + color-noir,
    fill: white,
    above: 1.5em,
    below: 1.5em,
    breakable: false,
  )[
    #text(
      font: font-display,
      size: 0.9em,
      fill: color-theme,
      tracking: 2pt,
    )[#upper(title)]
    #v(12pt)
    #block(
      inset: (left: 15pt),
      stroke: (left: 3pt + color-accent),
    )[
      #text(
        font: font-accent,
        style: "italic",
        size: 1.15em,
      )[#question]
    ]
  ]
}


// --- Framework Box (key concepts / frameworks) ---
#let framework-box(
  title: "Framework",
  body,
) = {
  block(
    width: 100%,
    inset: (x: 25pt, y: 20pt),
    stroke: 2pt + color-theme,
    fill: color-theme-light,
    above: 1.5em,
    below: 1.5em,
    breakable: false,
  )[
    #text(
      font: font-display,
      size: 0.9em,
      weight: "bold",
      fill: color-theme,
      tracking: 2pt,
    )[#upper(title)]
    #v(1em)
    #body
  ]
}


// --- Mistake Box (common errors / warnings) ---
#let mistake-box(
  title: "Common Mistake",
  fix: none,
  body,
) = {
  block(
    width: 100%,
    inset: (x: 25pt, y: 20pt),
    stroke: (left: 4pt + color-danger, rest: none),
    fill: color-danger.lighten(95%),
    above: 1.5em,
    below: 1.5em,
    breakable: false,
  )[
    #text(
      font: font-display,
      size: 0.9em,
      weight: "bold",
      fill: color-danger,
    )[#title]
    #v(0.75em)
    #set text(size: 0.9em)
    #body
    #if fix != none {
      v(0.75em)
      text(
        font: font-display,
        size: 0.65em,
        tracking: 1pt,
        fill: color-theme,
      )[#upper("Fix")]
      linebreak()
      text(size: 0.9em)[#fix]
    }
  ]
}


// --- Writing Box (user input area) ---
#let writing-box(
  label: none,
  height: 100pt,
) = {
  block(
    width: 100%,
    inset: (x: 20pt, y: 15pt),
    stroke: 1pt + color-noir,
    fill: white,
    above: 1em,
    below: 1.5em,
    breakable: false,
  )[
    #if label != none {
      text(
        font: font-display,
        size: 0.65em,
        tracking: 2pt,
        fill: color-theme,
      )[#upper(label)]
      v(0.5em)
    }
    #v(height)
  ]
}


// --- Checklist ---
#let checklist(..items) = {
  block(above: 1em, below: 1em, breakable: false)[
    #for item in items.pos() {
      block(inset: (left: 30pt, bottom: 8pt))[
        #place(
          dx: -30pt,
          dy: 2pt,
          rect(
            width: 16pt,
            height: 16pt,
            stroke: 1pt + color-theme,
            fill: white,
          ),
        )
        #text(size: 0.95em)[#item]
      ]
    }
  ]
}


// --- Workbook Table (styled data table) ---
#let workbook-table(
  headers: (),
  rows: (),
  example-rows: (),
  col-widths: none,
) = {
  let all-rows = ()

  // Example rows first (highlighted)
  for row in example-rows {
    all-rows.push(row.map(cell =>
      text(style: "italic", fill: color-text-muted)[#cell]
    ))
  }

  // Regular rows
  for row in rows {
    all-rows.push(row)
  }

  let cols = if col-widths != none { col-widths } else { range(headers.len()).map(_ => 1fr) }

  block(width: 100%, above: 1.5em, below: 1.5em)[
    #set par(justify: false)
    #table(
      columns: cols,
      fill: (col, row) => {
        if row == 0 { color-theme }
        else if row <= example-rows.len() { color-theme.lighten(92%) }
        else if calc.rem(row, 2) == 0 { rgb("#00000005") }
        else { none }
      },
      stroke: 1pt + color-noir,
      inset: 12pt,
      align: left,

      // Headers (repeat on page break)
      table.header(
        ..headers.map(h =>
          text(
            font: font-display,
            size: 0.7em,
            tracking: 1pt,
            weight: "bold",
            fill: white,
          )[#upper(h)]
        ),
      ),

      // All data rows
      ..all-rows.flatten(),
    )
  ]
}


// --- Structured Table (pre-filled labels, user fills in cells) ---
// Breakable with repeating headers. All rows have consistent height.
// No blank fill rows — every row has a label.
#let structured-table(
  headers: (),
  rows: (),
  example-rows: (),
  row-height: 55pt,
  preamble: none,
) = {
  let col-count = headers.len()

  let all-rows = ()

  // Example rows (italic, tinted background)
  for row in example-rows {
    all-rows.push(row.map(cell =>
      text(style: "italic", fill: color-text-muted, size: 0.85em)[#cell]
    ))
  }

  // Content rows with consistent height
  for row in rows {
    all-rows.push(row.map(cell => block(height: row-height)[#cell]))
  }

  // Estimate total table height to decide if it fits on a single page.
  // Tables that fit: non-breakable (prevents orphaned rows).
  // Tables that don't fit: breakable (allows natural page breaks).
  let effective-row-h = row-height / 1pt + 24
  let example-h = if example-rows.len() > 0 { calc.max(100, effective-row-h) * example-rows.len() } else { 0 }
  let preamble-h = if preamble != none { 150 } else { 0 }
  let total-height = 44 + example-h + rows.len() * effective-row-h + preamble-h
  let can-fit = total-height < 620

  block(width: 100%, above: 1.5em, below: 1.5em, breakable: not can-fit)[
    #if preamble != none { preamble }
    #set par(justify: false)
    #table(
      columns: range(col-count).map(_ => 1fr),
      fill: (col, row) => {
        if row == 0 { color-theme }
        else if row <= example-rows.len() { color-theme.lighten(92%) }
        else { white }
      },
      stroke: 1pt + color-noir,
      inset: 12pt,
      align: left,

      table.header(
        ..headers.map(h =>
          text(
            font: font-display,
            size: 0.7em,
            tracking: 1pt,
            weight: "bold",
            fill: white,
          )[#upper(h)]
        ),
      ),

      ..all-rows.flatten(),
    )
  ]
}


// --- Open-Ended Table (example + blank rows, fills page) ---
// For tables where users add their own entries. Uses layout() to fill
// remaining page space with blank rows. Use extra-rows for continuation.
#let open-table(
  headers: (),
  example-rows: (),
  rows: (),
  row-height: 55pt,
  extra-rows: 0,
  preamble: none,
) = {
  let col-count = headers.len()

  // Format example rows (italic, muted)
  let fmt-example-rows = example-rows.map(row =>
    row.map(cell =>
      text(style: "italic", fill: color-text-muted, size: 0.85em)[#cell]
    )
  )

  // Format labeled rows (normal style, like structured-table)
  let fmt-rows = rows.map(row =>
    row.map(cell => block(height: row-height)[#cell])
  )

  // Blank row template
  let blank-row = range(col-count).map(_ => block(height: row-height)[])

  // Shared table builder
  let make-table(all-rows, ex-count, labeled-count) = {
    set par(justify: false)
    table(
      columns: range(col-count).map(_ => 1fr),
      fill: (col, row) => {
        if row == 0 { color-theme }
        else if row <= ex-count { color-theme.lighten(92%) }
        else { white }
      },
      stroke: 1pt + color-noir,
      inset: 12pt,
      align: left,

      table.header(
        ..headers.map(h =>
          text(
            font: font-display,
            size: 0.7em,
            tracking: 1pt,
            weight: "bold",
            fill: white,
          )[#upper(h)]
        ),
      ),

      ..all-rows.flatten(),
    )
  }

  // Measure remaining page space and fill with blank rows
  layout(size => {
    let effective-row-h = row-height / 1pt + 24
    let header-h = 44
    let example-h = if example-rows.len() > 0 { calc.max(70, effective-row-h) * example-rows.len() } else { 0 }
    let rows-h = rows.len() * effective-row-h
    let preamble-h = if preamble != none { 150 } else { 0 }
    let overhead = header-h + example-h + rows-h + preamble-h + 24

    let available = size.height / 1pt - overhead
    let fill-count = calc.max(0, int(available / effective-row-h))

    // If labeled+example rows already exceed page, no blanks and allow breaking
    let can-fit = available > 0

    let all-rows = fmt-example-rows + fmt-rows
    if can-fit {
      let i = 0
      while i < fill-count {
        all-rows = all-rows + (blank-row,)
        i = i + 1
      }
    }

    block(width: 100%, above: 1.5em, below: 0pt, breakable: not can-fit)[
      #if preamble != none { preamble }
      #make-table(all-rows, example-rows.len(), rows.len())
    ]
  })

  // Extra continuation rows on a new page
  if extra-rows > 0 {
    let extra = ()
    let i = 0
    while i < extra-rows {
      extra = extra + (blank-row,)
      i = i + 1
    }

    pagebreak()
    block(width: 100%, above: 0pt, below: 0pt, breakable: false)[
      #make-table(extra, 0)
    ]
  }
}


// --- Section Number Label ---
#let section-number(num) = {
  text(
    font: font-display,
    size: 0.7em,
    tracking: 4pt,
    fill: color-theme,
  )[#upper("Section " + number-to-word(num))]
}


// --- Cross-Reference Callout ---
#let cross-ref(section: "", note: "") = {
  block(
    width: 100%,
    inset: (x: 20pt, y: 15pt),
    stroke: (left: 3pt + color-accent),
    fill: none,
    above: 1em,
    below: 1em,
    breakable: false,
  )[
    #text(weight: "bold")[Continue in #section]
    #linebreak()
    #text(
      font: font-accent,
      style: "italic",
      size: 0.95em,
      fill: color-text-sub,
    )[#note]
  ]
}


// --- Writing Lines (blank ruled lines) ---
#let writing-lines(count: 3) = {
  v(0.5em)
  for i in range(count) {
    line(length: 100%, stroke: 0.5pt + color-text-muted)
    v(1.5em)
  }
}
