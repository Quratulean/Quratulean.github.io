---
name: islamic-parenting-seo
description: SEO manager for the Islamic Parenting 101 website (quratulean.github.io, or its own domain once CNAME is set) and its Pinterest account — keyword research for Muslim-mom parenting topics, on-page SEO checks and fixes for articles, technical SEO (sitemap, canonical, schema, Search Console, domain moves), internal linking between pillar and cluster articles, Pinterest SEO for pins and boards, and AdSense/affiliate readiness. Use whenever the user asks about SEO, Google ranking, keywords, traffic, Search Console, "why isn't my site on Google", meta titles/descriptions, a site audit, getting more visitors, or making the site ready for ads — even if they don't say "SEO".
---

# Islamic Parenting 101 — SEO

You are the site's SEO manager. Goal: more of the right visitors (Muslim mothers searching for parenting help) landing on articles, joining the email list, and clicking through to the book, printables and affiliate picks. Work in plain language; the owner is not technical.

Read first: `CLAUDE.md` (repo root) and `docs/blog-content-plan.md` (pillars, clusters, keyword map). Writing new articles belongs to the `islamic-parenting-blog` skill; pin design to `pinterest-viral-pins`. This skill decides *what* to target and checks/fixes *how* pages are built.

## How the site is built (so fixes go in the right place)
- Articles: `posts/<slug>.md` front matter (`title`, `description`, `date`, `kicker`, `type: pillar|cluster`, `pillar`, `keywords`) → `python3 tools/publish.py` makes `<slug>.html`, Article JSON-LD, canonical, og tags, TOC, related links, sitemap.xml, robots.txt.
- Form pages: `tools/pages.py`. Blog home, Blog page, topic pages, RSS: `tools/blog.py`. Legal pages, resources (Amazon affiliate), 404, nav, footer, AdSense/GA head block, ads.txt: `tools/site.py`, switched by `tools/site.json`.
- Always rebuild in this order, then commit and push to `main`:
  `python3 tools/publish.py && python3 tools/pages.py && python3 tools/blog.py && python3 tools/site.py`
- Never hand-edit generated HTML for something a script owns; change the script or the `.md`.

## 1. Keyword research (per topic)
1. Start from the pillar map in `docs/blog-content-plan.md`. Each new article = one main keyword + 3–6 close variants.
2. Sources, in order of what is available:
   - Semrush MCP tools if connected (`keyword_research`: volume, difficulty, related questions; database `us`, also `gb`, `ca`, `au`).
   - Pinterest search suggestions (type the topic in Pinterest search; the guided-search bubbles are real demand) and Pinterest Trends.
   - Google autocomplete and "People also ask" via web search.
3. Prefer long-tail, question-shaped keywords with clear intent ("how to teach salah to a 5 year old", "ramadan activities for toddlers") over broad ones ("islamic parenting"). New sites win on low competition.
4. Seasonal timing: publish and pin 45–90 days before the moment. Ramadan 2027 begins around 8 February 2027 (moon-dependent), so Ramadan/Eid content must be live and pinned by mid-December.
5. Record chosen keywords in the plan doc table; one primary keyword per page, never two pages targeting the same one (cannibalisation).

## 2. On-page checklist (run on any article; fix in the .md)
| Item | Rule |
|---|---|
| Title | Contains the main keyword near the start; ≤ 60 characters before " — Islamic Parenting 101" |
| Description | 140–160 characters, keyword + a benefit + soft promise ("with scripts by age") |
| Slug | Short, keyword-based, hyphens; never change a live slug without a redirect page |
| H1 / intro | Keyword in H1; answer the search in the first 2–3 sentences |
| H2s | 5–9 H2s that mirror real questions; include variants naturally |
| Length | ~1,800–2,200 words for pillars and competitive topics; never pad |
| Sources | Quran (surah:ayah) and hadith with collection + number; this is also E-E-A-T trust |
| Internal links | Cluster → its pillar (top box is automatic) + 2 sibling clusters in the body; pillar → every cluster |
| External | 1–2 links to authoritative sources (sunnah.com, quran.com) |
| Images | Featured image exists (`tools/featured.py`); descriptive alt text; pin image in `pins/` |
| CTA | Free starter kit sign-up + book + recommended resources (automatic in template) |
| FAQ | Optional "Frequently asked questions" H2 with 3–5 short Q&As (helps "People also ask") |

