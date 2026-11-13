#!/usr/bin/env python3
"""
The GEMIS email signatures.

    python3 tools/make-signatures.py

    node tools/render-signatures.mjs      # then: the art panels and the PNGs

Writes one HTML signature per person into brand/email-signatures/, a preview
page that shows them all with copy buttons, and a README with the steps for
Outlook, Gmail and Apple Mail. Email clients strip stylesheets and ignore
most CSS, so each signature is a table with inline styles and system-font
fallbacks behind Montserrat.

The design is the site's stepped block laid on its side: a midnight art panel
on the left (the vertical hatch, two light streaks, the stone, the person's
initials as a giant light numeral, a vertical label, the notch cut top right),
the white panel with the name in the site's uppercase light heading and the
contact lines as a "+" list, and the navy strip beneath carrying the one
action — Book a discovery session. The art panel is the one hosted image per
person (this script writes its SVG source to assets/img/email/src/;
render-signatures.mjs rasterises it at 2× and also exports every signature
as a PNG). With images blocked the panel is a navy cell with the name in it.
There is no phone number anywhere on the site, so none here either.
"""
import os
import re

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(R, 'brand', 'email-signatures')
LIVE = 'https://sphamandla-designer.github.io/gemis-site/'
ART = LIVE + 'assets/img/email/'          # + sig-<slug>.png, the art panel
SRC = os.path.join(R, 'assets', 'img', 'email', 'src')
MARK = os.path.join(R, 'assets', 'img', 'logos', 'gemis-mark.svg')
SITE = 'https://www.gemis.co.za'
BOOK = LIVE + 'contact.html'
LINKEDIN = 'https://www.linkedin.com/company/gem-information-systems-pty-ltd/'

NAVY, MUTE, FAINT, LINE = '#0a1230', '#4a5068', '#7a7f93', '#d9dce5'
FONT = "Montserrat, 'Segoe UI', Helvetica, Arial, sans-serif"

STAFF = [
    {'slug': 'sphamandla-xaba', 'name': 'Sphamandla Xaba', 'role': 'UI/UX Designer', 'email': 'sphamandla@gemis.co.za'},
    {'slug': 'leon-small', 'name': 'Leon Small', 'role': 'Director', 'email': 'leon@gemis.co.za'},
    {'slug': 'vanessa-davis', 'name': 'Vanessa Davis', 'role': 'Senior Full Stack Developer', 'email': 'vanessa@gemis.co.za'},
]


def initials(p):
    return ''.join(w[0] for w in p['name'].split()[:2]).upper()


def art(p):
    """The art panel as SVG (180×170 at 1×): the stepped midnight block with the site's patterns."""
    mark = re.sub(r'</?svg[^>]*>', '', open(MARK, encoding='utf-8').read()).strip()
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="180" height="170" viewBox="0 0 180 170" role="img" aria-label="GEMIS — {p['name']}">
  <defs>
    <pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="1" height="6" fill="#ffffff" opacity=".085"/></pattern>
    <pattern id="dots" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".75" fill="#ffffff" opacity=".38"/></pattern>
    <linearGradient id="streak" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#ffffff" stop-opacity="0"/><stop offset=".5" stop-color="#ffffff" stop-opacity=".55"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>
    <clipPath id="step"><path d="M0 0H122V22H180V170H0Z"/></clipPath>
  </defs>
  <g clip-path="url(#step)">
    <rect width="180" height="170" fill="{NAVY}"/>
    <rect width="180" height="170" fill="url(#hatch)"/>
    <rect x="0" y="96" width="78" height="74" fill="url(#dots)"/>
    <g fill="none" stroke="url(#streak)" stroke-width="1.2"><path d="M-10 186L250-34"/><path d="M-10 162L250-58" opacity=".55"/></g>
    <text x="106" y="166" fill="#ffffff" font-family="Montserrat, Helvetica, Arial, sans-serif" font-weight="200" font-size="92" letter-spacing="-5" text-anchor="middle" opacity=".92">{initials(p)}</text>
    <text transform="translate(17 160) rotate(-90)" fill="#ffffff" opacity=".58" font-family="Montserrat, Helvetica, Arial, sans-serif" font-weight="500" font-size="6.6" letter-spacing="1.1">GEM INFORMATION SYSTEMS</text>
    <g transform="translate(30 18) scale(.5)" fill="#ffffff">{mark}</g>
    <path d="M122 0V22H180" fill="none" stroke="#ffffff" stroke-opacity=".3"/>
  </g>
