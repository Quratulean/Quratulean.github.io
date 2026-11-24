#!/usr/bin/env python3
"""Builds the PAID "Ramadan Family Planner & Kids Activity Pack" (Ramadan 2027 / 1448 AH).

    python3 tools/ramadan_pack.py <out_dir>

Writes <out_dir>/ramadan-pack.html, then tools/render_pack.js turns it into
ramadan-family-planner-A4.pdf and -Letter.pdf plus preview PNGs.
The PDFs are the product: NEVER commit them to this public repo (that would give
them away). Upload them to the shop (Payhip) instead. Only previews go in img/shop/.
Brand tokens copied from .claude/skills/islamic-parenting-design/templates/tokens-snapshot.css.
"""
import os, random, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.makedirs(OUT, exist_ok=True)

CSS = r'''
:root{--surface:#FBF5EC;--surface-raised:#fff;--surface-sunk:#F3E6DA;--ink:#3B2A20;--ink-muted:#6B5A4E;
--terracotta:#A8553F;--terracotta-soft:#D9917A;--sage:#4F7358;--sage-soft:#8FB39A;--mustard:#D9A94A;--dusty-blue:#4E7388;
--blush:#F3D9CF;--border:#EADFCF;--display:"Playfair Display",Georgia,serif;--body:Lato,sans-serif;--arabic:Amiri,"Traditional Arabic",serif;
--radius-sm:8px;--radius-md:16px;--radius-lg:22px;--radius-pill:999px}
@page{size:var(--pw,A4);margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--surface);color:var(--ink);font-family:var(--body);font-size:12pt;line-height:1.45;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:var(--W);height:var(--H);padding:16mm 16mm 18mm;position:relative;overflow:hidden;page-break-after:always;background:var(--surface)}
.page:last-child{page-break-after:auto}
.foot{position:absolute;left:0;right:0;bottom:7mm;text-align:center;font-weight:900;font-size:7.5pt;letter-spacing:3pt;color:var(--sage)}
.kicker{font-weight:900;letter-spacing:4px;font-size:9.5pt;color:var(--terracotta);text-transform:uppercase;text-align:center}
h1{font-family:var(--display);font-weight:800;font-size:28pt;line-height:1.05;margin:2mm 0 1mm;text-align:center}
h2{font-family:var(--display);font-weight:700;font-size:15pt;margin:0 0 2mm}
.sub{font-family:var(--display);font-style:italic;font-weight:700;color:var(--sage);text-align:center;font-size:12.5pt;margin:0 0 4mm}
.rule{width:28mm;height:1mm;background:var(--mustard);margin:2mm auto 5mm;border-radius:2px}
.card{background:var(--surface-raised);border-radius:var(--radius-md);padding:4.5mm 5mm;box-shadow:0 1.2mm 0 var(--border);margin-bottom:4mm}
.lines div{border-bottom:1px solid var(--border);height:8.5mm}
.lab{font-weight:900;font-size:9pt;letter-spacing:2px;color:var(--terracotta);text-transform:uppercase}
.small{font-size:10pt;color:var(--ink-muted)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:4mm}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm}
table{border-collapse:separate;border-spacing:0;width:100%;background:#fff;border-radius:var(--radius-md);overflow:hidden;box-shadow:0 1.2mm 0 var(--border)}
th{background:var(--sage);color:#fff;font-size:9pt;letter-spacing:1px;padding:2mm 1mm;font-weight:900}
td{border-top:1px solid var(--border);border-left:1px solid var(--border);padding:0 2mm;font-size:10pt;height:var(--rowh,7.2mm)}
td:first-child{border-left:none}
.days{display:grid;grid-template-columns:repeat(5,1fr);gap:2.6mm}
.day{background:#fff;border-radius:var(--radius-sm);box-shadow:0 .8mm 0 var(--border);padding:2mm 2.4mm;height:var(--dayh,33mm);position:relative;font-size:9.6pt;line-height:1.3}
.day b{display:block;font-family:var(--display);font-size:13pt;color:var(--terracotta)}
.day .box{position:absolute;right:2.4mm;bottom:2.2mm;width:6mm;height:6mm;border:1.4px solid var(--sage);border-radius:50%}
.ar{font-family:var(--arabic);direction:rtl;font-size:22pt;line-height:2;text-align:center;color:var(--ink)}
.tr{font-style:italic;text-align:center;color:var(--sage);font-weight:700}
.en{text-align:center}
.src{text-align:center;font-size:9pt;color:var(--ink-muted)}
.check li{list-style:none;margin:0 0 2.2mm;padding-left:8mm;position:relative}
.check li:before{content:"";position:absolute;left:0;top:1mm;width:4.4mm;height:4.4mm;border:1.4px solid var(--terracotta);border-radius:1.2mm}
ul.check{padding:0;margin:0}
.star{display:inline-block;width:7mm;height:7mm;margin:0 .6mm}
.ws{border-collapse:collapse;margin:0 auto;box-shadow:none;width:auto;background:#fff;border-radius:var(--radius-md)}
.ws td{width:10.2mm;height:10.2mm;text-align:center;font-weight:900;font-size:15pt;border:1px solid var(--border);padding:0;color:var(--ink)}
.key td{width:4.2mm;height:4.2mm;font-size:7pt;font-weight:700;color:#c9b9aa;border:none}
.key td.hit{color:var(--terracotta);font-weight:900}
.cover{background:linear-gradient(180deg,#F3E6DA 0%,#FBF5EC 55%)}
.badge{display:inline-block;background:var(--blush);color:var(--terracotta);border-radius:var(--radius-pill);padding:1.4mm 4mm;font-weight:900;font-size:9pt;letter-spacing:2px}
.flor{position:absolute;opacity:.9}
.cert{border:2.4mm solid var(--mustard);border-radius:8mm;height:100%;padding:12mm;text-align:center;background:#fff;position:relative}
'''

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Lato:wght@400;700;900&family=Playfair+Display:ital,wght@0,700;0,800;1,700&display=swap" rel="stylesheet">')

