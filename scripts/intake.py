#!/usr/bin/env python3
"""Open one use-case candidate issue per entry of the batch files in intake/.

The issue is written in the fields of the use-case form
(.github/ISSUE_TEMPLATE/use-case-candidate.yml), read from the form itself:
the same headings in the same order, as GitHub writes a filled-in form. What the
form has no field for (where the entry came from, the suggested working group,
the points to fix) goes into one comment.

A candidate whose title matches an existing use-case issue is not opened again.
Its issue is kept in step with the batch instead: title and description in the
form's fields, unless someone has edited the description by hand; the lighthouse
label; and the comment, updated rather than repeated. Its stage, status and
other labels are left alone.

Run from the repository root:
  python3 scripts/intake.py --dry-run     print what would be created
  GITHUB_TOKEN=… GITHUB_REPOSITORY=owner/repo python3 scripts/intake.py

Needs PyYAML.
"""

import csv
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import yaml

import issue_links
from working_groups import responsible

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


def existing_issues(repo):
    """Use-case issues by lower-case title."""
    issues, page = {}, 1
    while True:
        batch = api("GET", f"/repos/{repo}/issues?state=all&labels=use-case&per_page=100&page={page}")
        for i in batch:
            issues[i["title"].removeprefix("[Use case]").strip().lower()] = i   # earlier titles had a prefix
        if len(batch) < 100:
            return issues
        page += 1


def backlog_id(body):
    """The short id of an intake issue: its form field, or the first line of the first format."""
    body = body or ""
    m = re.search(r"^### Short id \(optional\)\n\n([a-z0-9-]+)\s*$", body, re.M)
    if m:
        return m.group(1)
    m = re.search(r"backlog (?:`[^`]*` · )?`([a-z0-9-]+)`", body.split("\n", 1)[0])
    return m.group(1) if m else None


def published_titles():
    """Title and id of each use case published in use-cases/ -> its path."""
    titles = {}
    for path in (ROOT / "use-cases").glob("*.md"):
        if path.name.startswith(("_", "README")):
            continue
        fm = yaml.safe_load(path.read_text(encoding="utf-8").split("---")[1]) or {}
        for key in (fm.get("title"), fm.get("id"), path.stem):
            if key:
                titles[str(key).strip().lower()] = str(path.relative_to(ROOT))
    return titles


def known(ids, table, what, title, warnings):
    out = []
    for i in ids or []:
        if i in table:
            out.append(i)
        else:
            warnings.append(f"{title}: unknown {what} {i!r}, left out")
    return out


LIST_FIELDS = ("sectors", "ambition_levels", "trust_flows", "ifm_patterns", "i14y_credentials",
               "credentials_reused", "credentials_new", "credentials_excluded", "related_use_cases",
               "upstream_use_cases", "downstream_use_cases", "glossary_terms")

LIGHTHOUSE_LABELS = ("lighthouse", "lighthouse-candidate")


def lighthouse_label(value):
    """The label for a lighthouse value: selected or candidate, else None."""
    v = str(value or "").strip().lower()
    if v in ("yes", "y", "ja", "x", "true", "1", "selected", "lighthouse"):
        return "lighthouse"
    if v in ("candidate", "kandidat"):
        return "lighthouse-candidate"
    return None


def review_points(notes):
    """Review notes written as (1) … (2) … as a list."""
    parts = [p.strip() for p in re.split(r"\(\d+\)\s*", notes or "") if p.strip()]
    return "\n".join(f"{n}. {p}" for n, p in enumerate(parts, 1))


def credential_entries():
    """Credential id -> (title, I14Y dataset or None), from credentials/."""
    out = {}
    for path in (ROOT / "credentials").glob("*.md"):
        if path.name.startswith(("_", "README")):
            continue
        fm = yaml.safe_load(path.read_text(encoding="utf-8").split("---")[1]) or {}
        out[path.stem] = (fm.get("title") or path.stem, fm.get("i14y_dataset"))
    return out


CREDENTIALS = credential_entries()
REPO_URL = "https://github.com/DIDAS-swiss/use-case-repository/blob/main"


FORM = yaml.safe_load((ROOT / ".github" / "ISSUE_TEMPLATE" / "use-case-candidate.yml").read_text(encoding="utf-8"))
FIELDS = [f for f in FORM["body"] if f.get("id")]
NO_RESPONSE = "_No response_"
BODY_MARKER = "<!-- intake-body sha="


def option(field_id, prefix):
    """The form's option text for a dropdown choice, found by its leading id."""
    field = next(f for f in FIELDS if f["id"] == field_id)
    for o in field["attributes"].get("options") or []:
        if o.lstrip("— ").startswith(f"{prefix} · ") or o.lstrip("— ") == prefix:
            return o
    return None


