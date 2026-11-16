"""Tests for claims referenced by id (scripts/check_data.py, scripts/draft_entry.py).

Run from the repository root:  python3 -m unittest discover -s tests -v
"""

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_data    # noqa: E402
import draft_entry   # noqa: E402

CREDS = {"beta-id": ("credentials/beta-id.md", {"claims": ["age_over_18", "birth_date"]}),
         "learner-permit-elfa": ("credentials/learner-permit-elfa.md", {"claims": ["categoryCode", "dateOfBirth"]})}


def uc(uid, claims, reused=("beta-id",), verifier="retailer", question="attestation"):
    return uid, (f"use-cases/{uid}.md", {"credentials_reused": list(reused), "claims_needed": list(claims),
                                         "verifier": verifier, "verifier_question": question})


class Claims(unittest.TestCase):
    def test_claim_of_a_credential_not_relied_on_is_an_error(self):
        e, _, _ = check_data.claim_findings(dict([uc("a", ["learner-permit-elfa#categoryCode"])]), CREDS)
        self.assertEqual(len(e), 1)
        self.assertIn("not in credentials_reused or credentials_new", e[0])

    def test_malformed_item_is_an_error(self):
        e, _, _ = check_data.claim_findings(dict([uc("a", ["age_over_18"])]), CREDS)
        self.assertIn("<credential-id>#<claim-id>", e[0])

    def test_unknown_claim_id_warns(self):
        _, w, _ = check_data.claim_findings(dict([uc("a", ["beta-id#age_over_21"])]), CREDS)
        self.assertEqual(len(w), 1)
        self.assertIn("age_over_21", w[0])

    def test_same_verifier_question_and_claims_is_probably_one_use_case(self):
        a, b = uc("a", ["beta-id#age_over_18"]), uc("b", ["beta-id#age_over_18"])
        _, w, _ = check_data.claim_findings(dict([a, b]), CREDS)
        self.assertEqual(w, ["`a` and `b` have the same verifier, verifier question and claims needed: probably one use case"])

    def test_combination_across_credentials_and_different_sets(self):
        a = uc("a", ["beta-id#age_over_18", "learner-permit-elfa#categoryCode"], reused=("beta-id", "learner-permit-elfa"))
        b = uc("b", ["beta-id#age_over_18"])
        e, w, _ = check_data.claim_findings(dict([a, b]), CREDS)
        self.assertEqual((e, w), ([], []))

    def test_unused_claims_are_noted(self):
        _, _, n = check_data.claim_findings(dict([uc("a", ["beta-id#age_over_18"])]), CREDS)
        self.assertTrue(any("beta-id.md: 1 of 2 claims" in x for x in n))
        self.assertTrue(any("learner-permit-elfa.md: 2 of 2 claims" in x for x in n))

    def test_repository_credentials_list_their_table_ids(self):
        errors = []
        check_data.credential_claim_tables(check_data.entries("credentials"), errors)
        self.assertEqual(errors, [])

    def test_draft_table_is_generated_from_claims_needed(self):
        table = draft_entry.credentials_table(["beta-id"], ["learner-permit-elfa"], [],
                                              ["beta-id#age_over_18", "beta-id#birth_date"])
        self.assertIn("| reused | `age_over_18`, `birth_date` |", table)
        self.assertIn("| new | to be defined |", table)


if __name__ == "__main__":
    unittest.main()
