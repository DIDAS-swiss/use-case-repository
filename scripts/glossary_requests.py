#!/usr/bin/env python3
"""Turn terms a use case needs into new-term requests in the DIDAS Glossary.

A use-case issue lists terms the glossary does not define yet in the form field
"Terms missing from the DIDAS Glossary", one per line, each with what it means
in that use case. For each such term this script:

  - skips it when the glossary already defines it, under its name or an alias
    (_data/glossary-terms.csv, kept current by scripts/sources_sync.py);
  - finds the glossary's issue for it, a "[Term] <term>" issue labelled
    `new term`, or opens one in the shape of the glossary's own new-term form
    (read from that repository), so the glossary handles it like any proposal;
  - keeps one comment on that glossary issue listing every use case that needs
    the term, and one comment on each use-case issue linking its requests.

A glossary issue closed as not planned is not reopened; the use-case comment
says so. Nothing is ever closed or deleted.

Run from the repository root:
  python3 scripts/glossary_requests.py --dry-run     read only: print the plan
  GITHUB_TOKEN=… GLOSSARY_TOKEN=… python3 scripts/glossary_requests.py

GITHUB_TOKEN writes the comments in this repository; GLOSSARY_TOKEN needs
Issues: Read and write on DIDAS-swiss/didas-glossary. Needs PyYAML.
"""

import csv
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

import yaml

import use_case_form as form

ROOT = form.ROOT
API = "https://api.github.com"
REPO = os.environ.get("GITHUB_REPOSITORY", "DIDAS-swiss/use-case-repository")
GLOSSARY = os.environ.get("GLOSSARY_REPOSITORY", "DIDAS-swiss/didas-glossary")
GLOSSARY_FORM = ".github/ISSUE_TEMPLATE/new-term.yml"
USE_CASE_MARKER = "<!-- glossary-requests -->"
GLOSSARY_MARKER = "<!-- use-case-requests -->"
TITLE_PREFIX = "[Term] "


class ReadOnlyError(RuntimeError):
    pass


def client(token_env, read_only):
    def api(method, path, body=None):
        if read_only and method != "GET":
            raise ReadOnlyError(f"read-only run refused {method} {path}")
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "didas-use-case-repository glossary-requests"}
        if os.environ.get(token_env):
            headers["Authorization"] = f"Bearer {os.environ[token_env]}"
        req = urllib.request.Request(f"{API}{path}", method=method, headers=headers,
                                     data=json.dumps(body).encode() if body is not None else None)
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read() or b"null")
    return api


def pages(api, path):
    out, page = [], 1
    while True:
        batch = api("GET", f"{path}{'&' if '?' in path else '?'}per_page=100&page={page}")
        out += batch
        if len(batch) < 100:
            return out
        page += 1


def norm(term):
    """A term in a comparable form: lower case, single spaces, no surrounding punctuation."""
    return re.sub(r"\s+", " ", re.sub(r"[`*_\"'«»“”]", "", term or "")).strip(" .:;,-").lower()


def requested_terms(body):
    """[(term, meaning)] from the missing-terms field of an issue body."""
    out = []
    for line in (form.parse(body).get("missing_terms") or "").split("\n"):
        line = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", line).strip()
        if not line:
            continue
        m = re.match(r"^(.+?)\s+(?:—|–|-|:)\s+(.+)$", line) or re.match(r"^(.+?):\s*(.+)$", line)
        term, meaning = (m.group(1), m.group(2)) if m else (line, "")
        term = term.strip(" `*_\"'")
        if term and len(term) <= 80:
            out.append((term, meaning.strip()))
    return out


