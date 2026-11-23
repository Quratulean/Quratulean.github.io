#!/usr/bin/env python3
"""Builds the form pages (free gift, thank-you, contact) with the site's header/footer from about.html.
Run from repo root: python3 tools/pages.py   (publish.py calls shell() the same way)"""
import re, html, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SIGNUP_FORM = '''<div class="ml-embedded" data-form="JjOyLM"></div>'''
def shell():
    src = open('about.html', encoding='utf-8').read()
    head, rest = src.split('<main>', 1); _, foot = rest.split('</main>', 1)
    return head, foot
def page(fname, title, desc, body, noindex=False, on=None):
    head, foot = shell()
    head = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)} — Islamic Parenting 101</title>', head, flags=re.S)
    head = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{html.escape(desc)}">', head)
    head = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{html.escape(title)}">', head)
    head = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{html.escape(desc)}">', head)
    head = re.sub(r' class=on', '', head)
    if on: head = head.replace(f'<a href="{on}">', f'<a href="{on}" class=on>', 1)
    if noindex: head = head.replace('</head>', '<meta name="robots" content="noindex,nofollow">\n</head>', 1)
    open(fname, 'w', encoding='utf-8').write(head + '<main>' + body + '</main>' + foot)

page('free-starter-kit.html', 'Free Calm Mama Starter Kit',
 'Get the free Calm Mama Starter Kit: 4 printable cards for gentler, calmer days with your children — phrases, Sunnah calm-down steps, bedtime routine and a weekly planner.',
 f'''<section class="wrap art" style="max-width:980px"><div class="kit"><img class="cover" src="img/cover.jpg" alt="Hearts Before Habits" style="max-width:300px"><div>
<div class="kick">FREE GIFT</div><h1>The Calm Mama Starter Kit</h1>
<p class="lead">Four printable cards for gentler, calmer days with your children. Stick them on the fridge and start with just one.</p>
<ul class="chk"><li><b>10 Phrases Every Child Needs to Hear</b> — words that build confidence and faith</li><li><b>7 Sunnah Steps Before You Raise Your Voice</b> — what to do in the heat of the moment</li><li><b>A Calm Bedtime Routine</b> — ten minutes, with du'as</li><li><b>Your One Step This Week</b> — a simple planner so change actually sticks</li></ul>
<div class="signup" hidden style="margin-top:20px"><h3>Where should I send it?</h3>{SIGNUP_FORM}</div>
<p class="needs-signup-off sm" id="soon">The free kit sign-up opens very soon. In the meantime, enjoy the <a href="printables.html">free printables</a> and <a href="articles.html">articles</a>.</p>
</div></div></section>
<script>document.addEventListener("DOMContentLoaded",function(){{if(window.SITE_FORMS&&window.SITE_FORMS.signup){{var s=document.getElementById("soon");if(s)s.hidden=true;}}}});</script>''', on='free-starter-kit.html')

page('thank-you.html', 'Thank you', 'Your free Calm Mama Starter Kit is ready to download.',
 '''<section class="wrap art c"><div class="kick">THANK YOU</div><h1>Your kit is ready</h1>
<p class="lead">Jazakillahu khayran for joining. Download your <b>Calm Mama Starter Kit</b> below, print it, and choose <b>one</b> card to start with this week.</p>
<p><a class="btn" href="gift/calm-mama-starter-kit.pdf" download>Download the Starter Kit (PDF)</a></p>
<p class="sm">Tip: print on A4 or US Letter ("fit to page"). Stick card 1 on the fridge and card 3 by the bedroom door.</p>
<p>While you are here: start with <a href="gentle-parenting-in-islam.html">Gentle Parenting in Islam: The Complete Guide</a>, or <a href="how-to-stop-yelling-at-your-kids.html">How to Stop Yelling at Your Kids</a>.</p></section>''', noindex=True)

page('contact.html', 'Contact', 'Send a message to Tabasum Majeed at Islamic Parenting 101 — questions, feedback or ideas for articles.',
 '''<section class="wrap art"><div class="kick">CONTACT</div><h1>Say salam</h1>
<p class="lead">Questions, feedback, or a topic you would love me to write about? I read every message.</p>
<div class="needs-contact" hidden><form class="cform contact-form" novalidate>
<input type="text" name="name" placeholder="Your name" required autocomplete="name"><input type="email" name="email" placeholder="Your email" required autocomplete="email">
<input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"><textarea name="message" placeholder="Your message" required></textarea>
<button class="btn" type="submit">Send message</button><p class="fnote" role="status"></p></form>
<p class="tiny">Your details are used only to reply to you. For religious rulings, please ask a qualified scholar.</p></div>
<div class="contact-fallback" hidden><p>The message form opens very soon. For now, please message me on <a href="https://www.pinterest.com/digitalallio428/" target="_blank" rel="noopener">Pinterest</a>.</p></div></section>''', on='contact.html')
print('built free-starter-kit.html, thank-you.html, contact.html')