def body_sha(text):
    import hashlib
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def render(values):
    """The issue body exactly as GitHub writes a filled-in form: every field, in order."""
    parts = []
    for f in FIELDS:
        v = values.get(f["id"])
        if f["type"] == "checkboxes":
            chosen = set(v or [])
            v = "\n".join(f"- [{'X' if o['label'] in chosen else ' '}] {o['label']}" for o in f["attributes"]["options"])
        elif isinstance(v, list):
            v = ", ".join(v)
        parts.append(f"### {f['attributes']['label']}\n\n{(v or '').strip() or NO_RESPONSE}")
    text = "\n\n".join(parts)
    return f"{text}\n\n{BODY_MARKER}{body_sha(text)} -->"


def issue(c, batch, warnings, published_path=None, numbers=None):
    """The issue for a batch entry, written in the fields of the use-case form."""
    numbers = numbers or {}
    title = str(c["title"]).strip()
    sectors = known(c.get("sectors"), SECTORS, "sector", title, warnings)
    flows = known(c.get("trust_flows"), FLOWS, "trust flow", title, warnings)
    patterns = known(c.get("ifm_patterns"), PATTERNS, "pattern", title, warnings)
    als = [a for a in c.get("ambition_levels") or [] if a in ("AL1", "AL2", "AL3")]
    group = c.get("working_group")
    if group and group not in GROUPS:
        warnings.append(f"{title}: unknown working group {group!r}, kept as label")

    def text(key):
        v = c.get(key)
        return str(v).strip() if v and str(v).strip() else ""

    def listed_text(key, numbered=False):
        """A ' | '-separated field as one item per line."""
        v = text(key)
        if " | " not in v:
            return v
        items = [x.strip() for x in v.split(" | ") if x.strip()]
        return "\n".join(x if numbered and re.match(r"^\d+[.)] ", x) else f"- {x}" for x in items)

    def points(v):
        items = [x.strip() for x in v.split("; ") if x.strip()]
        return "\n".join(f"- {x}" for x in items) if len(items) > 1 else v

    def both(en, de, fmt=lambda v: v):
        out = fmt(text(en))
        if text(de):
            out += ("\n\n" if out else "") + "**DE:**\n\n" + fmt(text(de))
        return out

    def bullets(pairs):
        return "\n".join(f"- **{label}**: {text(key)}" for label, key in pairs if text(key))

    def cred(cid):
        if cid in CREDENTIALS:
            return f"[{CREDENTIALS[cid][0]}]({REPO_URL}/credentials/{cid}.md)"
        return f"`{cid}`"

    def relations(key):
        return "\n".join(f"- `{x}`" + (f" (#{numbers[x]})" if x in numbers else "") for x in c.get(key) or [])

    creds = [text("credentials")]
    for label, key in (("Reused", "credentials_reused"), ("New", "credentials_new"), ("Deliberately excluded", "credentials_excluded")):
        if c.get(key):
            creds.append(f"- **{label}**: " + ", ".join(cred(x) for x in c[key]))
    on_i14y = list(c.get("i14y_credentials") or [])
    for key in ("credentials_reused", "credentials_new"):
        for x in c.get(key) or []:
            if x in CREDENTIALS and CREDENTIALS[x][1] and CREDENTIALS[x][1] not in on_i14y:
                on_i14y.append(CREDENTIALS[x][1])
    lh = lighthouse_label(c.get("lighthouse"))

    values = {
        "title": title,
        "entry_id": text("id") or text("entry_id"),
        "titles": text("titles") or " · ".join(f"{lang}: {text(k)}" for lang, k in (("DE", "title_de"), ("FR", "title_fr"), ("IT", "title_it")) if text(k)),
        "summary": both("summary", "summary_de"),
        "outcome": both("outcome", "outcome_de", points),
        "actors": listed_text("actors"),
        "process_flow": listed_text("process_flow", numbered=True),
        "design_basis": text("design_basis"),
        "credentials": "\n\n".join(x for x in (creds[0], "\n".join(creds[1:])) if x),
        "described_credentials": [o for x in (c.get("credentials_reused") or []) + (c.get("credentials_new") or [])
                                  if x in CREDENTIALS and (o := option("described_credentials", x))],
        "glossary_terms": [o for x in c.get("glossary_terms") or [] if (o := option("glossary_terms", x))],
        "i14y_credentials": [o for d in on_i14y if (o := option("i14y_credentials", d))],
        "schemas": text("schemas"),
        "ambition": als,
        "sectors": [o for s in sectors if (o := option("sectors", s))],
        "trust_flows": [o for f in flows if (o := option("trust_flows", f))],
        "ifm_patterns": [o for p in patterns if (o := option("ifm_patterns", p))],
        "other_flows": text("other_flows"),
        "implementations": text("implementations"),
        "related_use_cases": relations("related_use_cases"),
        "upstream_use_cases": relations("upstream_use_cases"),
        "downstream_use_cases": relations("downstream_use_cases"),
        "lighthouse": {"lighthouse": "Selected as lighthouse (DIDAS decision)",
                       "lighthouse-candidate": "Propose as lighthouse candidate"}.get(lh, ""),
        "lighthouse_basis": text("lighthouse_basis"),
        "governance": text("governance") or bullets((("Legal basis", "legal_basis"), ("Trust frameworks and registries", "trust_frameworks"),
                                                      ("Verifier governance", "verifier_governance"), ("Sensitive attributes", "sensitive_attributes"))),
        "demand": text("demand") or bullets((("Relying parties", "relying_parties"), ("Indicative scale", "indicative_scale"), ("Value", "value"))),
        "open_questions": both("coordination_and_open_questions", "coordination_and_open_questions_de") or text("open_questions"),
        "organisation": text("proposed_by") or str(batch.get("proposed_by") or ""),
        "sources": text("sources"),
    }
    labels = ["use-case", "stage: signal", "intake-batch"] + als
    labels += sorted({f"ISIC {section(s)}" for s in sectors if section(s)})
    if group:
        labels.append(f"wg: {group}")
    if lh:
        labels.append(lh)
    if published_path:
        labels.append("change")
    return {"title": title, "body": render(values), "labels": labels}