</svg>
'''


def signature(p):
    """The signature as a self-contained fragment: paste it into the client's signature editor."""
    L = "font-family:" + FONT + ";"
    return f'''<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;border-spacing:0;{L}color:{NAVY};width:100%;max-width:560px;">
  <tr>
    <td width="180" bgcolor="{NAVY}" style="padding:0;vertical-align:top;width:180px;background:{NAVY};">
      <a href="{SITE}" target="_blank" style="text-decoration:none;display:block;"><img src="{ART}sig-{p['slug']}.png" width="180" height="170" alt="GEMIS — {p['name']}" style="display:block;width:180px;height:170px;border:0;outline:none;{L}color:#ffffff;font-size:11px;letter-spacing:.14em;text-transform:uppercase;padding:0;"></a>
    </td>
    <td bgcolor="#ffffff" style="padding:20px 20px 16px 24px;vertical-align:top;background:#ffffff;border-top:1px solid {LINE};border-right:1px solid {LINE};">
      <p style="margin:0;{L}font-size:19px;line-height:25px;font-weight:300;letter-spacing:.08em;text-transform:uppercase;color:{NAVY};">{p['name']}</p>
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;margin:9px 0 8px;"><tr><td width="28" height="2" bgcolor="{NAVY}" style="width:28px;height:2px;line-height:2px;font-size:2px;background:{NAVY};">&nbsp;</td></tr></table>
      <p style="margin:0 0 12px;{L}font-size:10px;line-height:15px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:{MUTE};">{p['role']}</p>
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;width:100%;">
        <tr><td style="padding:7px 0;border-top:1px solid {LINE};{L}font-size:13px;line-height:18px;color:{NAVY};white-space:nowrap;"><span style="display:inline-block;width:16px;font-weight:300;color:{NAVY};">+</span><a href="mailto:{p['email']}" style="color:{NAVY};text-decoration:none;">{p['email']}</a></td></tr>
        <tr><td style="padding:7px 0;border-top:1px solid {LINE};{L}font-size:13px;line-height:18px;color:{NAVY};white-space:nowrap;"><span style="display:inline-block;width:16px;font-weight:300;color:{NAVY};">+</span><a href="{SITE}" target="_blank" style="color:{NAVY};text-decoration:none;">www.gemis.co.za</a></td></tr>
      </table>
    </td>
  </tr>
  <tr>
    <td colspan="2" bgcolor="{NAVY}" style="padding:0;background:{NAVY};">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;width:100%;">
        <tr>
          <td style="padding:12px 20px 12px 24px;{L}font-size:10px;line-height:16px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;white-space:nowrap;"><a href="{BOOK}" target="_blank" style="color:#ffffff;text-decoration:none;">Book a discovery session&nbsp;&nbsp;&rarr;</a></td>
          <td align="right" style="padding:12px 20px 12px 10px;{L}font-size:9px;line-height:16px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:#8d93ab;text-align:right;white-space:nowrap;">Est. 2014</td>
        </tr>
      </table>
    </td>
  </tr>
</table>'''


def plain(p):
    return (f"{p['name']}\n{p['role']} · GEMIS\n{p['email']} · www.gemis.co.za\n"
            f"GEM Information Systems · Cape Town · since 2014\nBook a discovery session: {BOOK}\n")


def page(title, body):
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<title>{title}</title>
<link rel="icon" type="image/svg+xml" href="../../assets/img/favicon.svg">
<link rel="preload" href="../../assets/fonts/montserrat-latin.woff2" as="font" type="font/woff2" crossorigin>
<style>
@font-face{{font-family:Montserrat;src:url(../../assets/fonts/montserrat-latin.woff2) format("woff2");font-weight:100 900;font-display:swap}}
html,body{{margin:0;background:#f3f4f7;color:{NAVY};font-family:{FONT}}}
.wrap{{max-width:760px;margin:0 auto;padding:48px 24px 80px}}
h1{{margin:0 0 8px;font-size:22px;font-weight:300;letter-spacing:.04em;text-transform:uppercase}}
.lede{{margin:0 0 36px;font-size:15px;line-height:1.6;color:{MUTE}}}
.card{{background:#fff;border:1px solid {LINE};padding:28px;margin:0 0 28px}}
.card h2{{margin:0 0 18px;font-size:11px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:{FAINT}}}
.sig{{padding:8px 0 20px;overflow-x:auto;-webkit-overflow-scrolling:touch}}
.sig table{{font-family:{FONT}}}
.row{{display:flex;flex-wrap:wrap;gap:10px;align-items:center;border-top:1px solid {LINE};padding-top:16px}}
button,.btn{{font:inherit;font-size:11px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;padding:12px 18px;border:1px solid {NAVY};background:{NAVY};color:#fff;cursor:pointer;text-decoration:none}}
.btn--ghost{{background:transparent;color:{NAVY}}}
.ok{{font-size:12px;color:{MUTE}}}
.note{{font-size:13px;line-height:1.6;color:{MUTE}}}
.note code{{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;background:#eef0f4;padding:1px 5px}}
</style></head><body><div class="wrap">{body}</div>
<script>
document.querySelectorAll('[data-copy]').forEach(function(b){{b.addEventListener('click',async function(){{var el=document.getElementById(b.getAttribute('data-copy'));var html=el.innerHTML,text=el.innerText;try{{await navigator.clipboard.write([new ClipboardItem({{'text/html':new Blob([html],{{type:'text/html'}}),'text/plain':new Blob([text],{{type:'text/plain'}})}})]);}}catch(e){{var r=document.createRange();r.selectNodeContents(el);var s=getSelection();s.removeAllRanges();s.addRange(r);document.execCommand('copy');s.removeAllRanges();}}var ok=b.parentElement.querySelector('.ok');if(ok){{ok.textContent='Copied — paste it into your email signature.';setTimeout(function(){{ok.textContent='';}},4000);}}}});}});
</script></body></html>'''


