#!/usr/bin/env python3
"""Open one use-case candidate issue per entry of the batch files in intake/.

Each issue is written as the use-case candidate form would write it, so the
rest of the funnel (labels, project board, triage) treats it the same way.
Candidates whose title matches an existing use-case issue are skipped.

Run from the repository root:
  python3 scripts/intake.py --dry-run     print what would be created
  GITHUB_TOKEN=… GITHUB_REPOSITORY=owner/repo python3 scripts/intake.py

Needs PyYAML.
"""

import csv
import json
import os
import pathlib
import sys
import urllib.request

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "https://api.github.com"


def rows(name):
    path = ROOT / "_data" / name
    if not path.exists():
        return []
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


SECTORS = {r["id"]: r for r in rows("sectors.csv")}
FLOWS = {r["id"]: r for r in rows("trust-flows.csv")}
PATTERNS = {r["id"]: r for r in rows("ifm-patterns.csv")}
GROUPS = {r["id"]: r for r in rows("working-groups.csv")}


def section(sector_id):
    s = SECTORS.get(sector_id)
    while s and s["broader"]:
        s = SECTORS.get(s["broader"])
    return s["notation"] if s else None


def api(method, path, body=None):
    req = urllib.request.Request(
        f"{API}{path}", method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "didas-use-case-repository intake"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read() or b"null")


def existing_titles(repo):
    titles, page = set(), 1
    while True:
        batch = api("GET", f"/repos/{repo}/issues?state=all&labels=use-case&per_page=100&page={page}")
        titles |= {i["title"].removeprefix("[Use case]").strip().lower() for i in batch}
        if len(batch) < 100:
            return titles
        page += 1


def published_titles():
    """Titles of the use cases already published as entries in use-cases/."""
    titles = set()
    for path in (ROOT / "use-cases").glob("*.md"):
        if path.name.startswith(("_", "README")):
            continue
        fm = yaml.safe_load(path.read_text(encoding="utf-8").split("---")[1]) or {}
        if fm.get("title"):
            titles.add(str(fm["title"]).strip().lower())
    return titles


def known(ids, table, what, title, warnings):
    out = []
    for i in ids or []:
        if i in table:
            out.append(i)
        else:
            warnings.append(f"{title}: unknown {what} {i!r}, left out")
    return out


def issue(c, batch, warnings):
    title = str(c["title"]).strip()
    sectors = known(c.get("sectors"), SECTORS, "sector", title, warnings)
    flows = known(c.get("trust_flows"), FLOWS, "trust flow", title, warnings)
    patterns = known(c.get("ifm_patterns"), PATTERNS, "pattern", title, warnings)
    als = [a for a in c.get("ambition_levels") or [] if a in ("AL1", "AL2", "AL3")]
    group = c.get("working_group")
    if group and group not in GROUPS:
        warnings.append(f"{title}: unknown working group {group!r}, kept as label")

    def text(key, default="_No response_"):
        v = c.get(key)
        return str(v).strip() if v else default

    sections = [
        ("Use case", title),
        ("Situation and outcome", text("summary", "_To be detailed by the working group that takes this candidate._")),
        ("Actors", text("actors")),
        ("Credentials needed", text("credentials")),
        ("Credentials already on I14Y (optional)", ", ".join(c.get("i14y_credentials") or []) or "_No response_"),
        ("Emerging or other schemas (optional)", text("schemas")),
        ("Ambition level(s)", "\n".join(f"- [{'X' if a in als else ' '}] {a}" for a in ("AL1", "AL2", "AL3"))),
        ("Sector(s)", ", ".join(f"{s} · {SECTORS[s]['label']}" for s in sectors) or "_No response_"),
        ("Trust flows (optional)", ", ".join(f"{f} · {FLOWS[f]['title']}" for f in flows) or "_No response_"),
        ("Use case pattern in the Industry Function Graph (optional)", ", ".join(f"{p} · {PATTERNS[p]['name']}" for p in patterns) or "_No response_"),
        ("Other flow diagrams (optional)", text("other_flows")),
        ("Implementations, pilots and showcases (optional)", text("implementations")),
        ("Legal basis and governance (optional)", text("governance")),
        ("Demand and value (optional)", text("demand")),
        ("Proposed on behalf of (optional)", text("proposed_by", batch.get("proposed_by") or "_No response_")),
        ("Sources (optional)", text("sources")),
    ]
    body = f"_Filed with the intake batch **{batch.get('batch', 'unnamed')}**._\n\n"
    body += "\n\n".join(f"### {h}\n\n{v}" for h, v in sections)
    labels = ["use-case", "stage: signal", "intake-batch"] + als
    labels += sorted({f"ISIC {section(s)}" for s in sectors if section(s)})
    if group:
        labels.append(f"wg: {group}")
    return {"title": f"[Use case] {title}", "body": body, "labels": labels}


def main():
    dry = "--dry-run" in sys.argv
    repo = os.environ.get("GITHUB_REPOSITORY", "DIDAS-swiss/use-case-repository")
    published = published_titles()
    have = set() if dry else existing_titles(repo)
    created = skipped = 0
    for path in sorted((ROOT / "intake").glob("*.y*ml")):
        if path.name.startswith("_"):
            continue
        batch = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for c in batch.get("candidates") or []:
            warnings = []
            new = issue(c, batch, warnings)
            for w in warnings:
                print(f"::warning file={path.relative_to(ROOT)}::{w}")
            key = new["title"].removeprefix("[Use case]").strip().lower()
            if key in published:
                skipped += 1
                print(f"skip   {new['title']} (already published in use-cases/)")
                continue
            if key in have:
                skipped += 1
                print(f"skip   {new['title']} (exists)")
                continue
            if dry:
                print(f"would create {new['title']}  labels={new['labels']}")
                print(new["body"][:400].replace("\n", "\n    "), "\n")
            else:
                made = api("POST", f"/repos/{repo}/issues", new)
                print(f"create #{made['number']} {new['title']}")
            have.add(key)
            created += 1
    print(f"{created} {'to create' if dry else 'created'}, {skipped} skipped")


if __name__ == "__main__":
    main()
