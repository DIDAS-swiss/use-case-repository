#!/usr/bin/env python3
"""Links for a use-case issue, read from the fields of the use-case form.

A use-case issue is written in the fields of the form
(.github/ISSUE_TEMPLATE/use-case-candidate.yml), whether someone filled in the
form or the intake wrote it. This reads those fields back and keeps one comment
on the issue with a link for everything it names: the credentials described in
this repository, the I14Y credential datasets, trust flows, Industry Function
Graph patterns, DIDAS Glossary terms and the related, upstream and downstream
use cases (their entry, or their candidate issue).

Run from the repository root, for one issue:
  GITHUB_TOKEN=… GITHUB_REPOSITORY=owner/repo python3 scripts/issue_links.py <number>

Needs PyYAML.
"""

import csv
import json
import os
import pathlib
import re
import sys
import urllib.request

import yaml

import use_case_form as form

ROOT = form.ROOT
API = "https://api.github.com"
SITE = "https://didas-swiss.github.io/use-case-repository"
REPO = "https://github.com/DIDAS-swiss/use-case-repository"
MARKER = "<!-- issue-links -->"

FIELDS = form.BY_ID


def rows(name):
    path = ROOT / "_data" / name
    if not path.exists():
        return []
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def credential_titles():
    out = {}
    for path in sorted((ROOT / "credentials").glob("*.md")):
        if not path.name.startswith(("_", "README")):
            fm = yaml.safe_load(path.read_text(encoding="utf-8").split("---")[1]) or {}
            out[path.stem] = fm.get("title") or path.stem
    return out


CREDENTIALS = credential_titles()
I14Y = {r["identifier"]: r for r in rows("i14y-credentials.csv")}
FLOWS = {r["id"]: r for r in rows("trust-flows.csv")}
PATTERNS = {r["id"]: r for r in rows("ifm-patterns.csv")}
TERMS = {r["id"]: r for r in rows("glossary-terms.csv")}
USE_CASES = {r["id"]: r for r in rows("use-case-index.csv")}


def fields(body):
    """The form's fields in an issue body, as {field id: text}; reads current and earlier forms."""
    return form.parse(body)


def chosen(field_id, text):
    """The leading ids of the dropdown options a field's text holds."""
    return form.chosen(field_id, text)


def ids(text, known):
    """Known ids named in a free-text field, in order."""
    found = []
    for token in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", (text or "").lower()):
        if token in known and token not in found:
            found.append(token)
    return found


def comment(body, numbers):
    """The links comment for an issue body, or None when it names nothing linkable.
    numbers maps the id of a candidate to its issue number."""
    f = fields(body)
    sections = []

    def section(title, items):
        if items:
            sections.append(f"**{title}**\n\n" + "\n".join(f"- {x}" for x in items))

    def use_case(uid):
        u = USE_CASES.get(uid) or {}
        if u.get("kind") == "entry":
            return f"[{u['title']}]({SITE}/use-cases/{uid}.html) `{uid}`"
        if uid in numbers:
            return f"#{numbers[uid]} {u.get('title', '')} `{uid}`".replace("  ", " ")
        return f"{u.get('title', uid)} `{uid}`"

    creds = chosen("described_credentials", f.get("described_credentials"))
    creds += [c for c in ids(f.get("credentials"), CREDENTIALS) if c not in creds]
    section("Credentials described in this repository",
            [f"[{CREDENTIALS[c]}]({SITE}/credentials/{c}.html)" for c in creds if c in CREDENTIALS])
    section("Credential datasets on I14Y",
            [f"[{I14Y[d]['title']}]({I14Y[d]['url']}) `{d}`" for d in chosen("i14y_credentials", f.get("i14y_credentials")) if d in I14Y])
    section("Trust flows",
            [f"[{FLOWS[x]['title']}]({FLOWS[x]['url']}) `{x}` ({FLOWS[x]['status']})" for x in chosen("trust_flows", f.get("trust_flows")) if x in FLOWS])
    section("Use case patterns (Industry Function Graph)",
            [f"[{PATTERNS[x]['name']}]({PATTERNS[x]['url']}) `{x}`" for x in chosen("ifm_patterns", f.get("ifm_patterns")) if x in PATTERNS])
    section("DIDAS Glossary terms",
            [f"[{TERMS[x]['term']}]({TERMS[x]['url']})" for x in chosen("glossary_terms", f.get("glossary_terms")) if x in TERMS])
    for key, title in (("upstream_use_cases", "Upstream use cases"), ("downstream_use_cases", "Downstream use cases"),
                       ("related_use_cases", "Related use cases")):
        section(title, [use_case(u) for u in ids(f.get(key), USE_CASES)])
    if not sections:
        return None
    return MARKER + "\n**Links**\n\n" + "\n\n".join(sections) + \
        "\n\n_Built from the fields of this issue; updated when the description changes._"


def numbers_from(issues):
    """Candidate id -> issue number, from the Short id field of use-case issues."""
    out = {}
    for i in issues:
        sid = form.short_id(i.get("body"))
        if sid:
            out[sid] = i["number"]
    return out


def upsert(api, repo, number, text):
    """Create, update or remove the links comment. Returns what it did."""
    comments = api("GET", f"/repos/{repo}/issues/{number}/comments?per_page=100")
    mine = next((c for c in comments if MARKER in (c.get("body") or "")), None)
    if text and mine and mine["body"] != text:
        api("PATCH", f"/repos/{repo}/issues/comments/{mine['id']}", {"body": text})
        return "links updated"
    if text and not mine:
        api("POST", f"/repos/{repo}/issues/{number}/comments", {"body": text})
        return "links"
    if not text and mine:
        api("DELETE", f"/repos/{repo}/issues/comments/{mine['id']}")
        return "links removed"
    return None


def api(method, path, body=None):
    req = urllib.request.Request(
        f"{API}{path}", method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "didas-use-case-repository issue-links"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read() or b"null")


def main():
    repo = os.environ.get("GITHUB_REPOSITORY", "DIDAS-swiss/use-case-repository")
    number = int(sys.argv[1])
    issue = api("GET", f"/repos/{repo}/issues/{number}")
    issues, page = [], 1
    while True:
        batch = api("GET", f"/repos/{repo}/issues?state=all&labels=use-case&per_page=100&page={page}")
        issues += batch
        if len(batch) < 100:
            break
        page += 1
    done = upsert(api, repo, number, comment(issue.get("body"), numbers_from(issues)))
    print(f"#{number}: {done or 'links in step'}")


if __name__ == "__main__":
    main()
