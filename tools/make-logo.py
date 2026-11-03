"""The GEMIS logo (python3.13 tools/make-logo.py <out-dir>; needs fonttools and brotli).
The GEMIS logo, built from the site's own language: a faceted stone cut from
six planes with light between them, and the name set in Montserrat."""
import sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

OUT = sys.argv[1] if len(sys.argv) > 1 else 'assets/img/logos'
FONT = '/home/user/gemis-site/assets/fonts/montserrat-latin.woff2'

# ── the stone (a 64-unit box): three crown facets over three pavilion facets,
#    separated by a constant gap so the cut reads at any size in one colour
FACETS = [
    [(10, 16), (22, 16), (18, 30), (4, 30)],
    [(22, 16), (42, 16), (46, 30), (18, 30)],
    [(42, 16), (54, 16), (60, 30), (46, 30)],
    [(4, 30), (18, 30), (32, 60)],
    [(18, 30), (46, 30), (32, 60)],
    [(46, 30), (60, 30), (32, 60)],
]
GAP = 1.1  # each facet steps in by this much, so the light between two is 2.2


def inset(poly, d):
    n = len(poly)
    area = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n)) / 2
    sgn = 1 if area > 0 else -1
    lines = []
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        ex, ey = x2 - x1, y2 - y1
        L = (ex * ex + ey * ey) ** .5
        nx, ny = -ey / L * sgn, ex / L * sgn  # inward normal
        lines.append(((x1 + nx * d, y1 + ny * d), (x2 + nx * d, y2 + ny * d)))
    out = []
    for i in range(n):
        (ax, ay), (bx, by) = lines[i - 1]
        (cx, cy), (dx, dy) = lines[i]
        r1x, r1y = bx - ax, by - ay
        r2x, r2y = dx - cx, dy - cy
        den = r1x * r2y - r1y * r2x
        t = ((cx - ax) * r2y - (cy - ay) * r2x) / den
        out.append((ax + r1x * t, ay + r1y * t))
    return out


def stone(x=0, y=0, s=1.0):
    polys = []
    for f in FACETS:
        p = inset(f, GAP)
        polys.append('<polygon points="' + ' '.join(f'{x + px * s:.2f},{y + py * s:.2f}' for px, py in p) + '"/>')
    return ''.join(polys)


# ── the words in Montserrat, outlined so the file needs no font
def face(wght):
    f = TTFont(FONT)
    return instantiateVariableFont(f, {'wght': wght})


def text_path(font, s, size, x, y, tracking):
    """Path data for s with its baseline at y, left edge at x; tracking as a fraction of size."""
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font['head'].unitsPerEm
    k = size / upm
    d, cx = [], x
    for ch in s:
        if ch == ' ':
            cx += font['hmtx'][cmap[ord('N')]][0] * k * .7
            continue
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, cx, y)))
        d.append(pen.getCommands())
        cx += font['hmtx'][g][0] * k + tracking * size
    return ' '.join(d), cx - tracking * size


def cap_height(font):
    return font['OS/2'].sCapHeight / font['head'].unitsPerEm


F600, F500 = face(600), face(500)
CAP = cap_height(F600)

# ── the horizontal lockup: the stone, then the two lines
#    GEMIS 18 units tall (cap), the descriptor 6 units tall, both from one left edge
H = 40
mark_s = 40 / 64
sx, sy = 0, -3.5
tx = 50
gemis_size = 18 / CAP
sub_size = 6.2 / CAP
gemis_d, gemis_end = text_path(F600, 'GEMIS', gemis_size, tx, 22.5, .14)
sub_d, sub_end = text_path(F500, 'GEM INFORMATION SYSTEMS', sub_size, tx, 34.5, .24)
W = round(max(gemis_end, sub_end) + 2, 1)
lockup = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="GEMIS — GEM Information Systems" fill="currentColor">'
          f'<g>{stone(sx, sy, mark_s)}</g><path d="{gemis_d}"/><path d="{sub_d}"/></svg>')
