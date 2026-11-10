#!/usr/bin/env python3
"""Check that the repository's data holds together.

  - the working-group assignment (_data/working-group-sectors.csv) follows the
    rules in scripts/working_groups.py
  - every use case and credential refers only to things that exist: sectors,
    trust flows, Industry Function Graph patterns, credentials, use cases, I14Y
    datasets, working groups
  - the batch files and editorial reviews in intake/ use known values and ids
  - the published-entry list (use-cases/README.md) agrees with use-cases/

Errors fail the check; notes are printed for information. Runs in CI on every
pull request that touches data or entries.

Run from the repository root:  python3 scripts/check_data.py
Needs PyYAML.
"""

import csv
import pathlib
import re
import sys

import yaml

import working_groups as wg

ROOT = pathlib.Path(__file__).resolve().parent.parent


def ids(name, key="id"):
    path = ROOT / "_data" / name
    with open(path, encoding="utf-8", newline="") as f:
        return {r[key] for r in csv.DictReader(f)}


def entries(folder):
    out = {}
    for path in sorted((ROOT / folder).glob("*.md")):
        if path.name.startswith(("_", "README")):
            continue
        fm = yaml.safe_load(path.read_text(encoding="utf-8").split("---")[1]) or {}
        out[path.stem] = (path.relative_to(ROOT), fm)
    return out


EVIDENCE = ("", "hypothesis", "documented need", "design", "prototype", "pilot", "production")
BENEFIT_BASIS = ("", "hypothesis", "reported", "measured")
DEPENDENCIES = ("e-id", "trust-infrastructure")
DISPOSITIONS = ("Retain", "Revise", "Split", "Merge", "Park")
LIGHTHOUSE_VALUES = ("", "yes", "y", "ja", "x", "true", "1", "selected", "lighthouse", "candidate", "kandidat")


