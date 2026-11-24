#!/usr/bin/env python3
"""Make a featured image for every article (and a tall Pinterest version).

Usage (from the repo root):  python3 tools/featured.py [slug ...]
- Writes img/articles/<slug>.jpg (1200x800, used on cards, at the top of the article
  and as the share image) and pins/<slug>.jpg (1000x1500, used by "Save to Pinterest").
- Each article gets a hand-drawn SVG illustration in the site palette. Add new
  articles to ART below (headline + icon); unknown slugs fall back to the title and a heart.
- Then run python3 tools/publish.py so pages pick the images up.
Needs Playwright + Chromium (node) — renders via tools/render_images.js.
"""
import glob, json, os, re, subprocess, sys, tempfile, html

C = dict(cream='#FBF5EC', terra='#A8553F', mustard='#D9A94A', sage='#4F7358', blush='#F3D9CF',
         blue='#4E7388', brown='#3B2A20', teal='#1B7C8C', leaf='#8FA98A', sand='#F6E7C5', mint='#E4ECDD')

# slug -> (short headline for the image, icon, background tint)
ART = {
    'gentle-parenting-in-islam': ('Gentle Parenting in Islam', 'hearts', 'blush'),
    'islamic-parenting-guide': ('Islamic Parenting, Simply Explained', 'tree', 'mint'),
    'how-to-stop-yelling-at-your-kids': ('How to Stop Yelling', 'bubble', 'blush'),
    'how-to-discipline-a-child-in-islam': ('Gentle, Firm & Fair Discipline', 'scale', 'sand'),
    'toddler-tantrums-islamic-parenting': ('Calm Through Toddler Tantrums', 'cloud', 'mint'),
    'daily-duas-for-kids': ('12 Daily Duas for Kids', 'tasbih', 'sand'),
    'muslim-mom-burnout': ('Rest for the Tired Muslim Mom', 'teacup', 'blush'),
    'teach-kids-about-allah': ('Teaching Kids About Allah', 'night', 'mint'),
    'phrases-every-child-needs-to-hear': ('10 Phrases Every Child Needs', 'bubbles', 'sand'),
    'teaching-salah-by-age': ('Teaching Salah by Age', 'mats', 'blush'),
    'get-kids-up-for-fajr': ('Fajr Without a Fight', 'sunrise', 'sand'),
    'teach-quran-to-kids-at-home': ('Teaching Quran at Home', 'quran', 'mint'),
    'ramadan-with-kids': ('Ramadan with Kids', 'lantern', 'sand'),
    'teach-kids-to-fast-ramadan': ('First Fasts, Gently', 'dates', 'blush'),
}

def heart(x, y, s, fill):
    return (f'<path transform="translate({x} {y}) scale({s})" fill="{fill}" d="M0 30 C-34 6 -40 -16 -26 -28 '
            f'C-15 -37 -4 -32 0 -22 C4 -32 15 -37 26 -28 C40 -16 34 6 0 30Z"/>')

def flower(x, y, r, fill, center=C['mustard']):
    petals = ''.join(f'<ellipse cx="{x}" cy="{y - r * .62}" rx="{r * .42}" ry="{r * .62}" fill="{fill}" '
                     f'transform="rotate({a} {x} {y})"/>' for a in range(0, 360, 72))
    return petals + f'<circle cx="{x}" cy="{y}" r="{r * .3}" fill="{center}"/>'

def sprig(x, y, rot, s=1, col=C['leaf']):
    leaves = ''.join(f'<ellipse cx="{12 * i}" cy="{-9 if i % 2 else 9}" rx="11" ry="5" fill="{col}" '
                     f'transform="rotate({-35 if i % 2 else 35} {12 * i} {-9 if i % 2 else 9})"/>' for i in range(1, 6))
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><path d="M0 0 Q36 -4 72 0" '
            f'stroke="{col}" stroke-width="3" fill="none"/>{leaves}</g>')

def star(x, y, r, fill):
    pts = []
    import math
    for i in range(10):
        rr = r if i % 2 == 0 else r * .45
        a = math.pi / 5 * i - math.pi / 2
        pts.append(f'{x + rr * math.cos(a):.1f},{y + rr * math.sin(a):.1f}')
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'

