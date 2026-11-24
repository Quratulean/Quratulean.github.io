#!/usr/bin/env python3
"""Site-wide pass for Islamic Parenting 101. Run LAST, after publish.py and pages.py:
    python3 tools/publish.py && python3 tools/pages.py && python3 tools/site.py

- Builds privacy.html, disclaimer.html, terms.html, resources.html (Amazon affiliate) and 404.html.
- Gives every page the same footer (with legal links) and the same <!--SITEHEAD--> block,
  which switches on Google AdSense / Google Analytics only when their ids are set in tools/site.json.
- Writes ads.txt when AdSense is set, and adds the new pages to sitemap.xml.
"""
import glob, html, json, os, re, urllib.parse

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CFG = json.load(open('tools/site.json', encoding='utf-8'))
DOMAIN = open('CNAME').read().strip() if os.path.exists('CNAME') else 'quratulean.github.io'
BASE = f'https://{DOMAIN}'
PIN = 'https://www.pinterest.com/digitalallio428/'
UPDATED = 'November 24, 2026'

FOOTER = f'''<footer><div class="wrap"><div class="fl"><img src="img/logo.png" alt=""><div><b>Islamic Parenting 101</b><br>Nurturing children's hearts before shaping their habits.</div></div>
<div class="fr"><a href="{PIN}" target="_blank" rel="noopener">Follow on Pinterest</a> · <a href="book.html">Hearts Before Habits</a> · <a href="printables.html">Free printables</a> · <a href="free-starter-kit.html">Free gift</a> · <a href="ramadan-planner.html">Ramadan Planner</a> · <a href="resources.html">Recommended</a> · <a href="contact.html">Contact</a></div>
<p class="sm legal"><a href="privacy.html">Privacy Policy</a> · <a href="disclaimer.html">Disclaimer &amp; Affiliate Disclosure</a> · <a href="terms.html">Terms of Use</a></p>
<p class="sm">© 2026 Tabasum Majeed · Islamic Parenting 101. This site shares general educational and spiritual guidance; it is not a substitute for professional or scholarly advice. As an Amazon Associate I earn from qualifying purchases.</p></div></footer>'''


