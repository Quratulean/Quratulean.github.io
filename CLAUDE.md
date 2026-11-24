# Islamic Parenting 101 — project handoff for Claude Code

Owner: Tabasum Majeed. Goal: sell the book *Hearts Before Habits* (Islamic parenting, for Muslim mothers) and grow Pinterest (digitalallio428) + this blog (https://quratulean.github.io, GitHub Pages from `main`).
Working rule from the owner: do everything online; don't pile files on her computer. Never enter her passwords; she handles sign-ups/verification clicks/CAPTCHAs.

## Skills (in .claude/skills/)
- `islamic-parenting-blog` — write/publish ~2,000-word SEO articles (read `docs/blog-content-plan.md` first).
- `pinterest-project-manager` — status, weekly report, pin pipeline, posting to Pinterest.
- `pinterest-viral-pins` — design pins (render.js / animate.js).

## Site system
- Articles live in `posts/<slug>.md` (front matter: title, description, date, kicker, type: pillar|cluster, pillar: <slug>, keywords).
- Build: `python3 tools/publish.py` (pages, sitemap, robots, articles.json) and `python3 tools/pages.py` (free-starter-kit, thank-you, contact). Then commit + push to `main`.
- Voice: "The Wise Older Sister"; tagline *Heart first. Habit second.* Only well-attributed Quran/hadith; contested fiqh/aqidah neutral; "ask a qualified scholar".
- 14 articles live (4 pillars + 10 clusters). 12 are ~1,000–1,300 words and still need expanding to ~2,000 (same slugs). Status table: `docs/blog-content-plan.md`.

## Forms and email
- Email sign-up: MailerLite (account 2818911, embed form `JjOyLM`, group "Starter Kit") — `forms.js` + `tools/pages.py`.
- Contact form: Formspree `https://formspree.io/f/mljbopga` (messages go to quratt428@gmail.com).
- Free gift PDF: `gift/calm-mama-starter-kit.pdf` (source was /home/claude/gift/kit.py — not in repo).
- Welcome automation "Welcome Series - Calm Mama Starter Kit" is ACTIVE in MailerLite (4 emails: day 0, 2, 4, 7). Sender: islamicparentingresearchteam@gmail.com (verified). Live sign-up test not yet confirmed.

## Accounts
- Pinterest digitalallio428 is a personal account; switch to free Business (owner action). Boards exist (8 new ones created 2026-11-23).
- GitHub Quratulean/Quratulean.github.io; GoDaddy (no domain yet; plan islamicparenting101.com later); Canva connected.
- Book buy link (Amazon) is MISSING — add to book.html and pins when KDP is live.

## Open work
1. Confirm MailerLite test sign-up end to end (confirm email → welcome email → PDF link).
2. Expand the 12 short articles to ~2,000 words; add Amazon link when live.
3. Post week-1 pins after owner approval (host images in repo `pins/` for a public URL).
4. Pinterest Business account; add website to profile; Google Search Console + sitemap.
5. Weekly Monday report (also a scheduled task in her Claude account).

See `docs/` for the content plan and the Amazon sales outlook.
