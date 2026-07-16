# Xtreme Mobile Detailing

Marketing website for Xtreme Mobile Detailing (mobile auto detailing, Omaha, NE & metro).
Static HTML/CSS/JS — no build step. Redesign of xtreme-mobiledetailing.com with real
business content (services, pricing, owner story, photos) pulled from the live site.

## Run locally

```bash
python3 serve.py 4322
# then open http://localhost:4322
```

`serve.py` is a tiny no-cache dev server so edits show up without hard-refreshing.

## Structure

- `index.html` — home (hero, marquee, mobile-convenience pitch, services teaser,
  why-us, gallery, CTA)
- `services.html` — full package list + pricing + ceramic coating detail
- `about.html` — owner Derrick Bravo's story, mission, detailer-vs-car-wash comparisons
- `reviews.html` — placeholder-ready (no reviews scraped yet — see below) + gallery
- `contact.html` — hours/phone/email + quote form
- `styles.css` — all styles (CSS variables at top)
- `script.js` — nav drawer, scroll reveals, quote form (Web3Forms + SMS fallback)
- `seo.py` — injects canonical/OG/Twitter/geo meta + LocalBusiness JSON-LD into every
  page, generates `sitemap.xml` + `robots.txt`. Idempotent — re-run any time after
  editing pages (same tool as Ari's site). **DOMAIN is a placeholder** (the business's
  current live domain) — edit `DOMAIN` in seo.py and re-run if a new domain is bought.
- `assets/logo.png` — logo pulled from xtreme-mobiledetailing.com (full res, 1170×623)
- `assets/img/` — 18 real work photos pulled from the live site (hero, gallery, about)

## Brand

Black `#08080a`, red `#e5141a` / bright red `#ff2f22`, white. Condensed bold
display type (Tanker) + General Sans for body/UI, via Fontshare. Diagonal
hazard-stripe motif + red glow (both lifted from the logo mark). Design direction
also references rydrdieautodetailing.com and sunprotectors.net (sticky angled CTA,
split diagonal hero, marquee ticker, repeated dual CTAs) for a high-conversion layout.

## Quote form

The contact form (`#qform`) is wired for Web3Forms but **no access key is set yet** —
until one is added it falls back to opening a pre-filled text to (402) 301-3243, so
it works immediately either way.
- Get a free access key at <https://web3forms.com> (enter
  xtrememobiledetailing7@gmail.com — submissions arrive there).
- Paste it into `WEB3FORMS_KEY` near the top of the form handler in `script.js`.

## Reviews

`reviews.html` has 4 real reviews (Mark pasted Facebook screenshots) as static
`.review-card` entries — Billy Johnson, Michaela Luttig Nissen, Joel Villanueva,
Yael Blanco-Zamudio. The same 4 are embedded in the JSON-LD `aggregateRating`/`review`
array via `seo.py` — update `REVIEWS` there too if more get added.

## SEO

`seo.py` handles canonical/OG/Twitter/geo meta, sitewide `AutoWash` LocalBusiness
JSON-LD (with the 4 real reviews), `sitemap.xml`, and `robots.txt`. Run it after any
content edit that changes a `<title>`/description, or after adding a page:

```bash
python3 seo.py
```

Domain is currently the placeholder `https://xtreme-mobiledetailing.com` (the
business's real, currently-registered domain) — if a different domain gets bought
(e.g. `xtrememobiledetail.com`, still under discussion), update `DOMAIN` in seo.py
and re-run.

## Privacy, cookies & Google Analytics

No cookie-consent banner — this site is US-only (Omaha, NE local service, no
EU/UK audience) and GA4 with no ad pixels doesn't require one; a banner here
would just be friction with no legal upside. `privacy.html` (linked in every
footer) is the factual policy: what the quote form collects, that GA4 is used
for analytics, no ad pixels/remarketing currently, no data sold, how to opt out
of analytics (browser settings / Google's opt-out add-on) or request deletion.

To turn Analytics on: create a GA4 property at analytics.google.com, then paste
the Measurement ID (`G-XXXXXXXXXX`) into `GA_MEASUREMENT_ID` near the top of
`script.js` — it loads on every page once set, no gating needed.

**If Meta Pixel, Google Ads conversion tracking, or remarketing ever get
added**, that changes the analysis — those count as "selling/sharing" data
under CA and other state privacy laws and need a "Your Privacy Choices"
opt-out link + mechanism, plus an updated policy. Revisit this doc and
`privacy.html` at that point (and consider a lawyer's review — the
CCPA/state-law applicability thresholds are a judgment call this README
isn't qualified to make for you).

## Still TODO before go-live

- `WEB3FORMS_KEY` for direct email delivery
- `GA_MEASUREMENT_ID` once the GA4 property is created (see above)
- Confirm hours (pulled from the live site: By appointment, Mon–Sat 9am–7pm)
- Decide on final domain (see SEO section) and re-run seo.py once chosen
- git init + connect to GitHub + host, same as Ari's site

## Deploy

Push this folder's repo to GitHub and connect a host (Cloudflare Pages / Netlify /
GitHub Pages). Pushes auto-deploy. Keep edits local until approved, then push.

Contact: (402) 301-3243 · xtrememobiledetailing7@gmail.com · Omaha, NE
