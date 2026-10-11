# CLAUDE.md — International Organisation Internship Opportunities

Build brief for Claude Code. Read this file fully before writing code. It is self-contained for building the site. The full product spec is PRD v2 (`docs/PRD.md` once exported; see `docs/README.md`); where they differ, this file wins for implementation details.

## What this is

A static website, hosted on GitHub Pages (github.io), listing **funded visits of up to 6 months at international organisations in Europe** (EU, EEA, Switzerland, UK) that are open to students of any nationality. Audience: master's and PhD students. Site name: **International Organisation Internship Opportunities**. Subtitle: "Funded visits across Europe, open to all nationalities".

The maintainer updates the site only by editing `data/database.xlsx` and pushing it. No code change is needed for data updates.

## Hard constraints

1. **Quarto only.** A Quarto website. All interactivity in Observable JS (`{ojs}`) cells. No `{r}` or `{python}` chunks, no R/Python/Node build step, no npm, no frameworks (React, Svelte, etc.).
2. **The site reads `data/database.xlsx` directly in the browser** via `FileAttachment("data/database.xlsx").xlsx()`. No conversion to JSON/CSV, no generated data files. Declare the workbook as a project resource so it is copied to `_site/`.
3. **Never edit `data/database.xlsx`.** It is maintainer-owned. Never hard-code counts, names or records in pages: compute everything from the workbook.
4. **Static hosting.** No server, no cookies, no tracking, no analytics, no browser storage. All shareable state (filters, selected place, compare selection) lives in the URL query string.
5. **Deep links via query parameters:** `place.html?city=geneva`, `place.html?country=switzerland`, `organisation.html?org=<org_id>`, `opportunities.html?discipline=STEM&type=research&compare=EU-048,EU-061`.
6. **Accessibility:** WCAG 2.2 AA. Real `<button>`, `<a href>`, `<input>` + `<label>`; colour never the only signal (every badge/segment has a text label); every chart has a data-table alternative; the map has a city table alternative; keyboard usable.
7. **Performance:** first meaningful content under 2 s on a normal connection; load map tiles after the figure tiles render.

## Repository layout (target)

```
_quarto.yml            # website config: title, navbar, theme, resources, fonts
_load.qmd              # shared OJS: load workbook, parse, join, validate (included in every page; underscore = not rendered alone)
index.qmd              # home (mockup E)
opportunities.qmd      # list + filters + search + sort + compare mode
place.qmd              # city/country pages (?city= / ?country=)
organisation.qmd       # organisation pages (?org=)
checks.qmd             # Data checks page (not in the navbar)
about.qmd              # About text from the workbook's About sheet
styles.scss            # design tokens
data/database.xlsx     # data (maintainer-owned)
.github/workflows/publish.yml
```

Include `_load.qmd` in each page with `{{< include _load.qmd >}}`. Keep files few; do not add helper JS files unless a page exceeds ~400 lines of OJS.

## Data contract (`data/database.xlsx`)

The site reads **four sheets**. Header row = row 1. Ignore other sheets (README, Seed list, Summary).

### Organisations (one row per organisation)
`org_id, name, org_type, country, city, website, official_domains, careers_page, contact_page, contact_type, visa_exempt, visa_scope, visa_note, visa_source_url, seed_source, last_checked, notes`

- `org_type` ∈ {Intergovernmental, UN agency, EU institution, International NGO, International foundation or union}
- `visa_exempt` ∈ {Yes, No, Not stated}; `visa_scope` = host country the value applies to
- `contact_type` ∈ {general contact page, programme or general inbox, media/press contact page}; `contact_page` may be a `mailto:` link

### Opportunities (one row per opportunity, every status)
`opportunity_id, org_id, name, summary, opportunity_type, discipline_area, career_stage, funding_type, funding_amount, funding_currency, funding_period, funding_note, duration_max_weeks, duration_note, nationality_note, host_city, location_note, location_country, deadline_type, next_deadline, application_url, source_url, source_official, verification_status, status_reasons, last_checked`

