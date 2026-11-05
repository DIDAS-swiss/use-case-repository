# 2026-11-05: ISIC Rev. 5 sectors, shared with the Industry Function Graph

## Added

- `_data/sectors.csv`: the ISIC Rev. 5 sector list of the
  [DIDAS Industry Function Graph](https://github.com/DIDAS-swiss/industry-function-graph),
  copied from its `data/sectors.csv` at commit `115ebb9`: the 22 sections plus
  the divisions and classes the graph uses, with the graph's ids (`ISIC-L`,
  `ISIC-65`, `ISIC-6512`)
- A sector selector on the published use-case list. Choosing a section also
  finds the divisions and classes inside it
- Sector names in the facts panel of each use-case page
- `ISIC A` … `ISIC V` labels, created by the *Sync labels* workflow and applied
  to use-case candidates from the sectors chosen in the form

## Changed

- `sectors` in use-case front matter now takes ISIC ids instead of free text.
  The two seed entries are mapped: vehicle leasing to `ISIC-64`, `ISIC-65` and
  `ISIC-84`; motor vehicle claims processing to `ISIC-6512` and `ISIC-84`
- The *Use-case candidate* form offers the sectors as a multi-select dropdown
- `label-signals.yml` is now *Label from issue forms* and also applies the
  sector labels
- The site publishes from the branch (Pages source *Deploy from a branch*,
  `main`, root). A separate Actions deploy was tried and removed, because it
  would deploy a second time on every push
- `CONTRIBUTING.md` documents the sector rules; `GOVERNANCE.md` replaces the
  free-form `sector:` labels with the ISIC section labels
