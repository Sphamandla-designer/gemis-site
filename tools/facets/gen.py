#!/usr/bin/env python3
"""Variations on the home hero for every image slot on the corporate site.

    python3 tools/facets/gen.py && node tools/facets/render.mjs

gen.py writes one SVG per slot (a steel-blue field with navy hexagonal facets
anchored to the edges, the hero's own composition, seeded so the set is
reproducible); render.mjs rasterises them with Chromium straight into
assets/img/ at each slot's original size. Change a seed in JOBS to get a new
variation for one slot; the light/dark flag follows the band it sits in.
"""
import random, json, sys, os
OUT=os.path.dirname(os.path.abspath(__file__))
LIGHT_FIELD=('#9bbcd6','#86abc8')      # the hero's field, top-left → bottom-right
DARK_FIELD=('#1a2c50','#0e1631')        # the same family for the dark bands
NAVY=('#1d3a5f','#8fb0cc')              # facet gradient: deep navy → field (fades out)
def hexagon(cx,cy,r,rot=0):
    import math
    pts=[(cx+r*math.cos(math.radians(60*i+rot)), cy+r*math.sin(math.radians(60*i+rot))) for i in range(6)]
    return ' '.join(f'{x:.1f},{y:.1f}' for x,y in pts)
def chevron(x,y,w,h,flip=False):
    # a half-hexagon slab, like the hero's left and right-hand shapes
    if not flip: pts=[(x,y),(x+w*.72,y),(x+w,y+h*.5),(x+w*.72,y+h),(x,y+h)]
    else: pts=[(x+w,y),(x+w*.28,y),(x,y+h*.5),(x+w*.28,y+h),(x+w,y+h)]
    return ' '.join(f'{px:.1f},{py:.1f}' for px,py in pts)
def svg(w,h,seed,dark=False,density=1.0):
    rnd=random.Random(seed)
    f1,f2=DARK_FIELD if dark else LIGHT_FIELD
    g1,g2=('#7aa6d2','#0e1631') if dark else ('#1c3a5e','#8fb0cc')
    defs=[]; shapes=[]
    # slabs anchored to the edges: (edge, along-position 0..1, size factor)
    edges=['left','right','top','bottom']; rnd.shuffle(edges)
    n=rnd.choice([3,3,4])
    for i,edge in enumerate(edges[:n]):
        t=rnd.uniform(.05,.75); size=rnd.uniform(.42,.7)*min(w,h)
        sw,sh=size*1.5,size*.78
        if edge=='left':   x,y=-sw*.42, t*h-sh*.5;  pts=[(x,y),(x+sw*.68,y),(x+sw,y+sh*.5),(x+sw*.68,y+sh),(x,y+sh)]; gx=(0,1)
        elif edge=='right':x,y=w-sw*.58, t*h-sh*.5; pts=[(x+sw,y),(x+sw*.32,y),(x,y+sh*.5),(x+sw*.32,y+sh),(x+sw,y+sh)]; gx=(1,0)
        elif edge=='top':  x,y=t*w-sw*.5, -sh*.45;  pts=[(x,y),(x+sw,y),(x+sw,y+sh*.55),(x+sw*.5,y+sh),(x,y+sh*.55)]; gx=(0,0)
        else:              x,y=t*w-sw*.5, h-sh*.55; pts=[(x,y+sh*.45),(x+sw*.5,y),(x+sw,y+sh*.45),(x+sw,y+sh),(x,y+sh)]; gx=(0,0)
        if edge in ('top','bottom'):
            y1,y2=(0,1) if edge=='top' else (1,0); x1,x2=(0,1) if rnd.random()<.5 else (1,0)
            defs.append(f'<linearGradient id="g{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"><stop offset="0" stop-color="{g1}"/><stop offset=".55" stop-color="{g1}" stop-opacity=".55"/><stop offset="1" stop-color="{g2}" stop-opacity="0"/></linearGradient>')
        else:
            defs.append(f'<linearGradient id="g{i}" x1="{gx[0]}" y1="0" x2="{gx[1]}" y2="0"><stop offset="0" stop-color="{g1}"/><stop offset=".5" stop-color="{g1}" stop-opacity=".6"/><stop offset="1" stop-color="{g2}" stop-opacity="0"/></linearGradient>')
        shapes.append('<polygon points="'+' '.join(f'{px:.1f},{py:.1f}' for px,py in pts)+f'" fill="url(#g{i})"/>')
    # one small full hexagon as an accent, like the hero's corner pieces
    hx,hy=rnd.choice([(w*.12,h*.1),(w*.88,h*.12),(w*.1,h*.9),(w*.9,h*.88)]); hr=min(w,h)*rnd.uniform(.16,.24)
    defs.append(f'<linearGradient id="gh" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{g1}"/><stop offset="1" stop-color="{g2}" stop-opacity=".05"/></linearGradient>')
    shapes.append(f'<polygon points="{hexagon(hx,hy,hr,rnd.choice([0,30]))}" fill="url(#gh)" opacity=".9"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><linearGradient id="field" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{f1}"/><stop offset="1" stop-color="{f2}"/></linearGradient>{''.join(defs)}</defs>
<rect width="{w}" height="{h}" fill="url(#field)"/>
{''.join(shapes)}
</svg>'''
# every image the corporate pages use that showed a product, at its original size
JOBS=[
 ('home/about-band.jpg',2000,860,11,False),('home/leadership-bg.jpg',2200,1150,12,True),('home/cta-bg.jpg',2400,900,13,True),
 ('menu/managem.jpg',760,475,21,False),('menu/gemis-tech.jpg',760,475,22,False),('menu/design-studio.jpg',760,475,23,False),
 ('portfolio/hero-displays.jpg',1500,1025,31,False),('portfolio/hero-wastemart.jpg',1920,1079,32,False),('portfolio/finos-wide.jpg',1920,959,33,False),('portfolio/gemistech-mock.jpg',900,1200,34,False),('portfolio/rentflow-tall.jpg',900,1200,35,False),
 ('work/managem-mock.jpg',1400,1050,41,False),('work/wastemart-mock.jpg',1400,1050,42,False),('work/smartstart-mock.jpg',1400,1050,43,False),('work/sonke-mock.jpg',1400,1050,44,False),
 ('shots/finos.jpg',1100,901,51,False),('shots/lungelo.jpg',1000,750,52,False),('shots/managem-desk.jpg',1000,750,53,False),('shots/nuracoach.jpg',1000,750,54,False),('shots/rentflow.jpg',1100,825,55,False),('shots/wastemart-driver.jpg',1000,750,56,False),
 ('proto/managem-poster.jpg',1280,800,61,True),('proto/wastemart-poster.jpg',1280,800,62,True),
]
os.makedirs(OUT+'/svg',exist_ok=True)
for name,w,h,seed,dark in JOBS:
    open(f'{OUT}/svg/{name.replace("/","__").replace(".jpg",".svg")}','w').write(svg(w,h,seed,dark))
json.dump(JOBS,open(OUT+'/jobs.json','w'))
print(len(JOBS),'svgs written')
