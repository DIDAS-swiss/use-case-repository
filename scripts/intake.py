#!/usr/bin/env python3
"""Open one use-case candidate issue per entry of the batch files in intake/.

The issue is written in the fields of the use-case form
(.github/ISSUE_TEMPLATE/use-case-candidate.yml), read from the form itself:
the same headings in the same order, as GitHub writes a filled-in form. What the
form has no field for (where the entry came from, the suggested working group,
the points to fix) goes into one comment.

A candidate whose short id (or title) matches an existing use-case issue is not
opened again. Its issue is kept in step with the batch instead: title and
description in the form's fields, unless someone has edited the description by
hand; the lighthouse label; and the comment, updated rather than repeated. Its
stage, status and other labels are left alone.

Editorial reviews of the backlog (intake/reviews/*-review.csv) add a section to
the comment: the recommendation, the finding and any proposed split or merge.
A recommendation changes nothing else; no issue is closed or opened for it.

Run from the repository root:
  python3 scripts/intake.py --dry-run [--write DIR]
      offline: what the batches render to; it does not look at existing issues
  python3 scripts/intake.py --reconcile [--issues FILE] [--comments DIR] [--write DIR]
      read only: what a live run would do to each existing issue, compared by
      short id. Reads the issues from GitHub (GET only; GITHUB_TOKEN optional) or
      from FILE, a saved JSON list of issues; writes the plan, and the current and
      new body of every issue that would change, to DIR
  GITHUB_TOKEN=… GITHUB_REPOSITORY=owner/repo python3 scripts/intake.py
      live: opens and updates issues

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
import use_case_form as form
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


READ_ONLY = False


class ReadOnlyError(RuntimeError):
    pass


def api(method, path, body=None):
    if READ_ONLY and method != "GET":
        raise ReadOnlyError(f"read-only run refused {method} {path}")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "didas-use-case-repository intake"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    req = urllib.request.Request(f"{API}{path}", method=method, headers=headers,
                                 data=json.dumps(body).encode() if body is not None else None)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read() or b"null")


def title_key(title):
    return (title or "").removeprefix("[Use case]").strip().lower()   # earlier titles had a prefix


def by_title(issues):
    """Use-case issues (a list) by lower-case title."""
    return {title_key(i["title"]): i for i in issues if not i.get("pull_request")}


def existing_issues(repo):
    """Use-case issues by lower-case title."""
    issues, page = [], 1
    while True:
        batch = api("GET", f"/repos/{repo}/issues?state=all&labels=use-case&per_page=100&page={page}")
        issues += batch
        if len(batch) < 100:
            return by_title(issues)
        page += 1


backlog_id = form.short_id   # the short id of an issue body


def match(c, existing):
    """The key in `existing` of the issue for a batch entry: by short id first, so a
    corrected title stays the same issue, then by title; None for a new candidate."""
    if c.get("id"):
        key = next((k for k, e in existing.items() if backlog_id(e.get("body")) == c["id"]), None)
        if key:
            return key
    key = title_key(str(c["title"]))
    return key if key in existing else None


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


FIELDS = form.FIELDS
NO_RESPONSE = form.NO_RESPONSE
BODY_MARKER = form.BODY_MARKER
option, body_sha, render, owned_body = form.option, form.body_sha, form.render, form.owned_body
SITE = "https://didas-swiss.github.io/use-case-repository"

# Reader-facing placeholders that say nothing; the batch keeps them, the issue leaves them out.
PLACEHOLDER = re.compile(r"^(no official figure|not known|unknown|n/a|none)\b", re.I)

DEPENDENCIES = {
    "e-id": "the state e-ID and the federal trust infrastructure",
    "trust-infrastructure": "the federal trust infrastructure (swiyu)",
}


def sources_text(value):
    """Batch sources ("label | date | URL | quote" entries separated by " || ") as a list."""
    entries = [e.strip() for e in (value or "").split(" || ") if e.strip()]
    if len(entries) < 2 and " | " not in (value or ""):
        return (value or "").strip()
    out = []
    for e in entries:
        parts = [x.strip() for x in e.split(" | ")]
        url = next((x for x in parts if x.startswith("http")), "")
        rest = [x for x in parts if x and x != url]
        label, date, quote = (rest + ["", "", ""])[:3] if rest else ("", "", "")
        if len(rest) > 3:
            quote = " | ".join(rest[2:])
        head = f"[{label}]({url})" if url and label else url or label
        out.append("- " + head + (f", {date}" if date else "") + (f": {quote}" if quote else ""))
    return "\n".join(out)


def dependency_line(value):
    """The shared dependencies of a batch entry, as one line linking the dependencies page."""
    names = [DEPENDENCIES[d] for d in re.split(r"[;,]\s*", value or "") if d in DEPENDENCIES]
    if not names:
        return ""
    return (f"**Shared dependency**: {' and '.join(names)}. Their current timing is kept once, with its "
            f"source and check date, on the [dependencies page]({SITE}/dependencies.html#e-id-and-trust-infrastructure).")


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
        return "\n".join(f"- **{label}**: {text(key)}" for label, key in pairs
                         if text(key) and not PLACEHOLDER.match(text(key)))

    def questions(lead, rest):
        """The open question first, then the coordination points, one per line."""
        items = ([text(lead)] if text(lead) else []) + [x.strip() for x in text(rest).split("; ") if x.strip()]
        return "\n".join(f"- {x}" for x in items) if len(items) > 1 else (items[0] if items else "")

    def cred(cid):
        if cid in CREDENTIALS:
            return f"[{CREDENTIALS[cid][0]}]({REPO_URL}/credentials/{cid}.md)"
        return f"`{cid}`"

    def relations(key):
        return "\n".join(f"- `{x}`" + (f" (#{numbers[x]})" if x in numbers else "") for x in c.get(key) or [])

    creds = [listed_text("credentials")]
    for label, key in (("Reused", "credentials_reused"), ("New", "credentials_new"), ("Deliberately excluded", "credentials_excluded")):
        if c.get(key):
            creds.append(f"- **{label}**: " + ", ".join(cred(x) for x in c[key]))
    on_i14y = list(c.get("i14y_credentials") or [])
    for key in ("credentials_reused", "credentials_new"):
        for x in c.get(key) or []:
            if x in CREDENTIALS and CREDENTIALS[x][1] and CREDENTIALS[x][1] not in on_i14y:
                on_i14y.append(CREDENTIALS[x][1])
    lh = lighthouse_label(c.get("lighthouse"))
    status = form.evidence_status(text("evidence_status"))
    flow = listed_text("process_flow", numbered=True)
    if flow and status in ("hypothesis", "documented need"):
        flow = "_Proposed flow: no actor has confirmed it yet._\n\n" + flow
    background = "\n\n".join(x for x in (both("background", "background_de"), dependency_line(text("dependencies"))) if x)
    basis = text("benefit_basis").lower() or "hypothesis"
    benefit = (f"- **Expected benefit ({basis})**: {text('expected_benefit')}" if text("expected_benefit") else "")
    open_de = questions("open_question_de", "coordination_and_open_questions_de")

    values = {
        "title": title,
        "entry_id": text("id") or text("entry_id"),
        "titles": text("titles") or " · ".join(f"{lang}: {text(k)}" for lang, k in (("DE", "title_de"), ("FR", "title_fr"), ("IT", "title_it")) if text(k)),
        "summary": both("summary", "summary_de"),
        "outcome": both("outcome", "outcome_de", points),
        "actors": listed_text("actors"),
        "evidence_status": option("evidence_status", status) if status else "",
        "background": background,
        "process_flow": flow,
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
        # the form records a proposal; a selection is the curator's label (see intake_comment)
        "lighthouse": "Propose as lighthouse candidate" if lh else "",
        "lighthouse_basis": text("lighthouse_basis"),
        "governance": text("governance") or bullets((("Legal basis", "legal_basis"), ("Trust frameworks and registries", "trust_frameworks"),
                                                      ("Verifier governance", "verifier_governance"), ("Sensitive attributes", "sensitive_attributes"))),
        "demand": text("demand") or "\n".join(x for x in (benefit, bullets((("Relying parties", "relying_parties"),
                                                                                 ("Indicative scale", "indicative_scale"),
                                                                                 ("Value", "value")))) if x),
        "open_questions": text("open_questions") or "\n\n".join(
            x for x in (questions("open_question", "coordination_and_open_questions"),
                        ("**DE:**\n\n" + open_de) if open_de else "") if x),
        "organisation": text("proposed_by") or str(batch.get("proposed_by") or ""),
        "sources": sources_text(text("sources")),
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
REVIEWS_DIR = ROOT / "intake" / "reviews"


def load_reviews():
    """Editorial reviews of the backlog: {short id: review row} (a later file wins) and
    {short id: [proposed scope rows]}. Files in intake/reviews/ named *-review.csv and
    *-scopes.csv; they are not batches, so no issue is opened from them."""
    reviews, scopes = {}, {}
    if REVIEWS_DIR.is_dir():
        for path in sorted(REVIEWS_DIR.glob("*-review.csv")):
            with open(path, encoding="utf-8-sig", newline="") as f:
                for r in csv.DictReader(f):
                    if r.get("id"):
                        reviews[r["id"]] = dict(r, file=str(path.relative_to(ROOT)))
        for path in sorted(REVIEWS_DIR.glob("*-scopes.csv")):
            with open(path, encoding="utf-8-sig", newline="") as f:
                for r in csv.DictReader(f):
                    if r.get("parent_id"):
                        scopes.setdefault(r["parent_id"], []).append(dict(r, file=str(path.relative_to(ROOT))))
    return reviews, scopes


REVIEWS, SCOPES = load_reviews()


def review_section(c, numbers):
    """The comment's part on the latest editorial review, or '' if there is none."""
    r = REVIEWS.get(c.get("id"))
    if not r:
        return ""
    ref = lambda uid: f"#{numbers[uid]} `{uid}`" if uid in numbers else f"`{uid}`"
    out = [f"**Editorial review, {r.get('review_date') or 'undated'}** (a recommendation, not a decision): "
           f"**{r.get('disposition') or 'no recommendation'}**.", (r.get("finding") or "").strip()]
    scopes = SCOPES.get(c.get("id")) or []
    if scopes:
        out.append("Proposed separate scopes, not opened as issues:\n\n" + "\n".join(
            f"- **{s['title']}** (`{s['scope_id']}`): {s['summary']}" for s in scopes))
    merge = [x.strip() for x in re.split(r"[;,]", r.get("merge_into") or "") if x.strip()]
    if merge:
        out.append("Proposed consolidation with " + ", ".join(ref(m) for m in merge) +
                   "; useful variants and the evidence of this issue are kept.")
    if r.get("verification_status"):
        out.append(f"Evidence checked by the review: {r['verification_status']}.")
    out.append(f"_This issue stays open; its stage, working group and lighthouse status are unchanged. "
               f"Full record: [`{r['file']}`]({REPO_URL}/{r['file']})._")
    return "\n\n".join(x for x in out if x)