# ---------- small SVG ornaments (drawn here, no external assets)
def lantern(w=46, fill='#D9A94A', stroke='#3B2A20', col=True):
    f = fill if col else 'none'
    return (f'<svg width="{w}mm" viewBox="0 0 100 170" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="{stroke}" stroke-width="3" stroke-linejoin="round">'
            f'<path d="M50 2v14"/><circle cx="50" cy="20" r="5" fill="{f if col else "none"}"/>'
            f'<path d="M30 30h40l-6 12H36z" fill="{"#A8553F" if col else "none"}"/>'
            f'<path d="M36 42c-14 12-20 30-20 48s6 36 20 48h28c14-12 20-30 20-48s-6-36-20-48z" fill="{f}"/>'
            f'<path d="M50 42v96M33 60c-5 9-7 19-7 30s2 21 7 30M67 60c5 9 7 19 7 30s-2 21-7 30"/>'
            f'<path d="M50 72c-7 8-10 14-10 20a10 10 0 0 0 20 0c0-6-3-12-10-20z" fill="{"#FBF5EC" if col else "none"}"/>'
            f'<path d="M34 138h32l5 12H29z" fill="{"#A8553F" if col else "none"}"/><path d="M42 150v12h16v-12"/></svg>')

def crescent(w=30, fill='#D9A94A', stroke='none'):
    return (f'<svg width="{w}mm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><path d="M62 8a44 44 0 1 0 30 70A36 36 0 1 1 62 8z" fill="{fill}" stroke="{stroke}" stroke-width="3"/></svg>')

def star(fill='#D9A94A', stroke='none', w=7):
    return (f'<svg class="star" style="width:{w}mm;height:{w}mm" viewBox="0 0 24 24"><path d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.8-6.2 3.8 1.6-7L2 9.2l7.1-.6z" fill="{fill}" stroke="{stroke}" stroke-width="1.4" stroke-linejoin="round"/></svg>')

