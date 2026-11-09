# 2026-11-09: Working groups by sector

## Added

- Fourteen working groups in `_data/working-groups.csv`, named by sector, each
  with the ISIC Rev. 5 sectors it covers: Banking (`ISIC-64`), Insurance
  (`ISIC-65`), Health (`ISIC-86`, `ISIC-R`), Pharma (`ISIC-21`), Public Sector
  (`ISIC-84`, `ISIC-P`), Education (`ISIC-85`, `ISIC-Q`), Retail (`ISIC-47`,
  `ISIC-G`), Mobility (`ISIC-H`), Hospitality (`ISIC-I`), Industry &
  Manufacturing (`ISIC-C`), Digital & Telecom (`ISIC-K`), Energy & Utilities
  (`ISIC-D`, `ISIC-E`), Real Estate (`ISIC-M`) and Sport (`ISIC-S`)
- *Sync labels* creates a `wg: <group>` label for each; *Sync project board*
  creates the matching options of the Working group field
- Batch candidates without a group get a *Suggested working group*, the one whose
  sectors match the primary sector most closely
