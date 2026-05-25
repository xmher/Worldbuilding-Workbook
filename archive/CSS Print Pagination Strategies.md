The Architecture of Paged Media: Strategies for Content Containment and Fragmentation Control
Executive Summary
The transition of HyperText Markup Language (HTML) from the fluid, infinite scroll of the digital viewport to the static, finite dimensions of physical media represents one of the most persistent engineering challenges in web development. Unlike the screen, where vertical space is theoretically unlimited, the printed page imposes strict, non-negotiable boundaries. When content exceeds these boundaries, the browser’s rendering engine must make a binary decision: fragment the content across multiple pages (overspill) or constrain it within the current page boundaries (containment).
This report provides an exhaustive technical analysis of the strategies available to developers for managing this transition. It addresses the dual requirements of preventing overflow entirely—forcing content to fit a single page—and managing inevitable overflow cleanly to preserve formatting integrity. The analysis synthesizes current W3C specifications, particularly the CSS Paged Media Module Level 3 and the CSS Fragmentation Module Level 3, with empirical data on browser rendering behaviors (Blink, Gecko, WebKit) as of 2025. It further explores algorithmic solutions for geometric scaling and the use of polyfills like Paged.js to overcome native browser limitations.
1. Introduction: The Divergence of Media Models
The fundamental friction in printing web content arises from the discrepancy between the "Continuous Media" model of the screen and the "Paged Media" model of the printer. In a continuous media context, the viewport acts as a sliding window over a potentially infinite canvas. There are no intrinsic physical boundaries that dictate where content must stop or split. If a data table has five thousand rows, the user simply scrolls. The concept of "overflow" in this context is usually managed via scrollbars or hidden containers, but it rarely results in data loss or structural disintegration.
In contrast, Paged Media is characterized by discrete, rigid page boxes. The canvas is not continuous; it is a series of finite slices. When content flows from one page box to the next, it encounters a physical discontinuity. The browser engine must perform "fragmentation"—the algorithmic process of splitting a single continuous box (like a div or a table) into multiple fragment boxes. This process is fraught with complexity. The engine must determine valid break points, handle borders and padding that are sliced in half, and ensure that semantic units (like a heading and its following paragraph) remain visually associated.
The user's query highlights two distinct architectural goals that often stand in tension with one another. The first is Strict Containment, where the requirement is to "make sure HTML doesn't overflow." This implies a constraint where the content must be forced, by scaling or truncation, to fit within the geometry of a single sheet. This is common for certificates, dashboards, or official forms where a second page is unacceptable. The second goal is Controlled Fragmentation, or "cleanly handling overspill." Here, multi-page output is permissible, but the default behavior of the browser—which might slice a line of text in half or decapitate a chart—must be overridden to maintain the document's formatting integrity.
Achieving professional-quality print output from HTML requires a departure from standard "Responsive Design" principles, which focus on variable width and infinite height. Instead, "Print Design" on the web requires a mental model focused on fixed width, fixed height, and the management of break opportunities. This report details the CSS properties, JavaScript algorithms, and structural strategies necessary to master this domain.
2. The Physics of the Page: The CSS Page Model
To control overflow, one must first understand the container into which the content flows. In the digital realm, the viewport is flexible and defined by the device window. In the print realm, the container is the "Page Box," a rectangular region that maps to the physical sheet of paper.
2.1 Anatomy of the Page Box
The CSS Paged Media Module defines the Page Box as a complex container consisting of two primary regions that compete for available surface area: the Page Area and the Margin Area.
The Page Area: This is the region where the document's flow content (the HTML body) is rendered. The dimensions of the Page Area are calculated by taking the full size of the Page Box and subtracting the page margins. Crucially, strictly "preventing overflow" means ensuring that the rendered height of the HTML content does not exceed the height of this Page Area.
The Margin Area: This is the ring of space surrounding the Page Area. While often empty in standard web printing, the specification divides this area into 16 distinct "Margin Boxes" (e.g., @top-left, @bottom-center, @right-middle). These boxes are reserved for generated content such as running headers, footers, and page numbers.1
Understanding this anatomy is vital because overflow often occurs not because the content is too wide for the paper, but because it is too wide for the Page Area once the default margins are applied. Browser user agents (UAs) typically apply default margins of roughly 0.5 to 1.0 inch (12.7mm to 25.4mm). On a standard US Letter page (8.5 inches wide), a 1-inch margin on both sides leaves only 6.5 inches (approx. 624 pixels at 96 DPI) for content. A layout designed for a 1024px desktop screen will immediately overflow horizontally, triggering scaling or clipping.
2.2 The @page Rule and Canvas Definition
The entry point for defining the physical constraints of the print environment is the @page at-rule. This rule allows the developer to specify the dimensions, orientation, and margins of the page box. To prevent overflow caused by mismatched paper sizes (e.g., printing an A4 design on Letter paper), the size must be explicitly declared.
The size property within the @page rule is the primary mechanism for establishing the canvas. It accepts keywords (auto, portrait, landscape) or length values.