- `verification_status` ∈ {Verified, Unverified, Excluded}. **Show Verified and Unverified; never show Excluded.**
- `opportunity_type` ∈ {Internship, Traineeship, Fellowship, Travel grant, PhD visit, Visiting researcher}. **Research visit** = Fellowship, Travel grant, PhD visit or Visiting researcher.
- `discipline_area` ∈ {STEM, Social sciences, Any}. Filters offer STEM and Social sciences; **records with Any appear under both**.
- `funding_amount` may be blank → display "amount not stated" with `funding_note` as detail. Never convert currencies.
- `next_deadline` may be a date or free text (e.g. "Late January 2027 (approx., annual)"); display as given; sort only real dates.
- `host_city` joins to Places.city; `org_id` joins to Organisations.org_id.
- Excel cells may arrive as numbers, strings, Date objects or empty: normalise in `_load.qmd` (trim strings, empty → null, IDs as strings).

### Places (one row per host city)
`city, country, latitude, longitude, visa_rule, visa_rule_source`. Slug for URLs: lowercase, spaces → hyphens (`the-hague`).

### About
Column `text`; each non-empty row is one paragraph of the About page, in order.

### Derived (never stored)
- Organisation shown on site = has ≥1 Verified/Unverified opportunity.
- Counts, charts, deadlines, stipends tiles: computed from shown rows (respecting active filters where the PRD says filter-aware).

## Data checks (`checks.qmd`)

Run on load in `_load.qmd`; a shown record that fails any check is **hidden from all pages** and listed on `checks.qmd` with the reason. Checks (shown rows only unless stated):

1. Required fields present: `opportunity_id, org_id, name, opportunity_type, discipline_area, funding_type, duration_max_weeks, host_city, source_url, verification_status, last_checked`.
2. `org_id` exists in Organisations.
3. `host_city` exists in Places, and that Places row has numeric latitude/longitude.
4. Enum values valid (lists above).
5. `duration_max_weeks` ≤ 26.
6. Verified rows: `source_official` = Yes and `status_reasons` empty.
7. Unverified rows: `status_reasons` non-empty.
8. `opportunity_id` and `org_id` unique (all rows).
9. URLs start with `http`, or `mailto:` for `contact_page`.

`checks.qmd` shows: total rows read per sheet, counts by status, and a table of failing rows (id, field, problem). When nothing fails, say so plainly.

## Design (chosen: mockup E)

Mockups canvas: https://claude.ai/artifact/6FnyoPCv1inwGQvWkh5pVW (artboard **E** is the chosen home screen).

**Tokens** (`styles.scss`, Bootstrap theme variables via Quarto `theme:`):
- Page background `#EEF2F6`; tiles white, radius 16px, no heavy shadows; ink `#15202B`; secondary text `#4A5868`.
- Accent / links `#1A5BB5`; dark band `#15202B`.
- Discipline colours: STEM `#1E63C4`, Social sciences `#D2741F`, Any field `#5E6A75`.
- Verified badge: solid green (`#1F6F43`, white text). Unverified badge: amber outline (`#B5730A` border, `#8A5300` text) + the missing detail.
- Fonts: **Space Grotesk** (headings, figures), **Source Sans 3** (body). Fallback stacks required. Self-hosted in `fonts/` (OFL, from @fontsource 5.3.0) so no visitor request goes to Google (decided 11 October 2026); do not load them from Google Fonts.
- Light theme only for the MVP.

**Home (`index.qmd`), top to bottom:**
1. Navbar: logo (inline SVG globe with an orange dot) + site name + subtitle; links: Overview, Opportunities, Places, Compare (count from URL), About.
2. Headline: "{N} funded visits at international organisations, open to every nationality" (N = shown count) + search box (submits to `opportunities.html?q=`).
3. Four figure tiles in one row: verified + unverified counts; organisations shown; host cities and countries; funded PhD research visits (blue tile, links to section 6).
4. **Full-width Leaflet map**: one marker per host city, radius on a capped sqrt scale, labelled for cities with ≥3; filter-aware; hover/focus card (city, counts by discipline, verified count, country visa rule, link); click → `place.html?city=`. Under it: "See all as a list" link and the city table alternative (can be collapsed).
5. Four summary tiles in one row: by discipline (bars); by country (top 6, links to country pages); upcoming deadlines (next 4 with real dates or text); stated monthly stipends (official amounts with period "Per month", plus "N of M records state no amount").
5b. "Apply any time" row: programmes with `deadline_type` = Rolling (up to 6) + "See all" → `opportunities.html?deadline=rolling` (decided 11 October 2026: Rolling is the most stable option, so it is prioritised).
6. Dark band "Funded research visits for PhD students": up to 4 cards (programme, place, duration, funding or deadline) + "See all" → `opportunities.html?type=research`.
7. "Browse by city" pill links with counts.
8. Footer line: "© 2026 Stefanus Bernard · Data checked up to <max `last_checked`>" (decided 11 October 2026). The "confirm details with the organisation before applying; visa decisions rest with the host country" disclaimer lives on the About page and on Unverified cards.

