"""Regression tests for the use-case form, the intake and the links comment.

They check behaviour, not editorial text: bodies written with the current and the
earlier form parse to the same fields, the intake's rendering is stable and
recognised as its own, an edited body is never overwritten, and the reconcile
mode cannot write to GitHub.

Run from the repository root:  python3 -m unittest discover -s tests -v
Needs PyYAML.
"""

import csv
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import intake            # noqa: E402
import issue_links       # noqa: E402
import use_case_form as form   # noqa: E402

FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"
LEGACY = (FIXTURES / "legacy-body-311e992.md").read_text(encoding="utf-8")
FIRST = (FIXTURES / "first-format-body.md").read_text(encoding="utf-8")


def batch():
    path = next(p for p in intake.batch_files() if p.suffix == ".csv")
    return intake.load_batch(path)


class FormStructure(unittest.TestCase):
    def test_ids_unique_and_core_first(self):
        ids = [f["id"] for f in form.FIELDS]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(tuple(ids[:len(form.CORE)]), form.CORE)

    def test_core_fields_required_except_sources(self):
        for fid in form.CORE:
            required = form.BY_ID[fid].get("validations", {}).get("required", False)
            self.assertEqual(required, fid != "sources", fid)

    def test_legacy_labels_do_not_collide(self):
        current = {f["attributes"]["label"] for f in form.FIELDS}
        for fid, old in form.LEGACY_LABELS.items():
            self.assertIn(fid, form.BY_ID)
            for label in old:
                self.assertNotIn(label, current, label)

    def test_lighthouse_selection_not_offered_to_submitters(self):
        self.assertNotIn("Selected as lighthouse (DIDAS decision)", form.options("lighthouse"))

    def test_evidence_status_options_cover_all_values(self):
        for value in form.EVIDENCE_STATUS:
            self.assertIsNotNone(form.option("evidence_status", value), value)


class Parsing(unittest.TestCase):
    def test_legacy_body_parses(self):
        f = form.parse(LEGACY)
        for fid in ("title", "summary", "outcome", "actors", "credentials", "demand", "open_questions", "sources"):
            self.assertTrue(f.get(fid), fid)
        self.assertEqual(form.short_id(LEGACY), f["entry_id"])
        self.assertNotIn("evidence_status", f)   # the earlier form had no such field

    def test_legacy_lighthouse_option_is_a_proposal_and_the_label_the_decision(self):
        f = form.parse(LEGACY)
        self.assertEqual(form.lighthouse(f, ["use-case", "lighthouse"]), ("candidate", "selected"))
        self.assertEqual(form.lighthouse(f, ["use-case"]), ("candidate", ""))

    def test_first_format_short_id(self):
        self.assertEqual(form.short_id(FIRST), "age-check-counter")
        self.assertTrue(form.owned_body(FIRST))

    def test_render_parse_round_trip(self):
        values = {"title": "Check a thing", "summary": "Who decides what.", "actors": "Verifier: X",
                  "outcome": "A fact", "demand": "- **Expected benefit (hypothesis)**: less checking",
                  "evidence_status": form.option("evidence_status", "design"), "entry_id": "check-a-thing",
                  "ambition": ["AL2"], "lighthouse": "Propose as lighthouse candidate"}
        body = form.render(values)
        f = form.parse(body)
        for k in ("title", "summary", "actors", "outcome", "demand", "entry_id"):
            self.assertEqual(f[k], values[k], k)
        self.assertEqual(form.evidence_status(f["evidence_status"]), "design")
        self.assertIn("- [X] AL2", f["ambition"])
        self.assertEqual(f["sources"], "")          # _No response_ reads as empty
        self.assertEqual(form.lighthouse(f, []), ("candidate", ""))

    def test_reader_sections_omit_empty_but_keep_core(self):
        body = form.render({"title": "T", "summary": "S", "actors": "A"})
        sections = dict(form.reader_sections(form.parse(body)))
        self.assertEqual(sections["Summary"], "S")
        self.assertEqual(sections["Facts to prove"], "Not yet known.")
        self.assertEqual(sections["Evidence status"], "Not yet known.")
        self.assertNotIn("Process flow (optional)", sections)
        self.assertNotIn("Background (optional)", sections)


class Ownership(unittest.TestCase):
    def test_rendered_body_is_owned_and_edit_is_not(self):
        body = form.render({"title": "T", "summary": "S"})
        self.assertTrue(form.owned_body(body))
        self.assertFalse(form.owned_body(body.replace("S", "S, edited by hand", 1)))
        self.assertFalse(form.owned_body("A body somebody wrote"))

    def test_legacy_generated_body_is_still_owned(self):
        self.assertTrue(form.owned_body(LEGACY))


