import os, html
os.chdir('/home/claude/site')
SITE = 'Islamic Parenting 101'
PIN = 'https://www.pinterest.com/digitalallio428/'

def page(fname, title, desc, body, og_img='img/cover.jpg'):
    nav = [('index.html', 'Home'), ('book.html', 'The Book'), ('articles.html', 'Articles'),
           ('printables.html', 'Free Printables'), ('about.html', 'About')]
    links = ''.join(f'<a href="{h}"{" class=on" if h == fname else ""}>{t}</a>' for h, t in nav)
    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{og_img}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;1,700&family=Lato:wght@400;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<link rel="icon" href="img/logo.png">
<script>document.documentElement.classList.add("js")</script>
<script src="anim.js" defer></script>
</head><body>
<header class="top"><div class="wrap bar"><a class="brand" href="index.html"><img src="img/logo.png" alt="Islamic Parenting 101 logo"><span>Islamic Parenting 101</span></a>
<nav>{links}</nav></div></header>
<main>{body}</main>
<footer><div class="wrap"><div class="fl"><img src="img/logo.png" alt=""><div><b>Islamic Parenting 101</b><br>Nurturing children's hearts before shaping their habits.</div></div>
<div class="fr"><a href="{PIN}" target="_blank" rel="noopener">Follow on Pinterest</a> · <a href="book.html">Hearts Before Habits</a> · <a href="printables.html">Free printables</a></div>
<p class="sm">© 2026 Tabasum Majeed · Islamic Parenting 101. This site shares general educational and spiritual guidance; it is not a substitute for professional or scholarly advice.</p></div></footer>
</body></html>'''
    open(fname, 'w').write(doc)

PET = ''.join(f'<i style="left:{l}%;animation-delay:-{d}s;animation-duration:{t}s;--s:{sc}"></i>' for l,d,t,sc in [(6,0,14,1),(18,5,17,.7),(31,9,15,.9),(47,2,19,.6),(63,7,16,1.1),(78,11,18,.8),(90,4,15,.7)])
FLOR = '<div class="flor" aria-hidden="true"></div><div class="petals" aria-hidden="true">'+PET+'</div>'

ARTICLES = [
 ('teaching-salah-by-age.html', 'Teaching Salah by Age: A Gentle, No-Yelling Roadmap', 'img/pin-salah.jpg',
  'How to teach children salah with love at every age — observe, invite, teach and expect — following the Prophetic timeline.',
  '''<p>The Prophet ﷺ gave parents a gentle and remarkably patient timeline: <em>"Command your children to pray when they are seven years old, and discipline them for it when they are ten"</em> (Abu Dawud). That leaves years for love to come first.</p>
<h2>Ages 0–3: Observe</h2><p>Let them see you pray. Smile when they crawl onto your prayer mat. Never push them away — it quietly teaches that prayer is for adults only.</p>
<h2>Ages 4–6: Invite</h2><p>"I'm going to talk to Allah now — want to stand with me?" If they run off after one rak'ah, let them go with a smile. The goal is association: prayer = warmth and welcome.</p>
<h2>Ages 7–9: Teach</h2><p>Formal teaching begins. Teach wudu step by step and build a gentle routine. Expect inconsistency and respond with patience — this is a three-year training window.</p>
<h2>Ages 10+: Expect</h2><p>Salah becomes a calm, clear family expectation. Consequences for missing it are introduced consistently — never with rage or humiliation.</p>
<h2>Make salah a place of joy</h2><p>The Prophet ﷺ let his grandsons climb onto his back during sujud, and shortened the prayer when he heard a baby crying. Make your prayer corner beautiful, pray together often, and tell your children what salah means to <em>you</em>.</p>
<blockquote>A child who is dragged to the prayer mat in anger will one day run away from it. A child who is invited with love will keep returning.</blockquote>'''),
 ('ramadan-with-kids.html', 'Ramadan with Kids: 7 Gentle Traditions', None,
  'Seven simple Ramadan traditions that help Muslim children love the holy month — from cozy suhoor to a family good-deeds jar.',
  '''<p>Ramadan is the family's yearly spiritual classroom. Children won't remember every rule — they will remember how Ramadan <em>felt</em>. Here are seven gentle traditions to start this year.</p>
