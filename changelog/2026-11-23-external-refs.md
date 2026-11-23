# 2026-11-23: References to other use-case lists; relations across batch files

## Added

- Field `external_refs`: the entries that describe a use case in other lists,
  as `<reference> (<status at the source>)`, for example
  `BJ-v41-001 (LAUNCH)`.
  - The form has it under *Details*, the batch as a column, the entry
    template in its front matter.
  - Only lists in `_data/external-sources.csv` are allowed. Their owners
    agreed to be named: the BJ list «Credential Use Cases» v41 and the
    use-case collections of the Fachbereich E-ID, both since 23.11.2026.
    *Check data* rejects references from other lists.
  - The status at the source travels with the reference; there is no
    separate availability field.

## Changed

- *Check data* resolves relations across all batch files in `intake/`, staged
  files included, and reports an id used in two batch files.

No issue and no entry is filled; references follow after the editorial review
decisions.
