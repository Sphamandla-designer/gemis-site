# GEMIS brand pieces

Everything here is generated. Edit the generator, not the output.

| Piece | Files | Generator |
|---|---|---|
| Logos (every variant, SVG + PNG, both brands) | `logos/` (preview sheet `logos/index.html`, `logos/GEMIS-logos.zip`) | `node tools/make-logo-kit.mjs` (after `tools/make-logo.py` if the mark changes) |
| Email signatures | `email-signatures/` (HTML, PNG, text, preview page) | `python3 tools/make-signatures.py`, then `node tools/render-signatures.mjs` |
| Letterhead | `letterhead/GEMIS-Letterhead.pdf`, `letterhead/GEMIS-Letterhead.docx` | `node tools/make-brand-print.mjs` |
| LinkedIn banner | `linkedin/GEMIS-LinkedIn-Banner.png` (1128×191), `@2x` (2256×382) | `node tools/make-brand-print.mjs` |
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

## LinkedIn banner

Upload `GEMIS-LinkedIn-Banner@2x.png` as the company page's cover image (Page admin,
Edit page, Header, Cover image). LinkedIn shows the cover at 1128×191 and places the
company logo over its lower left corner, which the design keeps clear.

## Business cards

- Trim size 90×50 mm, the South African standard, with 3 mm bleed on every edge
  (the PDF page is 96×56 mm). Keep the printer's trim to the 90×50 mm box.
- Page 1 is the front (navy, the logo and the slogan); page 2 is the back (the
  person's name, role, email, site and address, with the navy column and initials).
- The PDFs are RGB with the fonts embedded as TrueType. Ask the printer for a proof:
  the navy is `#0a1230`, and a deep navy shifts in CMYK.
- The navy front prints best on a matt or soft-touch stock of 350 gsm or more.

## Fonts

`fonts/` holds static cuts of Montserrat (SIL Open Font License, `fonts/OFL.txt`),
made from the site's variable font. The Word file embeds them, and the print PDFs
are rendered from them so they embed TrueType rather than Type 3 outlines.