def icon(name):
    t, m, s, b, br, te, bl = C['terra'], C['mustard'], C['sage'], C['blush'], C['brown'], C['teal'], C['blue']
    if name == 'hearts':
        return (heart(170, 190, 4.2, t) + heart(258, 250, 2.6, m) + heart(110, 290, 1.2, s)
                + sprig(250, 330, -20, 1.3) + flower(345, 70, 24, t, m))
    if name == 'tree':
        canopy = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r, c in
                         [(200, 165, 95, s), (120, 200, 62, '#6E8F74'), (280, 200, 62, '#6E8F74'),
                          (160, 110, 60, '#6E8F74'), (245, 110, 60, s)])
        hs = heart(160, 150, .7, t) + heart(240, 190, .7, m) + heart(205, 95, .6, b) + heart(130, 215, .55, b) + heart(275, 130, .55, t)
        return (f'<ellipse cx="200" cy="355" rx="150" ry="18" fill="{C["leaf"]}" opacity=".5"/>'
                f'<path d="M185 355 L190 250 L150 215 L158 208 L193 236 L196 190 L206 190 L208 236 L245 205 L252 213 L212 250 L217 355Z" fill="{br}"/>'
                + canopy + hs)
    if name == 'bubble':
        return (f'<path d="M70 90 h260 a40 40 0 0 1 40 40 v120 a40 40 0 0 1 -40 40 H170 l-60 50 l10 -50 H70 a40 40 0 0 1 -40 -40 V130 a40 40 0 0 1 40 -40Z" fill="{te}"/>'
                f'<path d="M80 190 l18 -30 l18 50 l18 -60 l18 70 l18 -40" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".55"/>'
                f'<path d="M170 190 q20 -14 40 0 t40 0" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round"/>'
                + heart(300, 185, 1.1, m) + flower(360, 50, 22, t, m) + sprig(40, 370, -25, 1.1))
    if name == 'scale':
        return (f'<rect x="192" y="80" width="16" height="250" rx="6" fill="{br}"/>'
                f'<rect x="130" y="325" width="140" height="22" rx="11" fill="{br}"/>'
                f'<circle cx="200" cy="78" r="16" fill="{m}"/>'
                f'<rect x="60" y="112" width="280" height="12" rx="6" fill="{br}"/>'
                f'<path d="M80 124 L45 225 M80 124 L115 225 M320 124 L285 225 M320 124 L355 225" stroke="{br}" stroke-width="3"/>'
                f'<path d="M35 225 h90 a45 30 0 0 1 -90 0Z" fill="{m}"/><path d="M275 225 h90 a45 30 0 0 1 -90 0Z" fill="{m}"/>'
                + heart(80, 200, .85, t)
                + f'<rect x="295" y="182" width="50" height="40" rx="4" fill="{s}"/><rect x="301" y="188" width="38" height="28" fill="{C["cream"]}"/>'
                + sprig(250, 370, -10, 1.1))
    if name == 'cloud':
        sun = f'<circle cx="275" cy="135" r="62" fill="{m}"/>' + ''.join(
            f'<rect x="271" y="40" width="8" height="26" rx="4" fill="{m}" transform="rotate({a} 275 135)"/>' for a in range(0, 360, 40))
        cloud = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r, c in
                        [(140, 215, 62, bl), (205, 185, 75, bl), (270, 220, 55, bl), (110, 250, 42, bl)])
        cloud += f'<rect x="100" y="220" width="210" height="72" rx="36" fill="{bl}"/>'
        drops = ''.join(f'<path d="M{x} {y} q-10 18 0 24 q10 -6 0 -24Z" fill="{te}"/>' for x, y in [(150, 310), (195, 325), (240, 310)])
        rainbow = ''.join(f'<path d="M{200 - r} 380 A{r} {r} 0 0 1 {200 + r} 380" stroke="{c}" stroke-width="13" fill="none"/>' for r, c in ((175, t), (162, m), (149, s)))
        return f'<g opacity=".9" transform="translate(0 0)">{rainbow}</g>' + sun + cloud + drops
    if name == 'tasbih':
        import math
        beads = ''.join(f'<circle cx="{200 + 130 * math.cos(2 * math.pi * i / 33 - math.pi / 2):.1f}" '
                        f'cy="{185 + 130 * math.sin(2 * math.pi * i / 33 - math.pi / 2):.1f}" r="13" '
                        f'fill="{t if i % 11 == 0 else (m if i % 2 else "#C98A55")}"/>' for i in range(33))
        return (beads + f'<path d="M200 315 v40" stroke="{t}" stroke-width="5"/><path d="M188 352 h24 l6 40 h-36Z" fill="{t}"/>'
                + star(200, 185, 46, s) + flower(330, 330, 22, b) + sprig(40, 360, -20, 1))
    if name == 'teacup':
        steam = ''.join(f'<path d="M{x} 140 q-18 -25 0 -50 t0 -50" stroke="{C["leaf"]}" stroke-width="7" fill="none" stroke-linecap="round" opacity=".8"/>' for x in (165, 205, 245))
        return (f'<ellipse cx="200" cy="320" rx="150" ry="28" fill="{m}"/><ellipse cx="200" cy="314" rx="110" ry="16" fill="#E7BF6E"/>'
                f'<path d="M95 160 h210 v40 a105 110 0 0 1 -210 0Z" fill="{s}"/>'
                f'<path d="M300 185 a40 40 0 1 1 0 80" stroke="{s}" stroke-width="16" fill="none"/>'
                f'<ellipse cx="200" cy="160" rx="105" ry="16" fill="#3F5E48"/>' + steam + heart(200, 225, .9, b)
                + f'<path d="M330 70 a34 34 0 1 0 22 58 a28 28 0 1 1 -22 -58Z" fill="{t}"/>')
    if name == 'night':
        stars = ''.join(star(x, y, r, m if i % 2 else '#fff') for i, (x, y, r) in enumerate(
            [(80, 80, 14), (320, 60, 10), (300, 150, 16), (110, 170, 9), (360, 230, 9), (60, 250, 11), (200, 40, 8)]))
        return (f'<rect x="20" y="20" width="360" height="360" rx="180" fill="{C["blue"]}"/>'
                f'<path d="M230 90 a85 85 0 1 0 60 145 a70 70 0 1 1 -60 -145Z" fill="{m}"/>' + stars
                + f'<path d="M20 300 q90 -60 180 0 t180 0 v0 a180 180 0 0 1 -360 0Z" fill="{s}"/>'
                + f'<path d="M40 330 q80 -40 160 0 t160 0 a180 180 0 0 1 -320 0Z" fill="#3F5E48"/>')
    if name == 'bubbles':
        dots = ''.join(f'<circle cx="{x}" cy="160" r="11" fill="#fff"/>' for x in (120, 160, 200))
        return (f'<path d="M50 80 h200 a35 35 0 0 1 35 35 v90 a35 35 0 0 1 -35 35 H120 l-45 40 l6 -40 H50 a35 35 0 0 1 -35 -35 V115 a35 35 0 0 1 35 -35Z" fill="{t}"/>'
                + dots + f'<path d="M150 190 h200 a35 35 0 0 1 35 35 v80 a35 35 0 0 1 -35 35 h-30 l6 40 l-45 -40 H150 a35 35 0 0 1 -35 -35 v-80 a35 35 0 0 1 35 -35Z" fill="{s}"/>'
                + heart(250, 262, 1.2, b) + flower(345, 75, 24, m, t))
    if name == 'mats':
        def mat(x, y, w, h, fill, border):
            return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}"/>'
                    f'<rect x="{x + w * .1}" y="{y + h * .06}" width="{w * .8}" height="{h * .88}" rx="4" fill="none" stroke="{border}" stroke-width="5"/>'
                    f'<path d="M{x + w * .25} {y + h * .45} v-{h * .12} a{w * .25} {w * .25} 0 0 1 {w * .5} 0 v{h * .12}Z" fill="{border}"/>'
                    + ''.join(f'<path d="M{x + w * k / 8} {y + h} v14" stroke="{border}" stroke-width="3"/>' for k in range(1, 8)))
        return (mat(60, 60, 170, 290, t, m) + mat(250, 160, 110, 190, s, C['sand'])
                + heart(305, 115, .7, t) + sprig(30, 385, -15, 1))
    if name == 'sunrise':
        rays = ''.join(f'<rect x="196" y="95" width="8" height="40" rx="4" fill="{m}" transform="rotate({a} 200 270)"/>' for a in range(-80, 81, 20))
        return (f'<path d="M20 270 A180 180 0 0 1 380 270Z" fill="{C["sand"]}"/>' + rays
                + f'<path d="M110 270 a90 90 0 0 1 180 0Z" fill="{m}"/>'
                + f'<path d="M150 270 v-60 h100 v60Z M160 212 a40 42 0 0 1 80 0Z" fill="{br}"/><path d="M196 172 v-14" stroke="{br}" stroke-width="4"/>'
                + f'<rect x="270" y="150" width="18" height="120" fill="{br}"/><path d="M266 152 l13 -30 l13 30Z" fill="{br}"/>'
                + f'<rect x="20" y="268" width="360" height="14" rx="7" fill="{s}"/>'
                + star(80, 90, 10, t) + star(330, 70, 8, t) + sprig(260, 340, -10, 1.3))
    if name == 'quran':
        lines = ''.join(f'<path d="M{110 + (5 if side else 0)} {y} h70" stroke="{C["leaf"]}" stroke-width="5" stroke-linecap="round" transform="translate({100 if side else 0} 0)"/>'
                        for side in (0, 1) for y in (150, 172, 194, 216))
        return (f'<path d="M110 330 L290 230 M290 330 L110 230" stroke="{br}" stroke-width="18" stroke-linecap="round"/>'
                f'<path d="M200 120 Q140 95 80 110 V260 Q140 245 200 270Z" fill="{te}"/><path d="M200 120 Q260 95 320 110 V260 Q260 245 200 270Z" fill="{te}"/>'
                f'<path d="M200 130 Q145 108 92 120 V250 Q145 238 200 258Z" fill="#fff"/><path d="M200 130 Q255 108 308 120 V250 Q255 238 200 258Z" fill="#fff"/>'
                + lines + star(200, 70, 18, m) + flower(345, 330, 22, b) + sprig(30, 80, 20, 1))
    if name == 'lantern':
        panes = ''.join(f'<path d="M{x} 150 h28 v120 h-28Z" fill="{c}"/>' for x, c in ((152, '#F3C566'), (186, '#F8D98C'), (220, '#F3C566')))
        return (f'<path d="M200 20 v40" stroke="{br}" stroke-width="4"/><circle cx="200" cy="66" r="10" fill="none" stroke="{br}" stroke-width="5"/>'
                f'<path d="M150 125 L200 75 L250 125Z" fill="{t}"/><rect x="138" y="122" width="124" height="20" rx="6" fill="{br}"/>'
                f'<path d="M140 142 h120 l-8 136 h-104Z" fill="{t}"/>' + panes
                + f'<rect x="138" y="275" width="124" height="20" rx="6" fill="{br}"/><path d="M160 295 h80 l-20 30 h-40Z" fill="{t}"/>'
                + f'<path d="M320 60 a40 40 0 1 0 30 70 a33 33 0 1 1 -30 -70Z" fill="{m}"/>' + star(80, 90, 12, m) + star(330, 230, 9, t)
                + sprig(40, 370, -20, 1.1))
    if name == 'dates':
        dates = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="30" ry="17" fill="{c}" transform="rotate({r} {x} {y})"/>' for x, y, r, c in
                        [(150, 225, -20, '#6B3A22'), (205, 215, 10, '#7A4329'), (255, 228, -10, '#6B3A22'), (178, 240, 25, '#5A2F1B'), (232, 245, -30, '#7A4329')])
        return (dates + f'<path d="M80 240 h240 a120 85 0 0 1 -240 0Z" fill="{t}"/><path d="M95 255 h210" stroke="{m}" stroke-width="5"/>'
                + f'<path d="M290 60 a45 45 0 1 0 34 78 a37 37 0 1 1 -34 -78Z" fill="{m}"/>' + star(110, 90, 12, m) + star(200, 60, 8, t)
                + sprig(250, 370, -10, 1.1))
    return heart(200, 200, 4, C['terra'])