def lighthouse_lines(c):
    """The lighthouse status as the batch records it: a selection is a curator decision,
    which the form cannot express (it only takes proposals)."""
    lh = lighthouse_label(c.get("lighthouse"))
    record = (c.get("lighthouse_decision_record") or "").strip()
    if lh == "lighthouse":
        return [f"**Lighthouse: selected.** A DIDAS decision, recorded in the batch and by the `lighthouse` label. "
                + (f"Decision record: {record}." if record else
                   "Decision record: not linked yet; a curator adds the approver, the date and the criteria "
                   f"assessed ([GOVERNANCE.md]({REPO_URL}/GOVERNANCE.md#lighthouses)).")]
    if lh == "lighthouse-candidate":
        return ["**Lighthouse candidate**, recorded in the batch. Selection is a separate curator decision."]
    return []


def intake_comment(c, batch, published_path, numbers=None):
    """The comment with what the form has no field for: where the entry came from,
    the working group it suggests, the lighthouse decision, the latest editorial
    review and the points to fix."""
    numbers = numbers or {}
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
    lines += lighthouse_lines(c)
    review = review_section(c, numbers)
    if review:
        lines.append(review)
    notes = review_points(c.get("review_notes"))
    if notes:
        lines.append("**To fix in the description**\n\n" + notes)
    lines.append("_Kept in step with the batch file by the intake. The stage and status of this use case are unchanged._")
    return MARKER + "\n" + "\n\n".join(lines)


