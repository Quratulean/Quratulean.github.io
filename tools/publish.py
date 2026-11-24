#!/usr/bin/env python3
"""Publish blog posts for the Islamic Parenting 101 website.

Usage (from the repo root):  python3 tools/publish.py
- Converts every posts/<slug>.md (front matter + Markdown) into <slug>.html,
  using the site's own header/footer (copied from about.html) so design stays consistent.
- Keeps articles.json (registry of ALL articles, incl. hand-made ones) up to date.
- Rebuilds the article cards on index.html (latest 3) and articles.html (all, newest first)
  between the <!--CARDS--> and <!--/CARDS--> markers.
- Writes sitemap.xml and robots.txt.

Front matter keys (between --- lines at the top of the .md):
  title, description, date (YYYY-MM-DD), image (optional, path in repo e.g. img/pin-x.jpg),
  kicker (optional small label), keywords (optional, comma separated)
"""
import json, re, html, os, glob, datetime, urllib.parse
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SITE_URL = open('CNAME').read().strip() if os.path.exists('CNAME') else 'quratulean.github.io'
BASE = f'https://{SITE_URL}'
AUTHOR = 'Tabasum Majeed'
SIGNUP_FORM = '''<div class="ml-embedded" data-form="JjOyLM"></div>'''

def read_post(path):
    raw = open(path, encoding='utf-8').read()
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', raw, re.S)
    if not m:
        raise SystemExit(f'{path}: missing front matter')
    meta = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip().strip('"')
    for k in ('title', 'description', 'date'):
        if not meta.get(k):
            raise SystemExit(f'{path}: front matter needs {k}')
    meta['slug'] = os.path.splitext(os.path.basename(path))[0]
    return meta, m.group(2)

def shell():
    """Header (up to <main>) and footer (from </main>) of an existing page."""
    src = open('about.html', encoding='utf-8').read()
    head, rest = src.split('<main>', 1)
    _, foot = rest.split('</main>', 1)
    return head, foot

def set_meta(head, title, desc, img, url):
    t = html.escape(title); d = html.escape(desc)
    head = re.sub(r'<title>.*?</title>', f'<title>{t} — Islamic Parenting 101</title>', head, flags=re.S)
    head = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{d}">', head)
    head = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{t}">', head)
    head = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{d}">', head)
    head = re.sub(r'<meta property="og:image" content=".*?">', f'<meta property="og:image" content="{BASE}/{img}">', head)
    verify = '' if 'p:domain_verify' in head else '<meta name="p:domain_verify" content="7ef4da08a9bc8f1ef568d82c019d2f69"/>\n'
    head = head.replace('</head>', f'<link rel="canonical" href="{url}">\n<meta property="og:type" content="article">\n{verify}</head>', 1)
    head = re.sub(r' class=on', '', head)
    head = head.replace('<a href="articles.html">', '<a href="articles.html" class=on>', 1)
    return head

