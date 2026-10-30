---
id: vehicle-leasing
title: Vehicle leasing
title_de: Fahrzeugleasing
title_fr: Leasing de véhicules
title_it: Leasing di veicoli
stage: signal
ambition_levels: [AL1, AL2, AL3]
sectors: [mobility, finance, insurance]
domain_steward: vacant
proposed_by: DIDAS (seeded from the DPSS pre-study flow work)
intake_issue:
credentials_reused: [swiss-e-id]
credentials_new: [residence-confirmation, debt-enforcement-extract, salary-employment-confirmation, motor-vehicle-liability-insurance-confirmation, vehicle-registration]
credentials_excluded: []
related_use_cases: [motor-vehicle-claims-processing]
glossary_terms: [issuer, verifier, wallet, ambition-level]
created: 2026-10-30
updated: 2026-10-30
---

# Vehicle leasing

> **Seed entry.** This use case is one of the two journeys the DPSS pre-study
> used to test the Ecosystem Discovery Catalog (§2.4, §4.3). Its credential
> mapping follows the pre-study's *illustrative* mockups. Statuses and issuers
> shown there are design material, not confirmed facts. Everything here is at
> stage `signal` until a domain steward confirms it.

## Summary

A private person leases a vehicle. The leasing company has to identify the
lessee, confirm their residence, check their creditworthiness and income, and
make sure the vehicle is insured and registered before handover. Today this is
assembled from paper extracts, uploads and self-declaration. With verifiable
credentials, the lessee presents each fact once from their
[wallet](https://didas-swiss.github.io/didas-glossary/#term:wallet), and the
registration and insurance credentials created here can be reused later, for
example in [motor vehicle claims processing](motor-vehicle-claims-processing.md).

## Outcome: what must be proven

The leasing company decides whether to conclude the leasing contract and hand
over the vehicle. To do so it needs proof that:

- the applicant is who they claim to be
- the applicant lives at the declared address
- the applicant has no open debt enforcement proceedings, or only acceptable ones
- the applicant's income supports the leasing instalments
- the vehicle has the mandatory motor vehicle liability insurance
- the vehicle is registered

## Actors and roles

| Role | Actor | Organisation type | Notes |
|---|---|---|---|
| Holder | Lessee | person | |
| Verifier | Leasing company | private | Decides on the contract |
| Issuer | fedpol | federal | Swiss e-ID |
| Issuer | Municipal residents' registration office | municipal / cantonal | Residence confirmation |
| Issuer | Debt enforcement office | cantonal | Debt enforcement register extract |
| Issuer | Employer | private / public | Salary and employment confirmation |
| Issuer | Motor vehicle insurer | private | Insurance confirmation |
| Issuer | Cantonal road traffic office | cantonal | Vehicle registration |
| Governing authority | to be confirmed | | Sectoral governance for leasing; FOJ for the trust infrastructure |

## Process flow

| # | Actor | Action | Credential |
|---|---|---|---|
| 1 | Lessee | Applies for a lease and identifies | Swiss e-ID |
| 2 | Leasing company | Requests proof of residence and creditworthiness | Residence confirmation, debt enforcement extract |
| 3 | Leasing company | Requests proof of income for the affordability check | Salary and employment confirmation |
| 4 | Leasing company | Verifies the presentations against the swiyu trust registry and concludes the contract | |
| 5 | Insurer | Issues the motor vehicle liability insurance confirmation | Insurance confirmation (new) |
| 6 | Road traffic office | Registers the vehicle | Vehicle registration (new) |
| 7 | Lessee | Holds registration and insurance credentials for later reuse | |

The order of steps 5 and 6, and who holds the vehicle registration credential
(lessee or leasing company as owner), are open questions.

## Credentials

| Credential | In this use case | Claims needed | Supply | Why |
|---|---|---|---|---|
| [Swiss e-ID](../credentials/swiss-e-id.md) | reused | name, date of birth | emerging | Identification of the lessee |
| [Residence confirmation](../credentials/residence-confirmation.md) | new | current address, residence since | emerging | Address verification |
| [Debt enforcement register extract](../credentials/debt-enforcement-extract.md) | new | open proceedings and loss certificates | emerging | Creditworthiness |
| [Salary and employment confirmation](../credentials/salary-employment-confirmation.md) | new | employer, employment status, income band | missing | Affordability check |
| [Motor vehicle liability insurance confirmation](../credentials/motor-vehicle-liability-insurance-confirmation.md) | new | insurer, policy, vehicle, validity | missing | Required for registration |
| [Vehicle registration](../credentials/vehicle-registration.md) | new | holder, vehicle identification, plate | missing | Proof of registration; reused downstream |

"Emerging" and "missing" reflect the pre-study's illustrative mapping and the
pre-launch state of swiyu. Each must be confirmed against the issuer.

## Governance and trust context

- **Legal basis** *(to be confirmed by a domain steward)*: the Consumer Credit Act
  (KKG, SR 221.214.1), which covers consumer leasing and requires a
  creditworthiness check; the Road Traffic Act (SVG, SR 741.01) for mandatory
  liability insurance and vehicle registration; the e-ID Act (BGEID) for the
  e-ID.
- **Trust frameworks and registries**: swiyu Trust Registry for issuer
  recognition and declared verifier requests.
- **Verifier governance**: under the Federal Council's additional measures of
  25 February 2026, the leasing company registers its intended data queries and
  purposes (pre-study §5.2).
- **Sensitive attributes**: income and debt enforcement data. Request only the
  minimum, for example an income band rather than an exact salary.

## Demand and value

- **Relying parties**: leasing companies, and car dealers acting for them
- **Indicative scale**: not yet known
- **Value**: faster onboarding; no paper extracts; reliable data instead of
  self-declaration; registration and insurance credentials that later use cases
  can reuse

## Coordination needs and open questions

- Who issues a salary and employment confirmation, and under which governance? No
  issuer is known yet.
- Can the debt enforcement extract be issued in a minimised form, such as "no open
  proceedings", rather than as a full extract?
- Who is the holder of the vehicle registration credential: the lessee, the
  leasing company as owner, or both?
- Is there a domain steward for leasing (AL3)?

## Sources

- [Pre-Study: Swiss Ecosystem Discovery Catalog](https://www.amministrazionedigitalesvizzera.ch/application/files/8317/8999/7309/Pre-Study_Swiss_Ecosystem_Discovery_Catalog_DPSS_June_2026.pdf),
  DPSS iSVC / Accelerate.swiss, June 2026: §2.4, §4.3 (use-case credential
  mapping mockup), §4.4
- [Federal Council's additional measures for the e-ID, 25 February 2026](https://www.eid.admin.ch/en/akzeptanz-der-e-id-mit-zusaetzlichen-massnahmen-staerken-e)
