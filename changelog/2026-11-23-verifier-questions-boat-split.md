# 2026-11-23: Verifier questions decided by DIDAS; boat permit split off

## Added

- Column `verifier_question` in `intake/2026-11-didas-use-case-backlog-v2.csv`,
  set where DIDAS decided it on 23 November 2026 for use cases whose BJ
  entries gave different categories: `residence-confirmation` attestation,
  `diploma-employer-verification` qualification, `tickets` permission,
  `boat-skipper-licences` qualification.
- New candidate `boat-permit-check` (permission): the boat permit
  (Schiffsausweis) at a control on the water, split from
  `boat-skipper-licences` because it answers a different verifier question. It
  takes over the reference `BJ-v41-053` and names `boat-skipper-licences` in
  `variant_of` (changed to `related_use_cases` in the follow-up below).

## Changed

- `boat-skipper-licences`: references only `BJ-v41-054`; its open question on
  the boat permit points to the new candidate.

## Changed (follow-up)

- `boat-permit-check` and `boat-skipper-licences` name each other in
  `related_use_cases` instead of `variant_of`: they ask different verifier
  questions, so they are not variants under the definition in CONTRIBUTING.md.
- `verifier_governance` records the DIDAS decisions of 23 November 2026:
  combined proof with identity for `residence-confirmation` and
  `diploma-employer-verification`; single use for `tickets`.