def site_head():
    parts = []
    if CFG.get('adsense_client'):
        c = CFG['adsense_client']
        parts.append(f'<meta name="google-adsense-account" content="{c}">\n'
                     f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={c}" crossorigin="anonymous"></script>')
    if CFG.get('ga4_id'):
        g = CFG['ga4_id']
        parts.append(f'<script async src="https://www.googletagmanager.com/gtag/js?id={g}"></script>\n'
                     f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{g}');</script>")
    parts.append(f'<link rel="alternate" type="application/rss+xml" title="Islamic Parenting 101" href="{BASE}/feed.xml">')
    return '<!--SITEHEAD-->' + '\n'.join(parts) + '<!--/SITEHEAD-->'


def shell():
    src = open('about.html', encoding='utf-8').read()
    head, rest = src.split('<main>', 1)
    _, foot = rest.split('</main>', 1)
    return head, foot


def page(fname, title, desc, body, noindex=False, on=None, og=None):
    head, foot = shell()
    t, d = html.escape(title), html.escape(desc)
    head = re.sub(r'<title>.*?</title>', f'<title>{t} — Islamic Parenting 101</title>', head, flags=re.S)
    head = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{d}">', head)
    head = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{t}">', head)
    head = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{d}">', head)
    head = re.sub(r'<link rel="canonical" href=".*?">\n?', '', head)
    if og:
        head = re.sub(r'<meta property="og:image" content=".*?">', f'<meta property="og:image" content="{BASE}/{og}">', head)
    head = re.sub(r' class=on', '', head)
    if on:
        head = head.replace(f'<a href="{on}">', f'<a href="{on}" class=on>', 1)
    canon = f'<link rel="canonical" href="{BASE}/{fname}">\n' if not noindex else '<meta name="robots" content="noindex">\n'
    head = head.replace('</head>', canon + '</head>', 1)
    open(fname, 'w', encoding='utf-8').write(head + '<main>' + body + '</main>' + foot)


def amazon(query):
    q = {'k': query}
    if CFG.get('amazon_tag'):
        q['tag'] = CFG['amazon_tag']
    return 'https://www.amazon.com/s?' + urllib.parse.urlencode(q)


# ---------- legal pages
page('privacy.html', 'Privacy Policy', 'How Islamic Parenting 101 collects, uses and protects your information.', f'''
<section class="wrap art"><div class="kick">LEGAL</div><h1>Privacy Policy</h1><p class="sm">Last updated: {UPDATED}</p>
<p>Islamic Parenting 101 ({html.escape(DOMAIN)}) is run by Tabasum Majeed. This policy explains what information is collected when you visit, and how it is used. If you have questions, please use the <a href="contact.html">contact page</a>.</p>
<h2>Information you give us</h2>
<ul><li><b>Email sign-up.</b> When you request the free Calm Mama Starter Kit, your name (optional) and email address are stored by our email provider, <b>MailerLite</b>, so we can send you the kit and occasional emails. Every email has an unsubscribe link.</li>
<li><b>Contact form.</b> Messages sent through the contact form are delivered by <b>Formspree</b> and used only to reply to you.</li></ul>
<h2>Information collected automatically</h2>
<p>Like most websites, our host and the services below may receive basic technical information (such as your IP address, browser type and the pages you visit) and may use cookies or similar technologies.</p>
<ul><li><b>Advertising (Google AdSense).</b> We may show ads served by Google. Google and its partners use cookies to serve ads based on your visits to this and other websites. You can opt out of personalised advertising at <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google Ads Settings</a> or <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a>. Learn how Google uses data at <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">policies.google.com/technologies/partner-sites</a>.</li>
<li><b>Analytics.</b> We may use Google Analytics to understand which articles are helpful. It collects anonymous usage statistics using cookies.</li>
<li><b>Affiliate links.</b> Some links go to Amazon. If you click one, Amazon may set a cookie to credit the referral. See our <a href="disclaimer.html">Disclaimer &amp; Affiliate Disclosure</a>.</li>
<li><b>Embedded services.</b> Pages load fonts from Google Fonts and may include Pinterest "Save" buttons and MailerLite forms, which may receive your IP address.</li></ul>
<h2>How we use information</h2><p>To send the emails you asked for, reply to messages, improve the site, and keep it free through ads and affiliate links. We never sell your personal information.</p>
<h2>Your choices and rights</h2><p>You can unsubscribe from emails at any time, block or delete cookies in your browser, and ask us to access, correct or delete your personal information by writing through the <a href="contact.html">contact page</a>. Depending on where you live (for example the EU/UK under GDPR, or California under CCPA/CPRA), you may have additional rights, which we will honour.</p>
<h2>Children</h2><p>This website is written for parents. It is not directed at children under 13, and we do not knowingly collect personal information from children.</p>
<h2>Changes</h2><p>We may update this policy; the date at the top shows the latest version.</p></section>''')

page('disclaimer.html', 'Disclaimer & Affiliate Disclosure', 'Disclaimer and affiliate disclosure for Islamic Parenting 101.', f'''
<section class="wrap art"><div class="kick">LEGAL</div><h1>Disclaimer &amp; Affiliate Disclosure</h1><p class="sm">Last updated: {UPDATED}</p>
<h2>General and religious guidance</h2><p>Articles on this site share general educational and spiritual guidance for parents. They are not medical, psychological or legal advice, and they are not religious rulings (fatwa). For questions of fiqh, please ask a qualified scholar; for health, development or safety concerns, please speak to a qualified professional. Quran and hadith are quoted with their sources so you can check them.</p>
<h2>Affiliate disclosure</h2><p>Islamic Parenting 101 is a participant in the <b>Amazon Services LLC Associates Program</b>, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. <b>As an Amazon Associate I earn from qualifying purchases.</b> This costs you nothing extra. I only recommend things I believe are genuinely useful for Muslim families.</p>
<h2>Advertising</h2><p>This site may show ads from Google AdSense. Ads are chosen by Google, not by us, and showing an ad is not an endorsement.</p>
<h2>Our own products</h2><p>Links to <i>Hearts Before Habits</i> and any printables we sell are our own products.</p></section>''')

page('terms.html', 'Terms of Use', 'Terms of use for the Islamic Parenting 101 website and free printables.', f'''
<section class="wrap art"><div class="kick">LEGAL</div><h1>Terms of Use</h1><p class="sm">Last updated: {UPDATED}</p>
<p>By using this website you agree to these terms.</p>
<h2>Content</h2><p>All articles, images and printables are © Tabasum Majeed / Islamic Parenting 101 unless stated otherwise. You are welcome to share links and to pin our images to Pinterest. Please do not copy full articles or resell printables.</p>
<h2>Free printables</h2><p>Free printables are for personal, family, classroom and masjid-school use. They may not be sold, redistributed as files, or uploaded to other websites.</p>
<h2>No guarantees</h2><p>We work hard to be accurate, but content is provided "as is" without warranties. See the <a href="disclaimer.html">Disclaimer</a>.</p>
<h2>Links to other sites</h2><p>We are not responsible for the content or privacy practices of other websites we link to.</p>
<h2>Contact</h2><p>Questions about these terms: please use the <a href="contact.html">contact page</a>.</p></section>''')

# ---------- recommended resources (Amazon affiliate)
GROUPS = [
    ('For little hearts (ages 2–6)', [
        ('Islamic board books for toddlers', 'Short, colourful first books about Allah, the Prophets and good manners.', 'islamic board books for toddlers'),
        ('My first Quran stories', 'Gentle picture-book retellings of Quran stories for bedtime.', 'quran stories for kids picture book'),
        ('Kids prayer mat', 'A child-sized prayer mat so they can "pray with mama".', 'kids prayer mat islamic'),
    ]),
    ('For growing Muslims (ages 6–12)', [
        ('Prophet stories for kids', 'Chapter books with the stories of the Prophets.', 'stories of the prophets for kids book'),
        ('Salah learning tools', 'Wudu and salah step cards, posters and talking prayer mats.', 'salah learning cards for kids'),
        ('Islamic board games', 'Family games night with an Islamic twist.', 'islamic board game for kids'),
    ]),
    ('Ramadan & Eid with kids', [
        ('Ramadan countdown calendar', 'A daily countdown that builds excitement for Ramadan.', 'ramadan countdown calendar kids'),
        ('Ramadan activity books', 'Colouring, puzzles and good-deed trackers for the month.', 'ramadan activity book for kids'),
        ('Ramadan lanterns & decor', 'Lights and lanterns to make the home feel like Ramadan.', 'ramadan lantern decoration'),
    ]),
    ('For you, mama', [
        ('Islamic parenting books', 'More reading on raising children with the Quran and Sunnah.', 'islamic parenting book'),
        ("Du'a journal", 'A journal to write your du\'as for your children.', 'islamic dua journal'),
    ]),
]
cards = ''
for title, items in GROUPS:
    cards += f'<h2>{html.escape(title)}</h2><div class="recs">'
    for name, why, q in items:
        cards += (f'<a class="rec" href="{html.escape(amazon(q))}" target="_blank" rel="sponsored noopener">'
                  f'<b>{html.escape(name)}</b><span>{html.escape(why)}</span><em>See options on Amazon →</em></a>')
    cards += '</div>'
page('resources.html', 'Recommended Islamic Books & Resources for Muslim Kids',
     'Hand-picked Islamic books, Ramadan activities, prayer mats and learning tools for Muslim children of every age.', f'''
<section class="wrap art"><div class="kick">RECOMMENDED</div><h1>Islamic Books &amp; Resources for Muslim Kids</h1>
<p class="lead">The kinds of books and tools that make faith feel warm and real at home, grouped by age. Start with one — a cozy book at bedtime does more than a shelf full of unread ones.</p>
<p class="sm"><i>As an Amazon Associate I earn from qualifying purchases, at no extra cost to you. <a href="disclaimer.html">Learn more</a>.</i></p>
{cards}
<div class="cta"><img src="img/cover.jpg" alt="Hearts Before Habits book cover"><div><b>And for you: Hearts Before Habits</b><p>A gentle Islamic parenting guide with scripts, du'as and a 30-day plan.</p><a class="btn" href="book.html">See the book</a></div></div></section>''', on=None)

SHOP = CFG.get('shop_url', '')
buy = (f'<a class="btn" href="{html.escape(SHOP)}" target="_blank" rel="noopener">Get the pack — $7</a>' if SHOP else
       '<a class="btn" href="free-starter-kit.html">Launching soon — join the list to hear first</a>')
INSIDE = [('Family intentions & pre-Ramadan checklist', 'Start calm, two weeks before the first suhoor.'),
          ('Family routine & suhoor/iftar planner', 'A simple rhythm for your days, with little-helper jobs for kids.'),
          ('30 Days of Good Deeds', 'One small deed a day for the whole family to colour in.'),
          ('My Fasting Stars & Ramadan Salah tracker', 'Gentle, by-age practice for children — no shaming.'),
          ('Family Quran tracker & sadaqah jar', 'Colour a juz, colour a coin, decide together where it goes on Eid.'),
          ("3 Ramadan du'as with Arabic, transliteration & sources", 'Including the du\'a for breaking the fast and for Laylat al-Qadr.'),
          ('Last ten nights planner', 'A small, special plan for each night.'),
          ('Kids pages', 'Word search with answers, colouring page, My Ramadan journal and a Ramadan Star award.')]
page('ramadan-planner.html', 'Ramadan Family Planner & Kids Activity Pack (Printable)',
     'A 19-page printable Ramadan planner for Muslim moms with kids activities: good-deeds calendar, fasting and salah trackers, Quran tracker, du\'as, word search and more. A4 and US Letter.', f'''
<section class="wrap art" style="max-width:1000px"><div class="kick">RAMADAN 2027 · PRINTABLE PACK</div>
<h1>Our Family Ramadan Planner &amp; Kids Activity Pack</h1>
<p class="lead">19 gentle, printable pages to plan a calm Ramadan — and help your children <b>love</b> the blessed month, not just get through it.</p>
<figure class="feature"><img src="img/shop/ramadan-planner.jpg" alt="Ramadan Family Planner cover and inside pages" width="1200" height="800"></figure>
<p class="btns">{buy}</p>
<h2>What's inside</h2><ul class="chk">{''.join(f'<li><b>{html.escape(a)}</b> — {html.escape(b)}</li>' for a, b in INSIDE)}</ul>
<img src="img/shop/ramadan-planner-pages.jpg" alt="Pages from the Ramadan planner: cover, good deeds calendar, fasting stars and word search" width="1000" height="1500" loading="lazy" style="width:100%;max-width:560px;height:auto;margin:24px auto;border-radius:16px">
<h2>Good to know</h2><ul><li>Instant PDF download in <b>A4 and US Letter</b>. Print at home as many times as you need for your family.</li>
<li>Made for ages 3–12 and their mamas. Ramadan and Eid dates are left blank for your local moon sighting.</li>
<li>Quran and hadith are quoted with their sources. For fiqh questions (like when a child must fast), please ask a qualified scholar.</li>
<li>Personal, family and single-classroom use. Please don't share the file.</li></ul>
<p class="btns">{buy}</p>
<p>Planning ahead? Read <a href="ramadan-with-kids.html">Ramadan with Kids: The Complete Guide</a> and <a href="teach-kids-to-fast-ramadan.html">How to Teach Kids to Fast</a>.</p></section>''', og='img/shop/ramadan-planner.jpg')

page('404.html', 'Page not found', 'This page could not be found.', '''
<section class="wrap art c"><div class="kick">404</div><h1>This page wandered off</h1>
<p class="lead">The page you were looking for isn't here. Try one of these instead:</p>
<p><a class="btn" href="articles.html">All articles</a> <a class="btn ghost" href="free-starter-kit.html">Free starter kit</a></p></section>''', noindex=True)

# ---------- site-wide footer + head block
NAV = [('index.html', 'Home'), ('articles.html', 'Blog'), ('ramadan-planner.html', 'Ramadan Planner'),
       ('printables.html', 'Free Printables'), ('book.html', 'The Book'), ('about.html', 'About'), ('contact.html', 'Contact')]
POSTS = {a['slug'] + '.html' for a in json.load(open('articles.json', encoding='utf-8'))}


def nav_for(f):
    cur = 'articles.html' if (f in POSTS or f.startswith('topic-')) else f
    return '<nav>' + ''.join(f'<a href="{h}"{" class=on" if h == cur else ""}>{t}</a>' for h, t in NAV) + '</nav>'


for f in sorted(glob.glob('*.html')):
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<footer>.*?</footer>', lambda m: FOOTER, s, count=1, flags=re.S)
    s = re.sub(r'<nav>.*?</nav>', lambda m: nav_for(f), s, count=1, flags=re.S)
    s = re.sub(r'<!--SITEHEAD-->.*?<!--/SITEHEAD-->\n?', '', s, flags=re.S)
    s = s.replace('</head>', site_head() + '\n</head>', 1)
    if f == '404.html':  # served from any path, so links must be absolute
        s = re.sub(r'(href|src)="(?!https?:|#|/|mailto:)([^"]+)"', r'\1="/\2"', s)
    open(f, 'w', encoding='utf-8').write(s)

if CFG.get('adsense_client'):
    pub = CFG['adsense_client'].replace('ca-', '')
    open('ads.txt', 'w').write(f'google.com, {pub}, DIRECT, f08c47fec0942fa0\n')
elif os.path.exists('ads.txt'):
    os.remove('ads.txt')

sm = open('sitemap.xml', encoding='utf-8').read()
lastmod = re.search(r'<lastmod>(.*?)</lastmod>', sm).group(1)
for p in ('ramadan-planner.html', 'resources.html', 'privacy.html', 'disclaimer.html', 'terms.html'):
    if f'/{p}</loc>' not in sm:
        sm = sm.replace('</urlset>', f'  <url><loc>{BASE}/{p}</loc><lastmod>{lastmod}</lastmod></url>\n</urlset>')
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
on = [k for k in ('adsense_client', 'amazon_tag', 'ga4_id') if CFG.get(k)]
print(f'site pass done for {DOMAIN}; switched on: {", ".join(on) or "nothing yet"}')
