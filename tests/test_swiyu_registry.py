"""Tests for the swiyu registry snapshot (scripts/swiyu_sync.py) and its check (scripts/check_data.py).

No network: the registry is replaced by fixed pages.
Run from the repository root:  python3 -m unittest discover -s tests -v
"""

import base64
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_data   # noqa: E402
import swiyu_sync   # noqa: E402


def jwt(claims):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    return f"{enc({'alg': 'ES256'})}.{enc(claims)}.sig"


def query(sub, *vcts):
    return {"sub": sub, "request": {"type": "DCQL", "query": {"credentials": [{"meta": {"vct_values": list(vcts)}}]}}}


IDENTITY = [
    {"sub": "did:webvh:Q1:reg.example:api:v1:did:a", "entity_name": "Road Office", "registry_ids": [], "is_state_actor": False},
    {"sub": "did:webvh:Q2:reg.example:api:v1:did:b", "entity_name": "Example AG",
     "registry_ids": [{"type": "UID", "value": "CHE-000.000.001"}], "is_state_actor": False},
    {"sub": "did:webvh:Q3:reg.example:api:v1:did:c", "entity_name": "Jane Tester", "registry_ids": [], "is_state_actor": False},
]
QUERIES = [query("did:webvh:Q1:reg.example:api:v1:did:a", "urn:vct:x.permit")] * 3 + [
    query("did:webvh:Q2:reg.example:api:v1:did:b", "urn:vct:x.permit", "other")]
TRUST_LIST = [{"vct_values": ["urn:vct:x.eid"]}]


def pages(kind_items, size=2):
    """A fetch that serves each kind in pages of `size` and reports a misleading totalPages."""
    def fetch(url):
        kind = url.split("/api/v2/")[1].split("/")[0]
        page = int(url.split("page=")[1])
        items = kind_items.get(kind, [])
        return {"content": [jwt(c) for c in items[page * size:(page + 1) * size]], "page": {"totalPages": 1}}
    return fetch


FETCH = pages({"identity-trust-statement": IDENTITY, "verification-query-public-statement": QUERIES,
               "protected-issuance-trust-list-statement": TRUST_LIST})
TYPES = {"permit": {"urn:vct:x.permit"}, "eid": {"urn:vct:x.eid"}}


class Snapshot(unittest.TestCase):
    def snap(self, env):
        return swiyu_sync.snapshot(env, "https://reg/api/v2", TYPES, FETCH,
                                   resolve=lambda did: did.endswith(":a"))

    def test_reads_all_pages_whatever_total_pages_says(self):
        totals, _, _ = self.snap("production")
        self.assertEqual(totals["identity_trust_statements"], 3)
        self.assertEqual(totals["verification_query_statements"], 4)
        self.assertEqual(totals["verifiers"], 2)

    def test_counts_per_credential_and_trust_list(self):
        _, rows, _ = self.snap("production")
        by = {r["credential"]: r for r in rows}
        self.assertEqual((by["permit"]["verification_query_statements"], by["permit"]["verifiers"]), (4, 2))
        self.assertEqual(by["eid"]["protected_issuance_trust_list"], "yes")
        self.assertEqual(by["permit"]["protected_issuance_trust_list"], "no")

    def test_production_lists_all_identities(self):
        totals, _, orgs = self.snap("production")
        self.assertEqual({o["organisation"] for o in orgs}, {"Road Office", "Example AG", "Jane Tester"})
        road = next(o for o in orgs if o["organisation"] == "Road Office")
        self.assertEqual((road["dids"], road["active_dids"], road["credentials"]), (1, 1, "permit"))
        self.assertEqual(totals["active_identity_dids"], 1)

    def test_sandbox_lists_only_uid_or_state_actor(self):
        totals, _, orgs = self.snap("sandbox")
        self.assertEqual([o["organisation"] for o in orgs], ["Example AG"])
        self.assertEqual(totals["unlisted_identities"], 2)

    def test_curator_can_keep_a_name_off(self):
        _, _, orgs = swiyu_sync.snapshot("production", "https://reg/api/v2", TYPES, FETCH, resolve=lambda d: True,
                                         hidden={("production", "Jane Tester")})
        self.assertNotIn("Jane Tester", {o["organisation"] for o in orgs})

    def test_no_dids_in_the_output(self):
        totals, rows, orgs = self.snap("production")
        self.assertNotIn("did:", json.dumps([totals, rows, orgs]))

    def test_did_log_url(self):
        self.assertEqual(swiyu_sync.did_log_url(
            "did:webvh:Qm1:identifier-reg.trust-infra.swiyu.admin.ch:api:v1:did:dd0d"),
            "https://identifier-reg.trust-infra.swiyu.admin.ch/api/v1/did/dd0d/did.jsonl")
        self.assertIsNone(swiyu_sync.did_log_url("did:web:example.org"))

    def test_deactivated_did_is_not_active(self):
        log = '{"parameters": {"method": "did:webvh:1.0"}}\n{"parameters": {"deactivated": true}}\n'
        self.assertFalse(swiyu_sync.did_active("did:webvh:Q:h:did:x", fetch_text=lambda u: log))
        self.assertTrue(swiyu_sync.did_active("did:webvh:Q:h:did:x", fetch_text=lambda u: log.split("\n")[0]))


class Check(unittest.TestCase):
    def creds(self, supply, vcts=("urn:vct:x.permit",)):
        return {"permit": ("credentials/permit.md", {"supply": supply, "vct_values": list(vcts)})}

    def rows(self, prod_queries, trust="no", sandbox=0):
        return {("permit", "production"): {"verification_query_statements": str(prod_queries), "protected_issuance_trust_list": trust},
                ("permit", "sandbox"): {"verification_query_statements": str(sandbox), "protected_issuance_trust_list": "no"}}

    def test_available_without_production_evidence_warns(self):
        _, w, _ = check_data.registry_findings(self.creds("available"), self.rows(0, sandbox=5))
        self.assertEqual(len(w), 1)
        self.assertIn("sandbox: 5", w[0])

    def test_available_with_queries_or_trust_list_passes(self):
        self.assertEqual(check_data.registry_findings(self.creds("available"), self.rows(3))[1], [])
        self.assertEqual(check_data.registry_findings(self.creds("available"), self.rows(0, trust="yes"))[1], [])

    def test_missing_with_production_evidence_warns(self):
        self.assertEqual(len(check_data.registry_findings(self.creds("missing"), self.rows(2))[1]), 1)

    def test_bad_vct_values_is_an_error_and_absent_row_a_note(self):
        e, _, _ = check_data.registry_findings({"p": ("x.md", {"vct_values": "urn:vct:x"})}, {})
        self.assertEqual(len(e), 1)
        _, _, n = check_data.registry_findings(self.creds("available"), {})
        self.assertEqual(len(n), 1)


if __name__ == "__main__":
    unittest.main()
