#!/usr/bin/env python3
"""Take a snapshot of the swiyu Trust Registry and base registry as evidence for the entries.

The swiyu Trust Registry publishes signed trust statements (Swiss Profile Trust
1.0, read endpoints of Trust Protocol 2.0) without authentication, in two
environments with the same paths:

  production  https://trust-reg.trust-infra.swiyu.admin.ch
  sandbox     https://trust-reg.trust-infra.swiyu-int.admin.ch

This script counts, per environment, the identity trust statements, the
verification query public statements (vqPS), the distinct verifiers behind
them and the protected verification authorizations, and writes them to
_data/swiyu-registry-totals.csv. For every credential in credentials/ that names
its credential types (`vct_values`), it counts the vqPS that ask for one of
those types and the distinct verifiers that publish them, and whether a type is
on the protected issuance trust list; one row per credential and environment in
_data/swiyu-registry.csv.

The organisations with an identity trust statement go to
_data/swiyu-organisations.csv, with the name and UID as the registry publishes
them, the number of their verification query statements and the credentials of
this repository those ask for. Production lists every identity; the sandbox
only those with a UID or marked as state actor, because it holds test accounts
named after persons. Names in _data/swiyu-unlisted.csv are never listed, so a
curator can keep a person's name out. The others are counted
(`unlisted_identities`).

For every identity, the script also resolves its DID in the base registry
(identifier registry, did:webvh): https://<host>/api/v1/did/<uuid>/did.jsonl.
A DID counts as active when its log resolves and its last entry is not
deactivated (`active_dids` per organisation, `active_identity_dids` in total).

Not kept: DIDs, and credential types that no entry names. The registry stays
the authoritative source. A change reaches the repository as a pull request
from the federation-sync workflow.

If an environment cannot be read, its earlier rows are kept and a warning is
printed; the script does not fail, because Trust Protocol 2.0 is a draft and
its endpoints may change.

Run from the repository root:  python3 scripts/swiyu_sync.py
Needs PyYAML.
"""

import base64
import csv
import json
import pathlib
import sys
import time
import urllib.request

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENVIRONMENTS = {
    "production": "https://trust-reg.trust-infra.swiyu.admin.ch/api/v2",
    "sandbox": "https://trust-reg.trust-infra.swiyu-int.admin.ch/api/v2",
}
TOTALS = ROOT / "_data" / "swiyu-registry-totals.csv"
BY_CREDENTIAL = ROOT / "_data" / "swiyu-registry.csv"
ORGANISATIONS = ROOT / "_data" / "swiyu-organisations.csv"
TOTAL_FIELDS = ["environment", "identity_trust_statements", "verification_query_statements",
                "verifiers", "protected_verification_authorizations", "active_identity_dids",
                "unlisted_identities"]
UNLISTED = ROOT / "_data" / "swiyu-unlisted.csv"
ORGANISATION_FIELDS = ["environment", "organisation", "uid", "state_actor", "dids", "active_dids",
                       "verification_query_statements", "credentials"]
CREDENTIAL_FIELDS = ["credential", "environment", "verification_query_statements", "verifiers",
                     "protected_issuance_trust_list"]
MAX_PAGES = 1000


def get(url, attempts=4):
    """JSON from the registry, retried with a growing pause when the connection drops."""
    req = urllib.request.Request(url, headers={"User-Agent": "didas-use-case-repository swiyu-sync"})
    for n in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read())
        except (OSError, ValueError):
            if n == attempts - 1:
                raise
            time.sleep(2 ** n)


def payload(jwt):
    """The claims of a signed statement (the JWT's middle part). The signature is not checked:
    the counts are evidence for curators, not a trust decision."""
    part = jwt.split(".")[1]
    return json.loads(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)))


def statements(base, kind, fetch=get):
    """Every statement of one kind. Pages are read until one comes back empty: the
    server caps the page size and computes totalPages from the size asked for, so
    totalPages cannot be trusted."""
    out = []
    for page in range(MAX_PAGES):
        content = fetch(f"{base}/{kind}/?page={page}").get("content") or []
        if not content:
            return out
        out += [payload(c) for c in content]
    raise RuntimeError(f"{kind}: more than {MAX_PAGES} pages")


def queried_types(vqps):
    """The credential types a verification query public statement asks for."""
    out = set()
    for cred in ((vqps.get("request") or {}).get("query") or {}).get("credentials") or []:
        out |= set((cred.get("meta") or {}).get("vct_values") or [])
    return out


def credential_types():
    """{credential id: set of vct values} from the front matter of credentials/*.md."""
    out = {}
    for path in sorted((ROOT / "credentials").glob("*.md")):
        if path.name.startswith(("_", "README")):
            continue
        fm = yaml.safe_load(path.read_text(encoding="utf-8").split("---")[1]) or {}
        if fm.get("vct_values"):
            out[path.stem] = {str(v) for v in fm["vct_values"]}
    return out


def name(statement):
    """The entity name of an identity trust statement; a localised name in German, else any."""
    if statement.get("entity_name"):
        return str(statement["entity_name"]).strip()
    names = {k.split("#", 1)[1]: v for k, v in statement.items() if k.startswith("entity_name#")}
    return str(names.get("de-CH") or names.get("de") or next(iter(names.values()), "")).strip()


