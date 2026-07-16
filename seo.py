#!/usr/bin/env python3
"""Inject technical SEO into every page + generate sitemap.xml and robots.txt.

Idempotent: strips the tags it manages and re-inserts them, so run it any time
after editing pages. Adds per-page canonical, Open Graph, Twitter, geo +
theme-color meta, and a sitewide LocalBusiness JSON-LD block.

⚠️  DOMAIN: currently set to the business's existing live domain as a
    placeholder for this redesign. If Mark registers a different domain
    (e.g. xtrememobiledetail.com), update DOMAIN below and re-run.
"""
import re
import glob
import datetime
import pathlib

ROOT = pathlib.Path(__file__).parent

# ── EDIT ME if the domain changes, then re-run this script ───────────────────
DOMAIN = "https://xtreme-mobiledetailing.com"   # no trailing slash
# ────────────────────────────────────────────────────────────────────────────

BUSINESS = "Xtreme Mobile Detailing"
PHONE = "+1-402-301-3243"
OG_IMAGE = f"{DOMAIN}/assets/img/IMG_2666.jpeg"
INSTAGRAM = "https://www.instagram.com/xtreme_mobiledetail/"
FACEBOOK = "https://www.facebook.com/437891520308105"

REVIEWS = [
    ("Billy Johnson", "I am very impressed with their work. My RS is the cleanest it's probably ever been. Their prices are very affordable and the level of detail they put into the work shows. I would recommend Xtreme Mobile Detailing to anyone."),
    ("Michaela Luttig Nissen", "They did an amazing job after an unfortunate incident of a friend throwing up in our car! Very professional and thoroughly cleaned and deodorized our car! Will use them again in the future."),
    ("Joel Villanueva", "Great price for the amount of time put into the job. Also the workers are very nice and professional with what they do. Removed stains I myself thought could not be taken out and are very realistic with what they will do. 100% would recommend."),
    ("Yael Blanco-Zamudio", "Extremely satisfied with the quality of the work. Highly recommend!"),
]

# sitemap priority / changefreq by page
PRIORITY = {"index.html": ("1.0", "weekly")}
DEFAULT_MAIN = ("0.8", "monthly")