def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def build_post(meta, body_md, registry):
    md = markdown.Markdown(extensions=['extra', 'sane_lists', 'smarty'])
    body = md.convert(body_md)
    # ids on h2 for the table of contents
    toc = []
    def add_id(m):
        text = re.sub('<.*?>', '', m.group(1))
        i = slugify(text)[:60]
        toc.append((i, text))
        return f'<h2 id="{i}">{m.group(1)}</h2>'
    body = re.sub(r'<h2>(.*?)</h2>', add_id, body)
    words = len(re.sub('<.*?>', ' ', body).split())
    mins = max(1, round(words / 220))
    img = meta.get('image') or 'img/cover.jpg'
    url = f'{BASE}/{meta["slug"]}.html'
    date = datetime.date.fromisoformat(meta['date'])
    toc_html = ''
    if len(toc) >= 3:
        toc_html = '<nav class="toc"><b>In this article</b><ol>' + ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in toc) + '</ol></nav>'
    hero = (f'<figure class="feature"><img src="{meta["image"]}" alt="{html.escape(meta["title"])}" width="1200" height="800" fetchpriority="high"></figure>'
            if meta.get('image') else '')
    pin_img = f'pins/{meta["slug"]}.jpg' if os.path.exists(f'pins/{meta["slug"]}.jpg') else img
    pin = ('https://www.pinterest.com/pin/create/button/?' +
           urllib.parse.urlencode({'url': url, 'media': f'{BASE}/{pin_img}', 'description': meta['title']}))
    me = next((a for a in registry if a['slug'] == meta['slug']), {})
    pillar_slug = meta.get('pillar') if meta.get('type') != 'pillar' else None
    by = {a['slug']: a for a in registry}
    # related: same-pillar siblings first (and the pillar itself), then newest others
    fam = []
    if pillar_slug:
        fam = [by[pillar_slug]] if pillar_slug in by else []
        fam += [a for a in registry if a.get('pillar') == pillar_slug and a['slug'] != meta['slug']]
    elif meta.get('type') == 'pillar':
        fam = [a for a in registry if a.get('pillar') == meta['slug']]
    rest = [a for a in registry if a['slug'] != meta['slug'] and a not in fam]
    others = (fam + rest)[:3]
    top_box = ''
    if pillar_slug and pillar_slug in by:
        pa = by[pillar_slug]
        top_box = f'<p class="guidebox">Part of the guide: <a href="{pa["slug"]}.html">{html.escape(pa["title"])}</a></p>'
    hub = ''
    if meta.get('type') == 'pillar':
        kids = [a for a in registry if a.get('pillar') == meta['slug']]
        if kids:
            hub = '<section class="hub"><h2>More in this guide</h2><ul>' + ''.join(f'<li><a href="{a["slug"]}.html"><b>{html.escape(a["title"])}</b></a><br><span>{html.escape(a["description"])}</span></li>' for a in kids) + '</ul></section>'
    related = ''
    if others:
        related = '<section class="related"><h2>Keep reading</h2><div class="cards">' + ''.join(card(a) for a in others) + '</div></section>'
    promo = ('<div class="cta"><img src="img/shop/ramadan-planner.jpg" alt="Ramadan Family Planner"><div><b>Plan a calm, joyful Ramadan</b><p>19 printable pages: good-deeds calendar, fasting and salah trackers for kids, Quran tracker, du\'as, word search and more.</p><a class="btn" href="ramadan-planner.html">See the Ramadan Planner</a></div></div>' if 'ramadan' in meta['slug'] else '')
    signup = '<div class="signup" hidden><h3>Get the free Calm Mama Starter Kit</h3><p>4 printable cards for calmer days: phrases, Sunnah calm-down steps, a bedtime routine and a weekly planner.</p>' + SIGNUP_FORM + '</div>'
    schema = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": meta['title'],
                         "description": meta['description'], "datePublished": meta['date'],
                         "author": {"@type": "Person", "name": AUTHOR}, "image": f'{BASE}/{img}',
                         "mainEntityOfPage": url, "keywords": meta.get('keywords', '')}, ensure_ascii=False)
    crumbs = [("Home", BASE + "/"), ("Blog", BASE + "/articles.html")]
    if pillar_slug and pillar_slug in by:
        crumbs.append((by[pillar_slug]['title'], f'{BASE}/{pillar_slug}.html'))
    crumbs.append((meta['title'], url))
    schema = schema[:-1] + ', "breadcrumb": ' + json.dumps({"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]}, ensure_ascii=False) + '}'
    enc = urllib.parse.quote
    share = (f'<div class="share"><b>Share this post</b>'
             f'<a href="{html.escape(pin)}" target="_blank" rel="noopener">Pinterest</a>'
             f'<a href="https://wa.me/?text={enc(meta["title"] + " " + url)}" target="_blank" rel="noopener">WhatsApp</a>'
             f'<a href="https://www.facebook.com/sharer/sharer.php?u={enc(url)}" target="_blank" rel="noopener">Facebook</a>'
             f'<a href="mailto:?subject={enc(meta["title"])}&amp;body={enc(url)}">Email</a></div>')
    authorbox = ('<div class="authorbox"><img src="img/logo-v2.jpg" alt="" width="80" height="80" loading="lazy"><div><b>Written by Tabasum Majeed</b>'
                 '<p>Author of <i>Hearts Before Habits</i>. I share gentle, Sunnah-rooted help for Muslim moms — heart first, habit second. '
                 '<a href="about.html">About me</a> · <a href="articles.html">More posts</a></p></div></div>')
    main = f'''<article class="wrap art">
<div class="kick">{html.escape(meta.get("kicker", "ISLAMIC PARENTING"))}</div>
{top_box}<h1>{html.escape(meta["title"])}</h1>
<p class="byline">By {AUTHOR} · {date.strftime("%B %-d, %Y")} · {mins} min read <a class="pinit" href="{html.escape(pin)}" target="_blank" rel="noopener">Save to Pinterest</a></p>
{hero}{toc_html}
{body}
{share}
<p class="postnote">This article shares general guidance from the Quran and Sunnah for parents. It is not a religious ruling, or medical or psychological advice. For fiqh questions please ask a qualified scholar, and for health or development concerns please speak to a professional. <a href="disclaimer.html">Disclaimer</a></p>
{authorbox}
{hub}
{promo}
{signup}
<div class="cta"><img src="img/cover.jpg" alt="Hearts Before Habits book cover"><div><b>Want the full guide?</b><p>This article draws on <i>Hearts Before Habits</i> — a complete Islamic parenting guide with scripts, du'as, printables and a 30-day plan.</p><a class="btn" href="book.html">See the book</a> <a class="btn ghost" href="printables.html">Free printables</a> <a class="btn ghost" href="resources.html">Recommended books</a></div></div>
{related}
</article>
<script type="application/ld+json">{schema}</script>'''
    head, foot = shell()
    page = set_meta(head, meta['title'], meta['description'], img, url) + '<main>' + main + '</main>' + foot
    open(f'{meta["slug"]}.html', 'w', encoding='utf-8').write(page)
    return words

GUIDES = {'islamic-parenting-guide': 'Islamic Parenting', 'gentle-parenting-in-islam': 'Gentle Parenting',
          'teaching-salah-by-age': 'Salah & Quran', 'ramadan-with-kids': 'Ramadan'}

def card(a):
    img = (f'<img src="{a["image"]}" alt="" width="1200" height="800" loading="lazy">' if a.get('image')
           else '<div class="ph">☾</div>')
    guide = a.get('pillar') or a['slug']
    chip = GUIDES.get(guide, 'Islamic Parenting') + (' · Guide' if a.get('type') == 'pillar' else '')
    return (f'<a class="card" href="{a["slug"]}.html" data-guide="{guide}">{img}<div><span class="chip">{html.escape(chip)}</span>'
            f'<h3>{html.escape(a["title"])}</h3><p>{html.escape(a["description"])}</p><span class="more">Read the article →</span></div></a>')

def replace_cards(fname, items):
    s = open(fname, encoding='utf-8').read()
    new = '<!--CARDS--><div class="cards">' + ''.join(card(a) for a in items) + '</div><!--/CARDS-->'
    if '<!--CARDS-->' in s:
        s = re.sub(r'<!--CARDS-->.*?<!--/CARDS-->', lambda m: new, s, flags=re.S)
    else:  # first run: wrap the existing first cards block
        s = re.sub(r'<div class="cards">.*?</a></div>', lambda m: new, s, count=1, flags=re.S)
    open(fname, 'w', encoding='utf-8').write(s)

def main():
    registry = json.load(open('articles.json', encoding='utf-8')) if os.path.exists('articles.json') else []
    by_slug = {a['slug']: a for a in registry}
    posts = sorted(glob.glob('posts/*.md'))
    metas = []
    for p in posts:
        meta, body = read_post(p)
        if not meta.get('image') and os.path.exists(f'img/articles/{meta["slug"]}.jpg'):
            meta['image'] = f'img/articles/{meta["slug"]}.jpg'  # made by tools/featured.py
        by_slug[meta['slug']] = {k: meta[k] for k in ('slug', 'title', 'description', 'date') } | ({'image': meta['image']} if meta.get('image') else {}) | ({'type': meta['type']} if meta.get('type') else {}) | ({'pillar': meta['pillar']} if meta.get('pillar') else {})
        metas.append((meta, body))
    registry = sorted(by_slug.values(), key=lambda a: a['date'], reverse=True)
    for meta, body in metas:
        w = build_post(meta, body, registry)
        print(f'built {meta["slug"]}.html — {w} words')
    json.dump(registry, open('articles.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    # index.html, articles.html and topic pages are built by tools/blog.py
    pages = ['', 'book.html', 'articles.html', 'printables.html', 'free-starter-kit.html', 'contact.html', 'about.html'] + [a['slug'] + '.html' for a in registry]
    today = datetime.date.today().isoformat()
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         ''.join(f'  <url><loc>{BASE}/{p}</loc><lastmod>{today}</lastmod></url>\n' for p in pages) + '</urlset>\n'
    open('sitemap.xml', 'w').write(sm)
    open('robots.txt', 'w').write(f'User-agent: *\nAllow: /\nDisallow: /gift/\nDisallow: /thank-you.html\nSitemap: {BASE}/sitemap.xml\n')
    print(f'{len(registry)} articles in registry; cards, sitemap.xml, robots.txt updated')

if __name__ == '__main__':
    main()