def svg(name):
    return f'<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">{icon(name)}</svg>'

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet">'

def page(slug, headline, kicker, ic, tint, tall):
    bg = C[tint]
    deco = (flower(50, 745, 26, C['blush']) + flower(95, 770, 14, C['sand'], C['terra']) + sprig(120, 760, -20, 1.1)) if not tall else \
           (flower(70, 70, 34, C['blush']) + flower(930, 1330, 30, C['blush']) + sprig(20, 150, 40, 1.4) + sprig(840, 1320, 200, 1.3))
    W, H = (1000, 1500) if tall else (1200, 800)
    if tall:
        body = f'''<div class="blob" style="left:110px;top:90px;width:780px;height:780px"></div>
<div class="art" style="left:140px;top:110px;width:720px;height:720px">{svg(ic)}</div>
<div class="txt" style="left:80px;right:80px;top:930px;text-align:center">
<div class="kick">{html.escape(kicker)}</div><h1 style="font-size:92px">{html.escape(headline)}</h1>
<p class="tag">Heart first. Habit second.</p></div>
<div class="foot">Read the full guide · islamicparenting101.com</div>'''
    else:
        body = f'''<div class="blob" style="left:620px;top:80px;width:540px;height:540px"></div>
<div class="art" style="left:645px;top:105px;width:490px;height:490px">{svg(ic)}</div>
<div class="txt" style="left:80px;width:510px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center">
<div class="kick">{html.escape(kicker)}</div><h1>{html.escape(headline)}</h1>
<p class="tag">Heart first. Habit second.</p><div class="brand">Islamic Parenting 101</div></div>'''
    return f'''<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
*{{margin:0;box-sizing:border-box}}html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{background:{C['cream'] if tall else '#FFFDF9'};position:relative;font-family:Lato,sans-serif;color:{C['brown']}}}
.blob{{position:absolute;border-radius:50%;background:{bg}}}.art{{position:absolute}}.art svg{{width:100%;height:100%}}
.deco{{position:absolute;inset:0}}.txt{{position:absolute}}
.kick{{font-weight:900;letter-spacing:.2em;color:{C['terra']};font-size:{26 if tall else 22}px;margin-bottom:18px}}
h1{{font-family:'Playfair Display',serif;font-weight:800;font-size:72px;line-height:1.08}}
.tag{{font-family:'Playfair Display',serif;font-style:italic;font-size:{36 if tall else 30}px;color:{C['sage']};margin-top:22px}}
.brand{{margin-top:40px;font-weight:900;font-size:22px;color:{C['teal']};border-top:3px solid {C['mustard']};padding-top:14px;width:max-content}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:120px;background:{C['terra']};color:#fff;font-weight:900;font-size:34px;display:flex;align-items:center;justify-content:center}}
</style></head><body><svg class="deco" viewBox="0 0 {W} {H}">{deco}</svg>{body}</body></html>'''

