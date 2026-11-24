# Islamic Parenting 101 — Blog Content Plan (v1, 23 Nov 2026)

Site: https://quratulean.github.io · Author: Tabasum Majeed · Goal: help Muslim moms → Pinterest traffic → book *Hearts Before Habits* + free printables.

## 1. How the keywords were chosen
- Method: live search-result review for each topic (who ranks, what angle they take, what's missing), plus how moms phrase problems (question-style, "how to…", by age, by situation).
- Honest limit: no paid keyword tool is connected, so exact monthly volumes are NOT known. Priorities below are based on (a) topic demand seen across top results, (b) low competition angle (practical + scripts + Sunnah), (c) Pinterest seasonality. Validate after 4–6 weeks with Pinterest Analytics / Google Search Console and re-rank.
- Gap we exploit: top results are either scholarly (long Q&A, few practical steps) or generic parenting lists with a Muslim label. Nobody owns **"practical scripts + Sunnah + warm voice"**. That is our lane.

## 2. Signature voice — "The Wise Older Sister"
- Tagline: **Heart first. Habit second.** (from the book's idea)
- Sounds like: warm, honest, practical, never guilt-tripping; an older sister who has been through it and is not a scholar.
- Always: open with a mom's real moment (2–3 sentences, present tense); short paragraphs; "you"; real scripts in quotes; a **"Try this tonight"** tip box; a table of "Instead of… / Try saying…" or "By age" where it fits; one honest "when it's harder" paragraph (counselor/doctor/scholar referral); close with **"Your one step this week"**; soft book/printable mention once.
- Never: shame, perfection language, fear-based religious pressure, "in today's fast-paced world", invented hadith/statistics, fiqh rulings stated as settled.
- Religious accuracy: Quran by Surah:ayah; hadith by collection; weak/disputed narrations flagged or left out; "ask a qualified scholar" for rulings.

## 3. Pillar → cluster map (hub-and-spoke)
Each pillar ≈ 2,200–2,600 words, targets the broad head term, links to every cluster. Each cluster ≈ 1,800–2,200 words, targets one long-tail term, links up to its pillar + 2 siblings + book/printable.

### Pillar A — Islamic Parenting (the complete guide)  `islamic-parenting-guide`
Head keyword: islamic parenting · related: how to raise muslim children, tarbiyah, parenting in islam, muslim parenting tips
Clusters:
- phrases-every-child-needs-to-hear — 10 phrases every child needs to hear (existing, expand)
- teach-kids-about-allah — how to teach kids about Allah (love, not fear)
- muslim-mom-burnout — Muslim mom burnout & self-care
- daily-duas-for-kids — daily duas for kids (morning, food, sleep, travel)

### Pillar B — Gentle Parenting in Islam  `gentle-parenting-in-islam`
Head keyword: gentle parenting in islam · related: islamic discipline, positive parenting islam, prophet muhammad ﷺ with children
Clusters:
- how-to-stop-yelling-at-your-kids — 7 Sunnah steps (existing, live)
- how-to-discipline-a-child-in-islam — discipline without hitting or shaming
- toddler-tantrums-islamic-parenting — big feelings, ages 1–4

### Pillar C — Teaching Kids Salah  `teaching-salah-by-age`  (existing slug, expand)
Head keyword: how to teach kids salah · related: teach child to pray, salah for kids by age, age 7 prayer
Clusters:
- get-kids-up-for-fajr — Fajr without fights
- teach-quran-to-kids-at-home — Quran at home, any age
- (cross-link) daily-duas-for-kids

### Pillar D — Ramadan with Kids  `ramadan-with-kids`  (existing slug, expand)
Head keyword: ramadan with kids · related: ramadan activities for kids, ramadan for toddlers, ramadan kindness calendar
Clusters:
- teach-kids-to-fast-ramadan — gradual fasting by age
- (cross-link) get-kids-up-for-fajr, daily-duas-for-kids, printables.html

(Later waves: Eid, Dhul Hijjah/Qurbani, back-to-school, teens & hijab talk, bedtime routine, sibling rivalry, screen time, Islamic names, new Muslim parents.)

## 4. Keyword map (primary · secondary · intent)
| Slug | Primary keyword | Secondary keywords | Intent |
|---|---|---|---|
| islamic-parenting-guide | islamic parenting | how to raise muslim children, tarbiyah, muslim parenting tips | Learn / pillar |
| gentle-parenting-in-islam | gentle parenting in islam | islamic discipline, positive parenting islam | Learn / pillar |
| teaching-salah-by-age | how to teach kids salah | teach child to pray, salah by age, prayer at age 7 | How-to / pillar |
| ramadan-with-kids | ramadan with kids | ramadan activities for kids, ramadan for toddlers | Seasonal / pillar |
| how-to-stop-yelling-at-your-kids | how to stop yelling at your kids | anger in islam, calm parenting | Problem-solving |
| how-to-discipline-a-child-in-islam | how to discipline a child in islam | islamic discipline without hitting, time out islam | Problem-solving |
| toddler-tantrums-islamic-parenting | toddler tantrums islam | big emotions toddler muslim | Problem-solving |
| get-kids-up-for-fajr | get kids up for fajr | child fajr prayer, fajr routine | Problem-solving |
| teach-quran-to-kids-at-home | teach quran to kids at home | quran for children, learn quran kids | How-to |
| daily-duas-for-kids | daily duas for kids | dua before eating kids, sleeping dua children | List / printable |
| teach-kids-to-fast-ramadan | how to teach kids to fast | kids fasting ramadan age, practice fast | Seasonal how-to |
| teach-kids-about-allah | how to teach kids about allah | explain allah to child, love of allah | How-to |
| muslim-mom-burnout | muslim mom burnout | self care muslim mothers, mom guilt islam | Support |
| phrases-every-child-needs-to-hear | phrases every child needs to hear | words of affirmation kids islam | List / shareable |

## 5. Internal-linking rules (enforced by tools/publish.py)
1. Every cluster has `pillar:` in front matter → shows a "Part of the guide" box at the top and a link to the pillar.
2. Every pillar lists all its clusters automatically ("In this guide") and links to each in-text.
3. "Keep reading" = siblings in the same pillar first, then newest.
4. In the body: each article links to its pillar once (descriptive anchor, not "click here"), 2 sibling articles where natural, `book.html` once, `printables.html` when relevant.
5. Never leave an orphan: every new article must be linked from its pillar and at least 2 others.
6. Never change a published slug; add a redirect page if one must move.

## 6. Cadence & seasonal calendar
- Now–Dec: publish waves 1–2 (pillars + clusters). 
- Weekly after: 2 new cluster articles + 1 refresh of an older article (add internal links, update date if materially changed).
- Pinterest: every article gets 3 pin designs (different hooks), posted over 3 weeks; pins link to the article, never the homepage.
- Seasonal: Ramadan 2027 is expected around early–mid February 2027 (moon sighting decides), so Ramadan pins should start by late December; Eid article + printable by mid-Jan; Dhul Hijjah/Qurbani wave in spring; back-to-school wave in July.
- Monthly review (first Monday): top articles by outbound clicks, saves; update titles/pins of the 3 weakest; plan next month's 8 topics.

## 7. Article checklist (quality gate)
Main keyword in title, first 100 words, one H2, description · 1,900–2,500 words · scripts + a table + tip box · accurate sources · pillar link + 2 siblings + book once · "Your one step this week" · phone + desktop render check · tracker updated.
