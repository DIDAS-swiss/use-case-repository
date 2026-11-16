# 2026-11-16: Boundary check for use cases

## Added

- *Check data* applies the rule "same verifier role and same verifier question
  = one use case" to published entries and batch candidates:
  - **error:** a `verifier_question` outside the five values;
  - **warning:** two use cases with the same verifier (lower case, trimmed) and
    the same question, unless one names the other in `related_use_cases` as a
    variant;
  - **note:** an entry from stage `candidate` on that lacks either field.
- Tests in `tests/test_boundaries.py`.