def sprig(w=26):
    return (f'<svg width="{w}mm" viewBox="0 0 120 40" xmlns="http://www.w3.org/2000/svg"><path d="M5 30C40 28 80 20 115 6" stroke="#4F7358" stroke-width="2.4" fill="none"/>'
            + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="9" ry="4" transform="rotate({r} {x} {y})" fill="#8FB39A"/>' for x, y, r in [(25,22,-30),(45,16,20),(62,17,-35),(80,9,15),(96,8,-40)])
            + '<circle cx="12" cy="29" r="5" fill="#F3D9CF"/><circle cx="12" cy="29" r="2" fill="#D9A94A"/></svg>')

FOOT = '<div class="foot">ISLAMIC PARENTING 101  ·  HEARTS BEFORE HABITS  ·  PERSONAL &amp; FAMILY USE ONLY</div>'
def page(inner, cls=''):
    return f'<section class="page {cls}">{inner}{FOOT}</section>'
def head(kicker, title, sub=None):
    return f'<div class="kicker">{kicker}</div><h1>{title}</h1>' + (f'<div class="sub">{sub}</div>' if sub else '') + '<div class="rule"></div>'
def lines(n):
    return '<div class="lines">' + '<div></div>' * n + '</div>'

P = []

# 1 cover
P.append(page(f'''
<div style="position:absolute;right:14mm;top:12mm">{crescent(26)}</div>
<div style="position:absolute;left:18mm;top:22mm">{star(w=8)}{star(w=5)}</div>
<div style="text-align:center;margin-top:30mm"><span class="badge">RAMADAN 2027 · 1448 AH</span></div>
<h1 style="font-size:40pt;margin-top:8mm">Our Family<br>Ramadan Planner</h1>
<div class="sub" style="font-size:16pt">&amp; Kids Activity Pack</div>
<div class="rule"></div>
<div style="display:flex;justify-content:center;gap:6mm;align-items:flex-end;margin:8mm 0">{lantern(30)}{lantern(44)}{lantern(30)}</div>
<p class="en" style="font-size:13pt;max-width:140mm;margin:6mm auto 0">Gentle pages to plan a calm, joyful Ramadan — and help your children <b>love</b> the blessed month, not just get through it.</p>
<p class="en" style="margin-top:14mm;font-family:var(--display);font-weight:700;font-size:13pt">Tabasum Majeed</p>
<p class="src">Author of <i>Hearts Before Habits</i> · Islamic Parenting 101</p>''', 'cover'))

# 2 welcome + how to use
P.append(page(head('BISMILLAH', 'Before you begin', 'Heart first. Habit second.') + '''
<div class="card"><p>Assalamu alaykum, dear sister.</p>
<p>Ramadan with children is beautiful — and busy. This pack is not a list of things you must do. It is a gentle toolbox. Pick the pages that fit your family this year and leave the rest without guilt.</p>
<p>Children won't remember every rule of Ramadan. They will remember how it <i>felt</i>: the cozy suhoor, the lantern by the window, the star they coloured after their first half-day fast. That feeling is what grows into love for Allah.</p>
<p style="margin:0">May Allah accept from you and your family. — <b>Tabasum</b></p></div>
<h2>How to use this pack</h2>
<table><tr><th>Page</th><th>For</th><th>Ages</th></tr>
<tr><td>Family intentions · Prep checklist · Routine · Meal planner · Last 10 nights</td><td>You, mama</td><td>—</td></tr>
<tr><td>30 Days of Good Deeds · Sadaqah jar</td><td>The whole family</td><td>3+</td></tr>
<tr><td>My Fasting Stars · My Ramadan Salah</td><td>Children practising</td><td>5–12</td></tr>
<tr><td>Family Quran tracker · Duas to learn</td><td>Everyone</td><td>4+</td></tr>
<tr><td>Word search · Colouring · My Ramadan journal · Ramadan Star award</td><td>Kids</td><td>4–11</td></tr></table>
<p class="small" style="margin-top:4mm">Printing: prints on A4 or US Letter. Choose "fit to page". Print the trackers once per child. Ramadan and Eid dates depend on the moon sighting — fill in your own local dates. For questions of fiqh (for example, when a child should begin fasting), please ask a qualified scholar.</p>'''))

