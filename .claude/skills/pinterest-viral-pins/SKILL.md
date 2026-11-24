---
name: pinterest-viral-pins
description: Research a niche and design scroll-stopping Pinterest pins in every format (standard 2:3, long infographic, square, carousel, video/idea pins) and every style (colorful infographic, illustrated, warm floral, quote, checklist, listicle, before/after, product or book mockup), then animate them into MP4 video pins, with SEO titles, descriptions, alt text and a posting plan. Use whenever the user wants Pinterest pins, pin templates, pin ideas, viral pins, Pinterest traffic or marketing, animated or video pins, or to promote a book, product, blog or shop on Pinterest — even if they just say "make pins" or "get me Pinterest traffic".
---

# Pinterest Viral Pins

Make pins that people save and click: researched topics, bold readable designs, keyword-rich copy, and optional animated versions — rendered as real PNG/MP4 files ready to upload.

## Workflow

1. **Understand the brief** (from the conversation; ask only what is truly missing):
   niche and audience, what the pin promotes (link, book, product, freebie, blog), brand colors/fonts or an existing cover/logo, how many pins, which formats.
   If the user has shared a product image (e.g. a book cover), use the real image in the pin — never redraw it as a fake mockup when the real thing is available.

2. **Research what works** (keep it fast; 3–6 searches, sent together):
   - WebSearch: `"<niche> pinterest ideas"`, `"<niche> pins" infographic`, `"pinterest trends <niche> <current year>"`, top blogs in the niche, seasonal hooks (holidays/events in the next 45–90 days — Pinterest users plan ahead, so seasonal pins should go out ~45 days early).
   - Pinterest pages and pin.it links usually block automated fetching. Don't fight it: rely on search snippets, blog articles that embed pins, and screenshots the user shares.
   - Extract: 10–20 search keywords people actually use, the recurring winning formats (numbered lists, checklists, "by age" charts, printables, quotes), common hooks, and gaps nobody fills well.
   - Summarize findings in 5–8 bullets before designing. Never copy another creator's pin, wording or artwork — learn the pattern, make something original.

3. **Plan the pins**: for each pin pick a *hook* + *format* + *style* (see tables below). Mix styles across a batch; vary the headline wording so pins aren't duplicates (Pinterest favors fresh pins).

4. **Design** each pin with one of the two engines below (Canva or code) following the Design rules.

5. **Animate** (when asked, or offer for 1–2 hero pins): add CSS keyframe animations to a code-built pin and render an MP4 with the animate script.

6. **Look at every render** before delivering (open the PNG / a frame strip). Fix overflow, cramped text, empty areas, low contrast.

7. **Write the copy** for every pin (format below) and, for batches, a posting schedule.

8. **Deliver**: send the PNG/MP4 files (and Canva edit links) plus a compact copy sheet (or a Sheet/Doc artifact for big batches). If a Pinterest connection (e.g. via Zapier) exists and the user asks to publish, confirm board, link and text with the user before posting — posting is public. Pinterest needs a public image URL: a fresh Canva PNG export URL works; a file that exists only in the workspace has to be uploaded by the user.

## Two design engines

**Canva (default for static pins when the Canva connector is available)** — the pin lands in the user's own Canva account, so they can tweak text, swap photos and reuse it as a template. Canva's generator adds illustrated icons and florals that look polished.
1. `create-design` with `format: "Pinterest Pin"` and a detailed `brief`: exact headline and every line of text, style (e.g. warm floral illustrated infographic), palette hex codes, fonts mood, CTA and brand line. Canva has no memory of earlier pins, so repeat brand details every time. If the user has a brand kit (`list-brand-kits`), pass `brand_kit_id`; pass `references` (asset/design ids) to include their book cover or logo.
2. Poll `get-create-design-async-job` with the latest `continuation_token`, waiting the `wait_seconds` it gives (about 30–60 s total).
3. Review with `read-design` (fields `design_content` + `thumbnails`): check every word for typos and accuracy, and look at the thumbnail. Fix with `edit-design` (or the canva edit-design skill if listed).
4. Other sizes: `resize-design` with custom width/height (1000×1500, 1000×2100, 1080×1920, 1000×1000) — creates a copy.
5. `export-design` as PNG (width 1000). The export returns a public download URL valid for a few hours — usable directly as the Pinterest `image_url` when posting. Share the Canva edit link with the user.
- The user's own images (book cover, logo) must already be in their Canva to be referenced. Uploading local files uses `create-upload-url` + an HTTP POST of the raw bytes (`curl -X POST -H "Content-Type: application/octet-stream" --data-binary @file "<upload_url>"`), which only works if the workspace can reach canva.com; if it's blocked, ask the user to upload the file to Canva once (or allow canva.com under Settings → Capabilities).
- Canva AI video (`create-video`) uses the user's Canva AI limit: before the first one in a conversation, give the heads-up its tool description requires and wait for a yes. For simple motion pins prefer the code engine.

