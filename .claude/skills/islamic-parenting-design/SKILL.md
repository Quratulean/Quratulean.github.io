---
name: islamic-parenting-design
description: Design any visual for the Islamic Parenting 101 brand — printables, worksheets, planners, trackers, badges, certificates, infographics, email headers, social graphics (not Pinterest pins), book interior pages, Canva-ready templates, free lead-magnet PDFs, or any new logo or icon variant — on-brand and on first try, using the project's design system (tokens + components). Use whenever the user asks for anything visual for Islamic Parenting 101, Tabasum Majeed, Hearts Before Habits, or the quratulean.github.io site — even when the user doesn't say "design" (e.g. "make a salah tracker", "I need a worksheet", "put together a lead magnet", "do a printable", "make a gift pdf"). For Pinterest pins specifically, use pinterest-viral-pins instead; this skill is for everything else visual.
---

# Islamic Parenting 101 — Design

Every visual that leaves this brand should feel like it came out of the same warm, cream-coloured workbook. That consistency is the brand's compounding advantage: a tired Muslim mom should recognise an Islamic Parenting 101 printable from across the room, before she reads a single word on it.

The design system does the heavy lifting. This skill tells you how to use it so that whatever you make — a free printable, a Ramadan tracker, a worksheet, an email header, a certificate for the kids, a badge for a blog section — looks like it belongs in the same family as the book, the website and the pins.

## When this skill fires vs. its siblings

- **This skill (`islamic-parenting-design`)**: anything visual that isn't a Pinterest pin. Printables (most common), worksheets, planners, trackers, badges, certificates, infographics for the website, email headers, social graphics (Instagram/Facebook), book-interior sections, logo variants, favicons, Open Graph images, PDF covers, lead magnets.
- **`pinterest-viral-pins`**: Pinterest pins (1000×1500 and its cousins). If the user says "pin", go there.
- **`islamic-parenting-blog`**: writing articles. Comes here only to add a featured image.

If you're unsure, ask one short question. If the user is away, do the simpler reading: anything with a "download" or "print" word is a printable; anything with "Facebook/Instagram story" is a social graphic; otherwise default to this skill.

## The one unskippable step: load the design system

Before you draw a rectangle, load the design system. It's a Claude design-system artifact titled **"Islamic Parenting 101"** on the owner's account (Tabasum Majeed).

1. `Artifact` list with `type: "Design System"` and pick the one titled "Islamic Parenting 101".
2. Read `project/README.md` (brand book — voice, rules, what-we-never-do), `project/tokens.json` (every colour, type style, spacing, radius, shadow), and the README of any component you'll copy.
3. Only then start drawing. If the artifact can't be reached in this session, fall back to the token snapshot in `templates/tokens-snapshot.css` and tell the user you're working from the cached copy.

Reaching for memory instead of the artifact is the fastest way to drift the brand.

## Picking the format

What you deliver depends on where the asset will live. Decide this early — it changes the dimensions, the fonts' delivery, the file type and whether you can bleed to the edge.

| Output | Deliver as | Size (px @ 1x / in @ 300dpi) | Notes |
|---|---|---|---|
| Printable (single page, most common) | PDF via WeasyPrint, A4 or Letter | A4 2480×3508 / Letter 2550×3300 at 300 dpi | 20 mm inner margin, no bleed. The mom prints at home. |
| Multi-page printable kit / lead magnet | PDF via WeasyPrint | A4 | Cover page uses the `Cover` component. One pass through `tools/compress_pdf.py` if it's going in the free-starter-kit. |
| Worksheet / tracker (digital-first) | PDF A4 and a tall PNG preview for pins | PDF A4 + PNG 1000×1500 | The PNG preview goes to the pin pipeline. |
| Infographic on the website (inline) | HTML block in a post, OR 1200×800 JPG under `img/articles/<slug>.jpg` | 1200×800 | Light file; cards on the index/articles pages display it at 600×400. |
| Email header | HTML inlined in the MailerLite template, OR 1200×400 JPG | 1200×400 (shown at 600×200) | MailerLite scales on retina. Keep text at 32 px+. |
| Instagram post | PNG square | 1080×1080 | Keep 60-px safe-zone around the edges for the feed crop. |
| Instagram / Facebook story | PNG 9:16 | 1080×1920 | Nothing important in top 250 px (username strip) or bottom 350 px (reply bar). |
| Book interior section opener | PDF A4 via WeasyPrint | A4 | Use the existing `build85/` pipeline — don't fork it. |
| Logo variant / favicon | PNG at powers of two | 1024, 512, 256, 192, 32, 16 | Flatten the florals out for sizes under 64 px — only the central H&H mark survives. |
| Open Graph / social share image | JPG | 1200×630 | Already generated per-article by `tools/featured.py`. |