# 3 family intentions
P.append(page(head('NIYYAH', 'Our family intentions', '"Actions are only by intentions." — Bukhari 1, Muslim 1907') + f'''
<div class="card"><div class="lab">This Ramadan, as a family, we hope to…</div>{lines(4)}</div>
<div class="grid2">
<div class="card"><div class="lab">My own goal (mama)</div>{lines(4)}</div>
<div class="card"><div class="lab">One habit to start</div>{lines(4)}</div>
<div class="card"><div class="lab">Child: ______________ — goal</div>{lines(3)}</div>
<div class="card"><div class="lab">Child: ______________ — goal</div>{lines(3)}</div>
<div class="card"><div class="lab">Child: ______________ — goal</div>{lines(3)}</div>
<div class="card"><div class="lab">One thing we will let go of</div>{lines(3)}</div></div>
<p class="small c" style="text-align:center">Keep goals small. One kept habit is worth more than ten abandoned ones.</p>'''))

# 4 prep checklist
prep = [('Two weeks before', ['Talk about Ramadan at dinner: why we fast and what it feels like', 'Read one Ramadan story at bedtime', 'Choose a spot for the Ramadan corner or window lantern', 'Decide each child’s fasting practice (see “My Fasting Stars”)', 'Plan a simple Ramadan routine (next page)']),
        ('One week before', ['Put up lights, lantern or decorations together', 'Stock suhoor basics: dates, oats, eggs, yoghurt, fruit, water bottles', 'Fill the freezer with 3–4 easy iftar meals', 'Set up the sadaqah jar and the good-deeds calendar', 'Move bedtime 20–30 minutes earlier for little ones']),
        ('The night before', ['Make du’a together for a blessed month', 'Lay out suhoor things and set alarms', 'Tell the children: “Tomorrow Ramadan begins!”'])]
body = ''.join(f'<div class="card"><h2>{t}</h2><ul class="check">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul></div>' for t, items in prep)
P.append(page(head('GET READY', 'Pre-Ramadan checklist', 'A calm start begins before the first suhoor') + body + f'<div style="position:absolute;right:14mm;bottom:16mm">{sprig(30)}</div>'))

# 5 daily routine
slots = [('Suhoor', 'before Fajr'), ('After Fajr', ''), ('Morning', ''), ('Midday / Dhuhr', ''), ('Afternoon / Asr', 'rest time?'), ('Before Maghrib', 'du’a time'), ('Iftar', ''), ('Isha / Taraweeh', ''), ('Bedtime', 'story + du’a')]
rows = ''.join(f'<tr><td style="width:36%"><b>{a}</b> <span class="small">{b}</span></td><td></td><td></td></tr>' for a, b in slots)
P.append(page(head('OUR RHYTHM', 'Family Ramadan routine', 'Write what your days will look like — then be kind when they don’t') +
              f'<table style="--rowh:17mm"><tr><th>Time</th><th>Me</th><th>The children</th></tr>{rows}</table>'))

# 6 weekly meal planner
days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']
rows = ''.join(f'<tr><td style="width:14%"><b>{d}</b></td><td></td><td></td><td></td></tr>' for d in days)
P.append(page(head('IN THE KITCHEN', 'Suhoor &amp; iftar planner', 'Print one for each week · Week: ____  Dates: ______________') +
              f'<table style="--rowh:21mm"><tr><th>Day</th><th>Suhoor</th><th>Iftar</th><th>Little helper job</th></tr>{rows}</table>'
              '<p class="small" style="margin-top:4mm">Little helper jobs: put dates on a plate · fill water cups · set the table · stir the soup · say the du’a for breaking the fast.</p>'))

