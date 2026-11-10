"""Tests for scripts/glossary_requests.py against a fake GitHub (nothing is sent).

Run from the repository root:  python3 -m unittest discover -s tests -v
"""

import base64
import os
import pathlib
import sys
import unittest
from unittest import mock

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import glossary_requests as gr   # noqa: E402
import use_case_form as form     # noqa: E402

GLOSSARY_FORM = {
    "name": "New term", "title": "[Term] ", "labels": ["glossary", "new term", "proposal"], "assignees": ["someone"],
    "body": [
        {"type": "markdown", "attributes": {"value": "intro"}},
        {"type": "input", "id": "term", "attributes": {"label": "Term (English)"}},
        {"type": "textarea", "id": "definition", "attributes": {"label": "Proposed definition"}},
        {"type": "textarea", "id": "sources", "attributes": {"label": "Sources"}},
        {"type": "dropdown", "id": "toip-check", "attributes": {"label": "ToIP check",
                                                                "options": ["Not in the ToIP glossary", "Not checked yet"]}},
        {"type": "input", "id": "alias-de", "attributes": {"label": "German alias(es)"}},
    ],
}


def use_case(number, terms, title=None, state="open"):
    body = form.render({"title": title or f"Use case {number}", "summary": "s", "missing_terms": "\n".join(terms)})
    return {"number": number, "title": title or f"Use case {number}", "state": state, "body": body, "comments": 1,
            "labels": [{"name": "use-case"}]}


class FakeGitHub:
    def __init__(self, use_cases, glossary_issues, comments=None):
        self.use_cases, self.glossary_issues = use_cases, glossary_issues
        self.comments = comments or {}
        self.writes = []
        self.next_number = 900

    def api(self, method, path, body=None):
        if method != "GET":
            self.writes.append((method, path, body))
        if method == "GET" and "/issues?" in path and gr.GLOSSARY in path:
            return self.glossary_issues if "page=1" in path else []
        if method == "GET" and "/issues?" in path:
            return self.use_cases if "page=1" in path else []
        if method == "GET" and "/contents/" in path:
            return {"content": base64.b64encode(yaml.safe_dump(GLOSSARY_FORM).encode()).decode()}
        if method == "GET" and path.endswith("/comments?per_page=100"):
            return self.comments.get(path, [])
        if method == "POST" and path.endswith(f"/repos/{gr.GLOSSARY}/issues"):
            self.next_number += 1
            return {"number": self.next_number, "state": "open",
                    "html_url": f"https://github.com/{gr.GLOSSARY}/issues/{self.next_number}"}
        return {}


def run(fake, dry=False):
    with mock.patch.object(gr, "client", lambda env, ro: (lambda m, p, b=None: (_ for _ in ()).throw(gr.ReadOnlyError(p))
                                                           if ro and m != "GET" else fake.api(m, p, b))), \
         mock.patch.object(sys, "argv", ["x"] + (["--dry-run"] if dry else [])), \
         mock.patch.dict(os.environ, {"GLOSSARY_TOKEN": "t"}), \
         mock.patch.object(gr, "defined_terms", lambda: {"credential": {"term": "credential", "url": "u#credential"},
                                                          "nachweis": {"term": "credential", "url": "u#credential"}}):
        gr.main()
    return fake.writes


