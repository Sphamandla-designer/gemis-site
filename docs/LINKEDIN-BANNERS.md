# LinkedIn banners: what the guidance says, and how the team's covers follow it

Researched 2026-11-25, before the personal covers in `brand/linkedin/people/` were
redesigned. The sources are third-party guides; LinkedIn publishes the size but no
pixel-exact safe zone, and the guides disagree on the numbers, so the design takes the
most cautious reading of each.

## The rules

| Rule | What the guides say | What the covers do |
|---|---|---|
| Size | Profile cover 1584×396 px (4:1), PNG or JPG, under 8 MB. A company page cover is a different size (1128×191). | Exactly 1584×396 PNG, under 100 KB. |
| The photo | The profile photo covers the lower left on desktop. Estimates run from a 152 px circle to a 568×264 px area to avoid; on a phone it is proportionally larger, and some guides say it sits lower-centre there. | The lower left carries only the pattern. Nothing that matters sits left of x 620. |
| Narrow screens | Phones show the cover about 400 px wide and may trim the ends; keep content in the central 60–70 %, or roughly x 300–1300. | The logo, the message and the slogan sit between x 620 and 1270, in the upper three quarters. The block on the right is decoration plus the site; nothing is lost if it is trimmed. |
| One message | "A banner combining a logo, tagline, quote and call to action reads as noise." Two or three pieces of information at most. It is a billboard, not a second About section or a business card. | One message per cover, the logo, the slogan, the site. |
| What the message is | What you do, who you help, or your area of expertise. The page already prints the name and the headline under the cover. | Each person's own focus at GEMIS, from their confirmed line on Our Story, set in the slogan's two-line rhythm. No name, no job title, no email. |
| Calls to action | Subtle: a site address in a corner, not "BOOK A CALL" across the cover. | The site address, small, in the white block. |
| Team covers | A shared template in the brand's colours and type with a personal message keeps a team cohesive; make it optional, since a profile is personal. | One template, six messages, six pictograms. |
| Check it | Preview on desktop and on a phone before publishing. | Checked in mock profiles at both sizes; check again on the real profile. |

## Per person

`focus` (the two lines) and `picto` (a key of `PICTO` in `scripts/build-stories.py`) in
`brand/staff.json`. The focus lines are the Our Story lines, which the owner confirmed
(`scripts/facts.md`, 2026-10-28). Change a line there and run
`node tools/make-brand-print.mjs`.

## Sources

- https://rightblogger.com/blog/linkedin-banner-size
- https://www.manypixels.co/blog/social-media-design/linkedin-banner-size
- https://www.zeliq.com/blog/linkedin-banner-size
- https://socialrails.com/sizes/linkedin/cover
- https://linkedgrow.ai/blog/linkedin-banner-size
- https://myfeedin.co/blog/linkedin-banner-size
- https://www.linkedin.com/pulse/linkedin-banner-secrets-perfect-proportions-placement-javier-y%C3%A9benes--yrdgc
- https://taplio.com/blog/linkedin-banner
- https://www.jeffbullas.com/thread/what-are-the-best-practices-for-a-linkedin-background-photo
- https://cclarity.io/blog/linkedin-banner-image
- https://www.adobe.com/express/learn/blog/10-customizable-linkedin-cover-photos-that-could-give-you-the-edge
- https://www.tribalimpact.com/blog/employee-branding-personal-vs.-company-banners-on-linkedin-profiles
- https://slite.agorapulse.com/p/AxMuKbdhO/Brand-Asset-LinkedIn-Best-Practices-and-Profile-Banners
- https://www.coreldraw.com/en/blog/linkedin-banners/
