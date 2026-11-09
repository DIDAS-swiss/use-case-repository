# 2026-11-09: Batch intake for working groups, sectors on the project board

## Added

- `intake/`: a list of use-case candidates filed as one YAML file becomes one
  candidate issue per entry, through the *Intake candidates* workflow
  (`intake.yml`, `scripts/intake.py`). Entries already filed or already published
  are skipped; unknown sector, trust-flow or pattern ids are reported. Format in
  `intake/README.md`
- Working groups: `_data/working-groups.csv`, `wg: <group>` labels (created by
  *Sync labels*) and a *Working groups* section in `GOVERNANCE.md` on how a group
  takes and develops a candidate
- Project board fields **Sector** (the primary ISIC Rev. 5 section) and **Working
  group**, set by *Sync project board*, and the views *By sector*, *Up for grabs*
  and *Working groups* in `PROJECT.md`

## Notes for review

- `_data/working-groups.csv` is empty until the DIDAS working groups are listed;
  the Working group field and labels are created once it has entries
