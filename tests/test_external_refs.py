"""Tests for external_refs and for relations across batch files (scripts/check_data.py, scripts/intake.py).

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
import use_case_form as form  # noqa: E402

SOURCES = check_data.external_sources()


class ExternalRefs(unittest.TestCase):
    def test_listed_sources_with_and_without_status_pass(self):
        e, w = check_data.external_ref_findings("t", "BJ-v41-001 (LAUNCH); FB-EID-E21-044; FB-EID-X1-01.04; BJ-v41-053 (PLANNED 2029)", SOURCES)
        self.assertEqual((e, w), ([], []))

    def test_unlisted_source_is_an_error(self):
        for ref in ("bank-list-K01", "fin-wg-2025-S01"):
            e, _ = check_data.external_ref_findings("t", ref, SOURCES)
            self.assertEqual(len(e), 1, ref)
            self.assertIn("not from a listed source", e[0])

    def test_malformed_item_is_an_error(self):
        e, _ = check_data.external_ref_findings("t", "BJ v41 001", SOURCES)
        self.assertIn("must be", e[0])

    def test_reference_twice_warns(self):
        _, w = check_data.external_ref_findings("t", "BJ-v41-001; BJ-v41-001 (LAUNCH)", SOURCES)
        self.assertEqual(len(w), 1)

    def test_batch_column_renders_one_per_line_and_parses(self):
        path = next(p for p in intake.batch_files() if p.suffix == ".csv")
        b = intake.load_batch(path)
        c = dict(b["candidates"][0], external_refs="BJ-v41-001 (LAUNCH); FB-EID-E21-044")
        f = form.parse(intake.issue(c, b, [])["body"])
        self.assertEqual(f["external_refs"].split("\n"), ["BJ-v41-001 (LAUNCH)", "FB-EID-E21-044"])


def write(path, rows):
    cols = ["id", "title", "related_use_cases", "upstream_use_cases", "downstream_use_cases"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


class CrossFileRelations(unittest.TestCase):
    def run_check(self, files):
        with tempfile.TemporaryDirectory() as tmp:
            (pathlib.Path(tmp) / "intake").mkdir()
            for name, rows in files.items():
                write(pathlib.Path(tmp) / "intake" / name, rows)
            errors, warnings = [], []
            with mock.patch.object(check_data, "ROOT", pathlib.Path(tmp)):
                check_data.check_batches({}, errors, warnings)
            return errors, warnings

    def test_staged_file_may_name_a_use_case_of_another_file(self):
        e, _ = self.run_check({"main.csv": [{"id": "a", "title": "A"}],
                               "_staged.csv": [{"id": "b", "title": "B", "related_use_cases": "a"}]})
        self.assertEqual(e, [])

    def test_unknown_id_is_still_an_error(self):
        e, _ = self.run_check({"main.csv": [{"id": "a", "title": "A", "related_use_cases": "zzz"}]})
        self.assertEqual(len(e), 1)

    def test_same_id_in_two_files_is_an_error(self):
        e, _ = self.run_check({"main.csv": [{"id": "a", "title": "A"}], "_staged.csv": [{"id": "a", "title": "A2"}]})
        self.assertTrue(any("already used" in x for x in e))

    def test_one_sided_relation_across_files_warns(self):
        _, w = self.run_check({"main.csv": [{"id": "a", "title": "A"}],
                               "_staged.csv": [{"id": "b", "title": "B", "upstream_use_cases": "a"}]})
        self.assertEqual(w, ["intake/_staged.csv: b names a in upstream_use_cases, "
                             "but a does not name b in downstream_use_cases"])
        _, w = self.run_check({"main.csv": [{"id": "a", "title": "A", "downstream_use_cases": "b"}],
                               "_staged.csv": [{"id": "b", "title": "B", "upstream_use_cases": "a"}]})
        self.assertEqual(w, [])

if __name__ == "__main__":
    unittest.main()
