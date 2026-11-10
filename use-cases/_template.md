---
id: short-outcome-name
title: Short outcome name
title_de:
title_fr:
title_it:
stage: signal          # new entries start at signal; see GOVERNANCE.md for the stages
ambition_levels: [AL2] # one or more of AL1, AL2, AL3
sectors: []   # ISIC Rev. 5 ids from _data/sectors.csv, e.g. [ISIC-65, ISIC-84]
domain_steward: vacant # a name from STEWARDS.md, or vacant
proposed_by:
intake_issue:          # number of the use-case candidate issue
credentials_reused: []   # credential ids from credentials/, taken over from another use case or issuer
credentials_new: []      # credential ids this use case newly requires
credentials_excluded: [] # credential ids deliberately not requested (data minimisation)
related_use_cases: []      # related use cases with no sequence
upstream_use_cases: []     # use cases that must happen first: they issue a credential this one verifies
downstream_use_cases: []   # use cases that reuse a credential this one issues
lighthouse:                # selected | candidate | empty: the curator-recorded decision (see GOVERNANCE.md, Lighthouses)
lighthouse_basis:          # one line on why, e.g. "meets 5 of 6 criteria"
lighthouse_decision_record: # for selected: link to the decision (approver, date, criteria assessed)
evidence_status:           # hypothesis | documented need | design | prototype | pilot | production
dependencies: []           # shared dependencies on dependencies.md, e.g. [e-id]
trust_flows: []        # Trust Flow ids from _data/trust-flows.csv, e.g. health/immunization/F-02
ifm_patterns: []       # Industry Function Graph pattern ids from _data/ifm-patterns.csv
implementations: []    # "<url> (<how far: demo, sandbox, pilot, production>)"
glossary_terms: []     # DIDAS Glossary term anchors, e.g. issuer, verifier
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Short outcome name

## Summary

In up to 70 words: who decides what, which evidence they need, and what is
difficult today. Keep a proposed change conditional ("could") unless it is
demonstrated.

## Facts to prove

The decision the verifier takes, and the minimum facts it needs proven to take
it. State each fact as a claim, for example "the applicant has no open debt
enforcement proceedings", rather than as a document. Say what the evidence does
not establish (freshness, completeness, authority, legal title) where it matters.

## Actors and roles

| Role | Actor | Organisation type | Notes |
|---|---|---|---|
| Holder | | person / organisation | |
| Verifier | | | |
| Issuer | | | |
| Governing authority | | | |

## Process flow

| # | Actor | Action | Credential |
|---|---|---|---|
| 1 | | | |

Where a trust flow in `trust_flows` models a step, name it in the action, for
example "(F-02)".

## Credentials

| Credential | In this use case | Claims needed | Supply | Why |
|---|---|---|---|---|
| [name](../credentials/id.md) · [I14Y](https://www.i14y.admin.ch/de/catalog/datasets/urn:vct:…/description) | reused / new / excluded | | available / emerging / missing | |

Link the credential's I14Y dataset next to it wherever it is published there.
A credential without an entry in `credentials/` gets one in the same pull request.

## Governance and trust context

- **Legal basis**:
- **Trust frameworks and registries**:
- **Verifier governance**: declared purpose and data request
- **Sensitive attributes**:

## Demand and value

- **Expected benefit (hypothesis | reported | measured)**: the current activity that would change
- **Relying parties**: who would verify
- **Indicative scale**: interactions per year, with source and date; leave out if not known
- **Value**: anything else that becomes possible

## Evidence status

One of hypothesis, documented need, design, prototype, pilot, production, for
the proposed exchange (not the existing paper process), with the source that
shows it. Publication of this entry is not evidence of qualification or
production readiness.

## Background

Legal and programme context, project-specific dates. Shared dependencies such as
the timing of the state e-ID are on [dependencies.md](../dependencies.md), not
repeated here.

## Open questions

What remains unknown, asked once, and who has to act for this use case to move
to the next stage.

## Sources

-