CSS


@page {
    size: A4 portrait; /* Locks dimensions to 210mm x 297mm */
    margin: 20mm;      /* Explicitly defines the breathing room */
}


By explicitly setting the size, the developer overrides the user's local printer settings in the browser's print dialog, ensuring that the layout calculations performed in CSS match the final output. However, one must be cautious. If the user physically loads US Letter paper but the CSS mandates A4, the printer driver may either scale the content (potentially causing unexpected resizing) or clip the edges.
The specification also introduces pseudo-classes for the @page rule, allowing for different geometries on different pages. The :first pseudo-class allows for a unique layout on the cover page (e.g., larger margins for a title), while :left and :right (or :recto and :verso) allow for mirrored margins in double-sided printing, accommodating the gutter binding.3
2.3 The "Unprintable Area" Constraint
A critical, often overlooked variable in overflow management is the hardware limitation of the printer itself. Most consumer and office printers cannot print to the very edge of the paper; they require a "gripper" margin, usually around 4mm to 6mm. If the @page margins are set to 0, content placed at the absolute edge will be clipped by the hardware, regardless of CSS rules. A robust strategy for preventing overflow involves normalizing these variables by defining a "safe zone"—typically a minimum margin of 10mm to 15mm—which ensures that the content remains visible across a wide range of output devices.5
3. Strategy A: Strict Containment (The "Single Page" Imperative)
The first part of the user's request is to "make sure html doesn't overflow." In many business contexts—such as printing invoices, certificates, labels, or executive dashboards—this is interpreted as a strict requirement for the content to fit on a single physical sheet. The content must be contained; spillover is considered a failure state.
Standard CSS flow layout is ill-suited for this requirement. CSS is designed to expand vertically to accommodate content. There is no native property like fit-to-page: true that automatically adjusts font sizes or layout density to respect a vertical boundary. Therefore, strict containment requires a combination of architectural constraints and algorithmic intervention.
3.1 The Limitations of CSS-Only Approaches
Developers often attempt to solve the single-page constraint using CSS viewport units (vh, vw) or percentage heights (height: 100%). While effective on screens, these techniques often fail in print. In the context of media="print", the body height generally resolves to the height of the content, not the page. Setting height: 100% on the html or body element does not constrain the rendering to the first page; it merely stretches the container to match the potentially multi-page flow.6
CSS Transforms offer a partial solution. By applying a static scale to the content container, developers can shrink the output.

CSS


@media print {
    body {
        width: 100%;
        height: 100%;
        overflow: hidden; /* Truncate anything that doesn't fit */
    }
   .print-container {
        transform: scale(0.75); /* Fixed zoom */
        transform-origin: top left;
        width: 133.33%; /* Compensate width: 100% / 0.75 */
    }
}


This approach is brittle. A static scale of 0.75 implies a guess about the content length. If the content is short, the page looks empty; if the content is exceptionally long, it will still overflow or be clipped by the overflow: hidden rule. This does not satisfy the requirement to "make sure" it fits; it only increases the probability that it might fit.
3.2 Algorithmic Geometry Management (JavaScript)
To guarantee a "One Page" fit for variable content, one must employ JavaScript to measure the rendered height against the page height and iteratively adjust the scale. This "Shrink-to-Fit" algorithm is the only exhaustive strategy for dynamic content.
3.2.1 The Binary Search Scaling Algorithm
The most robust implementation involves a script that runs immediately before the print action is triggered (using the window.onbeforeprint event or a dedicated print button handler).
The Algorithm Steps:
Define the Target: Calculate the printable height in pixels. For an A4 page at 96 DPI (the standard CSS resolution), the height is 1123 pixels. Subtracting 20mm margins (approx. 75px each) leaves a safe content height of roughly 970 pixels.
Measure Content: Capture the scrollHeight of the content wrapper element. This value represents the total height of the content, including overflow, before any scaling is applied.
Compare: Check if scrollHeight > targetHeight.
Calculate Scale: If overflow is detected, the required scale factor ($S$) is theoretically $targetHeight / scrollHeight$. However, due to layout shifts that occur during scaling (text reflow), a simple division is sometimes inaccurate.
Iterate: A binary search or iterative decrement loop can refine the scale. The script reduces the scale (e.g., from 1.0 to 0.9, 0.8...) until scrollHeight <= targetHeight.8
Implementation Strategy:

JavaScript


function fitToPage() {
    const pageHeight = 1122; // A4 height in pixels at 96 DPI
    const content = document.getElementById('print-wrapper');
    const maxIterations = 50;
    
    // Reset any existing transforms to get true measurements
    content.style.transform = '';
    content.style.width = '';
    
    let scale = 1;
    let contentHeight = content.scrollHeight;
    
    if (contentHeight > pageHeight) {
        // Simple linear calculation is a good starting point
        scale = pageHeight / contentHeight;
        
        // Apply preliminary scale
        content.style.transform = `scale(${scale})`;
        content.style.transformOrigin = 'top left';
        content.style.width = `${100 / scale}%`;
        
        // Verification loop (optional for high precision)
        // If the scaled content causes reflow that changes height, adjust further
        //... (iterative adjustment logic)
    }
}


This ensures that no matter how much content is present, it is mathematically forced to fit the page bounds.9 The visual result is similar to the "Fit to Page" feature found in spreadsheet software.
3.3 Text Truncation: The line-clamp Strategy
In scenarios where scaling content down renders it illegible (e.g., a scale factor below 0.5), the strict containment strategy must shift from scaling to truncation. If the priority is "do not spill to page 2," and the content simply cannot fit on page 1, the excess content must be sacrificed to preserve the layout's integrity.
The CSS line-clamp property is a highly effective tool for this. Originally a proprietary WebKit feature, it has been adopted by the CSS Overflow Module Level 3 and is supported in most modern browsers (including Firefox and Edge) via the -webkit- prefix. It allows the developer to specify a maximum number of lines for a block of text.

CSS


@media print {
   .summary-text {
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 5; /* Limit to 5 lines */
        overflow: hidden;
    }
}


This strategy is particularly useful for printing lists of cards, summaries, or descriptions where visual uniformity is preferred over textual completeness. The browser automatically inserts an ellipsis (…) at the point of truncation, signaling to the reader that content exists but was cut to fit the constraints.11 This satisfies the requirement of "clean handling"—the layout remains rigid and single-page, and the overflow is hidden rather than spilling messily.
4. Strategy B: Controlled Fragmentation (Managing Overspill)
When the strict "Single Page" constraint is lifted, the goal shifts to Controlled Fragmentation. The user's request to "cleanly handle overspill" implies that multi-page documents are acceptable, provided that the breaks do not destroy the formatting (e.g., slicing an image in half, breaking a table row, or leaving a heading stranded at the bottom of a page).
4.1 The Evolution of Break Properties
Historically, developers used page-break-before, page-break-after, and page-break-inside to control pagination. These are now legacy properties. While browsers largely treat them as aliases for compatibility, the modern CSS Fragmentation Module specifies the generic break-* properties, which apply not just to pages but also to multi-column layouts and regions.13
Table 1: Evolution of Fragmentation Properties
Legacy Property
Modern Property
Function
page-break-before
break-before
Controls the break opportunity before the generated box.
page-break-after
break-after
Controls the break opportunity after the generated box.
page-break-inside
break-inside
Controls the break opportunity within the box.

It is crucial to understand that break-* properties are not commands; they are hints to the rendering engine. A value of avoid does not guarantee that a break will not occur; it instructs the browser to avoid the break if possible. If an element with break-inside: avoid is taller than the page itself, the browser has no choice but to violate the rule and fragment the content.
4.2 The "Keep Together" Strategy (break-inside: avoid)
The most powerful tool for maintaining formatting integrity during overspill is break-inside: avoid. This instructs the fragmentation engine: "If this element cannot fit entirely on the current page, move the entire element to the next page."
This property is essential for:
Cards and Widgets: Ensuring a bordered box is not sliced in half.
Images and Figures: Preventing a chart from being decapitated.
Table Rows: Ensuring that a row of data remains readable as a single unit.

