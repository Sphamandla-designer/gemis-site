#!/usr/bin/env python3
"""
Static font cuts for the brand pieces, made from the site's own variable fonts.

    python3 tools/make-static-fonts.py      # needs fonttools (pip install fonttools brotli)

Word cannot use a variable font, and Chromium writes a variable font into a PDF as
Type 3 outlines, which printers dislike. So each weight the letterheads, cards and
signatures use is instanced to its own static TrueType file in brand/fonts/, each
named as its own family ("Montserrat SemiBold", "Manrope Light") with the Regular
style, so Word can embed and select it without bold or italic flags. The licence
travels with each family (all three are SIL Open Font License 1.1).
"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(R, 'brand', 'fonts')
FAMILIES = [
    ('Montserrat', 'assets/fonts/montserrat-latin.woff2', [(200, 'ExtraLight'), (300, 'Light'), (400, 'Regular'), (500, 'Medium'), (600, 'SemiBold')]),
    ('Manrope', 'assets/fonts/manrope-latin-wght-normal.woff2', [(300, 'Light'), (400, 'Regular'), (500, 'Medium'), (600, 'SemiBold')]),
    ('JetBrains Mono', 'assets/fonts/jetbrains-mono-latin-wght-normal.woff2', [(400, 'Regular'), (500, 'Medium')]),
]
OFL_BODY = open(os.path.join(R, 'assets/fonts/MONTSERRAT-LICENSE.txt'), encoding='utf-8').read().split('\n', 1)[1]

os.makedirs(OUT, exist_ok=True)
for family, src, cuts in FAMILIES:
    for w, cut in cuts:
        f = instancer.instantiateVariableFont(TTFont(os.path.join(R, src)), {'wght': w})
        f.flavor = None
        f.recalcTimestamp = False  # keep the source's date, so a re-run writes the same bytes
        name = family if w == 400 else f'{family} {cut}'
        ps = family.replace(' ', '') + '-' + cut
        nm = f['name']
        for rid in (1, 2, 3, 4, 6, 16, 17):
            nm.removeNames(nameID=rid)
        nm.setName(name, 1, 3, 1, 0x409)
        nm.setName('Regular', 2, 3, 1, 0x409)
        nm.setName(f'GEMIS:{name}:static', 3, 3, 1, 0x409)
        nm.setName(name, 4, 3, 1, 0x409)
        nm.setName(ps, 6, 3, 1, 0x409)
        f['OS/2'].usWeightClass = w
        f['OS/2'].fsSelection = (f['OS/2'].fsSelection & ~0b1100001) | 0b1000000  # REGULAR, not bold or italic
        f['head'].macStyle = 0
        f.save(os.path.join(OUT, ps + '.ttf'))
    if family == 'Montserrat':  # the site ships Montserrat's own licence file: copy it as it is
        lic = open(os.path.join(R, 'assets/fonts/MONTSERRAT-LICENSE.txt'), encoding='utf-8').read()
        open(os.path.join(OUT, 'OFL.txt'), 'w', encoding='utf-8').write(lic)
    else:
        copyright_line = TTFont(os.path.join(R, src))['name'].getDebugName(0)
        open(os.path.join(OUT, f'OFL-{family.replace(" ", "")}.txt'), 'w', encoding='utf-8').write(copyright_line + '\n' + OFL_BODY)
print('fonts:', ', '.join(sorted(n for n in os.listdir(OUT) if n.endswith('.ttf'))))