def load_batch(path):
    """A batch file as {batch, proposed_by, candidates}: YAML, or CSV with one candidate per row."""
    if path.suffix.lower() == ".csv":
        with open(path, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        candidates = []
        for r in rows:
            c = {k: (v or "").strip() for k, v in r.items() if k}
            for k in LIST_FIELDS:
                c[k] = [x.strip() for x in re.split(r"[;,]", c.get(k, "")) if x.strip()]
            if c.get("title"):
                candidates.append(c)
        return {"batch": path.stem, "candidates": candidates}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def create(repo, new):
    """Open the issue, pacing for GitHub's limit on creating content."""
    for attempt in range(6):
        try:
            made = api("POST", f"/repos/{repo}/issues", new)
            time.sleep(3)
            return made
        except urllib.error.HTTPError as e:
            if e.code not in (403, 429) or attempt == 5:
                raise
            wait = int(e.headers.get("Retry-After") or 60 * (attempt + 1))
            print(f"rate limited, waiting {wait}s")
            time.sleep(wait)


MARKER = "<!-- intake-relations -->"


def intake_comment(c, batch, published_path):
    """The comment with what the form has no field for: where the entry came from,
    the working group it suggests and the points to fix. None if there is nothing."""
    lines = []
    ref = f"Filed with the intake batch **{batch.get('batch', 'unnamed')}**"
    if c.get("no") or c.get("id"):
        ref += " · backlog " + " · ".join(f"`{c[k]}`" for k in ("no", "id") if c.get(k))
    lines.append(ref + ".")
    if published_path:
        lines.append(f"**Update of a published entry.** This use case is already published as "
                     f"[`{published_path}`]({REPO_URL}/{published_path}). Compare it with this issue and "
                     f"bring what is new into the entry in a pull request.")
    sectors = [s for s in c.get("sectors") or [] if s in SECTORS]
    suggested = None if c.get("working_group") else (responsible(sectors[0])[0] if sectors else None)
    if suggested:
        lines.append(f"**Suggested working group**: {suggested['name']}, from the primary sector. "
                     f"The group takes the candidate by adding `wg: {suggested['id']}`.")
    notes = review_points(c.get("review_notes"))
    if notes:
        lines.append("**To fix in the description**\n\n" + notes)
    lines.append("_Kept in step with the batch file by the intake. The stage and status of this use case are unchanged._")
    return MARKER + "\n" + "\n\n".join(lines)


def owned_body(body):
    """True when the body is the intake's own and nobody has edited it since."""
    body = body or ""
    if body.startswith("_Filed with the intake batch"):   # the first intake format
        return True
    m = re.search(r"\n\n" + re.escape(BODY_MARKER) + r"([0-9a-f]+) -->\s*$", body)
    return bool(m) and body_sha(body[:m.start()]) == m.group(1)


def annotate(repo, existing, new, c, batch, published_path, dry):
    """Bring an existing issue in step with its batch entry: title and body in the
    form's fields (unless edited by hand), lighthouse label, and one comment."""
    number, done = existing["number"], []
    patch = {}
    if existing["title"] != new["title"]:
        patch["title"] = new["title"]
    if existing.get("body") != new["body"]:
        if owned_body(existing.get("body")):
            patch["body"] = new["body"]
        else:
            done.append("description edited by hand, left as is")
    if patch:
        done.append(" and ".join(k for k in ("title", "body") if k in patch) + " rewritten")
        if not dry:
            api("PATCH", f"/repos/{repo}/issues/{number}", patch)
    have = {l["name"] for l in existing.get("labels") or []}
    want = lighthouse_label(c.get("lighthouse"))
    if want:
        if want not in have:
            done.append(f"+{want}")
            if not dry:
                api("POST", f"/repos/{repo}/issues/{number}/labels", {"labels": [want]})
        for other in LIGHTHOUSE_LABELS:
            if other != want and other in have:
                done.append(f"-{other}")
                if not dry:
                    api("DELETE", f"/repos/{repo}/issues/{number}/labels/{urllib.parse.quote(other)}")
    text = intake_comment(c, batch, published_path)
    if dry:
        done.append("comment")
    else:
        comments = api("GET", f"/repos/{repo}/issues/{number}/comments?per_page=100")
        mine = next((x for x in comments if MARKER in (x.get("body") or "")), None)
        if mine and mine["body"] != text:
            api("PATCH", f"/repos/{repo}/issues/comments/{mine['id']}", {"body": text})
            done.append("comment updated")
        elif not mine:
            api("POST", f"/repos/{repo}/issues/{number}/comments", {"body": text})
            done.append("comment")
    if not dry and done:
        time.sleep(2)
    return done


def main():
    dry = "--dry-run" in sys.argv
    out_dir = None
    if "--write" in sys.argv:
        out_dir = pathlib.Path(sys.argv[sys.argv.index("--write") + 1])
        out_dir.mkdir(parents=True, exist_ok=True)
    repo = os.environ.get("GITHUB_REPOSITORY", "DIDAS-swiss/use-case-repository")
    published = published_titles()
    existing = {} if dry else existing_issues(repo)
    # backlog id -> issue number, so relations can link the issues
    numbers = {i: e["number"] for e in existing.values() if (i := backlog_id(e.get("body")))}
    created = annotated = updates = 0
    files = sorted(p for p in (ROOT / "intake").iterdir() if p.suffix.lower() in (".yml", ".yaml", ".csv"))
    for path in files:
        if path.name.startswith("_"):
            continue
        batch = load_batch(path)
        candidates = batch.get("candidates") or []
        # open the new ones first, so the comments on existing issues can link them
        for c in sorted(candidates, key=lambda c: str(c["title"]).strip().lower() in existing):
            warnings = []
            title = str(c["title"]).strip()
            key = title.lower()
            # an issue is found by its short id first, so a corrected title stays the same issue
            by_id = next((k for k, e in existing.items() if c.get("id") and backlog_id(e.get("body")) == c["id"]), None)
            if by_id:
                key = by_id
            entry = published.get(key) or published.get(str(c.get("id") or "").lower())
            entry = entry or published.get(title.lower())
            new = issue(c, batch, warnings, published_path=entry, numbers=numbers)
            for w in warnings:
                print(f"::warning file={path.relative_to(ROOT)}::{w}")
            if key in existing:
                done = annotate(repo, existing[key], new, c, batch, entry, dry)
                links = issue_links.comment(new["body"], numbers)
                if dry:
                    done.append("links" if links else "no links")
                else:
                    did = issue_links.upsert(api, repo, existing[key]["number"], links)
                    if did:
                        done.append(did)
                annotated += bool(done)
                print(f"{'would update' if dry else 'update'} #{existing[key]['number']} {new['title']}: {', '.join(done) or 'in step'}")
                continue
            if out_dir:
                (out_dir / f"{c.get('no') or created:>03}.md").write_text(f"# {new['title']}\n\nlabels: {new['labels']}\n\n{new['body']}", encoding="utf-8")
            if dry:
                print(f"would create {new['title']}{'  (update of ' + entry + ')' if entry else ''}  labels={new['labels']}  body={len(new['body'])} chars")
            else:
                made = create(repo, new)
                api("POST", f"/repos/{repo}/issues/{made['number']}/comments", {"body": intake_comment(c, batch, entry)})
                issue_links.upsert(api, repo, made["number"], issue_links.comment(new["body"], numbers))
                print(f"create #{made['number']} {new['title']}{'  (update of ' + entry + ')' if entry else ''}")
                existing[key] = made
                if c.get("id"):
                    numbers[c["id"]] = made["number"]
            created += 1
            updates += bool(entry)
    print(f"{created} {'to create' if dry else 'created'} ({updates} updates of published entries), "
          f"{annotated} existing {'to bring' if dry else 'brought'} in step")


if __name__ == "__main__":
    main()
