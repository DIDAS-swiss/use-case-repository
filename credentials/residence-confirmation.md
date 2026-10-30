---
id: residence-confirmation
title: Residence confirmation
title_de: Wohnsitzbestätigung
title_fr: Attestation de domicile
title_it: Attestazione di domicilio
stage: signal
supply: emerging
ambition_level: AL2
likely_issuer: Municipal residents' registration office (Einwohnerkontrolle)
issuer_type: municipal
schema_refs: []
used_by: [vehicle-leasing]
demand_issues: []
created: 2026-10-30
updated: 2026-10-30
---

# Residence confirmation

## What it attests

That a person is registered as resident at an address in a municipality, and since when. It replaces the paper residence confirmation.

## Issuer and mandate

The municipal residents' registration office keeps the residents' register. Depending on the canton, a cantonal platform may issue on its behalf.

## Claims (indicative)

| Claim | Description | Needed by |
|---|---|---|
| Current address | Street, postcode, municipality | vehicle leasing |
| Residence since | Date of moving in | vehicle leasing |

These claims are indicative. The authoritative schema is defined in I14Y, eCH or
a sectoral repository, not here.

## Schema and semantic references

None published yet.

## Supply status

`emerging`: the pre-study's illustrative mapping shows it with a cantonal issuer. No production issuance is confirmed in this repository yet.

## Demand

Needed by [vehicle leasing](../use-cases/vehicle-leasing.md). Deliberately **excluded** in [motor vehicle claims processing](../use-cases/motor-vehicle-claims-processing.md).

## Sources

- [Pre-Study: Swiss Ecosystem Discovery Catalog](https://www.amministrazionedigitalesvizzera.ch/application/files/8317/8999/7309/Pre-Study_Swiss_Ecosystem_Discovery_Catalog_DPSS_June_2026.pdf), DPSS iSVC / Accelerate.swiss, June 2026