def page_url(fname):
    # .html kept in canonical/sitemap URLs (matches how the site is actually
    # served right now). If the eventual host strips .html via redirects
    # (e.g. Cloudflare Pages/Workers clean URLs), switch this to match —
    # same swap Ari's site made once its host was confirmed.
    return DOMAIN + "/" + fname


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def jsonld_escape(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def local_business_jsonld():
    reviews = ", ".join(
        '{{"@type":"Review","author":{{"@type":"Person","name":"{n}"}},'
        '"reviewRating":{{"@type":"Rating","ratingValue":"5","bestRating":"5"}},'
        '"reviewBody":"{b}"}}'.format(n=jsonld_escape(n), b=jsonld_escape(b))
        for n, b in REVIEWS
    )
    return (
        '<script type="application/ld+json" id="ld-business">'
        '{'
        '"@context":"https://schema.org","@type":"AutoWash",'
        f'"name":"{BUSINESS}",'
        f'"image":"{OG_IMAGE}",'
        f'"url":"{DOMAIN}/",'
        f'"telephone":"{PHONE}",'
        '"priceRange":"$$",'
        '"description":"Mobile auto detailing serving Omaha, NE and the metro. Interior & exterior detailing, ceramic coating, paint correction and maintenance plans, performed at your home or office.",'
        '"address":{"@type":"PostalAddress","addressLocality":"Omaha","addressRegion":"NE","addressCountry":"US"},'
        '"geo":{"@type":"GeoCoordinates","latitude":41.2565,"longitude":-95.9345},'
        '"areaServed":[{"@type":"City","name":"Omaha, NE"}],'
        f'"sameAs":["{INSTAGRAM}","{FACEBOOK}"],'
        '"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"09:00","closes":"19:00"}],'
        '"aggregateRating":{"@type":"AggregateRating","ratingValue":"5.0","reviewCount":"4","bestRating":"5"},'
        f'"review":[{reviews}]'
        '}'
        '</script>'
    )


def seo_block(title, desc, url):
    # title/desc are extracted from <title>/<meta> which are ALREADY HTML-escaped,
    # so use them as-is (re-escaping would double-encode & -> &amp;amp;).
    t, d = title, desc
    return "\n".join([
        '<!-- SEO:start (managed by seo.py) -->',
        f'<link rel="canonical" href="{url}" />',
        '<meta name="robots" content="index, follow" />',
        '<meta name="theme-color" content="#08080a" />',
        '<meta name="geo.region" content="US-NE" />',
        '<meta name="geo.placename" content="Omaha, Nebraska" />',
        '<meta name="ICBM" content="41.2565, -95.9345" />',
        '<meta property="og:type" content="website" />',
        '<meta property="og:site_name" content="Xtreme Mobile Detailing" />',
        f'<meta property="og:title" content="{t}" />',
        f'<meta property="og:description" content="{d}" />',
        f'<meta property="og:url" content="{url}" />',
        f'<meta property="og:image" content="{OG_IMAGE}" />',
        '<meta name="twitter:card" content="summary_large_image" />',
        f'<meta name="twitter:title" content="{t}" />',
        f'<meta name="twitter:description" content="{d}" />',
        f'<meta name="twitter:image" content="{OG_IMAGE}" />',
        local_business_jsonld(),
        '<!-- SEO:end -->',
    ])


# lines/blocks we manage and must strip before re-inserting (idempotency)
STRIP_LINE = re.compile(
    r'^[ \t]*(<link[^>]+rel="canonical"[^>]*>|'
    r'<meta[^>]+(property="og:|name="twitter:|name="geo\.|name="ICBM"|name="theme-color"|name="robots")[^>]*>)[ \t]*\n',
    re.M)
STRIP_BLOCK = re.compile(r'[ \t]*<!-- SEO:start.*?<!-- SEO:end -->\n?', re.S)
STRIP_LD = re.compile(r'[ \t]*<script type="application/ld\+json" id="ld-business">.*?</script>\n?', re.S)


def process_page(fp):
    html = fp.read_text()
    # remove previously-managed tags
    html = STRIP_BLOCK.sub("", html)
    html = STRIP_LD.sub("", html)
    html = STRIP_LINE.sub("", html)

    title_m = re.search(r"<title>(.*?)</title>", html, re.S)
    desc_m = re.search(r'<meta name="description" content="(.*?)"\s*/?>', html, re.S)
    title = (title_m.group(1).strip() if title_m else BUSINESS)
    desc = (desc_m.group(1).strip() if desc_m else "")
    url = page_url(fp.name)

    block = seo_block(title, desc, url)
    html = html.replace("</head>", block + "\n</head>", 1)
    fp.write_text(html)
    return url


def build_sitemap(urls_by_file):
    today = datetime.date.today().isoformat()
    rows = []
    for fname, url in urls_by_file:
        prio, freq = PRIORITY.get(fname, DEFAULT_MAIN)
        rows.append(
            f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n"
            f"    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>"
        )
    body = "\n".join(rows)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           f"{body}\n</urlset>\n")
    (ROOT / "sitemap.xml").write_text(xml)


def build_robots():
    txt = ("User-agent: *\n"
           "Allow: /\n\n"
           f"Sitemap: {DOMAIN}/sitemap.xml\n")
    (ROOT / "robots.txt").write_text(txt)


def main():
    pages = sorted(p for p in ROOT.glob("*.html"))
    urls = []
    for fp in pages:
        url = process_page(fp)
        urls.append((fp.name, url))
        print(f"  SEO -> {fp.name}")
    build_sitemap(urls)
    build_robots()
    print(f"  sitemap.xml ({len(urls)} urls) + robots.txt written")
    print(f"  domain: {DOMAIN}")


if __name__ == "__main__":
    main()
