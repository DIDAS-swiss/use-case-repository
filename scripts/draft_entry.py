#!/usr/bin/env python3
"""Draft a use-case entry from a use-case issue, read from its form fields.

The entry file use-cases/<id>.md is built from the fields of the use-case form
(.github/ISSUE_TEMPLATE/use-case-candidate.yml) as the issue holds them: front
matter from the structured fields, body sections from the text fields. The
entry starts at stage `signal`; a curator advances it.

Front matter can only name things that exist in this repository (Check data
enforces it): credentials described in credentials/, and published use cases.
Credentials and use cases the issue names that are not described yet stay in
the body text, so nothing is lost. Each credential the entry relies on gets the
entry added to its `used_by`.

Run from the repository root:
  python3 scripts/draft_entry.py <issue number>          from GitHub (GITHUB_TOKEN)
  python3 scripts/draft_entry.py --body FILE --number N  from a saved issue body
Prints the id of the entry it wrote. Needs PyYAML.
"""

import datetime
import json
import os
import pathlib
import re
import sys
import urllib.request

import yaml

import issue_links as links

ROOT = links.ROOT


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60].strip("-")


def entry_ids():
    return {p.stem for p in (ROOT / "use-cases").glob("*.md") if not p.name.startswith(("_", "README"))}


def credentials_named(text, label):
    """Credential ids in the '- **Reused**: …' style line of the credentials field."""
    m = re.search(rf"^- \*\*{label}\*\*:(.*)$", text or "", re.M)
    if not m:
        return []
    found = re.findall(r"/credentials/([a-z0-9-]+)\.(?:md|html)|`([a-z0-9-]+)`", m.group(1))
    return [a or b for a, b in found]