open(f'{OUT}/gemis-logo.svg', 'w').write(lockup)

# the symbol for the page sprite (same geometry)
symbol = (f'<symbol id="gemisLogo" viewBox="0 0 {W} {H}" fill="currentColor"><g>{stone(sx, sy, mark_s)}</g><path d="{gemis_d}"/><path d="{sub_d}"/></symbol>')
open(f'{OUT}/symbol.txt', 'w').write(symbol)
open(f'{OUT}/viewbox.txt', 'w').write(f'0 0 {W} {H}')

# the stone alone
open(f'{OUT}/gemis-mark.svg', 'w').write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="GEMIS" fill="currentColor">{stone(0, 0, 1)}</svg>')

# the stacked lockup: the stone centred over the name
g2_d, g2_end = text_path(F600, 'GEMIS', 26 / CAP, 0, 0, .16)
s2_d, s2_end = text_path(F500, 'GEM INFORMATION SYSTEMS', 7.6 / CAP, 0, 0, .26)
w2 = max(g2_end, s2_end)
SW, SH = round(w2 + 16, 1), 150
gx = (SW - g2_end) / 2
sx2 = (SW - s2_end) / 2
g2_d, _ = text_path(F600, 'GEMIS', 26 / CAP, gx, 114, .16)
s2_d, _ = text_path(F500, 'GEM INFORMATION SYSTEMS', 7.6 / CAP, sx2, 134, .26)
open(f'{OUT}/gemis-logo-stacked.svg', 'w').write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SW} {SH}" role="img" aria-label="GEMIS — GEM Information Systems" fill="currentColor">'
    f'{stone((SW - 80) / 2, 0, 80 / 64)}<path d="{g2_d}"/><path d="{s2_d}"/></svg>')

# the favicon: the stone in white on the midnight square
open(f'{OUT}/favicon.svg', 'w').write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#0a1230"/>'
    f'<g fill="#ffffff">{stone(7, 5, 50 / 64)}</g></svg>')
print('W', W, 'SW', SW)


# ── the studio's stone: the same cut in the studio's two colours — the crown
#    pink, the pavilion orange — and the white version for dark grounds
PINK, ORANGE = '#ff1f7a', '#ff7a12'


def stone_two(x, y, s, top, bottom):
    polys = []
    for i, f in enumerate(FACETS):
        p = inset(f, GAP)
        polys.append(f'<polygon fill="{top if i < 3 else bottom}" points="' + ' '.join(f'{x + px * s:.2f},{y + py * s:.2f}' for px, py in p) + '"/>')
    return ''.join(polys)


STUDIO = sys.argv[2] if len(sys.argv) > 2 else None
if STUDIO:
    head = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="GEMIS Studio">'
    open(f'{STUDIO}/mark-colour.svg', 'w').write(head + stone_two(0, 0, 1, PINK, ORANGE) + '</svg>')
    open(f'{STUDIO}/mark-white.svg', 'w').write(head + stone_two(0, 0, 1, '#ffffff', '#ffffff') + '</svg>')
    open(f'{STUDIO}/favicon.svg', 'w').write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#16161a"/>'
        + stone_two(7, 5, 50 / 64, PINK, ORANGE) + '</svg>')
    # the studio lockup: the coloured stone, GEMIS in ink, STUDIO tracked beneath
    gd, gend = text_path(F600, 'GEMIS', 26 / CAP, 96, 40, .12)
    sd, send = text_path(F500, 'STUDIO', 11 / CAP, 96, 62, .42)
    W3 = round(max(gend, send) + 2, 1)
    open(f'{STUDIO}/gemis-studio-logo.svg', 'w').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W3} 72" role="img" aria-label="GEMIS Studio">'
        f'{stone_two(0, 0, 72 / 64, PINK, ORANGE)}<path fill="#16161a" d="{gd}"/><path fill="#55565e" d="{sd}"/></svg>')
    print('studio ok', W3)