def defined_terms():
    """Every name the glossary defines (term and aliases), normalised -> its row."""
    out = {}
    path = ROOT / "_data" / "glossary-terms.csv"
    if path.exists():
        with open(path, encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                for name in [r["term"]] + [a for a in (r.get("aliases") or "").split(";")]:
                    if name.strip():
                        out[norm(name)] = r
    return out


def collect(issues, defined):
    """{normalised term: {"term", "requests": [(number, title, meaning)]}} for terms not defined."""
    wanted = {}
    for i in sorted(issues, key=lambda i: i["number"]):
        if i.get("pull_request") or i.get("state") != "open":
            continue
        for term, meaning in requested_terms(i.get("body")):
            key = norm(term)
            if key in defined:
                continue
            w = wanted.setdefault(key, {"term": term, "requests": []})
            if i["number"] not in [r[0] for r in w["requests"]]:
                w["requests"].append((i["number"], i["title"], meaning))
    return wanted


def glossary_issue_index(issues):
    """Glossary new-term issues by normalised term (from the "[Term] …" title)."""
    out = {}
    for i in issues:
        if i.get("pull_request"):
            continue
        title = i["title"]
        if title.startswith(TITLE_PREFIX.strip()):
            key = norm(title[len(TITLE_PREFIX.strip()):])
            # prefer an open issue over a closed one
            if key not in out or (out[key]["state"] != "open" and i["state"] == "open"):
                out[key] = i
    return out


def new_term_body(glossary_form, term, requests, repo):
    """An issue body in the shape of the glossary's new-term form, as GitHub writes it."""
    links = "\n".join(f"- [{repo}#{n}](https://github.com/{repo}/issues/{n}) {t}" + (f": {m}" if m else "")
                      for n, t, m in requests)
    meanings = "\n".join(f"- {m}" for _, _, m in requests if m)
    values = {
        "term": term,
        "definition": "_To be drafted._ Meaning in the requesting use case(s):\n\n" + (meanings or "- not stated"),
        "sources": "Requested by these use cases in the DIDAS use-case repository:\n\n" + links,
    }
    parts = []
    for f in glossary_form.get("body") or []:
        if not f.get("id"):
            continue
        v = values.get(f["id"], "")
        if f["type"] == "dropdown":
            opts = f["attributes"].get("options") or []
            v = next((o for o in opts if o.lower().startswith("not checked")), "")
        parts.append(f"### {f['attributes']['label']}\n\n{v.strip() or '_No response_'}")
    return "\n\n".join(parts)


def requests_comment(requests, repo):
    lines = [GLOSSARY_MARKER, "**Needed by these use cases**", ""]
    lines += [f"- [{repo}#{n}](https://github.com/{repo}/issues/{n}) {t}" + (f": {m}" if m else "") for n, t, m in requests]
    lines += ["", "_Kept in step by the use-case repository (`scripts/glossary_requests.py`) from each use case's "
              "\"Terms missing from the DIDAS Glossary\" field._"]
    return "\n".join(lines)


def use_case_comment(items, glossary):
    lines = [USE_CASE_MARKER, "**Terms requested from the DIDAS Glossary**", ""]
    for term, issue, note in items:
        if issue:
            lines.append(f"- **{term}**: [{glossary}#{issue['number']}]({issue['html_url']})" + (f" ({note})" if note else ""))
        else:
            lines.append(f"- **{term}**: {note or 'to be opened'}")
    lines += ["", "_From the field \"Terms missing from the DIDAS Glossary\"; updated when it changes._"]
    return "\n".join(lines)


def upsert_comment(api, repo, number, marker, text, dry, log):
    comments = api("GET", f"/repos/{repo}/issues/{number}/comments?per_page=100") if number else []
    mine = next((c for c in comments if marker in (c.get("body") or "")), None)
    if text and mine and mine["body"] != text:
        log.append(f"update comment on {repo}#{number}")
        if not dry:
            api("PATCH", f"/repos/{repo}/issues/comments/{mine['id']}", {"body": text})
    elif text and not mine:
        log.append(f"add comment on {repo}#{number}")
        if not dry:
            api("POST", f"/repos/{repo}/issues/{number}/comments", {"body": text})
    elif not text and mine:
        log.append(f"remove comment on {repo}#{number}")
        if not dry:
            api("DELETE", f"/repos/{repo}/issues/comments/{mine['id']}")


def main():
    dry = "--dry-run" in sys.argv
    if not dry and not os.environ.get("GLOSSARY_TOKEN"):
        print("::warning::GLOSSARY_TOKEN is not set, so no glossary request is opened. See CONTRIBUTING.md, Glossary requests.")
        return 0
    here = client("GITHUB_TOKEN", dry)
    there = client("GLOSSARY_TOKEN", dry)

    issues = pages(here, f"/repos/{REPO}/issues?state=all&labels=use-case")
    defined = defined_terms()
    wanted = collect(issues, defined)
    glossary_issues = glossary_issue_index(pages(there, f"/repos/{GLOSSARY}/issues?state=all&labels={urllib.parse.quote('new term')}"))
    raw = there("GET", f"/repos/{GLOSSARY}/contents/{GLOSSARY_FORM}")
    import base64
    glossary_form = yaml.safe_load(base64.b64decode(raw["content"]).decode("utf-8"))

    log, status = [], {}
    for key, w in sorted(wanted.items()):
        issue, note = glossary_issues.get(key), ""
        if issue and issue["state"] == "closed":
            note = ("closed as not planned in the glossary" if issue.get("state_reason") == "not_planned" else
                    "closed in the glossary; not in its term list yet")
        elif issue is None:
            title = TITLE_PREFIX + w["term"]
            log.append(f"open {GLOSSARY} issue {title!r} for {', '.join('#' + str(r[0]) for r in w['requests'])}")
            if not dry:
                issue = there("POST", f"/repos/{GLOSSARY}/issues", {
                    "title": title, "body": new_term_body(glossary_form, w["term"], w["requests"], REPO),
                    "labels": glossary_form.get("labels") or [], "assignees": glossary_form.get("assignees") or []})
                time.sleep(2)
        if issue and issue["state"] == "open":
            upsert_comment(there, GLOSSARY, issue["number"], GLOSSARY_MARKER, requests_comment(w["requests"], REPO), dry, log)
        status[key] = (issue, note)

    # each open use case that names terms gets one comment saying where each stands;
    # one that no longer names any loses its comment
    for i in issues:
        if i.get("pull_request") or i.get("state") != "open":
            continue
        items = []
        for term, _ in requested_terms(i.get("body")):
            key = norm(term)
            if key in defined:
                items.append((term, None, f"defined: [{defined[key]['term']}]({defined[key]['url']})"))
            elif key in status:
                items.append((term, *status[key]))
        text = use_case_comment(items, GLOSSARY) if items else None
        if text or i.get("comments"):
            upsert_comment(here, REPO, i["number"], USE_CASE_MARKER, text, dry, log)

    for line in log:
        print(("would " if dry else "") + line)
    print(f"{len(wanted)} term(s) requested and not in the glossary; {len(log)} change(s)"
          f"{' planned, nothing written' if dry else ''}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