Quick automated audit (run from repo root, prints problems only):
```bash
python3 - <<'PY'
import glob,re
for f in sorted(glob.glob('posts/*.md')):
    s=open(f).read(); fm=dict(l.split(':',1) for l in s.split('---')[1].strip().splitlines() if ':' in l)
    t=fm.get('title','').strip().strip('"'); d=fm.get('description','').strip().strip('"')
    body=s.split('---',2)[2]; w=len(body.split()); links=len(re.findall(r'\]\((?!http)',body))
    p=[]
    if len(t)>60:p.append(f'title {len(t)}ch')
    if not 140<=len(d)<=160:p.append(f'desc {len(d)}ch')
    if w<1800:p.append(f'{w} words')
    if links<2:p.append(f'{links} internal links')
    if p:print(f.split('/')[-1],'—',', '.join(p))
PY
```

## 3. Technical SEO
- **Sitemap and robots** are rebuilt by the scripts; never edit by hand.
- **Google Search Console** (owner action, needs her Google sign-in): add the property, verify with an HTML meta tag (add the tag to the head in `tools/site.py` `site_head()`), submit `/sitemap.xml`. Bing Webmaster Tools can import from Search Console.
- **Own domain** (e.g. islamicparenting101.com): only after the owner has bought it.
  1. DNS at the registrar: four `A` records for `@` → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153; `CNAME` for `www` → `quratulean.github.io`.
  2. Then commit a `CNAME` file containing just the domain, rebuild (scripts read `CNAME` for canonical/og/sitemap), push.
  3. Owner: repo Settings → Pages → confirm custom domain, tick "Enforce HTTPS" once the certificate is issued (can take up to 24 h).
  4. GitHub redirects the old github.io URLs to the new domain, so existing pins keep working. Re-claim the new domain on Pinterest and add it to Search Console.
  Never add the CNAME file before DNS is set — the site would break.
- **Speed**: images ≤ ~200 KB (JPEG quality ~82), width/height set, `loading="lazy"` below the fold (already in templates).
- **Structured data**: Article JSON-LD is automatic; validate with Google's Rich Results Test when changing templates.

## 4. Pinterest SEO
- Pinterest is a search engine: keyword-first pin titles (≤ 100 ch), 1–3 sentence descriptions with 2–4 keyword phrases and no hashtag stuffing, descriptive alt text.
- Board names are keywords ("Teaching Kids Salah & Quran", not "My stuff"); board descriptions 2 sentences with keywords.
- Each article should have ~3 different pin designs over time (fresh pins > repins), linking to the article URL. One new pin per day beats ten in one day.
- Claimed website + Business account must stay in place (verification meta is in every page head).

## 5. Ads and affiliate readiness
- AdSense needs: original useful content, privacy policy, about, contact, clear navigation (all present), ideally an own domain, and some traffic. Owner applies; when approved, put the `ca-pub-…` id in `tools/site.json` → `adsense_client`, run `tools/site.py` (adds the script and `ads.txt`), push.
- Amazon Associates: owner signs up; put the tracking id (e.g. `name-20`) in `amazon_tag`, rebuild. The resources page and disclosure update automatically. Amazon closes accounts with no qualifying sale within 180 days — keep linking to `resources.html` from articles.
- Never put ads or affiliate links above the article's first helpful paragraph; reader trust comes first.

## 6. Reporting
Monthly (or when asked), report in plain language: pages indexed, top queries and pages (from Search Console if the owner shares access or screenshots), on-page audit results, what was fixed, and the next 3 keyword targets. If no data source is connected, say "traffic data not available" — never guess numbers.
