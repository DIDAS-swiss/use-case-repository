# 2026-11-16: Verifier and verifier question

## Added

- Fields `verifier` (the relying party, as a role) and `verifier_question`
  (`identity`, `qualification`, `attestation`, `permission` or `membership`) in
  the entry template, the issue form, the intake and the drafting script. Both
  are optional at `signal` and required from `candidate` on.
- CONTRIBUTING.md, *Where one use case ends*: same verifier role and same
  verifier question = one use case; another context of the same decision is a
  variant. The question set is adapted from the BJ e-ID team's credential use
  case classification and kept in `_data/verifier-questions.csv`, from which the
  form's dropdown is generated.
- Triage checks the two fields for duplicates and variants.

No existing entry or issue is backfilled.
