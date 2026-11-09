#!/usr/bin/env python3
"""Refresh the lists this repository anchors its use cases to.

A use case here is the anchor that the other DIDAS repositories meet at. This
script copies the vocabularies it points into, from their own repositories:

  _data/trust-flows.csv  every flow of the DIDAS Trust Flow Diagram Repository,
                         identified as <sector>/<family>/<flow>
  _data/ifm-patterns.csv every use case pattern of the DIDAS Industry Function
                         Graph
  _data/sectors.csv      the graph's ISIC Rev. 5 sector list
  _data/glossary-terms.csv
                         every term of the DIDAS Glossary, with its link

The credential datasets on I14Y come from scripts/i14y_sync.py. After either
script, scripts/build_issue_form.py puts the lists into the issue form.

Run from the repository root:  python3 scripts/sources_sync.py
Needs git and PyYAML (the Trust Flow repository classifies flows in YAML).
"""

import csv
import io
import pathlib
import subprocess
import sys
import tempfile
import urllib.parse

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
TFR = "https://github.com/DIDAS-swiss/Trust-Flow-Diagram-Repository"
IFM = "https://github.com/DIDAS-swiss/industry-function-graph"
IFM_PAGE = "https://didas-swiss.github.io/industry-function-graph/"
GLOSSARY = "https://github.com/DIDAS-swiss/didas-glossary"
GLOSSARY_PAGE = "https://didas-swiss.github.io/didas-glossary/"


def clone(url, into):
    subprocess.run(["git", "clone", "--quiet", "--depth", "1", url, str(into)], check=True)
    head = subprocess.run(["git", "-C", str(into), "rev-parse", "--short", "HEAD"],
                          check=True, capture_output=True, text=True)
    return head.stdout.strip()


def write_csv(path, fieldnames, rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    if path.exists() and path.read_text(encoding="utf-8") == buf.getvalue():
        return False
    path.write_text(buf.getvalue(), encoding="utf-8")
    return True


def flow_url(repo, sector_dir, family, flow_id):
    """The flow's own file where it has one, else its family's directory."""
    for f in sorted(sector_dir.rglob(f"{flow_id}-*.md")):
        return f"{TFR}/blob/main/{urllib.parse.quote(str(f.relative_to(repo)))}"
    directory = family.get("directory")
    if directory and (sector_dir / directory).is_dir() and not directory.startswith("likec4"):
        return f"{TFR}/tree/main/{urllib.parse.quote(sector_dir.name + '/' + directory)}"
    return f"{TFR}/tree/main/{urllib.parse.quote(sector_dir.name)}"


def trust_flows(repo):
    rows = []
    for sector_file in sorted(repo.glob("*/sector.yaml")):
        sector = yaml.safe_load(sector_file.read_text(encoding="utf-8")) or {}
        if sector.get("sector") in (None, "basic-flow"):
            continue
        division = str((sector.get("noga") or {}).get("division") or "")
        for family in sector.get("families") or []:
            for flow in family.get("flows") or []:
                rows.append({
                    "id": f"{sector['sector']}/{family['id']}/{flow['id']}",
                    "sector": sector["sector"],
                    "isic_division": f"ISIC-{division}" if division else "",
                    "family": family.get("title") or family["id"],
                    "title": flow.get("title") or flow["id"],
                    "status": flow.get("status") or family.get("status") or "",
                    "url": flow_url(repo, sector_file.parent, family, flow["id"]),
                })
    return rows


def ifm_patterns(repo):
    with open(repo / "data" / "use-cases.csv", encoding="utf-8", newline="") as f:
        return [{"id": r["id"], "name": r["name"], "description": r["description"],
                 "url": f"{IFM_PAGE}#{r['id']}"} for r in csv.DictReader(f)]


def sectors(repo):
    """The graph's sectors, each section followed by its divisions and classes."""
    with open(repo / "data" / "sectors.csv", encoding="utf-8", newline="") as f:
        rows = [{"id": r["id"], "level": r["level"], "notation": r["notation"],
                 "label": r["pref_label_en"], "broader": r["broader"]} for r in csv.DictReader(f)]
    children = {}
    for r in rows:
        children.setdefault(r["broader"], []).append(r)
    ordered = []

    def walk(r):
        ordered.append(r)
        for c in sorted(children.get(r["id"], []), key=lambda c: c["notation"]):
            walk(c)

    for r in sorted(children.get("", []), key=lambda r: r["notation"]):
        walk(r)
    return ordered


def glossary_terms(repo):
    """Each term file's id, its name and its anchor on the published glossary."""
    import re
    rows = []
    for path in sorted((repo / "spec" / "terms-definitions").glob("*.md")):
        first = path.read_text(encoding="utf-8").split("\n", 1)[0]
        m = re.match(r"\[\[(?:def|tref):\s*(?:toip-glossary,\s*)?([^,\]]+)", first)
        if not m:
            continue
        term = m.group(1).strip()
        slug = re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")
        rows.append({"id": path.stem, "term": term, "url": f"{GLOSSARY_PAGE}#term:{slug}"})
    return rows


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tfr, ifm, glo = pathlib.Path(tmp, "tfr"), pathlib.Path(tmp, "ifm"), pathlib.Path(tmp, "glossary")
        tfr_head, ifm_head, glo_head = clone(TFR, tfr), clone(IFM, ifm), clone(GLOSSARY, glo)
        data = ROOT / "_data"
        results = {
            f"trust-flows.csv (Trust Flow Diagram Repository at {tfr_head})": write_csv(
                data / "trust-flows.csv",
                ["id", "sector", "isic_division", "family", "title", "status", "url"],
                trust_flows(tfr)),
            f"ifm-patterns.csv (Industry Function Graph at {ifm_head})": write_csv(
                data / "ifm-patterns.csv", ["id", "name", "description", "url"], ifm_patterns(ifm)),
            f"sectors.csv (Industry Function Graph at {ifm_head})": write_csv(
                data / "sectors.csv", ["id", "level", "notation", "label", "broader"], sectors(ifm)),
            f"glossary-terms.csv (DIDAS Glossary at {glo_head})": write_csv(
                data / "glossary-terms.csv", ["id", "term", "url"], glossary_terms(glo)),
        }
    for name, changed in results.items():
        print(f"{name}: {'updated' if changed else 'unchanged'}")


if __name__ == "__main__":
    sys.exit(main())
