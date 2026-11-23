# 2026-11-23: Candidates from the Fachbereich E-ID published

## Changed

- The two staged batch files lose their leading `_`, so the intake opens an
  issue for each of their nine candidates:
  `intake/2026-11-bj-credential-use-cases.csv` (six candidates from the BJ
  list «Credential Use Cases» v41) and `intake/2026-11-further-sources.csv`
  (three from the use-case collections of the Fachbereich E-ID).
- `event-entry-age-check` references `BJ-v41-001 (LAUNCH)`. The other
  candidates carry no BJ code; DIDAS decided on 23 November 2026 not to add
  them.
- `tests/test_form_pipeline.py` reads the review rows against all batch files,
  not only the first.
