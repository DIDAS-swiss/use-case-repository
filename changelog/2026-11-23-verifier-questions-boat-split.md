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
  `variant_of`.

## Changed

- `boat-skipper-licences`: references only `BJ-v41-054`; its open question on
  the boat permit points to the new candidate.
