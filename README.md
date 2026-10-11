# International Organisation Internship Opportunities

Funded visits of up to 6 months at international organisations across Europe (EU, EEA, Switzerland, UK), open to students of any nationality. A static Quarto site hosted on GitHub Pages.

Live site: https://stefanusbernard.github.io/intl-org-internship-opportunities/

Snapshot: data checked 7–11 October 2026. Every record links to its official source; confirm details with the organisation before applying. Visa decisions rest with the host country.

## Repository contents

| Path | Purpose |
|---|---|
| `data/database.xlsx` | The database. The only file edited to update the site. |
| `*.qmd`, `_load.qmd`, `_quarto.yml`, `styles.scss` | The site: pages, shared data layer (reads the workbook in the browser and runs the data checks), settings and design. |
| `fonts/`, `images/` | Self-hosted fonts (SIL Open Font License) and the favicon and link-preview image. |
| `.github/workflows/publish.yml` | Renders the site with Quarto and deploys it to GitHub Pages on every push to `main`. |
| `.github/workflows/link-check.yml` | Checks every link the site shows (monthly, and when the workbook changes) and keeps one open "broken-links" issue listing the links to fix. Maintenance only; not part of the site build. |
| `.github/ISSUE_TEMPLATE/report-record.yml` | The form visitors use to report an outdated or wrong record. |

## Preview locally

1. Install [Quarto](https://quarto.org/docs/get-started/) and, in VS Code, the Quarto extension (recommended automatically via `.vscode/extensions.json`).
2. Run `quarto preview` in the repository folder and open the address it prints.

## Updating the data

1. Research each record on the organisation's official website.
2. Edit `data/database.xlsx`: one row per record; set `verification_status` (Verified / Unverified / Excluded); never delete rows. Keep the sheet and column names as they are.
3. Commit and push. GitHub Actions rebuilds the site in a few minutes.
4. Open the site's **Data checks** page (`/checks.html`) and confirm no rows are flagged.
5. Check the repository's Issues for a **broken-links** issue (opened by the Link check workflow) and fix any links it lists. Sites that block automated visitors are not checked; open those in a browser at each quarterly refresh.
6. At each refresh, update the snapshot date in the workbook's About sheet.

Full guide: the README sheet inside the workbook.

## Licences

- Code: MIT (`LICENSE`)
- Data: CC BY 4.0 (`LICENSE-data`)