**Opportunity card (Opportunities page), in order:** name; organisation (link); city, country; type (+ "Research visit" marker); funding (type + amount/currency/period or "amount not stated"); duration (`duration_note`); career stage; nationality/eligibility note; verification badge (+ reason and the caution "Confirm nationality and right-to-work terms in the current vacancy notice before applying." for Unverified); visa value in words with scope ("Visa-exempt: yes (Switzerland)"); deadline; official source link; last checked; "Add to compare".

**Filters (Opportunities):** search (name, organisation, summary, city); discipline (STEM / Social sciences); type (Research visit / Internship / Traineeship); career stage (PhD eligible / Master's eligible — text match on `career_stage`); country; deadline (Rolling / Ad hoc vacancies / Fixed, from `deadline_type`; `?deadline=rolling|adhoc|fixed`); verification (Verified only); visa-exempt yes; amount stated. Sort: Rolling first (default; then Ad hoc, then Fixed, each by country), country, amount (within currency+period), duration, name, deadline. Empty state names the active filters with a "Clear filters" button.

**Compare:** max 3 IDs in `?compare=`; table with one column per opportunity and rows: organisation, location, type, funding, duration, career stage, eligibility note, visa, deadline, verification, source link. Adding a 4th asks which to replace.

**Place page:** header with counts, mini-map, Places `visa_rule` + source link, small charts, organisations in the place with their opportunities. Country page lists its cities.

**Organisation page:** facts, visa value + scope + note + source, careers and contact links (label by `contact_type`), all shown opportunities (Unverified labelled).

**About:** paragraphs from the About sheet, then licences (code MIT, data CC BY 4.0) and a "Report an issue" link to the GitHub issue form `.github/ISSUE_TEMPLATE/report-record.yml` (card links prefill `record` and `source`). No email address on the site.

## Libraries

- Observable Plot and d3: built into Quarto OJS.
- Leaflet 1.9.4: `L = require("leaflet@1.9.4")`; add its CSS via `include-in-header` in `_quarto.yml` (`https://unpkg.com/leaflet@1.9.4/dist/leaflet.css`).
- Basemap: a free light raster style, e.g. CARTO Positron (`https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png`) with attribution "© OpenStreetMap contributors © CARTO". Check the provider's usage terms before launch; keep tile requests modest (no tile prefetch, sensible max zoom).
- No other external libraries unless clearly needed; if added, pin the version.

## Build order (stop after each step for the maintainer to review)

1. **Skeleton:** `_quarto.yml` (website, navbar, theme with `styles.scss`, fonts, resources), empty pages, `publish.yml` works. Check: `quarto preview` runs; navbar shows; `_site/data/database.xlsx` exists after `quarto render`.
2. **Data layer + checks:** `_load.qmd` loads all four sheets, normalises, joins, derives shown rows, runs checks; `checks.qmd` complete. Check: checks page shows 0 failing rows on the current workbook and correct counts (49 shown: 42 Verified, 7 Unverified at the time of writing).
3. **Home (mockup E)** without the map, then the map. Check: figures match the checks page; map markers for every host city; keyboard and table alternatives work.
4. **Opportunities:** cards, filters, search, sort, URL state, empty state. Check: `?discipline=STEM` includes Any records; `?type=research` shows the research visits; Excluded never appears.
5. **Place and Organisation pages.** Check: `place.html?city=geneva`, `place.html?country=switzerland`, `organisation.html?org=world-meteorological-organization` render; unknown slug shows a friendly "not found".
6. **Compare.** Check: selection survives reload and sharing the URL.
7. **About + polish:** footer, snapshot date, accessibility pass (axe or Lighthouse ≥ 90 accessibility), mobile layout (tiles stack, map height reduces).

## Commands

- Preview: `quarto preview`
- Render: `quarto render` (output in `_site/`)
- Deploy: push to `main`; `.github/workflows/publish.yml` renders and deploys to GitHub Pages.

## Don'ts

- Don't add R, Python, Node build steps, or JSON/CSV copies of the data.
- Don't show Excluded records anywhere except the checks page counts.
- Don't invent or "fill in" missing data (amounts, deadlines, visa values). Blank stays blank with the agreed wording.
- Don't use emoji as icons; use inline SVG.
- Don't store anything in localStorage/sessionStorage/cookies.
