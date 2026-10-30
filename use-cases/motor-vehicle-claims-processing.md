---
id: motor-vehicle-claims-processing
title: Motor vehicle claims processing
title_de: Abwicklung von Motorfahrzeugschäden
title_fr: Traitement des sinistres de véhicules à moteur
title_it: Gestione dei sinistri di veicoli a motore
stage: signal
ambition_levels: [AL1, AL2, AL3]
sectors: [insurance, mobility, public-safety]
domain_steward: vacant
proposed_by: DIDAS (seeded from the DPSS pre-study flow work)
intake_issue:
credentials_reused: [swiss-e-id, vehicle-registration, motor-vehicle-liability-insurance-confirmation]
credentials_new: [accident-report, repair-assessment]
credentials_excluded: [residence-confirmation, debt-enforcement-extract, salary-employment-confirmation]
related_use_cases: [vehicle-leasing]
glossary_terms: [issuer, verifier, wallet, selective-disclosure]
created: 2026-10-30
updated: 2026-10-30
---

# Motor vehicle claims processing

> **Seed entry.** This use case is the pre-study's main illustrative example
> (§4.2, §4.3). It "demonstrates cross-sectoral credential reuse, schema reuse and
> trust resolution across federal, cantonal and private-sector actors". The flow
> and credential mapping follow the pre-study's *illustrative* mockups and stay at
> stage `signal` until a domain steward confirms them.

## Summary

After a road accident, the claimant reports the damage to the motor vehicle
liability insurer. The insurer has to establish who the claimant is, which vehicle
and policy are involved, what happened and what the repair will cost, before it
approves and settles the claim. Most of the identity, vehicle and policy facts
were already issued as credentials in an earlier journey, such as
[vehicle leasing](vehicle-leasing.md). The pre-study's finding is that **this reuse
only creates value when it is visible at use-case level** (§4.4, finding 3).

## Outcome: what must be proven

The insurer decides whether to approve the claim, and for how much. To do so it
needs proof that:

- the claimant is who they claim to be
- the vehicle is registered and identified
- a valid motor vehicle liability policy covers the vehicle
- the accident happened as reported
- the repair cost has been assessed by a qualified party

## Actors and roles

| Role | Actor | Organisation type | Notes |
|---|---|---|---|
| Holder | Claimant | person | Driver or vehicle holder |
| Verifier | Insurance company | private | Decides on the claim |
| Issuer | fedpol | federal | Swiss e-ID (reused) |
| Issuer | Cantonal road traffic office | cantonal | Vehicle registration (reused) |
| Issuer | Insurance company | private | Policy confirmation (reused); settlement confirmation |
| Issuer | Cantonal police | cantonal | Accident report |
| Issuer | Certified garage or expert | private | Repair assessment |
| Governing authority | FINMA | federal | Supervision of insurers (illustrative mockup) |
| Governing authority | Swiss Insurance Association (SVV) | sectoral | Sector-level coordination (illustrative mockup) |

## Process flow

This is the pre-study's illustrative "claims process flow" (§4.2):

| # | Actor | Action | Credential |
|---|---|---|---|
| 1 | Claimant | Reports the accident | Accident report |
| 2 | Insurer | Requests identity, vehicle and policy | |
| 3 | Claimant | Presents from the wallet | Swiss e-ID, vehicle registration, insurance confirmation |
| 4 | Insurer | Verifies the presentations against the trust registry | |
| 5 | Garage or expert | Issues the repair assessment | Repair assessment |
| 6 | Insurer | Approves the claim and issues the settlement | Settlement confirmation |
| 7 | | Claim settled and payment issued | |

## Credentials

| Credential | In this use case | Claims needed | Supply | Why |
|---|---|---|---|---|
| [Swiss e-ID](../credentials/swiss-e-id.md) | reused | name, date of birth | emerging | Identify the claimant |
| [Vehicle registration](../credentials/vehicle-registration.md) | reused (from leasing) | holder, vehicle identification, plate | missing | Identify the vehicle |
| [Motor vehicle liability insurance confirmation](../credentials/motor-vehicle-liability-insurance-confirmation.md) | reused (from leasing) | insurer, policy, vehicle, validity | missing | Confirm cover |
| [Accident report](../credentials/accident-report.md) | new | date, place, parties, vehicles, circumstances | missing | Establish the facts |
| [Repair assessment](../credentials/repair-assessment.md) | new | vehicle, damage, estimated cost, assessor | missing | Establish the amount |
| [Residence confirmation](../credentials/residence-confirmation.md) | **excluded** | | | Not needed for the claim decision |
| [Debt enforcement register extract](../credentials/debt-enforcement-extract.md) | **excluded** | | | Not needed for the claim decision |
| [Salary and employment confirmation](../credentials/salary-employment-confirmation.md) | **excluded** | | | Not needed for the claim decision |

The exclusions are deliberate. They record that the insurer does not ask for the
creditworthiness data the leasing journey collected, which is the data
minimisation the pre-study asks to make operational (§4.4, finding 3).

The pre-study mockup also shows a **settlement confirmation** issued by the insurer.
It has no entry yet because no other use case relies on it.

## Governance and trust context

- **Legal basis** *(to be confirmed by a domain steward)*: the Road Traffic Act
  (SVG, SR 741.01) for liability and mandatory insurance; the Insurance
  Supervision Act (VAG) for insurers; the e-ID Act (BGEID) for the e-ID.
- **Trust frameworks and registries**: swiyu Trust Registry for issuer
  recognition. Sector governance for insurance-issued credentials is to be
  defined.
- **Verifier governance**: the insurer registers its declared data queries and
  purposes (pre-study §5.2).
- **Sensitive attributes**: accident circumstances can include health
  information. A health-related claim would need separate treatment.

## Demand and value

- **Relying parties**: motor vehicle insurers
- **Indicative scale**: not yet known. The pre-study gap-board mockup shows
  "~60K p.a." per credential as an *illustrative* value only.
- **Value**: faster claims handling; fewer manual checks; reuse of credentials
  that already exist instead of new data requests

## Coordination needs and open questions

- Accident report: is the cantonal police the right issuer for all accidents, or
  only for those with police involvement? What about the jointly signed European
  accident statement?
- Repair assessment: which body certifies the garages or experts entitled to issue
  it?
- Vehicle registration and insurance confirmation are both blocked here *and* in
  vehicle leasing. A single issuer decision unblocks two use cases.
- Is there a domain steward for motor insurance (AL3)?

## Sources

- [Pre-Study: Swiss Ecosystem Discovery Catalog](https://www.amministrazionedigitalesvizzera.ch/application/files/8317/8999/7309/Pre-Study_Swiss_Ecosystem_Discovery_Catalog_DPSS_June_2026.pdf),
  DPSS iSVC / Accelerate.swiss, June 2026: §4.2 (illustrative use-case view),
  §4.3 (gap-board mockups), §4.4 (findings)
- [Federal Council's additional measures for the e-ID, 25 February 2026](https://www.eid.admin.ch/en/akzeptanz-der-e-id-mit-zusaetzlichen-massnahmen-staerken-e)
