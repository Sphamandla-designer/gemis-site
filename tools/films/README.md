# The case-study films

`ManaGEM_explainer` and `WasteMart_explainer` in `assets/video/case-studies/`
are built here (2026-11-26). Each film is one HTML file whose every frame is a
pure function of time (`engine.js`: `seek(t)`), rendered frame by frame with
Playwright and joined with ffmpeg.

| | ManaGEM | WasteMart |
|---|---|---|
| Look | indigo and gold, Outfit, the gem's facets | the app's teal on paper, Archivo, the giant WM |
| Device | real screens in windows, the camera pushing in | a collection route the truck drives along |
| Real screens | the 2026 ManaGEM prototype (`ManaGem.html`) | the driver-app prototype (`wastemart-driver.html`), the sign-in screen |
| Characters | the roofer (SBS, where it began), the gem, the crew | none |

- **Narration** is the text in `scripts/video-text.json`, word for word, read by
  the ElevenLabs voice "ZanB October 2026" (South African English, eleven_v4),
  one take each: `a/managem-vo.mp3`, `a/wastemart-vo.mp3`. Generated on the free
  plan: confirm the licence, or regenerate on a paid plan, before paid use.
- **Captions** are burned in, on the narration's own pauses (the `cap()` list
  at the foot of each film).
- **Music** is synthesised (`music.py`): no samples, no licence.
- **Screens** carry neutral sample data: capture them with
  `tools/studio-case-shots.mjs`, never from the raw prototypes.
- The avatars (`a/crew.png`, `a/gem.png`, `a/roofer.png`) and the ManaGEM logo
  come from the owner's marketing repository.

## Rebuild

```sh
cd tools/films
node ../studio-case-shots.mjs shots managem wastemart     # the real screens
node render.mjs managem.htm frames-m                     # 1788 frames
python3 music.py managem 59.6 m-music.wav                 # needs numpy, scipy
./mix.sh a/managem-vo.mp3 m-music.wav 700 59.6 m-audio.wav
ffmpeg -framerate 30 -i frames-m/f%05d.jpg -i m-audio.wav -c:v libx264 -preset slow -crf 28 \
  -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 112k -shortest ManaGEM_explainer_web.mp4
```

WasteMart: `wastemart.htm`, 63.6 s, voice offset 600 ms, `-crf 24`. Then the
WebM (`libvpx-vp9`), the poster (`_thumb.jpg`, one frame) and the stills in
`assets/img/cases/<slug>/` (frames at the times in the commit that added this),
and the durations in `scripts/stories.py`.

## The second batch (2026-11-26)

| Film | Look | Device | Screens |
|---|---|---|---|
| `sbs.htm` (1:07, voice offset 600 ms, crf 26) | SBS red on white, Space Grotesk, a red roofline | rain that becomes enquiries; the roofer; windows | ManaGEM prototype screens, labelled "the product this system became" |
| `homeassist.htm` (1:05, crf 24) | HomeAssist blue and navy, Manrope | a pipe system: two inlets, one job; the plumber cut from the crew | none exist, so none shown |
| `transhex.htm` (1:18, crf 23) | black and the emblem's blue, Inter Tight | five sources converging on one hexagon; lines that draw themselves | none exist, so none shown; no figure invented |

Sonke and Tore's are still the earlier cut: their voiceovers could not be
generated (ElevenLabs' free tier was busy). `music.py` already carries a bed
for each (`sonke`, `tores`).

## Saying "GEMIS" (2026-11-26)

The owner's correction: GEMIS is said like the word *gem* ("JEM-iss"). The voice
read the capitals wrongly, so in every prompt sent to the voice the name is
spelled **Jemmis**; the captions and transcripts keep GEMIS. The five films were
fixed by re-voicing only the twelve sentences that say the name
(`a/gemis-patch.mp3`) and splicing each into its slot (`splice.py`, tempo-fitted,
level-matched; the untouched takes belong in `orig-vo/`). The committed
`a/*-vo.mp3` are the spliced voiceovers. Any new narration: write Jemmis.
