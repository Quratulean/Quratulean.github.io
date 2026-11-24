#!/usr/bin/env python3
"""Blog front-end for Islamic Parenting 101. Run after publish.py and pages.py, before site.py:
    python3 tools/publish.py && python3 tools/pages.py && python3 tools/blog.py && python3 tools/site.py

Builds from articles.json:
- index.html      blog home: featured post, latest posts, sidebar (author, free kit, Ramadan planner, book, topics)
- articles.html   "Blog": every post with search + topic filter
- topic-<name>.html  one page per topic (Islamic Parenting, Gentle Parenting, Salah & Quran, Ramadan)
- feed.xml        RSS feed (Pinterest can auto-pin new posts from it)
and adds the topic pages to sitemap.xml.
"""
import datetime, html, json, os, re
from email.utils import format_datetime

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOMAIN = open('CNAME').read().strip() if os.path.exists('CNAME') else 'quratulean.github.io'
BASE = f'https://{DOMAIN}'
REG = json.load(open('articles.json', encoding='utf-8'))  # newest first
TOPICS = [  # (pillar slug, name, file, blurb)
    ('islamic-parenting-guide', 'Islamic Parenting', 'topic-islamic-parenting.html', 'Raising children who love Allah: foundations, faith, du\'as and everyday habits from the Quran and Sunnah.'),
    ('gentle-parenting-in-islam', 'Gentle Parenting', 'topic-gentle-parenting.html', 'Discipline without yelling or shaming: calm, firm, Prophetic ways through tantrums, anger and hard days.'),
    ('teaching-salah-by-age', 'Salah & Quran', 'topic-salah-and-quran.html', 'Teaching prayer and Quran with love, from toddlers on the prayer mat to Fajr with teens.'),
    ('ramadan-with-kids', 'Ramadan', 'topic-ramadan.html', 'Making Ramadan joyful for children: traditions, first fasts and a calm family plan.'),
]
TNAME = {t[0]: t[1] for t in TOPICS}
TFILE = {t[0]: t[2] for t in TOPICS}


def topic_of(a):
    return a.get('pillar') or a['slug']


def mins(a):
    s = open(f'{a["slug"]}.html', encoding='utf-8').read()
    m = re.search(r'(\d+) min read', s)
    return int(m.group(1)) if m else 5


def date_txt(a):
    return datetime.date.fromisoformat(a['date']).strftime('%b %-d, %Y')


def shell():
    src = open('about.html', encoding='utf-8').read()
    head, rest = src.split('<main>', 1)
    _, foot = rest.split('</main>', 1)
    return head, foot


def page(fname, title, desc, body, on='articles.html'):
    head, foot = shell()
    t, d = html.escape(title), html.escape(desc)
    head = re.sub(r'<title>.*?</title>', f'<title>{t}</title>', head, flags=re.S)
    head = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{d}">', head)
    head = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{t}">', head)
    head = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{d}">', head)
    head = re.sub(r'<link rel="canonical" href=".*?">\n?', '', head)
    head = re.sub(r'<link rel="alternate" type="application/rss\+xml".*?>\n?', '', head)
    head = re.sub(r' class=on', '', head)
    head = head.replace(f'<a href="{on}">', f'<a href="{on}" class=on>', 1)
    url = BASE + '/' + ('' if fname == 'index.html' else fname)
    head = head.replace('</head>', f'<link rel="canonical" href="{url}">\n</head>', 1)
    open(fname, 'w', encoding='utf-8').write(head + '<main>' + body + '</main>' + foot)


def card(a, big=False):
    tp = topic_of(a)
    img = (f'<img src="{a["image"]}" alt="" width="1200" height="800" loading="{"eager" if big else "lazy"}">'
           if a.get('image') else '<div class="ph">☾</div>')
    search = html.escape((a['title'] + ' ' + a['description']).lower())
    return (f'<a class="card{" featured" if big else ""}" href="{a["slug"]}.html" data-guide="{tp}" data-text="{search}">{img}<div>'
            f'<span class="chip">{html.escape(TNAME.get(tp, "Islamic Parenting"))}</span>'
            f'<h3>{html.escape(a["title"])}</h3><p>{html.escape(a["description"])}</p>'
            f'<span class="meta">{date_txt(a)} · {mins(a)} min read</span></div></a>')


