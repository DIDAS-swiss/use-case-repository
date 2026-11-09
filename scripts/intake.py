#!/usr/bin/env python3
"""Open one use-case candidate issue per entry of the batch files in intake/.

Each issue is written as the use-case candidate form would write it, so the
rest of the funnel (labels, project board, triage) treats it the same way.

A candidate whose title matches an existing use-case issue is not opened
again. Its issue is kept in step with the batch instead: the lighthouse label
the batch gives it, and one comment, kept up to date, with its upstream and
downstream use cases and the review notes. Nothing else on the issue changes:
not its stage, status, other labels or description.

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
            issues[i["title"].removeprefix("[Use case]").strip().lower()] = i
        if len(batch) < 100:
            return issues
        page += 1


def backlog_id(body):
    """The backlog id an intake issue was filed under, from its first line."""
    m = re.search(r"backlog (?:`[^`]*` · )?`([a-z0-9-]+)`", (body or "").split("\n", 1)[0])
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
               "upstream_use_cases", "downstream_use_cases")

LIGHTHOUSE_LABELS = ("lighthouse", "lighthouse-candidate")


def lighthouse_label(value):
    """The label for a lighthouse value: selected or candidate, else None."""
    v = str(value or "").strip().lower()
    if v in ("yes", "y", "ja", "x", "true", "1", "selected", "lighthouse"):
        return "lighthouse"
    if v in ("candidate", "kandidat"):
        return "lighthouse-candidate"
    return None


def relation_list(ids, numbers):
    return ", ".join(f"`{x}`" + (f" (#{numbers[x]})" if x in numbers else "") for x in ids)


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


def issue(c, batch, warnings, published_path=None, numbers=None):
    numbers = numbers or {}
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
        return str(v).strip() if v and str(v).strip() else default

    def listed_text(key, numbered=False):
        """A ' | '-separated field as a list, one item per line."""
        v = text(key, "")
        if " | " not in v:
            return v or "_No response_"
        items = [x.strip() for x in v.split(" | ") if x.strip()]
        return "\n".join(x if numbered and re.match(r"^\d+[.)] ", x) else f"- {x}" for x in items)

    def points(v):
        """A '; '-separated list of facts as bullet points."""
        items = [x.strip() for x in v.split("; ") if x.strip()]
        return "\n".join(f"- {x}" for x in items) if len(items) > 1 else v

    def both(en, de):
        """The English text, with the German version beneath it where there is one."""
        out = text(en, "")
        if c.get(de) and str(c[de]).strip():
            out += ("\n\n" if out else "") + f"**DE:** {str(c[de]).strip()}"
        return out

    def bullets(pairs):
        lines = [f"- **{label}**: {str(c[key]).strip()}" for label, key in pairs if c.get(key) and str(c[key]).strip()]
        return "\n".join(lines) or "_No response_"

    def cred(cid):
        if cid in CREDENTIALS:
            return f"[{CREDENTIALS[cid][0]}]({REPO_URL}/credentials/{cid}.md)"
        return f"`{cid}`"

    head = title
    titles = [f"{lang}: {c[k]}" for lang, k in (("DE", "title_de"), ("FR", "title_fr"), ("IT", "title_it")) if c.get(k)]
    if titles:
        head += "\n\n" + " · ".join(titles)

    situation = both("summary", "summary_de")
    outcome = points(text("outcome", ""))
    if c.get("outcome_de"):
        outcome += ("\n\n" if outcome else "") + "**DE:**\n\n" + points(str(c["outcome_de"]).strip())
    if outcome:
        situation = (situation + "\n\n" if situation else "") + "**Outcome: what must be proven**\n\n" + outcome
    creds = text("credentials", "")
    listed = []
    for label, key in (("Reused", "credentials_reused"), ("New", "credentials_new"), ("Deliberately excluded", "credentials_excluded")):
        if c.get(key):
            listed.append(f"- **{label}**: " + ", ".join(cred(x) for x in c[key]))
    creds = "\n\n".join(x for x in (creds, "\n".join(listed)) if x) or "_No response_"
    on_i14y = list(c.get("i14y_credentials") or [])
    for key in ("credentials_reused", "credentials_new"):
        for x in c.get(key) or []:
            if x in CREDENTIALS and CREDENTIALS[x][1] and CREDENTIALS[x][1] not in on_i14y:
                on_i14y.append(CREDENTIALS[x][1])

    sections = [
        ("Use case", head),
        ("Situation and outcome", situation or "_To be detailed by the working group that takes this candidate._"),
        ("Actors", listed_text("actors")),
        ("Process flow", listed_text("process_flow", numbered=True)),
        ("Design basis", text("design_basis")),
        ("Credentials needed", creds),
        ("Credentials already on I14Y (optional)", ", ".join(f"`{d}`" for d in on_i14y) or "_No response_"),
        ("Emerging or other schemas (optional)", text("schemas")),
        ("Ambition level(s)", "\n".join(f"- [{'X' if a in als else ' '}] {a}" for a in ("AL1", "AL2", "AL3"))),
        ("Sector(s)", ", ".join(f"{s} · {SECTORS[s]['label']}" for s in sectors) or "_No response_"),
        ("Related use cases", ", ".join(f"`{x}`" for x in c.get("related_use_cases") or []) or "_No response_"),
        ("Upstream use cases", relation_list(c.get("upstream_use_cases") or [], numbers) or "_No response_"),
        ("Downstream use cases", relation_list(c.get("downstream_use_cases") or [], numbers) or "_No response_"),
        ("Trust flows (optional)", ", ".join(f"{f} · {FLOWS[f]['title']}" for f in flows) or "_No response_"),
        ("Use case pattern in the Industry Function Graph (optional)", ", ".join(f"{p} · {PATTERNS[p]['name']}" for p in patterns) or "_No response_"),
        ("Other flow diagrams (optional)", text("other_flows")),
        ("Implementations, pilots and showcases (optional)", text("implementations")),
        ("Legal basis and governance (optional)", c.get("governance") and text("governance") or bullets(
            (("Legal basis", "legal_basis"), ("Trust frameworks and registries", "trust_frameworks"),
             ("Verifier governance", "verifier_governance"), ("Sensitive attributes", "sensitive_attributes"))))
        ,
        ("Demand and value (optional)", c.get("demand") and text("demand") or bullets(
            (("Relying parties", "relying_parties"), ("Indicative scale", "indicative_scale"), ("Value", "value")))),
        ("Coordination needs and open questions", both("coordination_and_open_questions", "coordination_and_open_questions_de") or "_No response_"),
        ("Proposed on behalf of (optional)", text("proposed_by", batch.get("proposed_by") or "_No response_")),
        ("Sources (optional)", text("sources")),
    ]
    lh = lighthouse_label(c.get("lighthouse"))
    if lh:
        level = "Lighthouse (selected)" if lh == "lighthouse" else "Lighthouse candidate"
        basis = text("lighthouse_basis", "")
        sections.append(("Lighthouse", level + (f": {basis}" if basis else "")))
    if c.get("review_notes"):
        sections.append(("Review notes", review_points(c["review_notes"])))
    suggested = None if group else (responsible(sectors[0])[0] if sectors else None)
    if suggested:
        sections.append(("Suggested working group",
                         f"{suggested['name']} (from the primary sector; the group takes the candidate by adding `wg: {suggested['id']}`)"))
    ref = f"_Filed with the intake batch **{batch.get('batch', 'unnamed')}**"
    if c.get("no") or c.get("id"):
        ref += " · backlog " + " · ".join(f"`{c[k]}`" for k in ("no", "id") if c.get(k))
    body = ref + "._\n\n"
    if published_path:
        body += (f"> **Update of a published entry.** This use case is already published as "
                 f"[`{published_path}`]({REPO_URL}/{published_path}). Compare this backlog version with "
                 f"the entry and bring what is new into it in a pull request.\n\n")
    body += "\n\n".join(f"### {h}\n\n{v}" for h, v in sections)
    labels = ["use-case", "stage: signal", "intake-batch"] + als
    labels += sorted({f"ISIC {section(s)}" for s in sectors if section(s)})
    if group:
        labels.append(f"wg: {group}")
    if lh:
        labels.append(lh)
    if published_path:
        labels.append("change")
    return {"title": f"[Use case] {title}", "body": body, "labels": labels}


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


def relations_comment(c, numbers, batch):
    """The comment that carries a candidate's relations and review notes, or None."""
    lines = []
    if c.get("upstream_use_cases"):
        lines.append("- **Upstream** (must happen first: issues a credential this use case verifies): "
                     + relation_list(c["upstream_use_cases"], numbers))
    if c.get("downstream_use_cases"):
        lines.append("- **Downstream** (reuses a credential this use case issues): "
                     + relation_list(c["downstream_use_cases"], numbers))
    lh = lighthouse_label(c.get("lighthouse"))
    if lh:
        level = "selected" if lh == "lighthouse" else "candidate"
        basis = str(c.get("lighthouse_basis") or "").strip()
        lines.append(f"- **Lighthouse**: {level}" + (f" ({basis})" if basis else ""))
    notes = review_points(c.get("review_notes"))
    if not lines and not notes:
        return None
    body = [MARKER, f"**Relations and review notes** from the intake batch **{batch.get('batch', 'unnamed')}**", ""]
    body += lines
    if notes:
        body += ["", "**To fix in the description**", "", notes]
    body += ["", "_Kept in step with the batch file by the intake. The stage and status of this use case are unchanged._"]
    return "\n".join(body)


def annotate(repo, existing, c, batch, numbers, dry):
    """Bring an existing issue in step with its batch entry: lighthouse label and relations comment."""
    number, done = existing["number"], []
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
    text = relations_comment(c, numbers, batch)
    if text:
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
            entry = published.get(key) or published.get(str(c.get("id") or "").lower())
            new = issue(c, batch, warnings, published_path=entry, numbers=numbers)
            for w in warnings:
                print(f"::warning file={path.relative_to(ROOT)}::{w}")
            if key in existing:
                done = annotate(repo, existing[key], c, batch, numbers, dry)
                annotated += bool(done)
                print(f"{'would update' if dry else 'update'} #{existing[key]['number']} {new['title']}: {', '.join(done) or 'in step'}")
                continue
            if out_dir:
                (out_dir / f"{c.get('no') or created:>03}.md").write_text(f"# {new['title']}\n\nlabels: {new['labels']}\n\n{new['body']}", encoding="utf-8")
            if dry:
                print(f"would create {new['title']}{'  (update of ' + entry + ')' if entry else ''}  labels={new['labels']}  body={len(new['body'])} chars")
            else:
                made = create(repo, new)
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
