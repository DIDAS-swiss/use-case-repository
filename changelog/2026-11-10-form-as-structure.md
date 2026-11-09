# 2026-11-10: The use-case form is the structure; links and dynamic choices

## Changed

- The use-case form is the one structure for use cases. Its fields follow the
  sections of an entry: short id, titles in three languages, summary, outcome,
  actors and roles, process flow, design basis, credentials, I14Y datasets,
  schemas, ambition levels, sectors, anchors (trust flows, patterns, flows,
  implementations, glossary terms), related, upstream and downstream use cases,
  lighthouse, governance, demand, open questions, organisation and sources
- Issue titles have no `[Use case]` prefix; workflows recognise use-case issues by
  the `use-case` label
- The intake writes issues in exactly the form's fields, read from the form
  itself. On the next run it rewrites the titles and descriptions of the existing
  backlog issues in that structure, unless a description was edited by hand (an
  invisible checksum tells). What the form has no field for (where an issue came
  from, the suggested working group, the points to fix) is in the intake comment.
  Stage, status and labels are left alone

## Added

- Dynamic choices in the form: the credentials described in `credentials/` and
  the DIDAS Glossary terms (`_data/glossary-terms.csv`, synced from the glossary),
  next to sectors, trust flows, patterns and I14Y datasets
- A [list of use-case ids](https://didas-swiss.github.io/use-case-repository/use-case-ids.html),
  published entries and candidates (`_data/use-case-index.csv`), for the related,
  upstream and downstream fields
- `scripts/issue_links.py`: one comment per use-case issue linking what its fields
  name: described credentials, I14Y datasets, trust flows, patterns, glossary
  terms and use cases. Run by the intake and, for issues filed through the form,
  on every edit
- `scripts/draft_entry.py` and the *Draft entry* workflow: the label `drafting`
  opens a pull request with `use-cases/<id>.md` written from the issue's form
  fields. The pull request does not close the issue; the entry starts at `signal`
- `check_data.py` checks glossary term ids; entry pages link their glossary terms

## Removed

- `cantonal-identity-confirmation` from the backlog CSV: its issue (#72) was
  deleted, and the intake would otherwise open it again
