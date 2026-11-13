#!/usr/bin/env python3
"""
The GEMIS email signatures.

    python3 tools/make-signatures.py

Writes one HTML signature per person into brand/email-signatures/, a preview
page that shows them all with copy buttons, and a README with the steps for
Outlook, Gmail and Apple Mail. Email clients strip stylesheets and ignore
most CSS, so each signature is a table with inline styles, system-font
fallbacks behind Montserrat, and one hosted image (the midnight tile with the
stone) that degrades to a navy square with alt text when images are blocked.
The copy follows the site: one accent (midnight navy), tracked uppercase
labels, hairlines, and the single action — Book a discovery session. There is
no phone number anywhere on the site, so none here either.
"""
import os

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(R, 'brand', 'email-signatures')
LIVE = 'https://sphamandla-designer.github.io/gemis-site/'
TILE = LIVE + 'assets/img/email/sig-tile.png'
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


def signature(p):
    """The signature as a self-contained fragment: paste it into the client's signature editor."""
    return f'''<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;border-spacing:0;font-family:{FONT};color:{NAVY};width:100%;max-width:560px;">
  <tr>
    <td style="padding:0 20px 0 0;vertical-align:top;width:64px;">
      <a href="{SITE}" target="_blank" style="text-decoration:none;display:block;"><img src="{TILE}" width="64" height="64" alt="GEMIS" style="display:block;width:64px;height:64px;border:0;outline:none;color:{NAVY};font-weight:600;font-size:11px;letter-spacing:.14em;text-align:center;line-height:64px;"></a>
    </td>
    <td style="padding:0 0 0 20px;vertical-align:top;border-left:1px solid {LINE};">
      <p style="margin:0;font-family:{FONT};font-size:17px;line-height:22px;font-weight:600;letter-spacing:.01em;color:{NAVY};">{p['name']}</p>
      <p style="margin:5px 0 0;font-family:{FONT};font-size:11px;line-height:16px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:{MUTE};">{p['role']}&nbsp;&nbsp;<span style="color:{LINE};">|</span>&nbsp;&nbsp;GEMIS</p>
      <p style="margin:12px 0 0;font-family:{FONT};font-size:13px;line-height:20px;color:{NAVY};">
        <a href="mailto:{p['email']}" style="color:{NAVY};text-decoration:none;">{p['email']}</a>
        <span style="color:{LINE};">&nbsp;&nbsp;|&nbsp;&nbsp;</span>
        <a href="{SITE}" target="_blank" style="color:{NAVY};text-decoration:none;">www.gemis.co.za</a>
      </p>
    </td>
  </tr>
  <tr>
    <td colspan="2" style="padding:16px 0 0;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;border-spacing:0;width:100%;">
        <tr>
          <td style="padding:10px 0 0;border-top:1px solid {LINE};font-family:{FONT};font-size:10px;line-height:15px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:{FAINT};">GEM Information Systems&nbsp;&nbsp;<span style="color:{LINE};">·</span>&nbsp;&nbsp;Cape Town&nbsp;&nbsp;<span style="color:{LINE};">·</span>&nbsp;&nbsp;Since 2014</td>
        </tr>
        <tr>
          <td style="padding:6px 0 0;font-family:{FONT};font-size:10px;line-height:15px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;"><a href="{BOOK}" target="_blank" style="color:{NAVY};text-decoration:none;">Book a discovery session&nbsp;&rarr;</a></td>
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
.sig{{padding:8px 0 20px}}
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
cards = []
for p in STAFF:
    sig = signature(p)
    open(os.path.join(OUT, p['slug'] + '.html'), 'w', encoding='utf-8').write(
        '<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><title>' + p['name'] + ' — GEMIS email signature</title></head>\n<body style="margin:0;padding:24px;background:#ffffff;">\n' + sig + '\n</body></html>\n')
    open(os.path.join(OUT, p['slug'] + '.txt'), 'w', encoding='utf-8').write(plain(p))
    cards.append(f'''<section class="card" id="c-{p['slug']}">
  <h2>{p['name']} &nbsp;·&nbsp; {p['role']}</h2>
  <div class="sig" id="sig-{p['slug']}">{sig}</div>
  <div class="row"><button type="button" data-copy="sig-{p['slug']}">Copy signature</button><a class="btn btn--ghost" href="{p['slug']}.html" target="_blank">Open on its own</a><a class="btn btn--ghost" href="{p['slug']}.txt" download>Plain text</a><span class="ok" aria-live="polite"></span></div>
</section>''')

body = ('<h1>GEMIS email signatures</h1>'
        '<p class="lede">Press <strong>Copy signature</strong>, then paste into your mail client\'s signature editor (Outlook, Gmail, Apple Mail). '
        'The tile is a hosted image, so it appears once the message is opened online; the rest is live text and stays sharp everywhere.</p>'
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
`STAFF` there and re-run). Live preview with copy buttons:
{LIVE}brand/email-signatures/

| Person | Role | File |
|---|---|---|
''' + ''.join(f"| {p['name']} | {p['role']} | `{p['slug']}.html` (+ `.txt`) |\n" for p in STAFF) + f'''
## How they are built

- A table with inline styles: email clients strip stylesheets.
- Montserrat where it is installed, falling back to Segoe UI, Helvetica, Arial.
- One hosted image, the midnight tile with the stone (`assets/img/email/sig-tile.png`,
  served at 2× and shown at 64px). With images blocked the cell still shows a navy
  square with "GEMIS" as alt text.
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
