# GEMIS brand pieces

Everything here is generated. Edit the generator, not the output.

| Piece | Files | Generator |
|---|---|---|
| Logos (every variant, SVG + PNG, both brands) | `logos/` (preview sheet `logos/index.html`, `logos/GEMIS-logos.zip`) | `node tools/make-logo-kit.mjs` (after `tools/make-logo.py` if the mark changes) |
| Email signatures | `email-signatures/` (HTML, PNG, text, preview page) | `python3 tools/make-signatures.py`, then `node tools/render-signatures.mjs` |
| Letterhead, GEMIS | `letterhead/GEMIS-Letterhead.pdf`, `letterhead/GEMIS-Letterhead.docx` | `node tools/make-brand-print.mjs` |
| Letterhead, GEMIS Studio | `letterhead/GEMIS-Studio-Letterhead.pdf`, `letterhead/GEMIS-Studio-Letterhead.docx` | `node tools/make-brand-print.mjs` |
| Meeting backgrounds (Zoom, Teams) | `meeting-backgrounds/GEMIS-Meeting-Background-Navy.jpg` (the team standard), `-Light.jpg`, and `meeting-backgrounds/people/<person>-{navy,light}.jpg` with the name and role | `node tools/make-brand-print.mjs` |
| LinkedIn banner | `linkedin/GEMIS-LinkedIn-Banner.png` (1128×191), `@2x` (2256×382) | `node tools/make-brand-print.mjs` |
| LinkedIn banner, GEMIS Studio | `linkedin/GEMIS-Studio-LinkedIn-Banner.png` (1128×191), `@2x` (2256×382) | `node tools/make-brand-print.mjs` |
| LinkedIn banners, personal | `linkedin/people/<person>.png` (1584×396, LinkedIn's profile cover size) | `node tools/make-brand-print.mjs` |
| Business cards | `business-cards/<person>.pdf` (print), `<person>-front.png`, `-back.png`, `all.png` | `node tools/make-brand-print.mjs` |

The team is in `staff.json`, shared by the signatures and the business cards. Add a
person there and run both generators.

The details come from the site: GEM Information Systems (Pty) Ltd, 9 Tapiola Way,
Edgemead, Cape Town, info@gemis.co.za, www.gemis.co.za, the slogan *Systems built to
last. Partners built to stay.*, and the confirmed figures (50+ systems, 5+ sectors,
founded 2014). There is no phone number on any piece.

## Letterhead

- **PDF:** A4, two pages. Page 1 carries the full head (the logo, the navy corner block
  with the slogan and the block cluster) and the navy foot with the address, email and
  site. Page 2 is the continuation page. Fold marks sit on the left edge at 99 and
  198 mm, with the punch mark at 148.5 mm. Print it, or use it as a background.
- **Word:** the same artwork sits behind the text, so it prints exactly like the PDF.
  Page 1 starts the letter under the corner block; continuation pages start under the
  slim head. Montserrat is embedded in the file, so it shows correctly on a machine
  without the font. To edit with the font installed, install the files in `fonts/`.
  Replace the bracketed placeholders and save as a new document.

## Studio letterhead

The same two pages and the same Word behaviour, in the studio's own language: white
paper, the coloured stone and GEMIS STUDIO, "Designed to be built." with *built.* in
the studio pink and an orange rule, the pink and orange faceted shards and the
outlined triangles from the studio site's hero, the dot grid, Manrope for words and
JetBrains Mono for labels, and the footer keyed E. / W. / A. in pink, as on the
studio's contact page. The Word file embeds Manrope and JetBrains Mono.

## Meeting backgrounds

1920×1080 JPEG, the size Zoom and Teams recommend. **Navy is the team standard**: use it
for every professional meeting so the whole team looks the same on screen. The light
version is for a dark room or dark clothes, which disappear into navy. Use the copy with
your name and role from `people/`, or the plain one.

The person covers the middle of the frame, so the design keeps it calm: the logo (and
the name and role) top left, the block cluster off the right edge, the slogan bottom
left, the site bottom right. The hatch is coarse and faint because video compression
makes fine lines shimmer.

- **Zoom:** Settings, Backgrounds & effects, Virtual backgrounds, the + button, Add image.
- **Teams:** before joining, Effects and avatars (or Background filters), then Add new;
  in a meeting, More, Effects and avatars, Background effects, Add new.
- Your own preview may show the words mirrored; everyone else sees them the right way
  round. In Zoom, untick *Mirror my video* to see them as others do.
- Virtual backgrounds work best with even light on your face and a plain
  wall behind you. Some organisations switch off custom backgrounds in Teams.

## LinkedIn banner

Upload `GEMIS-LinkedIn-Banner@2x.png` as the company page's cover image (Page admin,
Edit page, Header, Cover image). LinkedIn shows the cover at 1128×191 and places the
company logo over its lower left corner, which the design keeps clear.

## Studio LinkedIn banner

For the studio's showcase page (linkedin.com/showcase/gemis-design-studio), which uses
the same 1128×191 cover. It is the studio site's hero in a strip: the light ground, the
label *UX/UI and product design for digital products that work.* in the deep orange,
*Designed to be built.* with *built.* in pink, the shards, outlined triangles and dot
grid on the right, and the coloured stone. Upload the `@2x` file the same way as the
GEMIS banner; the lower left stays quiet for the page logo.

## Personal LinkedIn banners

One per person in `staff.json`, at exactly 1584×396, the size LinkedIn asks for on a
profile cover, designed to the guidance in `docs/LINKEDIN-BANNERS.md`:

- **One message, not a business card.** LinkedIn prints the name and the headline under
  the cover, so the cover does not repeat them and carries no contact details. The
  message is what the person does at GEMIS (`focus` in `staff.json`, their line on
  Our Story), with the slogan beneath and the logo above.
- **The safe zone.** The profile photo covers the lower left and phones may trim the
  ends, so everything that matters sits right of centre, in the upper three quarters.
- **Personal art.** The white stepped block holds the person's pictogram (`picto` in
  `staff.json`) and the site address.

Upload it from your profile: the pencil on the cover, Change photo (or Add cover
image), Upload photo. Then look at the profile on a phone as well.

## Business cards

- Trim size 90×50 mm, the South African standard, with 3 mm bleed on every edge
  (the PDF page is 96×56 mm). Keep the printer's trim to the 90×50 mm box.
- Page 1 is the front (navy, the logo and the slogan); page 2 is the back (the
  person's name, role, email, site and address, with the navy column and initials).
- The PDFs are RGB with the fonts embedded as TrueType. Ask the printer for a proof:
  the navy is `#0a1230`, and a deep navy shifts in CMYK.
- The navy front prints best on a matt or soft-touch stock of 350 gsm or more.

## Fonts

`fonts/` holds static cuts of Montserrat, Manrope and JetBrains Mono, made from the
site's variable fonts by `python3 tools/make-static-fonts.py` (each under the SIL Open
Font License: `fonts/OFL.txt`, `OFL-Manrope.txt`, `OFL-JetBrainsMono.txt`). The Word
files embed them, and the print PDFs are rendered from them so they embed TrueType
rather than Type 3 outlines. Install them to edit the Word letters with the real
fonts on screen.