def check_batches(use_cases, errors, warnings):
    """Relations and lighthouse values in the CSV batch files of intake/."""
    for path in sorted((ROOT / "intake").glob("*.csv")):
        where = path.relative_to(ROOT)
        with open(path, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        ids = {r.get("id") for r in rows if r.get("id")} | set(use_cases)
        rel = {}
        for n, r in enumerate(rows, start=2):
            if (r.get("lighthouse") or "").strip().lower() not in LIGHTHOUSE_VALUES:
                errors.append(f"{where} line {n}: lighthouse must be selected (or yes), candidate or empty")
            if (r.get("evidence_status") or "").strip().lower() not in EVIDENCE:
                errors.append(f"{where} line {n}: evidence_status must be one of {', '.join(EVIDENCE[1:])} or empty")
            if (r.get("benefit_basis") or "").strip().lower() not in BENEFIT_BASIS:
                errors.append(f"{where} line {n}: benefit_basis must be hypothesis, reported, measured or empty")
            for d in [x.strip() for x in re.split(r"[;,]", r.get("dependencies") or "") if x.strip()]:
                if d not in DEPENDENCIES:
                    errors.append(f"{where} line {n}: unknown dependency {d!r} (see dependencies.md)")
            words = len((r.get("summary") or "").split())
            if words > 90:
                warnings.append(f"{where} line {n}: summary of {r.get('id')} has {words} words (aim for 40-70)")
            for field in ("related_use_cases",):
                for v in [x.strip() for x in re.split(r"[;,]", r.get(field) or "") if x.strip()]:
                    if v not in ids:
                        errors.append(f"{where} line {n}: {field} names unknown use case {v!r}")
            for field in ("upstream_use_cases", "downstream_use_cases"):
                vals = [x.strip() for x in re.split(r"[;,]", r.get(field) or "") if x.strip()]
                rel[(r.get("id"), field)] = vals
                for v in vals:
                    if v not in ids:
                        errors.append(f"{where} line {n}: {field} names unknown use case {v!r}")
        for (rid, field), vals in rel.items():
            other = "upstream_use_cases" if field == "downstream_use_cases" else "downstream_use_cases"
            for v in vals:
                if (v, other) in rel and rid not in rel[(v, other)]:
                    warnings.append(f"{where}: {rid} names {v} in {field}, but {v} does not name {rid} in {other}")


def batch_ids():
    out = set()
    for path in sorted((ROOT / "intake").glob("*.csv")):
        with open(path, encoding="utf-8-sig", newline="") as f:
            out |= {r["id"] for r in csv.DictReader(f) if r.get("id")}
    return out


def check_reviews(known, errors, warnings):
    """Editorial reviews (intake/reviews/*-review.csv) and their proposed scopes
    (*-scopes.csv): known ids, known recommendations, every split with a scope."""
    folder = ROOT / "intake" / "reviews"
    if not folder.is_dir():
        return
    reviewed = {}
    for path in sorted(folder.glob("*-review.csv")):
        where = path.relative_to(ROOT)
        with open(path, encoding="utf-8-sig", newline="") as f:
            for n, r in enumerate(csv.DictReader(f), start=2):
                if r.get("id") not in known:
                    errors.append(f"{where} line {n}: unknown use case {r.get('id')!r}")
                if r.get("disposition") not in DISPOSITIONS:
                    errors.append(f"{where} line {n}: disposition must be one of {', '.join(DISPOSITIONS)}")
                for m in [x.strip() for x in re.split(r"[;,]", r.get("merge_into") or "") if x.strip()]:
                    if m not in known:
                        errors.append(f"{where} line {n}: merge_into names unknown use case {m!r}")
                if r.get("disposition") == "Merge" and not (r.get("merge_into") or "").strip():
                    errors.append(f"{where} line {n}: a Merge recommendation needs merge_into")
                reviewed[r.get("id")] = r.get("disposition")
    scoped, scope_ids = set(), set()
    for path in sorted(folder.glob("*-scopes.csv")):
        where = path.relative_to(ROOT)
        with open(path, encoding="utf-8-sig", newline="") as f:
            for n, r in enumerate(csv.DictReader(f), start=2):
                if r.get("parent_id") not in known:
                    errors.append(f"{where} line {n}: unknown parent use case {r.get('parent_id')!r}")
                sid = r.get("scope_id") or ""
                if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", sid):
                    errors.append(f"{where} line {n}: scope_id {sid!r} must be lower-case words joined by hyphens")
                if sid in scope_ids or sid in known:
                    errors.append(f"{where} line {n}: scope_id {sid!r} is already used")
                scope_ids.add(sid)
                scoped.add(r.get("parent_id"))
    for uid, d in reviewed.items():
        if d == "Split" and uid not in scoped:
            errors.append(f"intake/reviews: {uid} is recommended for a split but has no proposed scope")


def check_published_list(use_cases, errors):
    """use-cases/README.md says which entries are published; it must agree with the files."""
    readme = (ROOT / "use-cases" / "README.md").read_text(encoding="utf-8")
    says_none = "_None yet_" in readme
    if says_none and use_cases:
        errors.append("use-cases/README.md says none is published, but use-cases/ holds " + ", ".join(sorted(use_cases)))
    for cid in use_cases:
        if f"({cid}.md)" not in readme:
            errors.append(f"use-cases/README.md does not list the published entry {cid}")


def main():
    errors, notes = wg.check()
    warnings = []
    flows, patterns = ids("trust-flows.csv"), ids("ifm-patterns.csv")
    terms = ids("glossary-terms.csv")
    datasets = ids("i14y-credentials.csv", "identifier")
    use_cases, credentials = entries("use-cases"), entries("credentials")

    def refs(where, fm, field, known, what):
        for v in fm.get(field) or []:
            if v not in known:
                errors.append(f"{where}: {field} names unknown {what} {v!r}")

    for cid, (where, fm) in use_cases.items():
        if fm.get("id") != cid:
            errors.append(f"{where}: id {fm.get('id')!r} does not match the file name")
        refs(where, fm, "sectors", wg.SECTORS, "sector")
        refs(where, fm, "trust_flows", flows, "trust flow")
        refs(where, fm, "ifm_patterns", patterns, "pattern")
        refs(where, fm, "glossary_terms", terms, "DIDAS Glossary term")
        refs(where, fm, "related_use_cases", use_cases, "use case")
        refs(where, fm, "upstream_use_cases", use_cases, "use case")
        refs(where, fm, "downstream_use_cases", use_cases, "use case")
        if fm.get("lighthouse") not in (None, "", "selected", "candidate"):
            errors.append(f"{where}: lighthouse must be selected, candidate or empty")
        for field in ("credentials_reused", "credentials_new", "credentials_excluded"):
            refs(where, fm, field, credentials, "credential")
        if fm.get("working_group") and fm["working_group"] not in wg.GROUPS:
            errors.append(f"{where}: unknown working_group {fm['working_group']!r}")
        relied = set((fm.get("credentials_reused") or []) + (fm.get("credentials_new") or []))
        for c in relied & set(credentials):
            if cid not in (credentials[c][1].get("used_by") or []):
                errors.append(f"{where}: relies on {c}, but {credentials[c][0]} does not list it in used_by")

    # The two directions of a relation should agree; a disagreement is a warning.
    for cid, (where, fm) in use_cases.items():
        for d in fm.get("downstream_use_cases") or []:
            if d in use_cases and cid not in (use_cases[d][1].get("upstream_use_cases") or []):
                warnings.append(f"{where}: names {d} downstream, but {use_cases[d][0]} does not name {cid} upstream")
        for u in fm.get("upstream_use_cases") or []:
            if u in use_cases and cid not in (use_cases[u][1].get("downstream_use_cases") or []):
                warnings.append(f"{where}: names {u} upstream, but {use_cases[u][0]} does not name {cid} downstream")

    check_batches(use_cases, errors, warnings)
    check_reviews(batch_ids() | set(use_cases), errors, warnings)
    check_published_list(use_cases, errors)
    for cid, (where, fm) in use_cases.items():
        if str(fm.get("evidence_status") or "") not in EVIDENCE:
            errors.append(f"{where}: evidence_status must be one of {', '.join(EVIDENCE[1:])} or empty")
        if fm.get("lighthouse") == "selected" and not fm.get("lighthouse_decision_record"):
            warnings.append(f"{where}: selected as lighthouse, but no lighthouse_decision_record links the decision")

    for cid, (where, fm) in credentials.items():
        if fm.get("id") != cid:
            errors.append(f"{where}: id {fm.get('id')!r} does not match the file name")
        refs(where, fm, "used_by", use_cases, "use case")
        if fm.get("supply") not in ("available", "emerging", "missing"):
            errors.append(f"{where}: supply must be available, emerging or missing")
        if fm.get("schema_status") not in ("i14y", "emerging", "none"):
            errors.append(f"{where}: schema_status must be i14y, emerging or none")
        if fm.get("schema_status") == "i14y" and fm.get("i14y_dataset") not in datasets:
            errors.append(f"{where}: schema_status i14y, but i14y_dataset {fm.get('i14y_dataset')!r} "
                          "is not in the I14Y catalogue (_data/i14y-credentials.csv)")

    for n in notes:
        print(f"note: {n}")
    for w in warnings:
        print(f"::warning::{w}")
    for e in errors:
        print(f"::error::{e}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s), {len(notes)} note(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