If the user hasn't named a format, ask once. If they're away, pick the one that fits the intent: "tracker" and "planner" and "checklist" are printables; "worksheet" is a printable; "badge" is a PNG; "email" is HTML; "story" is 1080×1920.

## The one unskippable rule: use the tokens

A design token is just a named value (`terracotta`, `space-5`). The whole point is that when the brand shifts, one edit propagates. Four rules:

1. **Every colour is a token** — never a literal hex pulled from memory. Even "white" is `--surface-raised` (which is `#FFFFFF` in cream mode and `#2A241B` in night mode). Writing `color: #FBF5EC` instead of `var(--surface)` is how brands drift.
2. **Every font-size is a type style** — `hero`, `title`, `chapter`, `quote`, `lead`, `body`, `small`, `button`, `kicker`. If you need a size that doesn't exist, that's a signal to pick the closest style, not to invent a new one.
3. **Every spacing is a step** — `space-1` through `space-12`. Random `padding: 22px` reads as "someone else designed this".
4. **Every component is reused** — if you need a pill button, use `BrandButton`. If you need a numbered-step card, lift the CSS from `PinCard`. If you need an article opener on the page, use `ArticleHero`.

The rare valid exception: an asset that commits to a single visual world (a Ramadan night sky, a letterpress cover for a one-off gift). Then override with care, keep contrast legal, and note the exception in the delivery message.

## The three building engines

Pick the right one — don't switch mid-piece.

### 1. HTML → PDF with WeasyPrint (preferred for printables)

The existing book pipeline is here: `/home/claude/build85/` on this environment, with `build.py`, `style.css`, `bg-left.svg`, `bg-right.svg`. It prints at the right size with proper margins and bleed. For a one-page printable, write a small standalone HTML that imports the same `@font-face` rules and matching tokens in `:root`, then call WeasyPrint directly. The template at `templates/printable-a4.html` is a known-good starting point.

Why it's the default: WeasyPrint respects page breaks, hyphenation and `@page` size, so it produces genuinely printable PDFs that look identical on the mom's printer. Don't use canvas-to-PDF for printables.

### 2. HTML → PNG with Playwright (for pins' siblings, badges, social graphics)