# 7 30 days of good deeds
deeds = ['Smile at everyone at home', 'Say salam first', 'Help set the iftar table', 'Give water to someone fasting', 'Read or listen to a short surah',
         'Tidy your toys without being asked', 'Make du’a for a friend', 'Put a coin in the sadaqah jar', 'Say “JazakAllahu khayran” 3 times', 'Draw a card for a grandparent',
         'Learn the du’a for breaking the fast', 'Share a snack', 'Be patient when you want to shout', 'Help a sibling', 'Say Alhamdulillah for 5 things',
         'Pick up litter outside', 'Hug your parents and say thank you', 'Learn one of Allah’s names', 'Call or message a relative', 'Give a toy or book you don’t use',
         'Help wash the dishes', 'Make wudu carefully', 'Pray one prayer with the family', 'Say SubhanAllah 33 times', 'Make iftar treats for a neighbour',
         'Read a Prophet story', 'Forgive someone', 'Do a chore for mama', 'Write what you love about Ramadan', 'Make du’a for the whole ummah']
cells = ''.join(f'<div class="day"><b>{i+1}</b>{d}<span class="box"></span></div>' for i, d in enumerate(deeds))
P.append(page(head('FOR THE WHOLE FAMILY', '30 days of good deeds', 'Do the deed, then colour the circle') + f'<div class="days" style="--dayh:31.5mm">{cells}</div>'))

# 8 fasting stars
rows = ''.join(f'<tr><td style="width:12%;text-align:center"><b>{i}</b></td><td>{star("none","#D9A94A",6)}{star("none","#D9A94A",6)}{star("none","#D9A94A",6)}</td><td></td></tr>' for i in range(1, 16))
rows2 = ''.join(f'<tr><td style="width:12%;text-align:center"><b>{i}</b></td><td>{star("none","#D9A94A",6)}{star("none","#D9A94A",6)}{star("none","#D9A94A",6)}</td><td></td></tr>' for i in range(16, 31))
P.append(page(head('FOR CHILDREN PRACTISING', 'My fasting stars', 'Name: ____________________') +
    '<p class="small" style="text-align:center;margin-top:-2mm">1 star = fasted until a set time (e.g. lunch) · 2 stars = half the day · 3 stars = a full fast. Children who are not yet ready can colour a star for a kind deed instead. Ask a qualified scholar about when fasting becomes required for your child.</p>'
    f'<div class="grid2" style="--rowh:12.2mm"><table><tr><th>Day</th><th>Stars</th><th>How I felt</th></tr>{rows}</table><table><tr><th>Day</th><th>Stars</th><th>How I felt</th></tr>{rows2}</table></div>'))

# 9 salah tracker
pr = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
def srows(a, b):
    return ''.join(f'<tr><td style="text-align:center"><b>{i}</b></td>' + '<td></td>' * 5 + '</tr>' for i in range(a, b))
th = '<tr><th>Day</th>' + ''.join(f'<th>{p}</th>' for p in pr) + '</tr>'
P.append(page(head('MY RAMADAN SALAH', 'I pray with love', 'Name: ____________________ · Draw a heart for every prayer') +
    f'<div class="grid2" style="--rowh:12.4mm"><table>{th}{srows(1,16)}</table><table>{th}{srows(16,31)}</table></div>'
    '<p class="small" style="text-align:center;margin-top:3mm">“Command your children to pray when they are seven…” (Abu Dawud 495, graded hasan). Little ones simply join in — every heart counts.</p>'))

# 10 Quran tracker
juz = ''.join(f'<div class="day" style="height:27mm;text-align:center"><b style="font-size:17pt;margin-top:2mm">{i}</b><span class="small">Juz {i}</span><div style="margin-top:2mm">____</div></div>' for i in range(1, 31))
P.append(page(head('QURAN', 'Our family Quran tracker', 'Colour a juz when the family finishes it — write who read it underneath') +
    f'<div class="days" style="grid-template-columns:repeat(6,1fr)">{juz}</div>'
    '<div class="card" style="margin-top:5mm"><div class="lab">Small and steady</div><p style="margin:1mm 0 0">Not reading a whole juz a day? Track pages instead, or let each child own a short surah to memorise this month. “The most beloved deeds to Allah are those done consistently, even if small.” (Bukhari 6464, Muslim 783)</p></div>'))

