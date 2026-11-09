# 2026-11-09: DIDAS use-case backlog v2 filed as candidates

## Added

- `intake/2026-11-didas-use-case-backlog-v2.csv`: the external version of the
  DIDAS use-case backlog of 9 November 2026, 128 use cases (`UC-001` to `UC-128`),
  without its rating columns, which were empty
- The intake reads CSV batches with the columns of the use-case format, and writes
  every column into the issue: titles in four languages, summary and outcome in
  English and German, actors, process flow, design basis, credentials (with links
  to their entries and their I14Y datasets), governance, demand, open questions
  and sources
- A candidate already published in `use-cases/` becomes an update issue labelled
  `change`, linking the entry. Applies to vehicle leasing, motor vehicle claims
  processing and the vaccination record

## Changed

- The intake paces issue creation and waits when GitHub limits it
