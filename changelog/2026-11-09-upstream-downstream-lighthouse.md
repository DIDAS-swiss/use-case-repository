# 2026-11-09: Upstream and downstream use cases; two lighthouse levels

## Added

- Front matter `upstream_use_cases` (use cases that issue a credential this one
  verifies) and `downstream_use_cases` (use cases that reuse a credential this one
  issues); `related_use_cases` stays for relations with no sequence
- Front matter `lighthouse` (`selected`, `candidate` or empty) and
  `lighthouse_basis`; the label `lighthouse-candidate` next to `lighthouse`; the
  project's Lighthouse field gets the options *Lighthouse* and *Candidate*
- The lighthouse criteria and the meaning of upstream and downstream in
  `GOVERNANCE.md`
- `check_data.py`: relation ids must exist; a relation the two sides disagree
  about is a warning; `lighthouse` must be `selected`, `candidate` or empty. The
  CSV batches in `intake/` are checked the same way
- Issue form fields for both relations and a lighthouse proposal
- Use-case pages show the lighthouse level and the upstream and downstream use
  cases
- The intake reads the columns `upstream_use_cases`, `downstream_use_cases`,
  `lighthouse`, `lighthouse_basis` and `review_notes`, and keeps existing issues in
  step with them: the lighthouse label and one comment with relations and review
  notes. Stage, status, other labels and descriptions are left alone
- The backlog annex of 2026-11-09 in `intake/2026-11-didas-use-case-backlog-v2.csv`:
  relations for 72 use cases, 13 selected lighthouses, 12 candidates, review notes
  for 21; and the new candidate *GA as proof for partner benefits*
  (`ga-partner-benefits`), downstream of `sbb-ga-familia-residence`
- Published entries: vehicle leasing names motor vehicle claims processing
  downstream; motor vehicle claims processing names vehicle leasing upstream and is
  a lighthouse candidate

## Notes for review

- One relation of the annex is left out because it contradicts the use-case text:
  `debt-enforcement-extract` → `debt-certificate-secondary-market`. The certificate
  of loss use case lists the debt enforcement extract under
  `credentials_excluded`; it verifies the certificate of loss (Verlustschein), not
  the extract
- The new candidate's sectors ISIC-49 and ISIC-77 are recorded as the sections
  ISIC-H and ISIC-O, because the repository's sector list has no divisions 49
  and 77