# 11 duas
P.append(page(head('DUAS TO LEARN', 'Three Ramadan du’as', 'Learn one a week — say it together') + '''
<div class="card"><div class="lab">When breaking the fast</div>
<div class="ar">ذَهَبَ الظَّمَأُ وَابْتَلَّتِ الْعُرُوقُ وَثَبَتَ الأَجْرُ إِنْ شَاءَ اللَّهُ</div>
<div class="tr">Dhahaba-ẓ-ẓama’ wabtallati-l-‘urūq wa thabata-l-ajru in shā’ Allāh</div>
<div class="en">“The thirst has gone, the veins are moistened, and the reward is certain, if Allah wills.”</div>
<div class="src">Abu Dawud 2357 (graded hasan)</div></div>
<div class="card"><div class="lab">On Laylat al-Qadr (and any night)</div>
<div class="ar">اللَّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ الْعَفْوَ فَاعْفُ عَنِّي</div>
<div class="tr">Allāhumma innaka ‘afuwwun tuḥibbul-‘afwa fa‘fu ‘annī</div>
<div class="en">“O Allah, You are Pardoning and You love to pardon, so pardon me.”</div>
<div class="src">Tirmidhi 3513, Ibn Majah 3850 (graded sahih)</div></div>
<div class="card"><div class="lab">A du’a for our family (from the Quran)</div>
<div class="ar">رَبَّنَا هَبْ لَنَا مِنْ أَزْوَاجِنَا وَذُرِّيَّاتِنَا قُرَّةَ أَعْيُنٍ</div>
<div class="tr">Rabbanā hab lanā min azwājinā wa dhurriyyātinā qurrata a‘yun</div>
<div class="en">“Our Lord, grant us from our spouses and children the comfort of our eyes.”</div>
<div class="src">Surah al-Furqan 25:74</div></div>'''))

# 12 last ten nights
nights = ''.join(f'<tr><td style="text-align:center"><b>{n}</b></td><td></td><td></td><td></td></tr>' for n in range(21, 31))
P.append(page(head('THE LAST TEN NIGHTS', 'Seeking Laylat al-Qadr', '“Better than a thousand months” — Surah al-Qadr 97:3') +
    '<p class="small" style="text-align:center;margin-top:-2mm">The Prophet ﷺ said: “Seek it in the odd nights of the last ten.” (Bukhari 2017). Plan something small and special for each night.</p>'
    f'<table style="--rowh:13mm"><tr><th>Night</th><th>Our plan (e.g. extra prayer, du’a list, sadaqah)</th><th>Kids’ special job</th><th>Done</th></tr>{nights}</table>'
    f'<div class="card" style="margin-top:4mm"><div class="lab">My du’a list</div>{lines(4)}</div>'))

# 13 sadaqah jar
coins = ''.join('<div style="width:15mm;height:15mm;border-radius:50%;border:1.6px dashed var(--mustard);display:inline-block;margin:1.6mm"></div>' for _ in range(40))
P.append(page(head('GIVING', 'Our sadaqah jar', 'Colour a coin every time you give — big or small') +
    f'<div class="card" style="text-align:center">{coins}</div>'
    f'<div class="grid2"><div class="card"><div class="lab">We are saving for…</div>{lines(3)}</div><div class="card"><div class="lab">On Eid we will give it to…</div>{lines(3)}</div></div>'
    '<p class="small" style="text-align:center">“Charity does not decrease wealth.” (Muslim 2588). For zakat al-fitr amounts and timing, follow your local masjid or scholar.</p>'))