os.makedirs(OUT, exist_ok=True)
os.makedirs(SRC, exist_ok=True)
cards = []
for p in STAFF:
    sig = signature(p)
    open(os.path.join(SRC, p['slug'] + '.svg'), 'w', encoding='utf-8').write(art(p))
    open(os.path.join(OUT, p['slug'] + '.html'), 'w', encoding='utf-8').write(
        '<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><title>' + p['name'] + ' — GEMIS email signature</title></head>\n<body style="margin:0;padding:24px;background:#ffffff;">\n' + sig + '\n</body></html>\n')
    open(os.path.join(OUT, p['slug'] + '.txt'), 'w', encoding='utf-8').write(plain(p))
    cards.append(f'''<section class="card" id="c-{p['slug']}">
  <h2>{p['name']} &nbsp;·&nbsp; {p['role']}</h2>
  <div class="sig" id="sig-{p['slug']}">{sig}</div>
  <div class="row"><button type="button" data-copy="sig-{p['slug']}">Copy signature</button><a class="btn btn--ghost" href="{p['slug']}.html" target="_blank">Open on its own</a><a class="btn btn--ghost" href="{p['slug']}.png" download>PNG</a><a class="btn btn--ghost" href="{p['slug']}.txt" download>Plain text</a><span class="ok" aria-live="polite"></span></div>
</section>''')

body = ('<h1>GEMIS email signatures</h1>'
        '<p class="lede">Press <strong>Copy signature</strong>, then paste into your mail client\'s signature editor (Outlook, Gmail, Apple Mail). '
        'The navy panel is a hosted image, so it appears once the message is opened online; the rest is live text and stays sharp everywhere. '
        '<strong>PNG</strong> downloads the whole signature as one picture, for a client that only takes an image.</p>'
        + '\n'.join(cards) +
        '<section class="card"><h2>Setting it up</h2><p class="note"><strong>Outlook (new, Mac, web):</strong> Settings → Mail → Compose and reply → New signature → paste → Save. '
        '<strong>Outlook (classic Windows):</strong> File → Options → Mail → Signatures → New → paste into the editor. '
        '<strong>Gmail:</strong> Settings → See all settings → General → Signature → Create new → paste → Save changes. '
        '<strong>Apple Mail:</strong> Settings → Signatures → + → paste, and untick <em>Always match my default message font</em>. '
        '<strong>iPhone:</strong> paste into Settings → Mail → Signature (iOS keeps the text; the tile may not show). '
        'If a client asks for the code instead, open the signature on its own and copy the page source, or use the <code>.html</code> file.</p></section>')
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page('GEMIS email signatures', body))

open(os.path.join(OUT, 'README.md'), 'w', encoding='utf-8').write(f'''# GEMIS email signatures

One signature per person, generated by `tools/make-signatures.py` (add a person to
`STAFF` there, re-run it, then `node tools/render-signatures.mjs`). Live preview with copy buttons:
{LIVE}brand/email-signatures/

| Person | Role | File |
|---|---|---|
''' + ''.join(f"| {p['name']} | {p['role']} | `{p['slug']}.html` (+ `.png`, `.txt`) |\n" for p in STAFF) + f'''
## How they are built

- A table with inline styles: email clients strip stylesheets.
- Montserrat where it is installed, falling back to Segoe UI, Helvetica, Arial.
- One hosted image per person, the art panel (`assets/img/email/sig-<slug>.png`,
  served at 2× and shown at 180×170): the stepped midnight block with the vertical
  hatch, two light streaks, the stone, the initials as a giant light numeral and
  the notch. Its source is `assets/img/email/src/<slug>.svg`, rasterised by
  `node tools/render-signatures.mjs`, which also exports every signature as a
  PNG (`<slug>.png` here) for a client that only takes an image. With images
  blocked the cell is still navy, with the name as alt text.
- The brand's one accent (midnight navy `#0a1230`), tracked uppercase labels,
  hairlines, and the site's single action, *Book a discovery session*.
- No phone number: the site carries none (owner's instruction, 2026-10-23).
- Width is fluid up to 560px, so it reads on a phone.

## Installing

- **Outlook (new, Mac, web):** Settings → Mail → Compose and reply → New signature → paste → Save.
- **Outlook (classic Windows):** File → Options → Mail → Signatures → New → paste.
- **Gmail:** Settings → See all settings → General → Signature → Create new → paste → Save changes.
- **Apple Mail:** Settings → Signatures → + → paste; untick *Always match my default message font*.
- **iPhone / Android:** the plain-text `.txt` version is the safe choice.
''')
print('signatures:', ', '.join(p['slug'] for p in STAFF))