CSS


@media print {
   .card,.table-row, figure, img {
        break-inside: avoid;
        page-break-inside: avoid; /* Legacy fallback for older WebKit */
    }
}


However, the "Avoid" directive introduces a potential trap. If a user prints a document with a 2000-pixel high container that has break-inside: avoid, and the page height is only 1000 pixels, the behavior is browser-dependent. Typically, the browser will push the element to the start of a new page (to give it the maximum possible space) and then force a break anyway. This often results in a large blank space at the bottom of the previous page. To mitigate this, break-inside: avoid should be coupled with a reasonable max-height restriction on the element, ensuring it is mathematically possible for it to fit on a page.
4.3 Typographic Control: Orphans and Widows
When text flows across pages, "clean handling" requires avoiding typographic errors known as orphans and widows.
Orphan: A single line of a paragraph appearing at the bottom of a page.
Widow: A single line of a paragraph appearing at the top of the next page.
These are controlled via the orphans and widows properties, which accept an integer representing the minimum number of lines.

CSS


p {
    orphans: 3; /* Keep at least 3 lines at the bottom */
    widows: 3;  /* Keep at least 3 lines at the top */
}


Increasing these values from the default (usually 2) forces the browser to move larger chunks of text together. If only 2 lines would fit at the bottom, and orphans is set to 3, the entire paragraph moves to the next page. This contributes significantly to the "cleanliness" of the overspill, giving the document a professional, typeset appearance.4
5. The Flexbox and Grid Fragmentation Paradox
A significant portion of modern web layout relies on Flexbox and CSS Grid. However, printing these layouts presents a unique set of architectural challenges. For years, browser engines (particularly Chromium/Blink) treated Flex and Grid containers as "monolithic"—meaning the engine calculated the layout as a single, unbreakable box. If a Flex container spanned two pages, the content would simply clip or vanish rather than flowing to the next page.
5.1 The Browser Engine Landscape (2025 Status)
The implementation of fragmentation for Flex and Grid items varies significantly across rendering engines, creating a minefield for developers seeking a consistent strategy.
Firefox (Gecko): Firefox has historically had the most robust implementation of fragmentation for modern layouts. It correctly fragments Flex and Grid containers and respects break-inside: avoid on items within them.15
Chrome/Edge (Blink): Support has improved but remains buggy. As of 2024/2025, deeply nested Flex containers often fail to break correctly. A specific issue persists where break-inside: avoid is ignored on Flex items if the parent container has certain properties. Furthermore, the engine sometimes struggles to calculate the height of a broken grid, leading to content overlapping footer text.16
Safari (WebKit): WebKit often requires explicit display: block overrides to fragment content that is set to display: flex.
5.2 The "Float Fallback" Architecture
Given these inconsistencies, the most reliable strategy for "cleanly handling overspill" in 2025 involves disabling Flexbox and Grid in print stylesheets. By reverting to the older Block and Float layout models, developers tap into the most mature and stable fragmentation logic in the browser engines.
The Workaround Strategy:

CSS


@media print {
    /* Neutralize Flexbox and Grid */
   .grid-container,.flex-container {
        display: block!important;
    }
    
    /* Reconstruct layout using Floats or Inline-Block */
   .grid-item,.flex-item {
        width: 50%; /* Simulate 2 columns */
        float: left;
        box-sizing: border-box;
        break-inside: avoid; /* Works reliably on blocks */
    }
    
    /* Clearfix to ensure container height is respected */
   .grid-container::after {
        content: "";
        display: table;
        clear: both;
    }
}


This "regression" to older layout models is the only 100% reliable way to ensure that complex multi-column layouts fragment cleanly across pages without losing data or encountering rendering artifacts.18 It sacrifices the ease of vertical alignment provided by Flexbox but gains the robustness of block-level fragmentation.
6. Contextual Persistence: Headers, Footers, and Tables
A key aspect of maintaining formatting integrity during overspill is preserving context. If a data table spills to page 2, the user needs to see the column headers again to understand the data. If a document spills, the user needs running headers (e.g., "Report - Page 2") to maintain orientation.
6.1 Native Table Fragmentation
HTML tables have inherent fragmentation behaviors designed for print.
display: table-header-group: Applying this to the <thead> element causes the browser to repeat the header row at the top of every new page the table spans.
display: table-footer-group: Applying this to <tfoot> should theoretically repeat the footer at the bottom of every page.
Implementation:

CSS


@media print {
    thead { display: table-header-group; }
    tfoot { display: table-footer-group; }
    tr { break-inside: avoid; }
}


Browser Deviations:
While thead repetition is reliable across Chrome and Firefox, tfoot repetition is notoriously inconsistent. Chrome (Blink) has had long-standing bugs where the footer only prints on the final page of the table, rather than repeating at the bottom of each page fragment. Consequently, for strict requirements regarding repeated footers, relying solely on tfoot is risky.19
6.2 Fixed Positioning for Global Context
To ensure a header or footer appears on every page of a document (not just within a table), the position: fixed strategy is commonly employed. In the context of media="print", an element with position: fixed is anchored to the Page Box, not the content flow. This means the browser re-renders it on every single page generated.
The Overlap Problem:
Because fixed elements are removed from the document flow, the main content (body) will flow behind them, causing text to be obscured at the top and bottom of the page.
The "Phantom Spacer" Solution:
To prevent overlap, the body needs padding. However, padding on the body applies to every page.

CSS


@media print {
    header {
        position: fixed;
        top: 0;
        height: 50px;
    }
    body {
        padding-top: 50px; /* Pushes content down on every page */
    }
}


This solution works well for uniform headers. However, if the header height varies, or if there is a requirement to hide the header on the first page, position: fixed becomes difficult to manage without complex JavaScript manipulation of the DOM during the print process.21
7. Advanced Pagination: The Paged.js Solution
For requirements that go beyond simple containment or basic fragmentation—such as generating a Table of Contents, handling complex running headers (e.g., "Chapter 1" on page 5, "Chapter 2" on page 12), or precise footnote placement—native browser support is insufficient. The standard CSS features for these capabilities (CSS Generated Content for Paged Media) are largely unimplemented in browsers like Chrome and Safari.
To achieve "nuanced" control and "rich insight" into the document structure, developers must turn to Paged.js. This is an open-source JavaScript library that polyfills the CSS Paged Media specifications. It effectively bypasses the browser's native fragmentation engine.
7.1 Architecture of Paged.js
Paged.js works by rendering the content into a "virtual" canvas in the browser. It runs a process called "Chinking":
Chunker: It takes the content stream and fills a container until it detects overflow.
Split: It conceptually "cuts" the DOM at that exact pixel.
Reflow: It moves the remaining content to a new DOM node representing the next page.
Polisher: It applies generated content, counters, and layout adjustments based on the new structure.
7.2 Capabilities Unlock
By using Paged.js, developers can utilize CSS properties that standard browsers ignore.
Running Headers:
The library supports the string-set property, allowing content from the DOM to be moved into the margin boxes.

CSS


/* Define the value */
h2 { 
    string-set: chapterTitle content(); 
}

/* Use the value in the margin */
@page {
    @top-right {
        content: string(chapterTitle);
    }
}


With this configuration, if page 10 contains "Chapter 3," the header on page 10 (and subsequent pages) will automatically read "Chapter 3." This level of contextual awareness is impossible with standard position: fixed.1
Implications for the User:
If the user's definition of "cleanly handling overspill" includes maintaining complex document metadata across pages, adopting Paged.js is not just an option; it is a requirement. It standardizes the output across Chrome, Firefox, and Safari by taking control of the rendering pipeline, eliminating the engine-specific bugs discussed in Section 5.
8. Conclusion: A Unified Strategy
The challenge of controlling HTML overflow and fragmentation is not solved by a single property but by a tiered architectural strategy.
Table 2: Strategic Decision Matrix
Requirement
Primary Strategy
Key Technologies
Trade-offs
Strict Single Page
Containment
JS Scaling Algorithm, transform: scale, line-clamp
Content may become too small to read; logic is complex to implement.
Clean Overspill
Native Fragmentation
break-inside: avoid, orphans/widows, Float Layouts
Requires abandoning Flex/Grid for print; browser inconsistency in footers.
Professional Report
Polyfill
Paged.js, @page Margin Boxes
Heavy JavaScript dependency; slower rendering time; precise control.