# 14 word search (+ answer key)
WORDS = ['RAMADAN', 'SUHOOR', 'IFTAR', 'QURAN', 'DUA', 'SADAQAH', 'LANTERN', 'MOON', 'EID', 'DATES', 'PATIENCE', 'PRAYER', 'MERCY', 'FASTING']
N = 12
rnd = random.Random(1448)
def make_grid():
    while True:
        g = [[None] * N for _ in range(N)]; hits = set(); ok = True
        for w in sorted(WORDS, key=len, reverse=True):
            for _ in range(400):
                d = rnd.choice([(0, 1), (1, 0), (1, 1)])
                r = rnd.randrange(N - (len(w) - 1) * d[0]); c = rnd.randrange(N - (len(w) - 1) * d[1])
                cells = [(r + i * d[0], c + i * d[1]) for i in range(len(w))]
                if all(g[y][x] in (None, w[i]) for i, (y, x) in enumerate(cells)):
                    for i, (y, x) in enumerate(cells):
                        g[y][x] = w[i]; hits.add((y, x))
                    break
            else:
                ok = False; break
        if ok:
            for y in range(N):
                for x in range(N):
                    if g[y][x] is None:
                        g[y][x] = rnd.choice('ABCDEFGHIKLMNOPRSTUY')
            return g, hits
G, HITS = make_grid()
ws = '<table class="ws">' + ''.join('<tr>' + ''.join(f'<td>{G[y][x]}</td>' for x in range(N)) + '</tr>' for y in range(N)) + '</table>'
key = '<table class="ws key">' + ''.join('<tr>' + ''.join(f'<td class="{"hit" if (y, x) in HITS else ""}">{G[y][x]}</td>' for x in range(N)) + '</tr>' for y in range(N)) + '</table>'
wl = ''.join(f'<span style="display:inline-block;width:31%;font-weight:700">☐ {w}</span>' for w in WORDS)
P.append(page(head('PUZZLE TIME', 'Ramadan word search', 'Words go across, down and diagonally') + ws +
    f'<div class="card" style="margin-top:5mm;font-size:11.5pt">{wl}</div>'
    f'<div style="display:flex;justify-content:flex-end;align-items:flex-end;gap:3mm"><span class="small">Answers (for grown-ups) →</span>{key}</div>'))

# 15 colouring
P.append(page(head('COLOUR ME', 'Light up Ramadan', 'Colour the lanterns, the moon and the stars') +
    '<div style="display:flex;justify-content:center;align-items:flex-end;gap:8mm;margin-top:6mm">'
    + lantern(42, col=False) + lantern(62, col=False) + lantern(42, col=False) + '</div>'
    + '<div style="display:flex;justify-content:center;gap:10mm;align-items:center;margin-top:10mm">'
    + crescent(42, 'none', '#3B2A20') + star('none', '#3B2A20', 20) + star('none', '#3B2A20', 14) + star('none', '#3B2A20', 20) + '</div>'
    + '<p class="en" style="margin-top:8mm;font-family:var(--display);font-weight:700;font-size:20pt;color:var(--ink-muted)">Ramadan Mubarak!</p>'))

# 16 kids journal
P.append(page(head('MY RAMADAN JOURNAL', 'All about my Ramadan', 'Name: __________________ · Age: _____') + f'''
<div class="grid2"><div class="card" style="height:62mm"><div class="lab">Draw your iftar table</div></div>
<div class="card" style="height:62mm"><div class="lab">Draw your favourite Ramadan moment</div></div></div>
<div class="card"><div class="lab">My favourite thing about Ramadan is…</div>{lines(2)}</div>
<div class="card"><div class="lab">A good deed I am proud of</div>{lines(2)}</div>
<div class="card"><div class="lab">Something new I learned (a du’a, a surah, a story)</div>{lines(2)}</div>
<div class="card"><div class="lab">I made du’a for…</div>{lines(2)}</div>'''))

