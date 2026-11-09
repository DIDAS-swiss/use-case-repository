# Batch intake of use-case candidates

A list of candidates, for example collected in a workshop or commissioned for the
DIDAS working groups, is filed here as one YAML file. When the file reaches
`main`, the **Intake candidates** workflow opens one *use-case candidate* issue per
entry, exactly as if each had been submitted through the form: labelled
`use-case`, `stage: signal`, with its ISIC section and ambition-level labels, and
added to the [project board](https://github.com/orgs/DIDAS-swiss/projects/6).

From there the normal funnel applies ([GOVERNANCE.md](../GOVERNANCE.md)): a
working group takes a candidate (label `wg: <group>`), details it and drafts the
entry in a pull request.

## File format

One file per batch, `intake/<yyyy-mm>-<short-name>.yml`. Only `title` is
required; everything else can be filled in later by whoever takes the candidate.

```yaml
batch: 2026-11 DIDAS working-group candidates
proposed_by: DIDAS
candidates:
  - title: Vehicle leasing                 # the outcome, not the organisation
    summary: >-                            # situation, decision, what must be proven
      A leasing company identifies a lessee and checks residence,
      creditworthiness and income before concluding the contract.
    sectors: [ISIC-64, ISIC-65]            # ISIC ids from _data/sectors.csv; the first is the primary sector
    ambition_levels: [AL2, AL3]
    working_group: mobility                # optional: a working-group id from _data/working-groups.csv
    actors: Lessee (holder); leasing company (verifier); road traffic office, insurer (issuers)
    credentials: e-ID, residence confirmation, debt enforcement extract, insurance confirmation
    trust_flows: []                        # Trust Flow ids from _data/trust-flows.csv
    ifm_patterns: [due-diligence-onboarding]
    sources: https://…
```

Free-text fields (`summary`, `actors`, `credentials`, `governance`, `demand`,
`sources`) may be as short as a line.

## What happens

- A candidate whose title matches an existing use-case issue is skipped, so a file
  can be extended and pushed again without duplicates.
- Unknown sector, trust-flow or pattern ids are reported in the workflow log and
  left out; the candidate is still created.
- A candidate without `working_group` gets a *Suggested working group*: the group
  responsible for its primary sector under the
  [assignment table](https://didas-swiss.github.io/use-case-repository/working-groups.html)
  (Pharma before Industry & Manufacturing for `ISIC-21`). The group still takes
  it by adding its label.
- Files whose names start with `_`, and this README, are ignored.
