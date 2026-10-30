# Governance

This document defines how use cases and credential entries enter the repository,
mature and leave it. It adapts the governance model of the
[Ecosystem Discovery Catalog pre-study](VISION.md) (§7–§8) to a community
repository, and follows the intake model of the
[DIDAS Glossary](https://github.com/DIDAS-swiss/didas-glossary/blob/main/GOVERNANCE.md).

## Principles

1. **Issues are intake, the pull request is the governance artifact, merge to
   `main` is publication.** Every decision is recorded in issue and PR history.
2. **Low threshold to enter, stronger controls to advance.** Anyone can propose a
   use case or signal a need. Moving an entry up the lifecycle needs evidence and
   a named approver (pre-study §8.8, §9.2).
3. **Reference, don't duplicate.** Schemas, trust-registry entries and legal texts
   stay with their authoritative source. Entries link to them (pre-study §8.6).
4. **Use-case and schema lifecycles are separate.** This repository tracks how use
   cases mature. Schemas mature in I14Y, eCH or sectoral repositories, and an
   entry only records where they stand (pre-study §9.3).

## Lifecycle stages

Every use case and credential entry carries one `stage`, mirrored by a
`stage:` label on its issue. These are the stages of pre-study §8.10:

| Stage | Meaning | Criteria to reach it | Who approves |
|---|---|---|---|
| `signal` | A proposed use case or credential need has been submitted | Submitted through an issue form and accepted by triage | Catalog curator |
| `candidate` | Reviewed for clarity, completeness and duplication | All required fields filled; no duplicate entry; sources given | Catalog curator |
| `qualified` | Demand, governance context, semantic alignment and implementation relevance are clear enough to act on | At least one named relying party or issuer; legal basis or governance framework named; each credential mapped to a supply status | Domain steward (within a domain), or catalog curator (cross-domain) |
| `active` | Used in one or more pilot or operational contexts | A public reference to the pilot or deployment | Domain steward |
| `maintained` | Maintained in a recognised external pathway, such as I14Y, eCH or a sectoral body, and referenced from here | Link to the external home | Domain steward, or the standards authority where normative |
| `deprecated` | Visible for traceability but no longer recommended | Reason and successor, if any, recorded in the entry | Domain steward or catalog curator |

Transitions are judged on demonstrated demand, mandate fit, implementation
readiness, semantic consistency, governance clarity and reuse potential
(pre-study §8.10). A transition is a pull request that changes `stage`, states
which criteria are met and links the evidence.

## Roles

These are the pre-study's participation roles (§7.2), scaled to a repository.

| Role | In this repository | Pre-study equivalent |
|---|---|---|
| **Community participant** | Anyone with a GitHub account. Opens issues, comments, and adds 👍 to show demand | Community Participant |
| **Ecosystem contributor** | Someone who opens pull requests on behalf of an identified organisation (named in the entry) | Ecosystem Contributor |
| **Domain steward** | Recognised responsibility for a sector or policy domain. Approves stage transitions for that domain's entries. Listed in [STEWARDS.md](STEWARDS.md) | Domain Steward |
| **Catalog curator** (`@DIDAS-swiss/use-case-curators`) | Triages intake, checks quality and duplicates, keeps entries coherent across domains, and acts as provisional domain steward where none is named | Catalog Curator |
| **Data steward** | Not a role in this repository. Semantic stewardship stays with I14Y, eCH and sectoral bodies. Entries point to them | Data Steward |
| **Standards authority** | External (eCH, I14Y bodies, DPSS or a sectoral body). Its decisions are referenced, never made here | Standards Authority |

Where no domain steward is recognised for a sector, the catalog curator holds
provisional stewardship until one is confirmed (pre-study §7.3).

## Workflow A: use-case candidates

1. **Intake**: the proposer files a *Use-case candidate* issue (label `use-case`,
   `stage: signal`).
2. **Triage** within two weeks: a curator checks scope (does verifiable data play a
   role?), looks for duplicates, and adds ambition-level (`AL2`, `AL3`) and
   `sector:` labels. The curator may also apply `needs-work`, `duplicate` or
   `out-of-scope`, with reasons.
3. **Drafting**: the proposer, a curator or a volunteer opens a pull request adding
   `use-cases/<id>.md` at stage `signal` and a row in `use-cases/README.md`, with
   `Closes #N`. Any credential the use case needs that has no file yet is added in
   `credentials/` in the same pull request.
4. **Review**: one curator approval merges a `signal` or `candidate` entry. Later
   stages need the approver named in the stage table above.
5. **Publication**: the merge publishes the entry. A changelog entry is part of the
   same pull request.

## Workflow B: credential needs and supply signals

1. **Intake**: anyone files a *Credential need / supply signal* issue. A workflow
   labels it `credential-need` or `credential-supply` from the form's answer.
2. **Visibility**: the issue is the signal. It appears on the gap board (open
   `credential-need` issues) as soon as it is filed, with no approval needed (pre-study §7.1:
   demand signals are accepted automatically and only quality-checked).
3. **Aggregation**: a curator links the issue to the use cases it affects and to
   its credential file, creating the file with `supply: missing` if needed.
   Others add 👍 or comment to strengthen the signal.
4. **Matching**: when a potential issuer responds, through a comment or a
   `credential-supply` issue, the curator links both sides and updates the
   credential file's `likely_issuer`.
5. **Closing**: the issue closes when the credential becomes `available`, with a
   reference to the issuer's trust-registry entry or schema, or when it is
   rejected or superseded.

## Labels

| Label | Use |
|---|---|
| `use-case` | Use-case candidate or change |
| `credential-need` / `credential-supply` | Demand or supply signal (the gap board) |
| `stage: signal` … `stage: deprecated` | Lifecycle stage of the entry the issue concerns |
| `AL1`, `AL2`, `AL3` | Ambition level |
| `sector: …` | Sector, for example `sector: mobility` or `sector: insurance` |
| `needs-work`, `duplicate`, `out-of-scope` | Triage outcomes |
| `cross-domain` | Spans more than one domain, so the curator approves |

## Escalation

When ownership of a cross-domain use case or a stage transition is contested,
the curator mediates first. If that does not resolve it, the question goes to a
GitHub Discussion or the DIDAS community call, and the decision and its rationale
are recorded in the issue. This mirrors pre-study §7.3, with the DIDAS community
in place of the orchestrator secretariat.

## Neutrality

No organisation's contribution, sponsorship or membership buys editorial influence
over entries, stages or the gap board (pre-study §8.7).

## Repository settings (admin checklist)

These are configured in GitHub settings, not in files:

- Branch protection on `main`: require a pull request and code-owner review.
- Create the `use-case-curators` team and grant it write access.
- Run the **Sync labels** workflow once from the Actions tab. It creates the labels
  listed above. The **Label credential signals** workflow then sorts credential
  issues into `credential-need` and `credential-supply`.
- Enable GitHub Discussions for escalation.
- Pages: *Settings → Pages → Build and deployment*, source **Deploy from a
  branch**, branch `main`, folder `/ (root)`. The site then rebuilds on every
  merge to `main`.