def find_comment(comments, marker):
    return next((x for x in comments or [] if marker in (x.get("body") or "")), None)


def plan(existing, new, c, comment_text, links_text, comments=None):
    """What bringing an existing issue in step would do, without doing it.
    comments: the issue's comments, or None when they were not read."""
    p = {"number": existing["number"], "id": c.get("id"), "title": None, "body": "in step",
         "labels_add": [], "labels_remove": [], "comment": "unchecked", "links": "unchecked"}
    if existing["title"] != new["title"]:
        p["title"] = [existing["title"], new["title"]]
    if existing.get("body") != new["body"]:
        p["body"] = "rewrite" if owned_body(existing.get("body")) else "edited by hand"
    have = {l["name"] if isinstance(l, dict) else l for l in existing.get("labels") or []}
    want = lighthouse_label(c.get("lighthouse"))
    if want:
        if want not in have:
            p["labels_add"].append(want)
        p["labels_remove"] = [o for o in LIGHTHOUSE_LABELS if o != want and o in have]
    if comments is not None:
        mine = find_comment(comments, MARKER)
        p["comment"] = "create" if not mine else "update" if mine["body"] != comment_text else "in step"
        links = find_comment(comments, issue_links.MARKER)
        p["links"] = ("create" if links_text and not links else "remove" if links and not links_text else
                      "update" if links and links["body"] != links_text else "in step")
    return p


