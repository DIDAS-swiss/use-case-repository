"""Tests for variants: the relation variant_of and the [variant] marker in external_refs.

Run from the repository root:  python3 -m unittest discover -s tests -v
"""

import csv
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_data            # noqa: E402
import intake                # noqa: E402
import issue_links           # noqa: E402
import use_case_form as form  # noqa: E402

SOURCES = check_data.external_sources()
COLS = ["id", "title", "related_use_cases", "upstream_use_cases", "downstream_use_cases", "variant_of"]


def batch():
    path = next(p for p in intake.batch_files() if p.suffix == ".csv")
    return intake.load_batch(path)


class VariantMarker(unittest.TestCase):
    def test_marker_with_and_without_status_passes(self):
        e, w = check_data.external_ref_findings("t", "BJ-v41-002 (LAUNCH) [variant]; FB-EID-E21-001 [variant]", SOURCES)
        self.assertEqual((e, w), ([], []))

    def test_other_markers_or_order_fail(self):
        for item in ("FB-EID-E21-001 [similar]", "BJ-v41-002 [variant] (LAUNCH)", "FB-EID-E21-001 (variant"):
            e, _ = check_data.external_ref_findings("t", item, SOURCES)
            self.assertEqual(len(e), 1, item)

    def test_marker_does_not_hide_a_duplicate(self):
        _, w = check_data.external_ref_findings("t", "FB-EID-E21-001; FB-EID-E21-001 [variant]", SOURCES)
        self.assertEqual(len(w), 1)

    def test_form_explains_the_marker(self):
        self.assertIn("[variant]", form.BY_ID["external_refs"]["attributes"]["description"])


class VariantOf(unittest.TestCase):
    def run_check(self, rows):
        with tempfile.TemporaryDirectory() as tmp:
            (pathlib.Path(tmp) / "intake").mkdir()
            with open(pathlib.Path(tmp) / "intake" / "main.csv", "w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=COLS)
                w.writeheader()
                for r in rows:
                    w.writerow({c: r.get(c, "") for c in COLS})
            errors, warnings = [], []
            with mock.patch.object(check_data, "ROOT", pathlib.Path(tmp)):
                check_data.check_batches({}, errors, warnings)
            return errors, warnings

    def test_known_base_passes(self):
        self.assertEqual(self.run_check([{"id": "a"}, {"id": "b", "variant_of": "a"}]), ([], []))

    def test_unknown_base_and_self_are_errors(self):
        e, _ = self.run_check([{"id": "a", "variant_of": "zzz"}])
        self.assertEqual(len(e), 1)
        e, _ = self.run_check([{"id": "a", "variant_of": "a"}])
        self.assertIn("names itself", e[0])

    def test_mutual_variants_warn_once(self):
        _, w = self.run_check([{"id": "a", "variant_of": "b"}, {"id": "b", "variant_of": "a"}])
        self.assertEqual(len(w), 1)

    def test_variant_pair_passes_the_boundary_check(self):
        recs = [{"id": "a", "where": "x", "verifier": "retailer", "verifier_question": "attestation", "related": []},
                {"id": "b", "where": "y", "verifier": "retailer", "verifier_question": "attestation", "related": ["a"]}]
        _, w, _ = check_data.boundary_findings(recs, check_data.verifier_questions())
        self.assertEqual(w, [])

    def test_form_has_the_field_after_downstream(self):
        ids = [f["id"] for f in form.FIELDS]
        self.assertEqual(ids.index("variant_of"), ids.index("downstream_use_cases") + 1)

    def test_batch_column_renders_parses_and_links(self):
        b = batch()
        base = b["candidates"][1]["id"]
        c = dict(b["candidates"][0], variant_of=[base])
        body = intake.issue(c, b, [], numbers={base: 42})["body"]
        self.assertEqual(form.parse(body)["variant_of"], f"- `{base}` (#42)")
        links = issue_links.comment(body, {base: 42})
        self.assertIn("**Variant of**", links)


if __name__ == "__main__":
    unittest.main()