def meta_of(path):
    txt = open(path, encoding='utf-8').read()
    fm = re.match(r'---\n(.*?)\n---', txt, re.S).group(1)
    return dict(l.split(':', 1) for l in fm.splitlines() if ':' in l)

def main():
    want = set(sys.argv[1:])
    os.makedirs('img/articles', exist_ok=True); os.makedirs('pins', exist_ok=True)
    tmp = tempfile.mkdtemp()
    jobs = []
    for p in sorted(glob.glob('posts/*.md')):
        slug = os.path.basename(p)[:-3]
        if want and slug not in want:
            continue
        m = {k.strip(): v.strip() for k, v in meta_of(p).items()}
        headline, ic, tint = ART.get(slug, (m['title'].split(':')[0], 'hearts', 'blush'))
        kicker = m.get('kicker', 'ISLAMIC PARENTING')
        for tall, out, w, h in ((False, f'img/articles/{slug}.jpg', 1200, 800), (True, f'pins/{slug}.jpg', 1000, 1500)):
            src = os.path.join(tmp, f'{slug}-{int(tall)}.html')
            open(src, 'w', encoding='utf-8').write(page(slug, headline, kicker, ic, tint, tall))
            jobs.append({'src': src, 'out': os.path.abspath(out), 'w': w, 'h': h})
    json.dump(jobs, open(os.path.join(tmp, 'jobs.json'), 'w'))
    subprocess.run(['node', os.path.join(os.path.dirname(__file__), 'render_images.js'), os.path.join(tmp, 'jobs.json')], check=True)
    print(f'rendered {len(jobs)} images')

if __name__ == '__main__':
    main()