class Parsing(unittest.TestCase):
    def test_field_lines_parse_with_any_separator(self):
        body = form.render({"title": "t", "missing_terms": "mandate — authority to act\n- status attestation: a dated statement\n2. holder binding - ties a credential to a person\nbare term"})
        self.assertEqual(gr.requested_terms(body), [("mandate", "authority to act"), ("status attestation", "a dated statement"),
                                                    ("holder binding", "ties a credential to a person"), ("bare term", "")])

    def test_old_bodies_without_the_field_request_nothing(self):
        legacy = (ROOT / "tests" / "fixtures" / "legacy-body-311e992.md").read_text(encoding="utf-8")
        self.assertEqual(gr.requested_terms(legacy), [])

    def test_norm_ignores_case_and_markup(self):
        self.assertEqual(gr.norm("**Status  Attestation**."), "status attestation")

    def test_glossary_index_prefers_open_issue(self):
        idx = gr.glossary_issue_index([{"number": 1, "title": "[Term] Mandate", "state": "closed"},
                                       {"number": 2, "title": "[Term] mandate", "state": "open"}])
        self.assertEqual(idx["mandate"]["number"], 2)

    def test_body_follows_the_glossary_form(self):
        body = gr.new_term_body(GLOSSARY_FORM, "mandate", [(5, "Use case 5", "authority to act")], "o/r")
        labels = [line[4:] for line in body.split("\n") if line.startswith("### ")]
        self.assertEqual(labels, ["Term (English)", "Proposed definition", "Sources", "ToIP check", "German alias(es)"])
        self.assertIn("Not checked yet", body)
        self.assertIn("o/r#5", body)


class Plan(unittest.TestCase):
    def test_one_issue_per_term_shared_by_use_cases(self):
        fake = FakeGitHub([use_case(5, ["mandate — authority to act"]), use_case(7, ["Mandate: delegated authority"])], [])
        writes = run(fake)
        created = [w for w in writes if w[0] == "POST" and w[1].endswith(f"{gr.GLOSSARY}/issues")]
        self.assertEqual(len(created), 1)
        self.assertEqual(created[0][2]["title"], "[Term] mandate")
        self.assertEqual(created[0][2]["labels"], ["glossary", "new term", "proposal"])
        self.assertIn("#5", created[0][2]["body"])
        self.assertIn("#7", created[0][2]["body"])

    def test_defined_terms_and_aliases_are_not_requested(self):
        fake = FakeGitHub([use_case(5, ["Credential — a set of claims", "Nachweis"])], [])
        writes = run(fake)
        self.assertFalse([w for w in writes if w[1].endswith(f"{gr.GLOSSARY}/issues")])
        note = [w for w in writes if w[1].endswith("/issues/5/comments")]
        self.assertEqual(len(note), 1)
        self.assertIn("defined", note[0][2]["body"])

    def test_existing_issue_is_reused_and_not_planned_is_not_reopened(self):
        glossary = [{"number": 40, "title": "[Term] mandate", "state": "open", "html_url": "g/40"},
                    {"number": 41, "title": "[Term] wallet binding", "state": "closed", "state_reason": "not_planned",
                     "html_url": "g/41"}]
        fake = FakeGitHub([use_case(5, ["mandate", "wallet binding"])], glossary)
        writes = run(fake)
        self.assertFalse([w for w in writes if w[0] == "POST" and w[1].endswith(f"{gr.GLOSSARY}/issues")])
        self.assertFalse([w for w in writes if w[0] == "PATCH" and "/issues/41" in w[1]])
        self.assertTrue([w for w in writes if w[1].endswith(f"{gr.GLOSSARY}/issues/40/comments")])
        uc = [w for w in writes if w[1].endswith("/issues/5/comments")][0][2]["body"]
        self.assertIn("not planned", uc)

    def test_closed_use_cases_are_ignored(self):
        fake = FakeGitHub([use_case(5, ["mandate"], state="closed")], [])
        self.assertEqual(run(fake), [])

    def test_dry_run_writes_nothing(self):
        fake = FakeGitHub([use_case(5, ["mandate"])], [])
        self.assertEqual(run(fake, dry=True), [])

    def test_stale_comment_is_removed_when_the_field_is_emptied(self):
        path = f"/repos/{gr.REPO}/issues/5/comments?per_page=100"
        fake = FakeGitHub([use_case(5, [])], [], {path: [{"id": 77, "body": gr.USE_CASE_MARKER + "\nold"}]})
        writes = run(fake)
        self.assertIn(("DELETE", f"/repos/{gr.REPO}/issues/comments/77", None), writes)


if __name__ == "__main__":
    unittest.main()
