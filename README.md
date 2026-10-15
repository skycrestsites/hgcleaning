# H&G Cleaning Co. website

A fast, mobile-first static site (home page + 8 service pages) for H&G Cleaning Co., serving Salt Lake City, Utah and the surrounding areas.

## Files
- `index.html` - home page
- `services/<service>/index.html` - one page per service (8 total)
- `css/styles.css` - all styles (navy `#011729` + brand blue `#0b78dc` from the logo, Plus Jakarta Sans headings, Inter body)
- `js/main.js` - mobile menu, services dropdown and header behaviour
- `assets/` - logo, favicons, Open Graph image and optimized WebP photos
- `robots.txt`, `sitemap.xml`, `site.webmanifest`, `404.html`
- `tools/build.py` - generates every HTML page from one template (edit content here, then run `python tools/build.py`)

## Clean URLs (no .html)
Every page is an `index.html` inside its own folder, so any static host (Netlify, Vercel, Cloudflare Pages, GitHub Pages, Apache/Nginx) serves:

    https://hgcleaningco.com/
    https://hgcleaningco.com/services/deep-cleaning/

No `.html` ever shows in the address bar.

## Booking
All booking goes through the BookingKoala form at `https://hgcleaningco.bookingkoala.com/booknow?embed=true`,
embedded in the "Book Online" section (`#book`) on every page.

`embed.js` is intentionally NOT loaded. The iframe has a fixed viewport height (`100vh` / `100dvh` in
`css/styles.css`) with `scrolling="yes"`, so the form scrolls inside the iframe and BookingKoala's modals
appear in the visible viewport, exactly like opening the booknow URL in a tab. Do not add `embed.js` back.

## Before going live
These are placeholders. Update them in `BUSINESS` at the top of `tools/build.py` and rebuild:
1. Phone: `(801) 555-0142`
2. Email: `hello@hgcleaningco.com`
3. Domain: `https://hgcleaningco.com` (also used in `sitemap.xml` and `robots.txt`)
4. Hours: `Mon to Sat, 8:00 AM to 6:00 PM`
5. Service area: Salt Lake City and nearby cities (`AREAS` list)

Also: swap stock photos for real job photos when available, and add the site to Google Business Profile and Google Search Console.

## SEO included
- Unique title, description and keywords on every page, canonical URLs
- Open Graph and Twitter cards with a branded share image
- Geo meta tags and `HouseCleaningService` JSON-LD (services, service areas, hours, reviews)
- Per-service `Service`, `BreadcrumbList` and `FAQPage` structured data
- `robots.txt` and `sitemap.xml`