def describe(p):
    done = []
    if p["body"] == "edited by hand":
        done.append("description edited by hand, left as is")
    changed = [k for k in ("title", "body") if (p["title"] if k == "title" else p["body"] == "rewrite")]
    if changed:
        done.append(" and ".join(changed) + " rewritten")
    done += [f"+{x}" for x in p["labels_add"]] + [f"-{x}" for x in p["labels_remove"]]
    if p["comment"] in ("create", "update"):
        done.append("comment" if p["comment"] == "create" else "comment updated")
    if p["links"] in ("create", "update", "remove"):
        done.append({"create": "links", "update": "links updated", "remove": "links removed"}[p["links"]])
    return done


def annotate(repo, existing, new, c, batch, published_path, dry, numbers=None):
    """Bring an existing issue in step with its batch entry: title and body in the
    form's fields (unless edited by hand), lighthouse label, and one comment."""
    number = existing["number"]
    text = intake_comment(c, batch, published_path, numbers)
    links_text = issue_links.comment(new["body"], numbers or {})
    if dry:
        p = plan(existing, new, c, text, links_text)
        return describe(p) + ["comment"]
    comments = api("GET", f"/repos/{repo}/issues/{number}/comments?per_page=100")
    p = plan(existing, new, c, text, links_text, comments)
    patch = {}
    if p["title"]:
        patch["title"] = new["title"]
    if p["body"] == "rewrite":
        patch["body"] = new["body"]
    if patch:
        api("PATCH", f"/repos/{repo}/issues/{number}", patch)
    if p["labels_add"]:
        api("POST", f"/repos/{repo}/issues/{number}/labels", {"labels": p["labels_add"]})
    for other in p["labels_remove"]:
        api("DELETE", f"/repos/{repo}/issues/{number}/labels/{urllib.parse.quote(other)}")
    mine = find_comment(comments, MARKER)
    if p["comment"] == "update":
        api("PATCH", f"/repos/{repo}/issues/comments/{mine['id']}", {"body": text})
    elif p["comment"] == "create":
        api("POST", f"/repos/{repo}/issues/{number}/comments", {"body": text})
    issue_links.upsert(api, repo, number, links_text)
    done = describe(p)
    if done:
        time.sleep(2)
    return done


def batch_files():
    return [p for p in sorted((ROOT / "intake").iterdir())
            if p.is_file() and p.suffix.lower() in (".yml", ".yaml", ".csv") and not p.name.startswith("_")]