def draft(body, number, labels=()):
    f = links.fields(body)
    title = f.get("title", "").strip()
    uid = (f.get("entry_id") or "").strip() or slug(title)
    entries = entry_ids()
    known_creds = set(links.CREDENTIALS)

    titles = dict(re.findall(r"\b(DE|FR|IT):\s*([^·\n]+)", f.get("titles", "")))
    sectors = re.findall(r"ISIC-[A-Z0-9]+", f.get("sectors", ""))
    als = [a for a in ("AL1", "AL2", "AL3") if f"[X] {a}" in f.get("ambition", "")]
    described = links.chosen("described_credentials", f.get("described_credentials"))
    reused = [c for c in credentials_named(f.get("credentials"), "Reused") if c in known_creds]
    new = [c for c in credentials_named(f.get("credentials"), "New") if c in known_creds]
    excluded = [c for c in credentials_named(f.get("credentials"), "Deliberately excluded") if c in known_creds]
    for c in described:
        if c not in reused + new + excluded:
            new.append(c)

    def relations(key):
        named = links.ids(f.get(key), links.USE_CASES)
        return [u for u in named if u in entries and u != uid], [u for u in named if u not in entries]

    related, related_c = relations("related_use_cases")
    upstream, upstream_c = relations("upstream_use_cases")
    downstream, downstream_c = relations("downstream_use_cases")
    # the decision is the curator's label; the form only carries a proposal
    lighthouse = links.form.lighthouse(f, labels)[1]
    status = links.form.evidence_status(f.get("evidence_status"))
    dependencies = [d for d, key in (("e-id", "state e-ID"), ("trust-infrastructure", "trust infrastructure (swiyu)"))
                    if key in (f.get("background") or "")][:1]
    group = next((l[4:] for l in labels if l.startswith("wg: ")), None)
    today = datetime.date.today()

    fm = {
        "id": uid, "title": title,
        "title_de": titles.get("DE", "").strip() or None, "title_fr": titles.get("FR", "").strip() or None,
        "title_it": titles.get("IT", "").strip() or None,
        "stage": "signal", "ambition_levels": als, "sectors": sectors,
        "domain_steward": "vacant", "proposed_by": f.get("organisation") or None, "intake_issue": number,
        "credentials_reused": reused, "credentials_new": new, "credentials_excluded": excluded,
        "related_use_cases": related, "upstream_use_cases": upstream, "downstream_use_cases": downstream,
        "lighthouse": lighthouse or None, "lighthouse_basis": f.get("lighthouse_basis") or None,
        "lighthouse_decision_record": None,
        "evidence_status": status or None, "dependencies": dependencies,
        "trust_flows": links.chosen("trust_flows", f.get("trust_flows")),
        "ifm_patterns": links.chosen("ifm_patterns", f.get("ifm_patterns")),
        "implementations": [l.strip("- ").strip() for l in (f.get("implementations") or "").split("\n") if "http" in l],
        "glossary_terms": links.chosen("glossary_terms", f.get("glossary_terms")),
        "created": today, "updated": today,
    }
    if group:
        fm["working_group"] = group

    def candidates(label, ids_):
        return f"- **{label}** (candidates, not yet published): " + ", ".join(f"`{x}`" for x in ids_) if ids_ else ""

    rel_text = "\n".join(x for x in (candidates("Upstream", upstream_c), candidates("Downstream", downstream_c),
                                     candidates("Related", related_c)) if x)
    process = f.get("process_flow") or ""
    if f.get("design_basis"):
        process += ("\n\n" if process else "") + "**Design basis**: " + f["design_basis"]
    creds = f.get("credentials") or ""
    if f.get("schemas"):
        creds += ("\n\n" if creds else "") + "**Emerging or other schemas**: " + f["schemas"]
    open_q = f.get("open_questions") or ""
    if rel_text:
        open_q += ("\n\n" if open_q else "") + "**Relations to candidates**\n\n" + rel_text
    # (heading, text, kept when empty): the core of a signal stays visible as "Not yet known.";
    # other empty sections are left out of the entry
    sections = [
        ("Summary", f.get("summary"), True), ("Facts to prove", f.get("outcome"), True),
        ("Actors and roles", f.get("actors"), True), ("Demand and value", f.get("demand"), True),
        ("Evidence status", f.get("evidence_status"), True), ("Background", f.get("background"), False),
        ("Process flow", process, False), ("Credentials", creds, True),
        ("Governance and trust context", f.get("governance"), False),
        ("Open questions", open_q, False), ("Sources", f.get("sources"), True),
    ]
    sections = [(h, v) for h, v, keep in sections if (v or "").strip() or keep]
    class Dumper(yaml.SafeDumper):
        def ignore_aliases(self, data):   # write repeated values (created, updated) out in full
            return True

    head = yaml.dump(fm, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=10000, default_flow_style=None)
    head = re.sub(r": null$", ":", head, flags=re.M)   # empty fields stay empty, as in the template
    text = (f"---\n{head}---\n\n# {title}\n\n"
            f"> **Draft from #{number}.** Written from the issue's form fields; the working group "
            f"refines it before a curator advances its stage.\n\n"
            + "\n\n".join(f"## {h}\n\n{(v or '').strip() or 'Not yet known.'}" for h, v in sections) + "\n")
    (ROOT / "use-cases" / f"{uid}.md").write_text(text, encoding="utf-8")

    def add_to_list(path, field, value):
        t = path.read_text(encoding="utf-8")
        m = re.search(rf"^{field}: \[(.*)\]$", t, re.M)
        if m and value not in [x.strip() for x in m.group(1).split(",")]:
            items = [x.strip() for x in m.group(1).split(",") if x.strip()] + [value]
            path.write_text(t[:m.start()] + f"{field}: [{', '.join(items)}]" + t[m.end():], encoding="utf-8")

    # the published entries it names get the other direction of the relation
    for other in upstream:
        add_to_list(ROOT / "use-cases" / f"{other}.md", "downstream_use_cases", uid)
    for other in downstream:
        add_to_list(ROOT / "use-cases" / f"{other}.md", "upstream_use_cases", uid)

    # each relied-on credential lists the entry in used_by
    for c in reused + new:
        add_to_list(ROOT / "credentials" / f"{c}.md", "used_by", uid)
    return uid


def main():
    if "--body" in sys.argv:
        body = pathlib.Path(sys.argv[sys.argv.index("--body") + 1]).read_text(encoding="utf-8")
        number = int(sys.argv[sys.argv.index("--number") + 1])
        labels = sys.argv[sys.argv.index("--labels") + 1].split(",") if "--labels" in sys.argv else []
    else:
        repo = os.environ.get("GITHUB_REPOSITORY", "DIDAS-swiss/use-case-repository")
        number = int(sys.argv[1])
        req = urllib.request.Request(f"https://api.github.com/repos/{repo}/issues/{number}", headers={
            "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}", "Accept": "application/vnd.github+json",
            "User-Agent": "didas-use-case-repository draft-entry"})
        issue = json.loads(urllib.request.urlopen(req, timeout=60).read())
        body, labels = issue.get("body"), [l["name"] for l in issue.get("labels") or []]
    print(draft(body, number, labels))


if __name__ == "__main__":
    main()