<ol class="big"><li><b>Make suhoor a cozy family moment</b> — even little ones who aren't fasting can join for a few minutes.</li>
<li><b>A good-deeds jar</b> — one kind act a day, written on a slip and dropped in the jar.</li>
<li><b>Hang a lantern and count down the days</b> — a visible countdown builds excitement.</li>
<li><b>Read one Prophet story each night</b> — short, warm, and before bed.</li>
<li><b>Let little ones help prepare iftar</b> — setting dates on a plate counts!</li>
<li><b>Make du'a together before breaking the fast</b> — let them hear you mention them by name.</li>
<li><b>Give each child a small sadaqah box</b> — and decide together where it goes on Eid.</li></ol>
<p>Pick two or three — not all seven. Small traditions done every year become the memories your children carry for life.</p>'''),
 ('phrases-every-child-needs-to-hear.html', '10 Phrases Every Child Needs to Hear', 'img/pin-phrases.jpg',
  'Ten simple, loving phrases that build a child\'s confidence and connection — inspired by the Prophetic way of speaking to children.',
  '''<p>The Prophet ﷺ taught, <em>"If one of you loves his brother, let him tell him"</em> (Abu Dawud and Tirmidhi). Children need to hear love, not just feel it. These ten phrases build a child's heart:</p>
<ol class="big"><li>"I love you — no matter what."</li><li>"I'm so proud of how hard you tried."</li><li>"You are such a kind person."</li><li>"I trust you."</li><li>"Allah made you perfectly."</li>
<li>"You can come to me with anything."</li><li>"I believe in you."</li><li>"I notice how much effort you put in."</li><li>"I love being your parent."</li><li>"You can always come back to me. I will always be here."</li></ol>
<p><b>Try this tonight:</b> pick the phrase you say the least, and say it sincerely before bedtime. Watch their face.</p>'''),
]

# ---------- home
cards = ''.join(f'''<a class="card" href="{f}">{f'<img src="{img}" alt="">' if img else '<div class="ph">☾</div>'}<div><h3>{t}</h3><p>{d}</p></div></a>''' for f, t, img, d, _ in ARTICLES)
page('index.html', 'Islamic Parenting 101 — Gentle, Heart-First Muslim Parenting',
 'Practical Islamic parenting for Muslim moms: gentle tips from the Quran and Sunnah, free printables, and the book Hearts Before Habits.',
 f'''<section class="hero">{FLOR}<div class="wrap hg"><div><div class="kick">FOR MUSLIM MOMS</div>
<h1>Raise children who love Allah — from the heart.</h1>
<p class="lead">Gentle, practical Islamic parenting from the Quran and Sunnah. Less yelling, more connection — and children whose good habits grow from a loving heart.</p>
<div class="btns"><a class="btn" href="book.html">Discover the book</a><a class="btn ghost" href="printables.html">Free printables</a></div></div>
<img class="cover" src="img/cover.jpg" alt="Hearts Before Habits book cover by Tabasum Majeed"></div></section>
<section class="wrap c4"><h2 class="c">The 4 C's of heart-first parenting</h2>
<div class="grid4"><div class="t teal"><b>1. Connection</b><p>Build the bond first. Without it, every piece of advice feels like criticism.</p></div>
<div class="t green"><b>2. Character</b><p>Children copy what they see. You are their beautiful example.</p></div>
<div class="t gold"><b>3. Consciousness</b><p>Introduce Allah with love — as a warm, present reality, not a threat.</p></div>
<div class="t brown"><b>4. Correction</b><p>Only then, discipline that nurtures (tarbiyah), never humiliates.</p></div></div></section>
<section class="wrap"><h2 class="c">Latest from the blog</h2><div class="cards">{cards}</div><p class="c"><a href="articles.html">All articles →</a></p></section>
<section class="band"><div class="wrap c"><h2>Free Salah Tracker for kids</h2><p>Print it, stick it on the fridge, and watch the habit grow — one colored box at a time.</p><a class="btn" href="printables.html">Get the free printables</a></div></section>''')

# ---------- book
page('book.html', 'Hearts Before Habits — Islamic Parenting Guide to Raise Righteous Children',
 'Hearts Before Habits by Tabasum Majeed: an Islamic parenting guide built on the 4 C\'s — Connection, Character, Consciousness and Correction.',
 f'''<section class="wrap book">{FLOR}<img class="cover big" src="img/cover.jpg" alt="Hearts Before Habits book cover">