To satisfy the user's original request:
For Prevention (Containment): Do not rely on CSS alone. Implement the binary search "Shrink-to-Fit" JavaScript algorithm detailed in Section 3.2. This provides the mathematical certainty that height: 100% fails to deliver.
For Mitigation (Clean Overspill): Adopt the "Float Fallback" architecture. Override modern display: flex and display: grid layouts with display: block and float inside @media print blocks. Apply break-inside: avoid strictly to atomic components (cards, rows, images) and never to high-level wrappers.
By layering these techniques—starting with a robust @page definition, applying fragmentation protection to components, and polyfilling missing features where necessary—developers can bridge the gap between the screen and the page, ensuring that the "spill" is not a mess, but a feature.
Works cited
Add content to the margins of web pages when printed using CSS | Blog, accessed January 20, 2026, https://developer.chrome.com/blog/print-margins
CSS Paged Media Module Level 3 - W3C, accessed January 20, 2026, https://www.w3.org/TR/css-page-3/
@page | CSS-Tricks, accessed January 20, 2026, https://css-tricks.com/almanac/rules/p/page/
CSS paged media - MDN Web Docs - Mozilla, accessed January 20, 2026, https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Paged_media
CSS print page styling - DocuSeal, accessed January 20, 2026, https://www.docuseal.com/blog/css-print-page-style
Scale HTML to fit one page when printing - Stack Overflow, accessed January 20, 2026, https://stackoverflow.com/questions/50549663/scale-html-to-fit-one-page-when-printing
print css: fit in one page - Stack Overflow, accessed January 20, 2026, https://stackoverflow.com/questions/2435036/print-css-fit-in-one-page
Programmatically "Fit" Variable Length HTML Content to a Single Printed Page?, accessed January 20, 2026, https://stackoverflow.com/questions/27278935/programmatically-fit-variable-length-html-content-to-a-single-printed-page
How to design a printable HTML page layout | by Karthikeyan Rajendran - Medium, accessed January 20, 2026, https://medium.com/@karthikricssion/how-to-design-a-printable-html-page-layout-802bc9ea61dd
Need Javascript Help with Printing a Page (fixed height/width) | Articulate - Community, accessed January 20, 2026, https://community.articulate.com/discussions/discuss/need-javascript-help-with-printing-a-page-fixed-heightwidth/693774
line-clamp - CSS-Tricks, accessed January 20, 2026, https://css-tricks.com/almanac/properties/l/line-clamp/
line-clamp - CSS - MDN Web Docs, accessed January 20, 2026, https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/line-clamp
break-inside - CSS - MDN Web Docs, accessed January 20, 2026, https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/break-inside
page-break-inside - CSS - MDN Web Docs, accessed January 20, 2026, https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/page-break-inside
Chrome/Safari adding margin to elements with `width: 0`, but Firefox doesn't : r/css - Reddit, accessed January 20, 2026, https://www.reddit.com/r/css/comments/bl90ec/chromesafari_adding_margin_to_elements_with_width/
Page-breaks on grid and flexbox items not behaving properly · Issue #2076 · Kozea/WeasyPrint - GitHub, accessed January 20, 2026, https://github.com/Kozea/WeasyPrint/issues/2076
Page-break-inside:avoid not working - Stack Overflow, accessed January 20, 2026, https://stackoverflow.com/questions/34534231/page-break-insideavoid-not-working
Prevent break inside grid when printing - Stack Overflow, accessed January 20, 2026, https://stackoverflow.com/questions/68850438/prevent-break-inside-grid-when-printing
HTML tables cut in half on print to pdf - Qt Forum, accessed January 20, 2026, https://forum.qt.io/topic/97092/html-tables-cut-in-half-on-print-to-pdf
html - Table repeated footer group in chrome - Stack Overflow, accessed January 20, 2026, https://stackoverflow.com/questions/40966622/table-repeated-footer-group-in-chrome
Printed Static Footer Overlapping Page Content - Stack Overflow, accessed January 20, 2026, https://stackoverflow.com/questions/72352371/printed-static-footer-overlapping-page-content
Printing a Page - Is there a way to repeat a header / footer on page breaks - Reddit, accessed January 20, 2026, https://www.reddit.com/r/webdev/comments/g72zci/printing_a_page_is_there_a_way_to_repeat_a_header/
Web design for print - Paged.js —, accessed January 20, 2026, https://pagedjs.org/en/documentation/5-web-design-for-print/
Strange behaviors of block elements in paged-footnotes · Issue #156 · rstudio/pagedown, accessed January 20, 2026, https://github.com/rstudio/pagedown/issues/156