def sidebar():
    topics = ''.join(f'<li><a href="{f}">{html.escape(n)}</a><span>{sum(1 for a in REG if topic_of(a) == s)}</span></li>' for s, n, f, _ in TOPICS)
    popular = [a for a in REG if a.get('type') == 'pillar'][:4]
    pop = ''.join(f'<li><a href="{a["slug"]}.html">{html.escape(a["title"])}</a></li>' for a in popular)
    return f'''<aside class="side">
<div class="box author"><img src="img/logo-v2.jpg" alt="Islamic Parenting 101 logo" width="96" height="96" loading="lazy"><b>Assalamu alaykum, I'm Tabasum</b>
<p>I write gentle, Sunnah-rooted help for Muslim moms — less yelling, more connection, and children whose good habits grow from a loving heart.</p><a href="about.html">More about me →</a></div>
<div class="box gift"><span class="chip">Free gift</span><b>Calm Mama Starter Kit</b><p>4 printable cards for calmer days: phrases, Sunnah calm-down steps, a bedtime routine and a planner.</p><a class="btn" href="free-starter-kit.html">Get it free</a></div>
<div class="box"><span class="chip">New</span><a href="ramadan-planner.html"><img src="img/shop/ramadan-planner.jpg" alt="Ramadan Family Planner" width="1200" height="800" loading="lazy"></a><b>Ramadan Family Planner &amp; Kids Pack</b><p>19 printable pages to plan a calm, joyful Ramadan.</p><a href="ramadan-planner.html">See inside →</a></div>
<div class="box"><b>Topics</b><ul class="topics">{topics}</ul></div>
<div class="box"><b>Start here</b><ul class="pop">{pop}</ul></div>
<div class="box book"><a href="book.html"><img src="img/cover.jpg" alt="Hearts Before Habits book cover" loading="lazy"></a><b>Hearts Before Habits</b><p>The complete guide: the 4 C's, scripts, du'as and a 30-day plan.</p><a href="book.html">About the book →</a></div>
<div class="box"><a class="btn pinbtn" href="https://www.pinterest.com/digitalallio428/" target="_blank" rel="noopener">Follow on Pinterest</a></div>
</aside>'''


FILTERS = ('<div class="filters" role="group" aria-label="Filter posts by topic"><button class="on" data-f="all">All</button>'
           + ''.join(f'<button data-f="{s}">{html.escape(n)}</button>' for s, n, _, _ in TOPICS) + '</div>')

# ---------- home
HOME_SCHEMA = json.dumps({"@context": "https://schema.org", "@graph": [
    {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": "Islamic Parenting 101",
     "description": "A gentle Islamic parenting blog for Muslim moms.", "publisher": {"@id": BASE + "/#org"},
     "potentialAction": {"@type": "SearchAction", "target": BASE + "/articles.html?q={search_term_string}", "query-input": "required name=search_term_string"}},
    {"@type": "Organization", "@id": BASE + "/#org", "name": "Islamic Parenting 101", "url": BASE + "/",
     "logo": BASE + "/img/icon-512.png", "sameAs": ["https://www.pinterest.com/digitalallio428/"],
     "founder": {"@type": "Person", "name": "Tabasum Majeed"}}]}, ensure_ascii=False)
feat, rest = REG[0], REG[1:]
topic_tiles = ''.join(f'<a class="tile" href="{f}"><b>{html.escape(n)}</b><span>{html.escape(b)}</span></a>' for _, n, f, b in TOPICS)
page('index.html', 'Islamic Parenting 101 — A Gentle Islamic Parenting Blog for Muslim Moms',
     'A gentle Islamic parenting blog for Muslim moms: practical help from the Quran and Sunnah on salah, Ramadan, discipline without yelling, and raising children who love Allah.', f'''
<section class="bloghead"><div class="wrap"><div class="kick">THE BLOG FOR MUSLIM MOMS</div><h1>Heart first. Habit second.</h1>
<p class="lead">Gentle, practical Islamic parenting from the Quran and Sunnah — less yelling, more connection.</p></div></section>
<div class="wrap blog"><div class="main">
<h2 class="sec">Latest post</h2>{card(feat, big=True)}
<h2 class="sec">Recent posts</h2><!--CARDS--><div class="cards two">{''.join(card(a) for a in rest[:8])}</div><!--/CARDS-->
<p class="c"><a class="btn ghost" href="articles.html">See all {len(REG)} posts →</a></p>
<h2 class="sec">Browse by topic</h2><div class="tiles">{topic_tiles}</div>
<div class="signup" hidden><h3>Get the free Calm Mama Starter Kit</h3><p>4 printable cards for calmer days: phrases, Sunnah calm-down steps, a bedtime routine and a weekly planner.</p><div class="ml-embedded" data-form="JjOyLM"></div></div>
</div>{sidebar()}</div>
<script type="application/ld+json">{HOME_SCHEMA}</script>''', on='index.html')