def reconcile(existing, comments_for, out_dir=None):
    """The plan of a live run against the existing issues, by short id. Nothing is written
    to GitHub (READ_ONLY). Returns the list of plan items."""
    published = published_titles()
    numbers = {i: e["number"] for e in existing.values() if (i := backlog_id(e.get("body")))}
    items, seen = [], set()
    for path in batch_files():
        batch = load_batch(path)
        for c in batch.get("candidates") or []:
            warnings = []
            key = match(c, existing)
            entry = published.get(key or "") or published.get(str(c.get("id") or "").lower()) \
                or published.get(str(c["title"]).strip().lower())
            new = issue(c, batch, warnings, published_path=entry, numbers=numbers)
            text = intake_comment(c, batch, entry, numbers)
            links_text = issue_links.comment(new["body"], numbers)
            if key is None:
                item = {"number": None, "id": c.get("id"), "action": "create", "title": new["title"], "warnings": warnings}
            else:
                e = existing[key]
                seen.add(e["number"])
                item = plan(e, new, c, text, links_text, comments_for(e["number"]))
                item["action"] = "update" if describe(item) else "in step"
                item["warnings"] = warnings
                item["owned"] = owned_body(e.get("body"))
            items.append(item)
            if out_dir is not None:
                d = out_dir / (str(item["number"]) if item["number"] else f"new-{c.get('id') or len(items)}")
                d.mkdir(parents=True, exist_ok=True)
                if key is not None:
                    (d / "before.md").write_text(f"# {existing[key]['title']}\n\n{existing[key].get('body') or ''}", encoding="utf-8")
                (d / "after.md").write_text(f"# {new['title']}\n\nlabels: {', '.join(new['labels'])}\n\n{new['body']}", encoding="utf-8")
                (d / "comment.md").write_text(text, encoding="utf-8")
                (d / "links.md").write_text(links_text or "", encoding="utf-8")
    for e in existing.values():
        if e["number"] not in seen and "intake-batch" in {l["name"] if isinstance(l, dict) else l for l in e.get("labels") or []}:
            items.append({"number": e["number"], "id": backlog_id(e.get("body")), "action": "not in any batch (left alone)"})
    if out_dir is not None:
        (out_dir / "plan.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    return items


def main():
    global READ_ONLY
    dry = "--dry-run" in sys.argv
    out_dir = None
    if "--write" in sys.argv:
        out_dir = pathlib.Path(sys.argv[sys.argv.index("--write") + 1])
        out_dir.mkdir(parents=True, exist_ok=True)
    repo = os.environ.get("GITHUB_REPOSITORY", "DIDAS-swiss/use-case-repository")
    if "--reconcile" in sys.argv:
        READ_ONLY = True
        if "--issues" in sys.argv:
            saved = json.loads(pathlib.Path(sys.argv[sys.argv.index("--issues") + 1]).read_text(encoding="utf-8"))
            existing = by_title(saved)
        else:
            existing = existing_issues(repo)
        if "--comments" in sys.argv:
            folder = pathlib.Path(sys.argv[sys.argv.index("--comments") + 1])
            comments_for = lambda n: (json.loads((folder / f"{n}.json").read_text(encoding="utf-8"))
                                      if (folder / f"{n}.json").exists() else None)
        elif "--with-comments" in sys.argv:
            comments_for = lambda n: api("GET", f"/repos/{repo}/issues/{n}/comments?per_page=100")
        else:
            comments_for = lambda n: None
        items = reconcile(existing, comments_for, out_dir)
        counts = {}
        for i in items:
            print(f"{i['action']:>10} {('#' + str(i['number'])) if i['number'] else '':>5} {i.get('id') or ''}: "
                  f"{', '.join(describe(i)) if i['action'] == 'update' else i.get('title') or ''}")
            counts[i["action"]] = counts.get(i["action"], 0) + 1
        hand = sum(1 for i in items if i.get("body") == "edited by hand")
        print("plan: " + ", ".join(f"{n} {a}" for a, n in sorted(counts.items())) +
              f"; {hand} description(s) edited by hand would be left as is. Nothing was written to GitHub.")
        return
    published = published_titles()
    existing = {} if dry else existing_issues(repo)
    # backlog id -> issue number, so relations can link the issues
    numbers = {i: e["number"] for e in existing.values() if (i := backlog_id(e.get("body")))}
    created = annotated = updates = 0
    for path in batch_files():
        batch = load_batch(path)
        candidates = batch.get("candidates") or []
        # open the new ones first, so the comments on existing issues can link them
        for c in sorted(candidates, key=lambda c: match(c, existing) is not None):
            warnings = []
            title = str(c["title"]).strip()
            key = match(c, existing)
            entry = published.get(key or "") or published.get(str(c.get("id") or "").lower())
            entry = entry or published.get(title.lower())
            new = issue(c, batch, warnings, published_path=entry, numbers=numbers)
            for w in warnings:
                print(f"::warning file={path.relative_to(ROOT)}::{w}")
            if key is not None:
                done = annotate(repo, existing[key], new, c, batch, entry, dry, numbers)
                annotated += bool(done)
                print(f"{'would update' if dry else 'update'} #{existing[key]['number']} {new['title']}: {', '.join(done) or 'in step'}")
                continue
            if out_dir:
                (out_dir / f"{c.get('no') or created:>03}.md").write_text(f"# {new['title']}\n\nlabels: {new['labels']}\n\n{new['body']}", encoding="utf-8")
            if dry:
                print(f"would create {new['title']}{'  (update of ' + entry + ')' if entry else ''}  labels={new['labels']}  body={len(new['body'])} chars")
            else:
                made = create(repo, new)
                api("POST", f"/repos/{repo}/issues/{made['number']}/comments", {"body": intake_comment(c, batch, entry, numbers)})
                issue_links.upsert(api, repo, made["number"], issue_links.comment(new["body"], numbers))
                print(f"create #{made['number']} {new['title']}{'  (update of ' + entry + ')' if entry else ''}")
                existing[title_key(title)] = made
                if c.get("id"):
                    numbers[c["id"]] = made["number"]
            created += 1
            updates += bool(entry)
    print(f"{created} {'to create' if dry else 'created'} ({updates} updates of published entries), "
          f"{annotated} existing {'to bring' if dry else 'brought'} in step")
    if dry:
        print("note: --dry-run does not look at existing issues; use --reconcile for the plan of a live run.")


if __name__ == "__main__":
    main()
