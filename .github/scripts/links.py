"""Link check helper for .github/workflows/link-check.yml (maintenance only, not part of the site build).

  python links.py list   <workbook> <links.txt> <links-map.json>
      Writes every URL the site displays (shown records only: Verified and Unverified),
      one per line, plus a map of which record and field uses each URL.

  python links.py report <lychee.json> <links-map.json> <issue.md>
      Turns lychee's JSON output into an issue body grouped by record.
      Prints the number of broken links (also written to $GITHUB_OUTPUT as `broken`).
"""
import json
import os
import sys
from collections import defaultdict


def cell(v):
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def rows(wb, name):
    it = wb[name].iter_rows(values_only=True)
    header = [cell(h) for h in next(it)]
    out = []
    for r in it:
        rec = {h: cell(v) for h, v in zip(header, r) if h}
        if any(rec.values()):
            out.append(rec)
    return out


def list_links(workbook, links_txt, map_json):
    import openpyxl

    wb = openpyxl.load_workbook(workbook, read_only=True, data_only=True)
    opps = [o for o in rows(wb, "Opportunities") if o.get("verification_status") in ("Verified", "Unverified")]
    orgs = {o["org_id"]: o for o in rows(wb, "Organisations") if o.get("org_id")}
    places = {p["city"]: p for p in rows(wb, "Places") if p.get("city")}

    used = defaultdict(list)

    def add(url, label):
        if url and url.lower().startswith(("http://", "https://")):
            used[url].append(label)

    for o in opps:
        for f in ("source_url", "application_url"):
            add(o.get(f), f"{o['opportunity_id']} ({o.get('name')}): {f}")
    for org_id in sorted({o.get("org_id") for o in opps if o.get("org_id")}):
        g = orgs.get(org_id)
        if g:
            for f in ("website", "careers_page", "contact_page", "visa_source_url"):
                add(g.get(f), f"Organisation {org_id}: {f}")
    for city in sorted({o.get("host_city") for o in opps if o.get("host_city")}):
        p = places.get(city)
        if p:
            add(p.get("visa_rule_source"), f"Place {city}: visa_rule_source")

    with open(links_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(used)) + "\n")
    with open(map_json, "w", encoding="utf-8") as f:
        json.dump(used, f, indent=1)
    print(f"{len(used)} links listed from {len(opps)} shown records")


def report(lychee_json, map_json, issue_md):
    with open(lychee_json, encoding="utf-8") as f:
        result = json.load(f)
    with open(map_json, encoding="utf-8") as f:
        used = json.load(f)

    failed = {}
    for key in ("fail_map", "error_map"):
        for entries in (result.get(key) or {}).values():
            for e in entries:
                status = e.get("status")
                if isinstance(status, dict):
                    text = status.get("text") or ""
                    code = status.get("code")
                    status = f"{code} {text}".strip() if code else text
                failed[e.get("url")] = str(status or "failed")

    broken = len(failed)
    lines = [
        "The monthly link check found links in `data/database.xlsx` that no longer work.",
        "",
        "Fix them in the workbook: prefer the organisation's standing programme page over a single vacancy; "
        "if no official page remains, set the record to Unverified or Excluded with the reason in `status_reasons`. "
        "Update `last_checked` on each record you fix.",
        "",
        "| Link | Problem | Used by |",
        "|---|---|---|",
    ]
    for url in sorted(failed, key=lambda u: used.get(u, ["~"])[0]):
        where = "<br>".join(used.get(url, ["(not in the workbook list)"]))
        lines.append(f"| {url} | {failed[url]} | {where} |")
    lines += [
        "",
        f"Checked {result.get('total', '?')} links. Pages that block automated visitors (HTTP 403/429) are not "
        "counted as broken; open them in a browser at each quarterly refresh.",
        "",
        "This issue is updated by the Link check workflow and closed automatically when every link works.",
    ]
    with open(issue_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            f.write(f"broken={broken}\n")
    print(f"{broken} broken links")


if __name__ == "__main__":
    cmd, *args = sys.argv[1:]
    {"list": list_links, "report": report}[cmd](*args)