# ---------- all posts
page('articles.html', 'Blog — Islamic Parenting 101', 'Every post on the Islamic Parenting 101 blog: gentle, Sunnah-rooted help for Muslim moms on salah, Quran, Ramadan, discipline and faith.', f'''
<section class="bloghead"><div class="wrap"><div class="kick">THE BLOG</div><h1>All posts</h1><p class="lead">Gentle, Sunnah-rooted help for everyday parenting moments.</p></div></section>
<div class="wrap blog"><div class="main">
<label class="search"><span class="sr">Search posts</span><input type="search" id="q" placeholder="Search posts — e.g. fajr, tantrums, Ramadan" autocomplete="off"></label>
{FILTERS}<p class="none" id="none" hidden>No posts match that yet. Try another word, or <a href="contact.html">ask me to write about it</a>.</p>
<!--CARDS--><div class="cards two">{''.join(card(a) for a in REG)}</div><!--/CARDS-->
</div>{sidebar()}</div>''')

# ---------- topic pages
for slug, name, fname, blurb in TOPICS:
    posts = [a for a in REG if topic_of(a) == slug]
    posts = [a for a in posts if a['slug'] == slug] + sorted([a for a in posts if a['slug'] != slug], key=lambda a: a['date'], reverse=True)
    page(fname, f'{name} — Islamic Parenting 101 Blog', f'{blurb} Posts for Muslim moms on {name.lower()}.', f'''
<section class="bloghead"><div class="wrap"><div class="kick">TOPIC</div><h1>{html.escape(name)}</h1><p class="lead">{html.escape(blurb)}</p></div></section>
<div class="wrap blog"><div class="main"><h2 class="sec">Start with the guide</h2>{card(posts[0], big=True)}
<h2 class="sec">More on {html.escape(name.lower())}</h2><div class="cards two">{''.join(card(a) for a in posts[1:])}</div>
<p class="c"><a href="articles.html">← All posts</a></p></div>{sidebar()}</div>''')

# ---------- RSS
items = ''
for a in REG[:20]:
    d = datetime.datetime.fromisoformat(a['date'] + 'T08:00:00+00:00')
    img = f'{BASE}/{a["image"]}' if a.get('image') else f'{BASE}/img/cover.jpg'
    items += (f'<item><title>{html.escape(a["title"])}</title><link>{BASE}/{a["slug"]}.html</link><guid>{BASE}/{a["slug"]}.html</guid>'
              f'<pubDate>{format_datetime(d)}</pubDate><category>{html.escape(TNAME.get(topic_of(a), "Islamic Parenting"))}</category>'
              f'<description>{html.escape(a["description"])}</description><enclosure url="{img}" type="image/jpeg" length="0"/></item>\n')
rss = (f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
       f'<title>Islamic Parenting 101</title><link>{BASE}/</link><atom:link href="{BASE}/feed.xml" rel="self" type="application/rss+xml"/>'
       f'<description>Gentle Islamic parenting for Muslim moms, from the Quran and Sunnah.</description><language>en</language>\n{items}</channel></rss>\n')
open('feed.xml', 'w', encoding='utf-8').write(rss)

# ---------- sitemap
sm = open('sitemap.xml', encoding='utf-8').read()
lastmod = re.search(r'<lastmod>(.*?)</lastmod>', sm).group(1)
for _, _, f, _ in TOPICS:
    if f'/{f}</loc>' not in sm:
        sm = sm.replace('</urlset>', f'  <url><loc>{BASE}/{f}</loc><lastmod>{lastmod}</lastmod></url>\n</urlset>')
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print(f'blog built: home, all posts, {len(TOPICS)} topic pages, feed.xml ({len(REG)} posts)')