def uid(statement):
    return next((str(r.get("value")) for r in statement.get("registry_ids") or [] if r.get("type") == "UID"), "")


def did_log_url(did):
    """did:webvh:<scid>:<host>:<path…> -> https://<host>/<path…>/did.jsonl (did:webvh 1.0)."""
    parts = (did or "").split(":")
    if len(parts) < 4 or parts[:2] != ["did", "webvh"]:
        return None
    return "https://" + "/".join([parts[3].replace("%3A", ":")] + parts[4:]) + "/did.jsonl"


def did_active(did, fetch_text=None):
    """True when the DID log resolves in the base registry and its last entry is not deactivated."""
    url = did_log_url(did)
    if not url:
        return False
    try:
        if fetch_text:
            text = fetch_text(url)
        else:
            req = urllib.request.Request(url, headers={"User-Agent": "didas-use-case-repository swiyu-sync"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                text = resp.read().decode("utf-8")
        lines = [ln for ln in text.splitlines() if ln.strip()]
        return bool(lines) and not (json.loads(lines[-1]).get("parameters") or {}).get("deactivated")
    except Exception:
        return False


def unlisted_names():
    """{(environment, name)} that a curator keeps off the list."""
    return {(r["environment"], r["organisation"]) for r in read(UNLISTED)}


def organisations(env, identity, vqps, types, active, hidden=frozenset()):
    """(rows, number of identities left out): one row per organisation (name and UID), over all its DIDs.
    `active` is the set of DIDs that resolve as active in the base registry."""
    by_sub = {}
    for s in vqps:
        by_sub.setdefault(s.get("sub"), []).append(s)
    orgs, unlisted = {}, set()
    for s in identity:
        if (env, name(s)) in hidden or not (env == "production" or uid(s) or s.get("is_state_actor")):
            unlisted.add(s.get("sub"))
            continue
        key = (name(s), uid(s))
        o = orgs.setdefault(key, {"subs": set(), "state": False})
        o["subs"].add(s.get("sub"))
        o["state"] = o["state"] or bool(s.get("is_state_actor"))
    rows = []
    for (org, u), o in orgs.items():
        asked = [q for sub in o["subs"] for q in by_sub.get(sub, [])]
        creds = sorted(c for c, vcts in types.items() if any(queried_types(q) & vcts for q in asked))
        rows.append({"environment": env, "organisation": org, "uid": u, "state_actor": "yes" if o["state"] else "no",
                     "dids": len(o["subs"]), "active_dids": len(o["subs"] & active),
                     "verification_query_statements": len(asked), "credentials": "; ".join(creds)})
    return sorted(rows, key=lambda r: r["organisation"].lower()), len(unlisted)


def snapshot(env, base, types, fetch=get, resolve=did_active, hidden=frozenset()):
    """(totals row, [credential rows], [organisation rows]) for one environment."""
    identity = statements(base, "identity-trust-statement", fetch)
    vqps = statements(base, "verification-query-public-statement", fetch)
    pva = statements(base, "protected-verification-authorization-trust-statement", fetch)
    trust_list = set()
    for s in statements(base, "protected-issuance-trust-list-statement", fetch):
        trust_list |= set(s.get("vct_values") or [])
    totals = {"environment": env, "identity_trust_statements": len(identity),
              "verification_query_statements": len(vqps),
              "verifiers": len({s.get("sub") for s in vqps}),
              "protected_verification_authorizations": len(pva)}
    active = {d for d in {s.get("sub") for s in identity} if resolve(d)}
    totals["active_identity_dids"] = len(active)
    orgs, totals["unlisted_identities"] = organisations(env, identity, vqps, types, active, hidden)
    rows = []
    for cred, vcts in sorted(types.items()):
        asking = [s for s in vqps if queried_types(s) & vcts]
        rows.append({"credential": cred, "environment": env, "verification_query_statements": len(asking),
                     "verifiers": len({s.get("sub") for s in asking}),
                     "protected_issuance_trust_list": "yes" if trust_list & vcts else "no"})
    return totals, rows, orgs


def read(path):
    if not path.exists():
        return []
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write(path, fields, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    types = credential_types()
    old_totals, old_rows, old_orgs = read(TOTALS), read(BY_CREDENTIAL), read(ORGANISATIONS)
    totals, rows, orgs = [], [], []
    hidden = unlisted_names()
    for env, base in ENVIRONMENTS.items():
        try:
            t, r, o = snapshot(env, base, types, hidden=hidden)
        except Exception as e:  # keep the earlier snapshot of this environment
            print(f"::warning::swiyu {env}: could not read the Trust Registry ({e}); earlier rows kept")
            totals += [x for x in old_totals if x["environment"] == env]
            rows += [x for x in old_rows if x["environment"] == env and x["credential"] in types]
            orgs += [x for x in old_orgs if x["environment"] == env]
            continue
        totals.append(t)
        rows += r
        orgs += o
        print(f"swiyu {env}: {t['identity_trust_statements']} identity, {t['verification_query_statements']} "
              f"verification query statements from {t['verifiers']} verifier(s)")
    write(TOTALS, TOTAL_FIELDS, totals)
    write(BY_CREDENTIAL, CREDENTIAL_FIELDS, sorted(rows, key=lambda x: (x["credential"], x["environment"])))
    write(ORGANISATIONS, ORGANISATION_FIELDS, orgs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
