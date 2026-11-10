# 2026-11-10: eLFA live; driving-licence credentials; swiyu.admin.ch sources

## Added

- Credential entries:
  - **Electronic learner's permit (eLFA)**: supply *available*. It is in live
    use in all cantons, and DIDAS reports about 100,000 active as of 10
    November 2026. The Confederation calls it a pilot. Its schema exists on the
    issuer side but is not on I14Y.
  - **Digital driving licence**: supply *emerging*, announced as "soon
    available" on swiyu.admin.ch. It joins the gap board, needed by 7
    candidates.
- Dependencies page: the eLFA status, the credentials swiyu announces as "soon
  available", and the move from eid.admin.ch to swiyu.admin.ch.

## Changed

- The eLFA facts and their sources (the pilot page, ASTRA's LicenceCheck and
  the DIDAS figure) are added to the learner-driver carsharing, traffic-control
  and carsharing cases (#76, #40, #45).
- Credential ids for the learner's permit and driving licence are harmonised
  across the batch: `learner-permit-elfa` and `digital-driving-licence`.
- Five sources citing the retired eid.admin.ch now cite the same statements on
  swiyu.admin.ch (#6, #8, #73, #90, #100), and so does `credentials/swiss-e-id.md`.
- #101 cites BAV's register dataset of train drivers' licences on I14Y, for
  comparing a credential with a register query.

## Not changed

- No evidence status moves. The eLFA being live makes the *credential*
  available; the exchanges these cases propose (carsharing acceptance, the
  full digital licence at traffic stops) are not confirmed yet.