The script is at `/home/claude/pinskill/render.js`: `node render.js <in.html> <out.png> [width] [height]`. The HTML uses the same fonts via `file://` paths. Write to `/home/claude/quratulean.github.io/img/<descriptive-name>.jpg` (convert PNG → JPG for file size if it's a flat design), commit to the repo, and reference the public URL `https://quratulean.github.io/img/<name>.jpg`.

Why not use Canva here: the whole point of these designs is that they're generated from the design system in code, so when a token changes you re-render and ship. Canva breaks that loop.

### 3. HTML, inline, served from the site (for infographics in articles, email headers, interactive widgets)

For anything that lives in a page, write real HTML/CSS in the article markdown or the template. This stays accessible, searchable and SEO-friendly, and it participates in the site's light/dark theming when that comes.

Canva is reserved for cases the owner explicitly asks for it (so she can tweak later) or where motion requires it.

## Workflow for any new design

1. **Confirm the brief in one line** — "A single-page salah tracker, A4 PDF, kids colour in a star after each prayer". If any of {format, audience, text content} is missing, ask one short question.
2. **Load the design system** (above). Specifically read the tokens and any component README you expect to reuse.
3. **Sketch the layout in words** before HTML — hero, body, footer; grid of 7×5 cells; cover page + tracker page + reward page. It costs a sentence and prevents reworking a rendered PDF.
4. **Write the HTML from `templates/printable-a4.html`** (printable), `templates/social-1080.html` (square social), `templates/email-header.html` (email), or the matching `pinskill` template (PNG-rendered graphic). Adjust the body — never the `:root` tokens inside the template.
5. **Render once** (PDF or PNG).
6. **Look at it** with the Read tool to view the output file, or open the PDF to the first page. Fix anything the glance catches: overflow, cramped text, contrast failures, ornaments covering content, missing brand strip.
7. **Deliver** by sending the file (`SendUserFile`) with one sentence of context and the link to the design system artifact so the owner can check it against the brand book if she wants.
8. **Commit any reusable asset to the repo**: a tracker PDF goes to `printables/`, a badge PNG to `img/badges/`, an infographic JPG to `img/articles/`. Push.
9. **Update CLAUDE.md's "Design decisions" list** when you introduce a new reusable asset or make an intentional brand exception.

## Writing the copy

The design makes it look right. The copy makes it worth saving. Use **The Wise Older Sister** voice (brand-book README). Specifics:

- Open with a real moment or a specific promise ("A gentle salah tracker that doesn't shame"), not a category label ("Salah Tracker for Kids").
- One job per asset. A tracker tracks. A certificate celebrates. A worksheet works through one question. Don't stuff three things onto a printable to "add value" — it reads as cluttered.
- Qur'an and hadith get full attribution (verse number or book + grade). On contested fiqh/aqidah stay neutral and point to a qualified scholar.
- Credit: every asset ends with "Islamic Parenting 101 · quratulean.github.io" in `pin-brand` or `kicker` style.
- The book plug goes once on a multi-page asset, never on a one-pager.

## Accessibility & legibility

Printables are read by tired adults in low light and by kids learning to read. Hold the line on these:

- Body text no smaller than 14 pt (≈19 px). Numbered circles with text inside: 24 pt min.
- Contrast: body text passes 4.5:1 on its background in the cream palette (dark palette is for screens only — don't design a printable in dark mode).
- Arabic text: use the `arabic` font family from tokens, direction `rtl`, line height ≥ 1.9, size ≥ 22 pt. Always paired with an English transliteration and translation.
- Never rely on colour alone to convey state — pair red/green with icons or shapes.
- Focus rings on any interactive HTML output use the `focus` token (2 px, 2 px offset).

## Deliverables and where they live

| Asset | Lives at | Why |
|---|---|---|
| Printable PDFs for download | `printables/<slug>.pdf` in the repo, linked from `printables.html` | Public URL; the mom clicks and gets it. |
| Free lead-magnet PDFs | `gift/<slug>.pdf`, delivered via MailerLite welcome email | Not linked from the public site. |
| Website images | `img/<name>.jpg` or `img/articles/<slug>.jpg` | Served by GitHub Pages. |
| Logo variants | `img/logos/<name>.png` | Includes favicons, email headers, badges. |
| Design system (source of truth) | Claude design-system artifact "Islamic Parenting 101" | Tokens + components live there, not in a stray file. |

After writing to the repo, commit and push so the asset has a public URL the pin pipeline, the welcome emails and the book page can all reach.

## When to break the rules

The brand is a tool, not a cage. One genuine reason to break a rule: the asset needs something the system doesn't yet cover (a new icon set for Ramadan night-sky worksheets, a dark palette for a Qur'an-recitation night-mode widget). When that happens: name the exception, use it only for that asset, and propose adding it to the design system in your delivery message so the next asset doesn't have to invent it again.

## Templates

- `templates/printable-a4.html` — single-page A4 printable with the brand `:root` tokens, Playfair headline, Lato body, cream background, bottom brand strip, optional corner florals.
- `templates/social-1080.html` — 1080×1080 square (Instagram feed).
- `templates/email-header.html` — 600×200 header (renders fine at 1200×400 retina).

Copy a template, edit the body, render with the matching engine. Don't touch the `:root` block unless the design system itself changes.
