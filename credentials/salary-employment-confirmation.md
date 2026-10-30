---
id: salary-employment-confirmation
title: Salary and employment confirmation
title_de: Lohn- und Arbeitsbestätigung
title_fr: Attestation de salaire et d'emploi
title_it: Attestazione di salario e d'impiego
stage: signal
supply: missing
ambition_level: AL3
likely_issuer: Employer, with schema coordination by a sector body (the pre-study mockup names an eCH working group, SAV and SGV)
issuer_type: private
schema_refs: []
used_by: [vehicle-leasing]
demand_issues: []
created: 2026-10-30
updated: 2026-10-30
---

# Salary and employment confirmation

## What it attests

That a person is employed by an employer, in which capacity, and with which income or income band.

## Issuer and mandate

The employer holds the data. A shared schema needs sector coordination, so that thousands of employers issue the same credential.

## Claims (indicative)

| Claim | Description | Needed by |
|---|---|---|
| Employer | Name and identifier of the employer | vehicle leasing |
| Employment status | Employed since, permanent or temporary | vehicle leasing |
| Income band | Income range rather than the exact salary | vehicle leasing |

These claims are indicative. The authoritative schema is defined in I14Y, eCH or
a sectoral repository, not here.

## Schema and semantic references

None published yet.

## Supply status

`missing`: no issuer known. It appears on the pre-study's gap-board mockup as an open credential request with target 2027 (illustrative).

## Demand

Needed by [vehicle leasing](../use-cases/vehicle-leasing.md). Deliberately **excluded** in [motor vehicle claims processing](../use-cases/motor-vehicle-claims-processing.md).

## Sources

- [Pre-Study: Swiss Ecosystem Discovery Catalog](https://www.amministrazionedigitalesvizzera.ch/application/files/8317/8999/7309/Pre-Study_Swiss_Ecosystem_Discovery_Catalog_DPSS_June_2026.pdf), DPSS iSVC / Accelerate.swiss, June 2026
