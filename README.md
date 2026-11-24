# DIDAS Use Case Repository

**Business use cases for the Swiss verifiable data ecosystem**: what a verifier
needs to know, from whom, with which credentials and under which governance.
DIDAS maintains the repository.

It is intended as an early version of the **use-case section of the Swiss
Ecosystem Discovery Catalog** proposed in the DPSS pre-study of June 2026.
[VISION.md](VISION.md) describes how the two relate.

<p align="center" class="gh-only">
  <a href="https://didas-swiss.github.io/use-case-repository/"><img alt="Open the website" src="https://img.shields.io/badge/Open%20the%20website-0b7285?style=for-the-badge"></a>
  &nbsp;
  <a href="https://github.com/DIDAS-swiss/use-case-repository/issues/new?template=use-case-candidate.yml"><img alt="Register your use case" src="https://img.shields.io/badge/%2B%20Register%20your%20use%20case-1971c2?style=for-the-badge"></a>
  &nbsp;
  <a href="https://github.com/DIDAS-swiss/use-case-repository/issues/new?template=credential-signal.yml"><img alt="Signal a credential need" src="https://img.shields.io/badge/Signal%20a%20credential%20need-495057?style=for-the-badge"></a>
  &nbsp;
  <a href="https://github.com/orgs/DIDAS-swiss/projects/6"><img alt="Project board" src="https://img.shields.io/badge/Project%20board-495057?style=for-the-badge"></a>
</p>

<p class="gh-only"><strong>📖 Start here: <a href="https://didas-swiss.github.io/use-case-repository/">didas-swiss.github.io/use-case-repository</a></strong>,
the website with the <a href="https://didas-swiss.github.io/use-case-repository/backlog.html">backlog</a>,
the published use cases, the credentials and gap board, and the anchors to the
other DIDAS repositories.</p>

**[➕ Register your use case](https://github.com/DIDAS-swiss/use-case-repository/issues/new?template=use-case-candidate.yml)**: half a page of plain prose is enough.
A curator helps turn it into a structured entry.

**🗂 For curators and working groups: the [project board](https://github.com/orgs/DIDAS-swiss/projects/6)** ([how it works](PROJECT.md))

Everything runs on GitHub itself, with no separate server. Entries are Markdown
files, intake runs through issue forms, and the lifecycle is tracked with labels
and pull requests. GitHub Pages publishes the same files as the website, with its
built-in Jekyll. GitHub Actions workflows open issues from intake batches, open
draft entries, check the data, sync labels and the project board, and keep the
federated sources current.

## Browse

- **[Use cases](use-cases/)**: one file per use case, indexed in
  [`use-cases/README.md`](use-cases/README.md)
- **[Credentials](credentials/)**: one file per credential type that a use case
  relies on, with its supply status, indexed in
  [`credentials/README.md`](credentials/README.md)
- **[Anchors](anchors.md)**: every trust flow of the
  [Trust Flow Diagram Repository](https://github.com/DIDAS-swiss/Trust-Flow-Diagram-Repository),
  every pattern of the [Industry Function Graph](https://github.com/DIDAS-swiss/industry-function-graph)
  and every credential dataset on I14Y, with the use cases that reference it
- **[Federated schemas](federation/i14y/)**: credential schemas federated from
  [I14Y](https://www.i14y.admin.ch/), such as the Beta-ID and the simple residence
  confirmation, refreshed weekly by a workflow
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
