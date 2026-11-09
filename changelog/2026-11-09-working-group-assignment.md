# 2026-11-09: A manageable assignment of ISIC sectors to working groups

## Added

- `_data/working-group-sectors.csv`: the assignment of ISIC sectors to working
  groups as one table, one row per group and sector code. A group can hold any
  number of codes; `_data/working-groups.csv` now lists only the groups
- Rules, in `scripts/working_groups.py`: a code belongs to at most one group; the
  most specific assignment wins; a code without an assignment inherits the group of
  the nearest broader code
- `check_data.py` and the *Check data* workflow: on every change, reject a code
  assigned twice, an unknown code or group, and any entry that refers to a sector,
  trust flow, pattern, credential, use case or I14Y dataset that does not exist;
  report sections without a working group
- A [Working groups page](https://didas-swiss.github.io/use-case-repository/working-groups.html):
  each group with its codes, and each sector with the group responsible for it,
  marked where inherited or missing
- The two working-group tables are owned by the maintainers in `CODEOWNERS`

## Changed

- `_data/sectors.csv` lists each section followed by its divisions and classes
- The intake suggests the responsible group through the same rules

## Removed

- A Python cache file committed by mistake; `.gitignore` now excludes them

## Notes for review

- Ten sections have no working group yet, among them L as a whole (Banking holds
  64 and Insurance 65, so division 66 would have none). The Working groups page
  lists them
