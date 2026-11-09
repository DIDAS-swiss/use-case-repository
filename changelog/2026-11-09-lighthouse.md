# 2026-11-09: Lighthouse selection on the project board

## Added

- A `lighthouse` label, created by *Sync labels*, to select a use case as a
  lighthouse
- A **Lighthouse** field on the project board, set by *Sync project board* while
  the label is on the item and cleared when it is removed, and a *Lighthouses*
  view in `PROJECT.md`
- Batch files can set the label with a `lighthouse` column (`yes`, `ja`, `x`)

## Notes for review

- The board's Sector, Type, Working group and Lighthouse fields are created on
  the first manual run of *Sync project board*, which needs the `PROJECT_TOKEN`
  secret. Until then the 128 backlog issues carry their sectors only as
  `ISIC <letter>` labels