**Code (HTML → PNG/MP4)** — full control, exact text, fast batches, and the only engine here for frame-exact animated pins. See Build kit below. Use it for animations, long infographics with lots of exact data, or when Canva isn't connected.

A good batch often mixes both: Canva for static pins the user may edit, code for the animated versions.

## Formats

| Format | Size (px) | Use |
|---|---|---|
| Standard pin | 1000×1500 (2:3) | default for everything |
| Long infographic | 1000×2100 (max ratio 1:2.1) | step-by-step guides, "by age" charts, checklists |
| Square | 1000×1000 | quotes, product shots (shows smaller in feed) |
| Video / idea pin | 1080×1920 (9:16) or 1000×1500 | animations, 6–15 s, MP4 H.264, loops well |
| Carousel | 2–5 slides, same ratio (1000×1500) | tips series, mini-lesson, before/after |
| Printable preview | 1000×1500 showing the printable on a tilted page | freebies / lead magnets |

Video safe zones: keep text out of the top ~12% and bottom ~20% (Pinterest overlays UI there) and away from the right edge.

## Styles (pick per pin, mix in a batch)

| Style | Recipe |
|---|---|
| Colorful infographic | numbered/colored blocks, icons or small illustrations per step, strong header band, 4–7 items |
| Illustrated / warm floral | SVG flowers, leaves, people/objects in flat style, soft palette, hand-drawn feel |
| Bold text overlay | huge 2–3 line headline, high-contrast band, minimal decoration — works for clicks |
| Quote | one short line, big serif type, decorative frame, small brand mark |
| Checklist / printable | ☐ boxes, cream paper look, "Save this checklist" |
| Listicle | "7 Ways to…" headline, list in cards |
| By-age / chart | table or timeline, color per row, perfect for long pins |
| Before / after or Do / Don't | split layout, red/green or two brand colors |
| Product / book promo | real product image large, 1 benefit line, CTA button |

## Design rules (what makes pins get saved)

- **Fill the canvas.** Empty space reads as unfinished; plain text-only pins underperform. Every pin needs at least one visual element: illustration, icon set, photo/product image, pattern, or colored blocks.
- **Readable on a phone thumbnail**: headline ≥ 70px on 1000px width, body ≥ 30px, max ~25 words of body text on a standard pin, contrast strong (dark on light or white on deep color).
- **Headline = hook + keyword**: "7 Gentle Ways to Teach Kids Salah", "Screen Time Rules by Age". Numbers, "how to", "by age", "mistakes", "printable" all pull.
- **One clear focal point** top-to-bottom: kicker → headline → visual/list → CTA/brand.
- **Brand**: small logo or website/handle at the bottom on every pin; consistent palette and 2 fonts across the batch.
- **CTA** that fits: "Save for later", "Free printable", "Get the guide".
- Draw illustrations as inline SVG (simple shapes: flowers = rotated ellipses round a circle; leaves = ellipses on a curved stem; people = circle head + rounded body). Avoid real people's faces or copyrighted characters/logos.
- Default palettes (override with brand): warm floral — cream #FBF5EC, terracotta #A8553F, mustard #D9A94A, sage #4F7358, blush #F3D9CF, dusty blue #4E7388, brown text #3B2A20. Bold — navy #1E2A47, coral #FF6B5B, yellow #FFC94A, white.

## Copy for each pin

```
Pin N — <style> / <format>
Title (≤100 chars, keyword first): ...
Description (250–500 chars, natural sentences with 3–5 keywords, ends with a CTA): ...
Alt text (what the image shows, ≤500 chars): ...
Board: ...   Link: ...   Keywords: kw1, kw2, kw3
```
No hashtag stuffing (0–3 max). Write like a helpful person, not a keyword list.

## Posting plan (for batches)

3–10 fresh pins per week beats dumping 50 at once. Spread pins for the same link over weeks with different designs. Schedule seasonal pins ~45 days early. Pin to the most relevant board first. Keep a simple calendar table: date · pin · board · link.

