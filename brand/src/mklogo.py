#!/usr/bin/env python3
"""Build the GEMIS Studio logo files.

The mark is the three-step ladder already used in the site nav (bar widths
22/15/8 at 4px tall with a 3px gap); everything here is that geometry scaled
x4 so the wordmark can be outlined at a sane precision. The wordmark is
converted to real paths, so the logos need no fonts installed.
"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.misc.transform import Transform

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = HERE
OUT = os.path.join(HERE, "..", "logo")
os.makedirs(OUT, exist_ok=True)

INK, OFFWHITE, PINK = "#16161a", "#f5f6f8", "#ff1f7a"


def load(path, wght):
    f = TTFont(path)
    return instancer.instantiateVariableFont(f, {"wght": wght})


def text_path(font, text, size, tracking_em):
    """Outline `text` as one SVG path string, y-down, origin at the baseline."""
    upem = font["head"].unitsPerEm
    scale = size / upem
    cmap = font.getBestCmap()
    glyphs = font.getGlyphSet()
    hmtx = font["hmtx"]
    track = tracking_em * size
    pen_out, x, bounds = [], 0.0, [None, None, None, None]

    for ch in text:
        name = cmap[ord(ch)]
        # y is flipped: font units are y-up, SVG is y-down
        t = Transform(scale, 0, 0, -scale, x, 0)
        sp = SVGPathPen(glyphs)
        glyphs[name].draw(TransformPen(sp, t))
        d = sp.getCommands()
        if d:
            pen_out.append(d)
        bp = BoundsPen(glyphs)
        glyphs[name].draw(TransformPen(bp, t))
        if bp.bounds:
            x0, y0, x1, y1 = bp.bounds
            bounds = [
                x0 if bounds[0] is None else min(bounds[0], x0),
                y0 if bounds[1] is None else min(bounds[1], y0),
                x1 if bounds[2] is None else max(bounds[2], x1),
                y1 if bounds[3] is None else max(bounds[3], y1),
            ]
        x += hmtx[name][0] * scale + track

    return " ".join(pen_out), bounds, x - track  # drop trailing track


# ── geometry (site nav x4) ────────────────────────────────────────────────
BAR_H, BAR_GAP = 16, 12
BARS = [88, 60, 32]
MARK_W, MARK_H = 88, BAR_H * 3 + BAR_GAP * 2          # 88 x 72
GAP = 48                                               # mark -> wordmark
GEMIS_SIZE, STUDIO_SIZE, WORD_GAP = 56, 36, 14

manrope = load(f"{FONTS}/manrope-latin-wght-normal.woff2", 700)
mono = load(f"{FONTS}/jetbrains-mono-latin-wght-normal.woff2", 400)

gem_d, gem_b, _ = text_path(manrope, "GEMIS", GEMIS_SIZE, 0.08)
std_d, std_b, _ = text_path(mono, "STUDIO", STUDIO_SIZE, 0.16)

gem_w, gem_h = gem_b[2] - gem_b[0], gem_b[3] - gem_b[1]
std_w, std_h = std_b[2] - std_b[0], std_b[3] - std_b[1]
word_w, word_h = max(gem_w, std_w), gem_h + WORD_GAP + std_h


def mark_svg(fill, x=0, y=0):
    out = []
    for i, w in enumerate(BARS):
        out.append(f'<rect x="{x}" y="{y + i * (BAR_H + BAR_GAP)}" width="{w}" height="{BAR_H}" fill="{fill}"/>')
    return "\n  ".join(out)


def word_svg(fill, x, y):
    """y = top of the wordmark block."""
    gx, gy = x - gem_b[0], y - gem_b[1]
    sx, sy = x - std_b[0], y + gem_h + WORD_GAP - std_b[1]
    return (f'<path d="{gem_d}" fill="{fill}" transform="translate({gx:.2f} {gy:.2f})"/>\n'
            f'  <path d="{std_d}" fill="{fill}" transform="translate({sx:.2f} {sy:.2f})"/>')


def write(name, w, h, body, title):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
           f'width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}">\n'
           f'  <title>{title}</title>\n  {body}\n</svg>\n')
    open(f"{OUT}/{name}", "w").write(svg)
    print(f"{name:42} {w:7.0f} x {h:.0f}")


# ── horizontal lockup ─────────────────────────────────────────────────────
H_W, H_H = MARK_W + GAP + word_w, max(MARK_H, word_h)
for tag, fill in (("", INK), ("-light", OFFWHITE)):
    body = (mark_svg(fill, 0, (H_H - MARK_H) / 2) + "\n  " +
            word_svg(fill, MARK_W + GAP, (H_H - word_h) / 2))
    write(f"gemis-studio-lockup{tag}.svg", H_W, H_H, body, "GEMIS Studio")

# ── stacked lockup ────────────────────────────────────────────────────────
S_GAP = 40
S_W, S_H = max(MARK_W, word_w), MARK_H + S_GAP + word_h
for tag, fill in (("", INK), ("-light", OFFWHITE)):
    body = (mark_svg(fill, 0, 0) + "\n  " +
            word_svg(fill, 0, MARK_H + S_GAP))
    write(f"gemis-studio-stacked{tag}.svg", S_W, S_H, body, "GEMIS Studio")

# ── mark alone ────────────────────────────────────────────────────────────
for tag, fill in (("", INK), ("-light", OFFWHITE), ("-pink", PINK)):
    write(f"gemis-studio-mark{tag}.svg", MARK_W, MARK_H, mark_svg(fill), "GEMIS Studio")

# ── square avatar badge (LinkedIn / social) ───────────────────────────────
# Mark is kept inside the circle LinkedIn inscribes in the square.
A = 512
a_scale = 2.5
aw, ah = MARK_W * a_scale, MARK_H * a_scale
bars = "\n    ".join(
    f'<rect x="{(A - aw) / 2:.1f}" y="{(A - ah) / 2 + i * (BAR_H + BAR_GAP) * a_scale:.1f}" '
    f'width="{w * a_scale:.1f}" height="{BAR_H * a_scale:.1f}" fill="{OFFWHITE}"/>'
    for i, w in enumerate(BARS))
write("gemis-studio-avatar.svg", A, A,
      f'<rect width="{A}" height="{A}" fill="{INK}"/>\n    {bars}', "GEMIS Studio")

print(f"\nlockup   {H_W:.1f} x {H_H:.1f}   word block {word_w:.1f} x {word_h:.1f}")
print(f"GEMIS    {gem_w:.1f} x {gem_h:.1f}\nSTUDIO   {std_w:.1f} x {std_h:.1f}")