class Generation(unittest.TestCase):
    def test_every_batch_entry_renders_stably_and_parses(self):
        b = batch()
        self.assertTrue(b["candidates"])
        for c in b["candidates"]:
            first = intake.issue(c, b, [])
            again = intake.issue(c, b, [])
            self.assertEqual(first, again, c["id"])
            self.assertTrue(form.owned_body(first["body"]), c["id"])
            f = form.parse(first["body"])
            self.assertEqual(f["entry_id"], c["id"])
            self.assertEqual(f["title"], c["title"])
            self.assertNotIn("Selected as lighthouse", first["body"])

    def test_batch_lighthouse_decision_stays_a_label(self):
        b = batch()
        for c in b["candidates"]:
            want = intake.lighthouse_label(c.get("lighthouse"))
            labels = intake.issue(c, b, [])["labels"]
            for lh in intake.LIGHTHOUSE_LABELS:
                self.assertEqual(lh in labels, lh == want, c["id"])

    def test_placeholders_left_out_of_demand(self):
        b = batch()
        c = dict(b["candidates"][0], indicative_scale="no official figure", value="", relying_parties="Banks")
        demand = form.parse(intake.issue(c, b, [])["body"])["demand"]
        self.assertNotIn("no official figure", demand)
        self.assertIn("Banks", demand)

    def test_links_comment_reads_legacy_and_current_bodies(self):
        legacy = issue_links.comment(LEGACY, {})
        self.assertIsNotNone(legacy)
        self.assertIn(issue_links.MARKER, legacy)
        b = batch()
        c = next(c for c in b["candidates"] if c.get("credentials_reused") or c.get("credentials_new"))
        current = issue_links.comment(intake.issue(c, b, [])["body"], {})
        if any(x in issue_links.CREDENTIALS for x in (c.get("credentials_reused") or []) + (c.get("credentials_new") or [])):
            self.assertIsNotNone(current)


class Reconcile(unittest.TestCase):
    def setUp(self):
        self.b = batch()
        self.c = self.b["candidates"][0]
        self.new = intake.issue(self.c, self.b, [])
        self.comment = intake.intake_comment(self.c, self.b, None)
        self.links = issue_links.comment(self.new["body"], {})

    def existing(self, body, title=None, labels=()):
        return {"number": 1, "title": title or self.new["title"], "body": body,
                "labels": [{"name": n} for n in ("use-case", "intake-batch", *labels)]}

    def comments(self):
        out = [{"id": 10, "body": self.comment}]
        if self.links:
            out.append({"id": 11, "body": self.links})
        return out

    def test_in_step_issue_needs_nothing(self):
        want = intake.lighthouse_label(self.c.get("lighthouse"))
        e = self.existing(self.new["body"], labels=(want,) if want else ())
        p = intake.plan(e, self.new, self.c, self.comment, self.links, self.comments())
        self.assertEqual(intake.describe(p), [])

    def test_owned_old_body_is_rewritten(self):
        e = self.existing(LEGACY)
        p = intake.plan(e, self.new, self.c, self.comment, self.links, None)
        self.assertEqual(p["body"], "rewrite")
        self.assertEqual(p["comment"], "unchecked")

    def test_body_edited_by_hand_is_left_alone(self):
        edited = self.new["body"].replace("### Summary\n\n", "### Summary\n\nA curator's note. ", 1)
        e = self.existing(edited)
        p = intake.plan(e, self.new, self.c, self.comment, self.links, self.comments())
        self.assertEqual(p["body"], "edited by hand")
        self.assertIn("description edited by hand, left as is", intake.describe(p))

    def test_match_by_short_id_survives_a_new_title(self):
        e = self.existing(self.new["body"], title="An earlier title")
        existing = intake.by_title([e])
        self.assertEqual(intake.match(self.c, existing), "an earlier title")
        p = intake.plan(e, self.new, self.c, self.comment, self.links, None)
        self.assertEqual(p["title"], ["An earlier title", self.new["title"]])

    def test_reconcile_is_read_only(self):
        intake.READ_ONLY = True
        try:
            with self.assertRaises(intake.ReadOnlyError):
                intake.api("POST", "/repos/x/y/issues", {"title": "t"})
            with self.assertRaises(intake.ReadOnlyError):
                intake.api("PATCH", "/repos/x/y/issues/1", {"body": "b"})
        finally:
            intake.READ_ONLY = False

    def test_reconcile_plans_every_batch_entry_against_saved_issues(self):
        issues = []
        for n, c in enumerate(self.b["candidates"], start=1):
            issues.append({"number": n, "title": "old " + c["title"], "body": f"### Short id (optional)\n\n{c['id']}\n",
                           "labels": [{"name": "use-case"}, {"name": "intake-batch"}]})
        intake.READ_ONLY = True
        try:
            items = intake.reconcile(intake.by_title(issues), lambda n: None)
        finally:
            intake.READ_ONLY = False
        by_id = {i["id"]: i for i in items}
        for c in self.b["candidates"]:
            self.assertEqual(by_id[c["id"]]["action"], "update", c["id"])
            self.assertEqual(by_id[c["id"]]["body"], "edited by hand", c["id"])   # no hash: never overwritten


class Reviews(unittest.TestCase):
    def test_review_rows_name_batch_entries(self):
        ids = {c["id"] for c in batch()["candidates"]}
        for uid in intake.REVIEWS:
            self.assertIn(uid, ids)
        for uid in intake.SCOPES:
            self.assertIn(uid, ids)

    def test_review_section_in_comment_is_marked_as_recommendation(self):
        b = batch()
        for c in b["candidates"]:
            if c["id"] in intake.REVIEWS:
                text = intake.intake_comment(c, b, None)
                self.assertIn("a recommendation, not a decision", text)
                self.assertIn("stays open", text)
                break


if __name__ == "__main__":
    unittest.main()