## Build kit

Work in a scratch folder. Fonts: Google Fonts may be blocked in sandboxes, so install fonts locally and reference the files:

```bash
npm i @fontsource/playfair-display @fontsource/lato   # any Google font: @fontsource/<name>
# files: node_modules/@fontsource/<name>/files/<name>-latin-<weight>-normal.woff2
```
```css
@font-face{font-family:'Playfair Display';font-weight:800;src:url(file:///ABS/PATH/node_modules/@fontsource/playfair-display/files/playfair-display-latin-800-normal.woff2)}
```

Pin HTML skeleton: `html,body{margin:0}` and one root `<div>` exactly the pin size (`width:1000px;height:1500px;overflow:hidden;position:relative`). Embed images with absolute `file://` paths or data URIs.

**render.js** — HTML → PNG (shows the final state of any animations):
```js
// node render.js pin.html out.png [width=1000] [height=1500]
const {chromium}=require('playwright');
(async()=>{const [,,src,out,w='1000',h='1500']=process.argv;
const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:1});
await p.goto('file://'+require('path').resolve(src));await p.evaluate(()=>document.fonts.ready);
await p.evaluate(()=>document.getAnimations().forEach(a=>{a.pause();const e=a.effect.getComputedTiming().endTime;a.currentTime=isFinite(e)?e:0}));
await p.screenshot({path:out});await b.close();})();
```

**animate.js** — HTML with CSS animations → MP4, frame-exact (steps every animation's clock, so timing is deterministic):
```js
// node animate.js pin.html out.mp4 [seconds=8] [width=1080] [height=1920] [fps=30]
const {chromium}=require('playwright');const fs=require('fs'),path=require('path'),{execSync}=require('child_process');
(async()=>{const [,,src,out,sec='8',w='1080',h='1920',fps='30']=process.argv;
const dir=fs.mkdtempSync('/tmp/frames-');const b=await chromium.launch();
const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:1});
await p.goto('file://'+path.resolve(src));await p.evaluate(()=>document.fonts.ready);
await p.evaluate(()=>document.getAnimations().forEach(a=>a.pause()));
const n=Math.round(+sec*+fps);
for(let i=0;i<n;i++){const t=i*1000/+fps;
 await p.evaluate(t=>document.getAnimations().forEach(a=>a.currentTime=t),t);
 await p.screenshot({path:`${dir}/f${String(i).padStart(5,'0')}.png`});}
await b.close();
execSync(`ffmpeg -y -loglevel error -framerate ${fps} -i ${dir}/f%05d.png -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -movflags +faststart ${out}`);
fs.rmSync(dir,{recursive:true});console.log('wrote',out);})();
```
Requires Playwright (`require('playwright')`) and ffmpeg; install if missing (`npm i playwright && npx playwright install chromium`).

### Animation recipes (CSS keyframes, staggered with `animation-delay`)

- Entrance: kicker → headline (0.3s) → list items one by one (every 0.4–0.6s) → CTA pop (last). Use `animation-fill-mode: both` so elements stay hidden before their turn.
- `@keyframes up{from{opacity:0;transform:translateY(40px)}to{opacity:1;transform:none}}`
- `@keyframes pop{from{opacity:0;transform:scale(.6)}to{opacity:1;transform:scale(1)}}`
- Ambient loops for life: flowers rotating slowly, leaves swaying (`rotate(-4deg)↔4deg`), gentle float (`translateY ±8px`), shimmer on a CTA.
- Typewriter headline: `steps()` on `width` with `overflow:hidden;white-space:nowrap`.
- Count-up numbers or progress bars for infographics (`width` 0→100%).
- Timing: total 6–12 s; finish all entrances by ~70% of the clip, then hold so the viewer can read; end frame should equal the static pin so it loops cleanly.
- Check: extract a frame strip (`ffmpeg -i out.mp4 -vf "select='eq(n\,15)+eq(n\,90)+eq(n\,200)',scale=250:-1,tile=3x1" -frames:v 1 strip.png`) and look at it.

## Quality check before delivering

- Text fully inside the canvas, nothing clipped, no lone word on a line in the headline.
- Repeated blocks line up (give fixed-width columns `flex:none` so rows don't shift).
- No big empty areas; visual element present.
- Readable at 25% size (resize and look).
- Facts, quotes and religious/medical claims are accurate and sourced; spelling consistent.
- Video: plays, correct size, text clear of safe zones, loops cleanly.
