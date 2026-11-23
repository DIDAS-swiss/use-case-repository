"""Tests for the use-case boundary check in scripts/check_data.py (no repository data is changed).

Run from the repository root:  python3 -m unittest discover -s tests -v
"""

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_data   # noqa: E402

Q = check_data.verifier_questions()


def rec(uid, verifier="", question="", related=(), stage="signal"):
    return {"id": uid, "where": f"test {uid}", "verifier": verifier, "verifier_question": question,
            "related": list(related), "stage": stage}


class Boundaries(unittest.TestCase):
    def test_the_five_questions_are_known(self):
        self.assertEqual(Q, {"identity", "qualification", "attestation", "permission", "membership"})

    def test_unknown_question_is_an_error(self):
        errors, _, _ = check_data.boundary_findings([rec("a", "retailer", "maybe")], Q)
        self.assertEqual(len(errors), 1)
        self.assertIn("verifier_question", errors[0])

    def test_same_verifier_and_question_warns(self):
        _, warnings, _ = check_data.boundary_findings(
            [rec("a", "Retailer ", "attestation"), rec("b", "retailer", "attestation")], Q)
        self.assertEqual(warnings, ["`a` and `b` have the same verifier and verifier question: "
                                    "one use case or a documented variant?"])

    def test_documented_variant_does_not_warn(self):
        _, warnings, _ = check_data.boundary_findings(
            [rec("a", "retailer", "attestation"), rec("b", "retailer", "attestation", related=["a"])], Q)
        self.assertEqual(warnings, [])

    def test_different_question_does_not_warn(self):
        _, warnings, _ = check_data.boundary_findings(
            [rec("a", "retailer", "attestation"), rec("b", "retailer", "identity")], Q)
        self.assertEqual(warnings, [])

    def test_candidate_without_fields_gets_a_note_signal_does_not(self):
        _, _, notes = check_data.boundary_findings(
            [rec("a", stage="candidate"), rec("b", stage="signal"), rec("c", "retailer", stage="qualified")], Q)
        self.assertEqual(len(notes), 2)
        self.assertTrue(any("a is at stage candidate" in n for n in notes))
        self.assertTrue(any("c is at stage qualified" in n for n in notes))

    def test_repository_data_passes(self):
        errors, _, _ = check_data.boundary_findings(check_data.boundary_records(check_data.entries("use-cases")), Q)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
