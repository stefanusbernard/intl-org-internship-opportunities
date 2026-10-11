# International Organisation Internship Opportunities

Funded visits of up to 6 months at international organisations across Europe (EU, EEA, Switzerland, UK), open to students of any nationality. A static Quarto site hosted on GitHub Pages.

Snapshot: data checked 7–11 October 2026. Every record links to its official source; confirm details with the organisation before applying. Visa decisions rest with the host country.

## Repository contents

| Path | Purpose |
|---|---|
| `data/database.xlsx` | The database. The only file edited to update the site. |
| `CLAUDE.md` | Build brief for Claude Code (stack, data contract, design, build order). |
| `docs/` | PRD v2 link and how to export it as `docs/PRD.md`; mockup link. |
| `.github/workflows/publish.yml` | Renders the site with Quarto and deploys it to GitHub Pages on every push to `main`. |
| `.github/workflows/link-check.yml` | Checks every link the site shows (monthly, and when the workbook changes) and keeps one open "broken-links" issue listing the links to fix. Maintenance only; not part of the site build. |

## First-time setup

1. Create a new **public** GitHub repository (no README, no licence; this pack has them).
2. Unzip this pack into the cloned folder, then commit and push to `main`.
3. In the repository: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. Install [Quarto](https://quarto.org/docs/get-started/) and, in VS Code, the Quarto extension (recommended automatically via `.vscode/extensions.json`).
5. Open the folder in VS Code and start Claude Code. Ask it to read `CLAUDE.md` and do **step 1** of the build order. Review each step before continuing.

The site will be at `https://<your-username>.github.io/<repository-name>/`.

## Updating the data

1. Research with Claude in a chat (upload the current `data/database.xlsx`).
2. Edit `data/database.xlsx`: one row per record; set `verification_status` (Verified / Unverified / Excluded); never delete rows.
3. Commit and push. GitHub Actions rebuilds the site in a few minutes.
4. Open the site's **Data checks** page (`/checks.html`) and confirm no rows are flagged.
5. Check the repository's Issues for a **broken-links** issue (opened by the Link check workflow) and fix any links it lists. Sites that block automated visitors are not checked; open those in a browser at each quarterly refresh.

Full guide: `docs/PRD.md`, section "Maintainer guide: updating the database", and the README sheet inside the workbook.

## Licences

- Code: MIT (`LICENSE`)
- Data: CC BY 4.0 (`LICENSE-data`)
