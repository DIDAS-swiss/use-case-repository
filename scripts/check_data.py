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


def external_sources():
    """Prefixes of the source lists whose references may appear in the repository."""
    path = ROOT / "_data" / "external-sources.csv"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8", newline="") as f:
        return {r["prefix"]: r for r in csv.DictReader(f)}


EXTERNAL_REF = re.compile(r"^([A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9.]+)+)(?: \(([^()]+)\))?$")


def external_ref_findings(where, value, sources):
    """external_refs: '<reference>' or '<reference> (<status at the source>)', separated by ';'.
    Only references of listed sources (they agreed to be named) are allowed.
    Returns (errors, warnings)."""
    errors, warnings, seen = [], [], set()
    for item in [x.strip() for x in str(value or "").split(";") if x.strip()]:
        m = EXTERNAL_REF.match(item)
        if not m:
            errors.append(f"{where}: external_refs item {item!r} must be '<reference>' or '<reference> (<status>)'")
            continue
        ref = m.group(1)
        if not any(ref.startswith(p + "-") for p in sources):
            errors.append(f"{where}: external_refs {ref!r} is not from a listed source "
                          f"(_data/external-sources.csv); unlisted sources stay outside the repository")
        if ref in seen:
            warnings.append(f"{where}: external_refs names {ref!r} twice")
        seen.add(ref)
    return errors, warnings


def check_batches(use_cases, errors, warnings):
    """Relations, values and external references in the CSV batch files of intake/.
    Relations may name a use case in any batch file, staged ones (_*.csv) included."""
    rows = []
    for path in sorted((ROOT / "intake").glob("*.csv")):
        with open(path, encoding="utf-8-sig", newline="") as f:
            rows += [(path.relative_to(ROOT), n, r) for n, r in enumerate(csv.DictReader(f), start=2)]
    first = {}
    for where, n, r in rows:
        rid = r.get("id")
        if rid and rid in first and first[rid] != where:
            errors.append(f"{where} line {n}: id {rid!r} is already used in {first[rid]}")
        elif rid:
            first.setdefault(rid, where)
    ids = set(first) | set(use_cases)
    sources = external_sources()
    rel, place = {}, {}
    for where, n, r in rows:
        at = f"{where} line {n}"
        if (r.get("lighthouse") or "").strip().lower() not in LIGHTHOUSE_VALUES:
            errors.append(f"{at}: lighthouse must be selected (or yes), candidate or empty")
        if (r.get("evidence_status") or "").strip().lower() not in EVIDENCE:
            errors.append(f"{at}: evidence_status must be one of {', '.join(EVIDENCE[1:])} or empty")
        if (r.get("benefit_basis") or "").strip().lower() not in BENEFIT_BASIS:
            errors.append(f"{at}: benefit_basis must be hypothesis, reported, measured or empty")
        for d in [x.strip() for x in re.split(r"[;,]", r.get("dependencies") or "") if x.strip()]:
            if d not in DEPENDENCIES:
                errors.append(f"{at}: unknown dependency {d!r} (see dependencies.md)")
        words = len((r.get("summary") or "").split())
        if words > 90:
            warnings.append(f"{at}: summary of {r.get('id')} has {words} words (aim for 40-70)")
        e, w = external_ref_findings(at, r.get("external_refs"), sources)
        errors += e
        warnings += w
        for field in ("related_use_cases", "upstream_use_cases", "downstream_use_cases"):
            vals = [x.strip() for x in re.split(r"[;,]", r.get(field) or "") if x.strip()]
            for v in vals:
                if v not in ids:
                    errors.append(f"{at}: {field} names unknown use case {v!r}")
            if field != "related_use_cases":
                rel[(r.get("id"), field)] = vals
                place[r.get("id")] = where
    for (rid, field), vals in rel.items():
        other = "upstream_use_cases" if field == "downstream_use_cases" else "downstream_use_cases"
        for v in vals:
            if (v, other) in rel and rid not in rel[(v, other)]:
                warnings.append(f"{place[rid]}: {rid} names {v} in {field}, but {v} does not name {rid} in {other}")


STAGES = ("signal", "candidate", "qualified", "active", "maintained", "deprecated")


def verifier_questions():
    path = ROOT / "_data" / "verifier-questions.csv"
    with open(path, encoding="utf-8", newline="") as f:
        return {r["id"] for r in csv.DictReader(f)}


def boundary_findings(records, questions):
    """Use-case boundaries: same verifier role and same verifier question = one use case.
    records: dicts with id, where, verifier, verifier_question, related (list), stage.
    Returns (errors, warnings, notes)."""
    errors, warnings, notes = [], [], []
    seen = {}
    for r in records:
        q = (r.get("verifier_question") or "").strip()
        v = (r.get("verifier") or "").strip().lower()
        if q and q not in questions:
            errors.append(f"{r['where']}: verifier_question {q!r} must be one of {', '.join(sorted(questions))}")
        stage = (r.get("stage") or "signal").strip()
        if stage in STAGES and STAGES.index(stage) >= 1 and stage != "deprecated" and not (v and q):
            notes.append(f"{r['where']}: {r['id']} is at stage {stage} but lacks verifier or verifier_question")
        if v and q in questions:
            seen.setdefault((v, q), []).append(r)
    related = {r["id"]: set(r.get("related") or []) for r in records}
    for (v, q), group in seen.items():
        for i, a in enumerate(group):
            for b in group[i + 1:]:
                if a["id"] == b["id"] or b["id"] in related.get(a["id"], ()) or a["id"] in related.get(b["id"], ()):
                    continue
                warnings.append(f"`{a['id']}` and `{b['id']}` have the same verifier and verifier question: "
                                f"one use case or a documented variant?")
    return errors, warnings, notes


def boundary_records(use_cases):
    """Verifier fields of the published entries and of the batch candidates."""
    out = []
    for cid, (where, fm) in use_cases.items():
        out.append({"id": cid, "where": str(where), "verifier": fm.get("verifier"),
                    "verifier_question": fm.get("verifier_question"), "related": fm.get("related_use_cases") or [],
                    "stage": fm.get("stage")})
    for path in sorted((ROOT / "intake").glob("*.csv")):
        with open(path, encoding="utf-8-sig", newline="") as f:
            for n, r in enumerate(csv.DictReader(f), start=2):
                if r.get("id") and r["id"] not in use_cases:
                    out.append({"id": r["id"], "where": f"{path.relative_to(ROOT)} line {n}",
                                "verifier": r.get("verifier"), "verifier_question": r.get("verifier_question"),
                                "related": [x.strip() for x in re.split(r"[;,]", r.get("related_use_cases") or "") if x.strip()],
                                "stage": r.get("stage")})
    return out


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
    e, w, n = boundary_findings(boundary_records(use_cases), verifier_questions())
    errors += e
    warnings += w
    notes += n
    for cid, (where, fm) in use_cases.items():
        if str(fm.get("evidence_status") or "") not in EVIDENCE:
            errors.append(f"{where}: evidence_status must be one of {', '.join(EVIDENCE[1:])} or empty")
        e, w = external_ref_findings(str(where), "; ".join(map(str, fm.get("external_refs") or [])), external_sources())
        errors += e
        warnings += w
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