<div><div class="kick">THE BOOK</div><h1>Hearts Before Habits</h1><p class="lead">Islamic Parenting Guide to Raise Righteous Children — by Tabasum Majeed</p>
<p>You love your child deeply. But some days, parenting feels overwhelming. You remind them to pray and they ignore you. You promise yourself you'll stay calm — and then you raise your voice again.</p>
<p>You want to raise a child who loves Allah — not out of fear, but from the heart. <b>Hearts Before Habits</b> shows you how, using the 4 C's framework rooted in the Quran and the Prophetic example.</p>
<h3>Inside you'll find</h3><ul class="chk"><li>How the Prophet ﷺ connected with, corrected and honored children</li><li>Teaching Salah and Quran with love, not fear</li><li>Discipline without damage — and calming your own anger</li>
<li>Screens, peer pressure and raising confident Muslims today</li><li>Du'as for your children, ready-to-use scripts and a 30-day plan</li><li>6 bonus tools: routine planner, habit trackers, reflection workbook and du'a journal</li></ul>
<div class="btns"><span class="btn soon">Coming soon on Amazon</span><a class="btn ghost" href="{PIN}" target="_blank" rel="noopener">Follow for launch news</a></div></div></section>''')

# ---------- articles index
page('articles.html', 'Articles — Islamic Parenting 101', 'Gentle Islamic parenting articles for Muslim moms.',
 f'<section class="wrap"><h1 class="c">Articles</h1><div class="cards">{cards}</div></section>')

for f, t, img, d, body in ARTICLES:
    page(f, f'{t} — Islamic Parenting 101', d,
     f'''<article class="wrap art"><div class="kick">ISLAMIC PARENTING</div><h1>{t}</h1>{f'<img class="pinimg" src="{img}" alt="{html.escape(t)} pin">' if img else ''}{body}
<div class="cta"><img src="img/cover.jpg" alt=""><div><b>Want the full guide?</b><p>These ideas come from <i>Hearts Before Habits</i> — a complete Islamic parenting guide with scripts, du'as and a 30-day plan.</p><a class="btn" href="book.html">See the book</a></div></div></article>''',
     og_img=img or 'img/cover.jpg')

# ---------- printables
page('printables.html', 'Free Islamic Parenting Printables — Islamic Parenting 101',
 'Free printable Salah tracker and good-deeds checklist for Muslim kids.',
 '''<section class="wrap"><h1 class="c">Free Printables</h1><p class="c lead">Print at home — free for personal and family use.</p>
<div class="cards">
<a class="card" href="printables/salah-tracker.pdf" download><div class="ph">✓</div><div><h3>30-Day Salah Tracker</h3><p>Color one box for each day all five prayers are done. A gentle, visual way to build the habit.</p><span class="dl">Download PDF</span></div></a>
<a class="card" href="printables/good-deeds-checklist.pdf" download><div class="ph">♡</div><div><h3>Daily Good Deeds Checklist</h3><p>Seven small, beautiful deeds for kids to tick off every day.</p><span class="dl">Download PDF</span></div></a>
</div></section>''')

# ---------- about
page('about.html', 'About Tabasum Majeed — Islamic Parenting 101', 'About the author of Hearts Before Habits.',
 '''<section class="wrap art"><img class="logo-big" src="img/logo.png" alt="Islamic Parenting 101 logo"><h1>About</h1>
<p><b>Tabasum Majeed</b> is the creator of Islamic Parenting 101, a platform dedicated to sharing beneficial knowledge and practical guidance on raising children with strong iman, love for Allah, and good character.</p>
<p>She is a student and researcher with a deep interest in Islamic parenting and personal development, aiming to contribute toward a better future society through conscious, faith-centered upbringing.</p>
<p>Her work simplifies Islamic parenting into clear, actionable steps that help families build a peaceful and nurturing home — helping parents move from reactive parenting to an intentional, heart-centered approach: nurturing children's hearts before shaping their habits.</p>
<blockquote>To help families raise children whose hearts are connected to Allah, whose character is grounded in adab, and whose homes are shaped by mercy, reflection, and intentional parenting.</blockquote></section>''')
print('pages built')
