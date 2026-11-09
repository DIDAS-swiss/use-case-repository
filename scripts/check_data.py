#!/usr/bin/env python3
"""Check that the repository's data holds together.

  - the working-group assignment (_data/working-group-sectors.csv) follows the
    rules in scripts/working_groups.py
  - every use case and credential refers only to things that exist: sectors,
    trust flows, Industry Function Graph patterns, credentials, use cases, I14Y
    datasets, working groups

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


def main():
    errors, notes = wg.check()
    warnings = []
    flows, patterns = ids("trust-flows.csv"), ids("ifm-patterns.csv")
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
