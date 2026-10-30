# DIDAS Use Case Repository

A community repository for collecting, describing and assembling **business use
cases for the Swiss verifiable data ecosystem**: what needs to be proven, by
whom, using which credentials and under which governance conditions. It is
maintained by the DIDAS community.

Our aim is for this repository to grow into an early, working version of the
**use-case section of the Swiss Ecosystem Discovery Catalog**, the coordination and
discovery layer proposed in the DPSS pre-study of June 2026. See
[VISION.md](VISION.md) for how the two relate.

Everything runs on GitHub itself, with no website or build step. Entries are
Markdown files that GitHub renders, intake runs through issue forms, and the
lifecycle is tracked with labels and pull requests. Two small GitHub Actions only
manage labels.

## Browse

- **[Use cases](use-cases/)**: one file per use case, indexed in
  [`use-cases/README.md`](use-cases/README.md)
- **[Credentials](credentials/)**: one file per credential type that a use case
  relies on, with its supply status, indexed in
  [`credentials/README.md`](credentials/README.md)
- **Gap board**: open demand for credentials no one issues yet. These are the
  [open `credential-need` issues](https://github.com/DIDAS-swiss/use-case-repository/issues?q=is%3Aissue+is%3Aopen+label%3Acredential-need),
  with the `missing` credentials listed in the
  [credentials index](credentials/README.md#gap-board)
- **Intake queue**: [open `use-case` candidates](https://github.com/DIDAS-swiss/use-case-repository/issues?q=is%3Aissue+is%3Aopen+label%3Ause-case)

## How a use case enters (the funnel)

The intake works like the [DIDAS Glossary](https://github.com/DIDAS-swiss/didas-glossary)'s:
**issues are intake, the pull request is the governance artifact, and merging to `main` is
publication.**

```
 issue form             triage                 pull request            merge to main
┌───────────────┐    ┌────────────────┐    ┌───────────────────┐    ┌──────────────────┐
│ Use-case      │ →  │ curator:       │ →  │ entry file at     │ →  │ published; stage │
│ candidate  or │    │ scope, dupes,  │    │ stage `signal`,   │    │ advances through │
│ credential    │    │ AL + sector    │    │ index row,        │    │ later PRs        │
│ need          │    │ labels         │    │ Closes #N         │    │                  │
└───────────────┘    └────────────────┘    └───────────────────┘    └──────────────────┘
```

1. **Propose a use case** with the *Use-case candidate* issue form. Half a page of
   plain prose is enough. A curator helps turn it into a structured entry.
2. **Signal a credential need**, or the ability to supply one, with the *Credential
   need / supply signal* form.
3. **Change an entry or advance its stage** with the *Change to an entry* form, or
   open a pull request directly.

The lifecycle stages, roles and review gates are in [GOVERNANCE.md](GOVERNANCE.md).
How to write an entry is in [CONTRIBUTING.md](CONTRIBUTING.md).

## What this repository does not do

It does not create or manage authoritative data, credential schemas or trust
decisions. Following the pre-study's design boundary, schemas live in
[I14Y](https://www.i14y.admin.ch/), eCH-linked processes or recognised sectoral
repositories, and issuer and verifier status lives in the swiyu registries. Entries
here **link** to those sources and do not copy them.

Vocabulary follows the [DIDAS Glossary](https://didas-swiss.github.io/didas-glossary/).
When a use case needs a term the glossary lacks, propose it there.

## Licensing

| What | License |
|---|---|
| Use-case and credential content (`use-cases/`, `credentials/`) | [CC BY 4.0](LICENSE-CONTENT) |
| Repository configuration (issue forms, workflows, templates) | [MIT](LICENSE) |
| Third-party material | Original terms. See [NOTICE.md](NOTICE.md) |
