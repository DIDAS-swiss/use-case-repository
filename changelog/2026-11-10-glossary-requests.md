# 2026-11-10: Glossary requests from use cases

## Added

- Form field *Terms missing from the DIDAS Glossary*: one term per line, each
  with what it means in the use case.
- *Glossary requests* workflow and `scripts/glossary_requests.py`. Each listed
  term that the glossary does not define becomes one `[Term] …` issue in the
  DIDAS Glossary, in the shape of its *New term* form. Use cases asking for the
  same term share the issue. A comment on each side links the other, and the
  use-case comment says whether each term is requested, defined or declined.
  It writes with the existing `PROJECT_TOKEN`, extended to `didas-glossary` with Issues: Read and write, or with a dedicated `GLOSSARY_TOKEN` if one is set (see CONTRIBUTING.md).
- `_data/glossary-terms.csv` lists each term's other names (plural, German,
  French, Italian), so a request for an alias of a defined term is not sent.
- Batch column `missing_terms` for the intake.
