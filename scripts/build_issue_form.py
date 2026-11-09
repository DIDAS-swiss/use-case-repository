#!/usr/bin/env python3
"""Fill the choice lists of the issue forms from _data/.

GitHub issue forms are static YAML, so the dropdowns that offer the anchor
vocabularies are written into the form from the lists the repository keeps:
sectors, trust flows, Industry Function Graph patterns, I14Y credential datasets
and DIDAS Glossary terms (kept current by the sync scripts), the credentials
described in credentials/, and the use cases (published entries and the
candidates of the intake batches, written to _data/use-case-index.csv here).
Only the `options:` block of those dropdowns is replaced; the rest of the form
is edited by hand as usual.

Run from the repository root:  python3 scripts/build_issue_form.py
Standard library only.
"""

import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FORMS = sorted((ROOT / ".github" / "ISSUE_TEMPLATE").glob("*.yml"))
DATA = ROOT / "_data"


def rows(name):
    with open(DATA / name, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def sector_options():
    sectors = rows("sectors.csv")
    children = {}
    for s in sectors:
        children.setdefault(s["broader"], []).append(s)
    out = []

    def walk(s, depth):
        out.append("— " * depth + f"{s['id']} · {s['label']}")
        for c in sorted(children.get(s["id"], []), key=lambda c: c["notation"]):
            walk(c, depth + 1)

    for s in children.get("", []):
        walk(s, 0)
    return out


def front_matter(path):
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8").split("---")[1]) or {}


def credential_options():
    out = []
    for path in sorted((ROOT / "credentials").glob("*.md")):
        if path.name.startswith(("_", "README")):
            continue
        out.append(f"{path.stem} · {front_matter(path).get('title') or path.stem}")
    return out


def use_case_index():
    """Published entries and batch candidates, id -> (title, kind); written to _data/."""
    index = {}
    for path in sorted((ROOT / "use-cases").glob("*.md")):
        if not path.name.startswith(("_", "README")):
            index[path.stem] = (front_matter(path).get("title") or path.stem, "entry")
    for path in sorted((ROOT / "intake").glob("*.csv")):
        with open(path, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                if r.get("id") and r["id"] not in index:
                    index[r["id"]] = (r.get("title") or r["id"], "candidate")
    rows = sorted(index.items())
    with open(DATA / "use-case-index.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "title", "kind"])
        w.writerows([(i, t, k) for i, (t, k) in rows])
    return [f"{i} · {t}" for i, (t, _) in rows]


def options():
    use_case_index()   # the ids the relation fields refer to, listed on the site
    return {
        "sectors": sector_options(),
        "trust_flows": [f"{r['id']} · {r['title']} ({r['status']})" for r in rows("trust-flows.csv")]
        + ["Not listed: linked under Other flow diagrams"],
        "ifm_patterns": [f"{r['id']} · {r['name']}" for r in rows("ifm-patterns.csv")]
        + ["No pattern fits yet"],
        "described_credentials": credential_options(),
        "glossary_terms": [f"{r['id']} · {r['term']}" for r in rows("glossary-terms.csv")],
        "i14y_credentials": [
            f"{r['identifier']} · {r['title']} ({r['publisher']}, {r['registration_status']})"
            for r in rows("i14y-credentials.csv")
        ],
    }


def fill(form, lists):
    original = form.read_text(encoding="utf-8")
    lines = original.split("\n")
    out, i, current = [], 0, None
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("id: "):
            current = stripped[4:]
        out.append(line)
        if stripped == "options:" and current in lists:
            indent = " " * (len(line) - len(line.lstrip()) + 2)
            i += 1
            # an option may wrap onto continuation lines, indented deeper than its "- "
            while i < len(lines) and (lines[i].startswith(indent + "- ")
                                      or (lines[i].startswith(indent + "  ") and lines[i].strip())):
                i += 1
            out += [f"{indent}- {json.dumps(o, ensure_ascii=False)}" for o in lists[current]]
            current = None
            continue
        i += 1
    text = "\n".join(out)
    if text != original:
        form.write_text(text, encoding="utf-8")
        print(f"{form.relative_to(ROOT)}: updated")


def main():
    lists = options()
    for form in FORMS:
        fill(form, lists)


if __name__ == "__main__":
    main()
