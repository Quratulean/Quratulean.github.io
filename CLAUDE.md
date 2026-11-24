# Islamic Parenting 101 — project handoff for Claude Code

Owner: Tabasum Majeed. Goal: sell the book *Hearts Before Habits* (Islamic parenting, for Muslim mothers) and grow Pinterest (digitalallio428) + this blog (https://islamicparenting101.com — custom domain since 2026-11-24 via `CNAME`; old https://quratulean.github.io redirects; GitHub Pages from `main`).
Working rule from the owner: do everything online; don't pile files on her computer. Never enter her passwords; she handles sign-ups/verification clicks/CAPTCHAs.

## Skills (in .claude/skills/)
- `islamic-parenting-blog` — write/publish ~2,000-word SEO articles (read `docs/blog-content-plan.md` first).
- `pinterest-project-manager` — status, weekly report, pin pipeline, posting to Pinterest.
- `pinterest-viral-pins` — design pins (render.js / animate.js).
- `islamic-parenting-design` — design any non-pin visual (printables, trackers, worksheets, badges, certificates, infographics, email headers, social graphics, logo variants), using the published "Islamic Parenting 101" design system. Templates in its `templates/`.
- `islamic-parenting-seo` — keyword research, on-page audit (one-command checker inside), technical SEO, domain move steps, Pinterest SEO, AdSense/affiliate readiness.

## Site system
- Articles live in `posts/<slug>.md` (front matter: title, description, date, kicker, type: pillar|cluster, pillar: <slug>, keywords).
- Images: `python3 tools/featured.py [slug]` draws each article's featured image (`img/articles/<slug>.jpg`, 1200x800, used on cards, article top and og:image) and a tall Pinterest version (`pins/<slug>.jpg`, 1000x1500, used by "Save to Pinterest"). New article → add its headline + icon to `ART` in that script, run it, then publish.py. Needs `pip install markdown` and Playwright.
- Build (always this order): `python3 tools/publish.py` (articles, sitemap, robots, articles.json) → `python3 tools/pages.py` (free-starter-kit, thank-you, contact) → `python3 tools/blog.py` (blog home index.html, Blog page articles.html with search + topic filter, topic-*.html pages, feed.xml RSS) → `python3 tools/site.py` (privacy, disclaimer, terms, resources = Amazon affiliate page, 404, shared footer, AdSense/GA head block, ads.txt). Then commit + push to `main`.
- Money switches live in `tools/site.json`: `adsense_client` (ca-pub-…), `amazon_tag` (Associates id), `ga4_id`, `shop_url`. Empty = off. Fill in when the owner's accounts are approved, rebuild, push.
- Own domain: the scripts read `CNAME`. Only add `CNAME` after DNS points to GitHub Pages (steps in the SEO skill).
- Voice: "The Wise Older Sister"; tagline *Heart first. Habit second.* Only well-attributed Quran/hadith; contested fiqh/aqidah neutral; "ask a qualified scholar".
- 14 articles live (4 pillars + 10 clusters). 12 are ~1,000–1,300 words and still need expanding to ~2,000 (same slugs). Status table: `docs/blog-content-plan.md`.

## Forms and email
- Email sign-up: MailerLite (account 2818911, embed form `JjOyLM`, group "Starter Kit") — `forms.js` + `tools/pages.py`.
- Contact form: Formspree `https://formspree.io/f/mljbopga` (messages go to quratt428@gmail.com).
- Free gift PDF: `gift/calm-mama-starter-kit.pdf` (source was /home/claude/gift/kit.py — not in repo).
- Welcome automation "Welcome Series - Calm Mama Starter Kit" is ACTIVE in MailerLite (4 emails: day 0, 2, 4, 7). Sender: islamicparentingresearchteam@gmail.com (verified).
- Double opt-in is OFF on the "Free Starter Kit" form (2026-11-24, owner request) so the welcome email sends immediately; reCAPTCHA stays on. Form redirect URL = https://quratulean.github.io/thank-you.html (PDF download there). Live test confirmed: welcome email arrives (lands in Gmail Promotions, which is normal for a Gmail sender; a custom-domain sender later will help).
- Earlier test sign-ups that stayed "unconfirmed" will not get the series; re-sign-up fixes it.

## Accounts
- Pinterest digitalallio428 — **Business account**, display name "Islamic Parenting 101 | Hearts Before Habits", website quratulean.github.io **claimed** (p:domain_verify meta already inserted by tools/publish.py and tools/pages.py; content "7ef4da08a9bc8f1ef568d82c019d2f69"). Profile logo: `img/logo-v2.jpg` (the round H&H mark). 13 boards exist.
- GitHub Quratulean/Quratulean.github.io; GoDaddy: **islamicparenting101.com** registered 2026-11-24, expires 2027-11-24, auto-renew OFF (consider moving to Cloudflare Registrar before renewal), privacy on. DNS at GoDaddy: 4 A records @ → 185.199.108-111.153, CNAME www → quratulean.github.io (verified via dns.google); Canva connected.
- Zapier Pinterest connection: "digitalallio428 #2" (selected_api PinterestCLIAPI) — used by the pinterest-project-manager skill to post pins via `create_pin`.
- KDP: both formats submitted 2026-11-24, status "In review" (up to 72 h). Paperback $14.99 (8.5x11, standard color, 76 pp). Kindle $4.99 (70% royalty). Worldwide rights. No KDP Select. AI disclosure: texts "some sections, extensive editing"; cover one/few AI-generated images, minimal editing; tool "Claude"; translations none. Amazon buy link still MISSING until books go live.

## Brand / design system
- Published as a Claude design-system artifact titled "Islamic Parenting 101": tokens (cream #FBF5EC, terracotta #A8553F, mustard #D9A94A, sage #4F7358, blush #F3D9CF, dusty blue #4E7388, plus Playfair Display + Lato), the brand book (README), and components Cover / PinCard / ArticleHero / BrandButton. Any new output should reach for those tokens and components first.
- Round profile logo (H&H monogram) source: `img/logo-v2.jpg` (also uploaded to the design system under assets/Logos). Featured "Heart first. Habit second." cover pin: `img/pin-cover.jpg`.

## Pins posted (2026-11-24)
- "Teaching Salah by Age" — pin 943504190726399898, board Teaching Kids Salah & Quran, link /teaching-salah-by-age.html.
- "Heart First. Habit Second. Islamic Parenting 101" (brand cover pin) — pin 943504190726404005, board Hearts Before Habits Islamic Parenting Book, link / (home).
- Article pins (2026-11-24): "Ramadan with Kids" 943504190726405824 and "Teach Kids to Fast" 943504190726405830 (board Ramadan with Kids); "Gentle Parenting in Islam" 943504190726405837 (board Gentle Muslim Parenting). Posting works with Zapier `create_pin` (the raw POST /v5/pins request returned "Invalid request body").
- Scheduled task "Post daily Pinterest pin" (trig_01SkptkeMEhU4TnNWULzw7gc) runs daily ~10:17 Asia/Kolkata starting 2026-11-25 and posts the next unposted pin from a 13-pin queue (yelling, phrases, duas, quote, fajr, mama, quran, tantrums, burnout, allah, discipline, guide, phrases article pin), then idles. Idempotent: checks the board before posting.

## Paid product
- **Ramadan Family Planner & Kids Activity Pack** (19 pages, A4 + Letter, $7). Source: `tools/ramadan_pack.py <out_dir>` then `node tools/render_pack.js <out_dir>`. The PDFs are the product: NEVER commit them to this public repo; the owner uploads them to the shop (Payhip planned). Sales page `ramadan-planner.html` (built by `tools/site.py`); its buy button uses `shop_url` in `tools/site.json` (empty = "launching soon" → free kit sign-up). Previews in `img/shop/`. Ramadan articles show a promo box (publish.py).

## Open work
0. Money goal: $500 by 31 Dec 2026 — plan and owner actions in `docs/money-plan-december.md`.
0b. Domain follow-ups: owner ticks "Enforce HTTPS" in repo Settings → Pages once the certificate is ready; re-claim islamicparenting101.com on Pinterest (new p:domain_verify code needed — add it next to the old one in publish.py/pages.py); add the new domain to Google Search Console. The daily pin task still uses quratulean.github.io image/link URLs (they redirect).
1. (Done) MailerLite sign-up works end to end. Optional: add a "check Promotions/Spam" note on thank-you + sign-up pages (tools/pages.py).
2. Expand the 12 short articles to ~2,000 words.
3. When KDP shows the Amazon link: update book.html (replace "Coming soon on Amazon"), welcome email 4, the book promo pin (`img/pin-book.jpg`, not yet posted), and append to CLAUDE.md.
4. Google Search Console + sitemap submission; later, domain islamicparenting101.com.
5. Weekly Monday report (also a scheduled task in her Claude account) — now covers Pinterest analytics (unlock after a few weeks of data).

See `docs/` for the content plan and the Amazon sales outlook, and the project doc `claude/publishing-and-launch-status.md` for the live KDP state.
