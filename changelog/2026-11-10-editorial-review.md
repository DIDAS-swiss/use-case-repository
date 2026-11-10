# 2026-11-10: Editorial review of the backlog; a shorter form

## Changed

- All 128 candidates in `intake/2026-11-didas-use-case-backlog-v2.csv` rewritten
  from the editorial review of 10 November 2026. Each has a title naming one
  decision, a summary of 40 to 70 words, the expected benefit, whether that is
  a hypothesis, and one open question. English and German were changed
  together; the German drafts need a domain review. The earlier summaries move
  to *Background*, without the shared e-ID timing.
- Substantive corrections from the review, among them:
  - #2/#9: identity proofing kept apart from later AGOV login.
  - #18: the income evidence is the employer's, not the bank's.
  - #36: the one-day promise is removed; a signature does not replace the
    public deed.
  - #47: the e-collecting design variant is reconciled, with its status
    rechecked.
  - #60, #77 and #105: the remote ZertES signing correction: the e-ID can
    enable or trigger signing, including QES, through a certified provider.
    This capability is planned.
  - #79: the proof matches the tariff's tax-liability rule, rechecked against
    the 2026/27 tariff.
  - #83: one claim type, with no policy data the insurer already holds.
  - #92: no claim of physical authenticity.
  - #94: only the documented expiry example.
  - #99: St. Gallen's evidence period is three months, not one year.
  - #109: no invented transfer register.
  - #113: core fields filled in.
  - #117: the ETH/SWITCH issuance process.
  - #124: mandate, organisation evidence and the bank's checks kept apart.
  - #131: no dependency on #107.
- Upstream and downstream relations now require a credential that is actually
  issued; relations that only described a similar earlier transaction move to
  *related*, on both sides.
- The use-case form asks first for six things: the use case, summary, actors,
  facts to prove, demand and value, and evidence status with sources. The rest
  follows as details. A hypothesis is a valid start. Lighthouse selection is no
  longer a submitter option; curators record it with a decision record.
- The backlog page shows each case's evidence status and its non-empty core
  fields. It also says that a published entry is not a qualified or
  production-ready one.

## Added

- `intake/reviews/2026-11-10-editorial-review.csv`: per case, the review's
  recommendation (31 retain, 58 revise, 23 split, 8 merge, 8 park), the finding,
  how far its evidence was checked, the fields changed, departures, open domain
  questions and the reconciliation with the live issue.
- `intake/reviews/2026-11-10-proposed-scopes.csv`: the 37 separate scopes
  proposed for the 23 splits. These are proposals; no issue is opened for them.
- [Dependencies page](../dependencies.md): the e-ID, trust-infrastructure and
  signing status, kept once with its source and check date.
- `scripts/use_case_form.py`, the one reader of the form, which also reads
  earlier labels. `intake.py --reconcile` gives a read-only plan against the live
  issues. `tests/` holds regression tests run by *Check data*.

## Not changed

- No issue is closed, opened or merged by the review. Stages, working groups and
  lighthouse selections are as they were; the 13 selections are kept, and their
  comment says the decision record is still to be linked.
