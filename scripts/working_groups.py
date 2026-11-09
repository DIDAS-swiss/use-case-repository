"""Which DIDAS working group is responsible for which ISIC sector.

The assignment lives in one table, _data/working-group-sectors.csv, with one row
per (group, sector). The rules that keep it manageable:

  - a sector code is assigned to at most one group
  - the most specific assignment wins: a group assigned a division takes it over
    from the group that holds its section, and a class likewise from its division
  - a sector without an assignment of its own inherits the group of the nearest
    broader sector that has one; if none has, no group is responsible

Standard library only.
"""

import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "_data"


def _rows(name):
    path = DATA / name
    if not path.exists():
        return []
    with open(path, encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f) if any((v or "").strip() for v in r.values())]


SECTORS = {r["id"]: r for r in _rows("sectors.csv")}
GROUPS = {r["id"]: r for r in _rows("working-groups.csv")}
ASSIGNMENTS = _rows("working-group-sectors.csv")
BY_SECTOR = {a["sector"]: a["group"] for a in ASSIGNMENTS}


def chain(sector_id):
    """The sector and every broader one above it, most specific first."""
    out, s = [], SECTORS.get(sector_id)
    while s:
        out.append(s["id"])
        s = SECTORS.get(s["broader"])
    return out


def responsible(sector_id):
    """(group row, sector the assignment is on) or (None, None)."""
    for s in chain(sector_id):
        if s in BY_SECTOR and BY_SECTOR[s] in GROUPS:
            return GROUPS[BY_SECTOR[s]], s
    return None, None


def check():
    """Problems with the assignment table: (errors, notes)."""
    errors, notes, seen = [], [], {}
    for n, a in enumerate(ASSIGNMENTS, start=2):
        where = f"_data/working-group-sectors.csv line {n}"
        if a["group"] not in GROUPS:
            errors.append(f"{where}: unknown group {a['group']!r} (not in working-groups.csv)")
        if a["sector"] not in SECTORS:
            errors.append(f"{where}: unknown sector {a['sector']!r} (not in sectors.csv; "
                          "use a section or add the code in the Industry Function Graph first)")
        if a["sector"] in seen and seen[a["sector"]] != a["group"]:
            errors.append(f"{where}: {a['sector']} is already assigned to {seen[a['sector']]!r}; "
                          "a sector belongs to one group")
        elif a["sector"] in seen:
            errors.append(f"{where}: duplicate row for {a['group']} / {a['sector']}")
        seen.setdefault(a["sector"], a["group"])
    for g in GROUPS:
        if g not in {a["group"] for a in ASSIGNMENTS}:
            notes.append(f"group {g!r} has no sector assigned")
    for s in SECTORS.values():
        if s["level"] == "section" and responsible(s["id"])[0] is None:
            notes.append(f"section {s['notation']} ({s['label']}) has no working group")
    return errors, notes