# 17 mama reflection
P.append(page(head('FOR YOU, MAMA', 'End-of-Ramadan reflection', 'Write this on the last night, before Eid') + f'''
<div class="card"><div class="lab">A moment I want to remember</div>{lines(3)}</div>
<div class="card"><div class="lab">What worked for our family</div>{lines(3)}</div>
<div class="card"><div class="lab">What I will do differently next year</div>{lines(3)}</div>
<div class="card"><div class="lab">One habit we will keep after Ramadan</div>{lines(2)}</div>
<div class="card"><div class="lab">Alhamdulillah for…</div>{lines(3)}</div>'''))

# 18 certificate
P.append(page(f'''<div class="cert"><div style="position:absolute;left:10mm;top:10mm">{crescent(18)}</div><div style="position:absolute;right:10mm;top:10mm">{star(w=12)}{star(w=8)}</div>
<div class="kicker" style="margin-top:18mm">THIS AWARD IS PROUDLY GIVEN TO</div>
<div style="border-bottom:1.5px solid var(--ink);width:120mm;margin:16mm auto 4mm;height:12mm"></div>
<h1 style="font-size:42pt;margin-top:10mm">Ramadan Star</h1>
<div class="sub" style="font-size:15pt">for fasting, praying, giving and growing with a beautiful heart</div>
<div style="margin:8mm 0">{star(w=16)}{star(w=22)}{star(w=16)}</div>
<p style="font-size:13pt;max-width:130mm;margin:0 auto">Your family is so proud of you. May Allah accept your good deeds and fill your heart with love for Him.</p>
<div style="display:flex;justify-content:space-around;margin-top:20mm"><div><div style="border-bottom:1.4px solid var(--ink);width:60mm;height:10mm"></div><span class="small">Signed</span></div>
<div><div style="border-bottom:1.4px solid var(--ink);width:60mm;height:10mm"></div><span class="small">Ramadan 1448 AH</span></div></div>
<div style="position:absolute;bottom:10mm;left:0;right:0;display:flex;justify-content:center">{lantern(22)}</div></div>'''))

# 19 closing / book
P.append(page(head('JAZAKILLAHU KHAYRAN', 'Thank you, dear sister', 'May this Ramadan be the gentlest one yet') + f'''
<div class="card" style="text-align:center"><p>If this pack helped your family, the one thing that helps me most is a kind word: share it with a friend (send them the link — please don’t share the file), or tell me how your Ramadan went.</p></div>
<div class="card" style="display:flex;gap:6mm;align-items:center"><div style="flex:0 0 46mm;height:62mm;border-radius:3mm;background:linear-gradient(160deg,#A8553F,#D9917A);color:#fff;display:flex;flex-direction:column;justify-content:center;text-align:center;padding:4mm"><div style="font-family:var(--display);font-weight:800;font-size:17pt;line-height:1.1">Hearts Before Habits</div><div style="font-size:8pt;margin-top:3mm;letter-spacing:1px">TABASUM MAJEED</div></div>
<div><div class="lab">Want more?</div><h2>Hearts Before Habits</h2><p style="margin:0 0 2mm">A gentle Islamic parenting guide built on the 4 C’s — Connection, Character, Consciousness and Correction — with scripts for hard moments, du’as and a 30-day plan.</p><p class="small" style="margin:0">Find it on Amazon, and free articles and printables at <b>quratulean.github.io</b></p></div></div>
<div class="card"><div class="lab">Licence</div><p class="small" style="margin:1mm 0 0">© 2026 Tabasum Majeed · Islamic Parenting 101. For personal, family and single-classroom use. Please do not resell, share the file, or upload it elsewhere. Ramadan and Eid dates depend on moon sighting. This pack shares general guidance and is not a religious ruling; for fiqh questions please ask a qualified scholar.</p></div>
<div style="text-align:center;margin-top:6mm">{sprig(40)}</div>'''))

html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Ramadan Family Planner &amp; Kids Activity Pack</title>{FONTS}<style>{CSS}</style></head><body>' + ''.join(P) + '</body></html>'
open(os.path.join(OUT, 'ramadan-pack.html'), 'w', encoding='utf-8').write(html)
print(f'{len(P)} pages written to {OUT}/ramadan-pack.html')
