---
id: debt-enforcement-extract
title: Debt enforcement register extract
title_de: Betreibungsregisterauszug
title_fr: Extrait du registre des poursuites
title_it: Estratto del registro delle esecuzioni
stage: signal
supply: emerging
ambition_level: AL2
likely_issuer: Cantonal or regional debt enforcement office (Betreibungsamt)
issuer_type: cantonal
schema_refs: []
used_by: [vehicle-leasing]
demand_issues: []
created: 2026-10-30
updated: 2026-10-30
---

# Debt enforcement register extract

## What it attests

Whether debt enforcement proceedings or loss certificates are registered against a person. It replaces the paper extract used for creditworthiness checks.

## Issuer and mandate

The debt enforcement office competent for the person's place of residence keeps the register, under the Debt Enforcement and Bankruptcy Act (SchKG).

## Claims (indicative)

| Claim | Description | Needed by |
|---|---|---|
| Open proceedings | Whether, or how many, proceedings are open | vehicle leasing |
| Loss certificates | Whether loss certificates exist | vehicle leasing |

These claims are indicative. The authoritative schema is defined in I14Y, eCH or
a sectoral repository, not here.

## Schema and semantic references

None published yet.

## Supply status

`emerging`: the pre-study's illustrative mapping shows it with a cantonal issuer. No production issuance is confirmed in this repository yet. A minimised form, such as "no open proceedings", is an open question.

## Demand

Needed by [vehicle leasing](../use-cases/vehicle-leasing.md). Deliberately **excluded** in [motor vehicle claims processing](../use-cases/motor-vehicle-claims-processing.md).

## Sources

- [Pre-Study: Swiss Ecosystem Discovery Catalog](https://www.amministrazionedigitalesvizzera.ch/application/files/8317/8999/7309/Pre-Study_Swiss_Ecosystem_Discovery_Catalog_DPSS_June_2026.pdf), DPSS iSVC / Accelerate.swiss, June 2026
