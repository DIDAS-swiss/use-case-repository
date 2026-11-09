# Batch intake of use-case candidates

A list of candidates, for example collected in a workshop or commissioned for the
DIDAS working groups, is filed here as one YAML file. When the file reaches
`main`, the **Intake candidates** workflow opens one *use-case candidate* issue per
entry, written in the fields of the use-case form, exactly as if each had been
submitted through it: labelled
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

## CSV batches

A batch can also be a CSV file, one candidate per row, with the column names of the
use-case front matter and body: `title`, `title_de`, `title_fr`, `title_it`,
`ambition_levels`, `sectors`, `credentials_reused`, `credentials_new`,
`credentials_excluded`, `related_use_cases` (lists separated by `;`), and
`summary`, `summary_de`, `outcome`, `outcome_de`, `actors`, `process_flow`,
`design_basis`, `credentials`, `legal_basis`, `trust_frameworks`,
`verifier_governance`, `sensitive_attributes`, `relying_parties`,
`indicative_scale`, `value`, `coordination_and_open_questions`,
`coordination_and_open_questions_de`, `sources`, plus `no` and `id` as the
backlog reference. Actors and process steps separated by ` | ` become lists.

Further columns:

| Column | Values |
|---|---|
| `upstream_use_cases` | ids of use cases that must happen first, because they issue a credential this one verifies, separated by `;` |
| `downstream_use_cases` | ids of use cases that reuse a credential this one issues, separated by `;` |
| `lighthouse` | `yes` or `selected` sets the label `lighthouse`; `candidate` sets `lighthouse-candidate`; empty leaves the labels alone |
| `lighthouse_basis` | one line on why |
| `review_notes` | points the description has to fix, numbered `(1) … (2) …` |

## What happens

- A candidate whose title matches an existing use-case issue is not opened again.
  Its issue is kept in step with the file instead: its title and description in
  the form's fields, unless someone has edited the description by hand (an
  invisible checksum tells); the lighthouse label; one comment with where it came
  from, the suggested working group and the points to fix; and one comment with
  links. Comments are updated, not repeated. The issue's stage, status and other
  labels are left as they are.
- A candidate that is already published in `use-cases/` (same title or id) is
  opened as an **update issue**, labelled `change`, that links the entry so the
  backlog version can be compared and merged into it.
- Unknown sector, trust-flow or pattern ids are reported in the workflow log and
  left out; the candidate is still created.
- A candidate without `working_group` gets a *Suggested working group*: the group
  responsible for its primary sector under the
  [assignment table](https://didas-swiss.github.io/use-case-repository/working-groups.html)
  (Pharma before Industry & Manufacturing for `ISIC-21`). The group still takes
  it by adding its label.
- Files whose names start with `_`, and this README, are ignored.
