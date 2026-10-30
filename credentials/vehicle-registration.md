---
id: vehicle-registration
title: Vehicle registration
title_de: Fahrzeugausweis
title_fr: Permis de circulation
title_it: Licenza di circolazione
stage: signal
supply: missing
ambition_level: AL2
likely_issuer: Cantonal road traffic office (Strassenverkehrsamt); federal coordination by FEDRO (ASTRA)
issuer_type: cantonal
schema_refs: []
used_by: [vehicle-leasing, motor-vehicle-claims-processing]
demand_issues: []
created: 2026-10-30
updated: 2026-10-30
---

# Vehicle registration

## What it attests

That a vehicle is registered for road traffic, to which holder, under which plate. It is the digital counterpart of the vehicle registration document.

## Issuer and mandate

The cantonal road traffic offices register vehicles under the Road Traffic Act (SVG). The federal vehicle register is run by the Federal Roads Office (FEDRO/ASTRA).

## Claims (indicative)

| Claim | Description | Needed by |
|---|---|---|
| Holder | Registered holder of the vehicle | both use cases |
| Vehicle identification | VIN, make, model | both use cases |
| Plate | Licence plate | both use cases |

These claims are indicative. The authoritative schema is defined in I14Y, eCH or
a sectoral repository, not here.

## Schema and semantic references

None published yet.

## Supply status

`missing`: no issuer known. It appears on the pre-study's gap-board mockup as an open request (illustrative score 94, "blocks 2 use cases").

## Demand

Created in [vehicle leasing](../use-cases/vehicle-leasing.md) and **reused** in [motor vehicle claims processing](../use-cases/motor-vehicle-claims-processing.md). One issuer decision unblocks both.

## Sources

- [Pre-Study: Swiss Ecosystem Discovery Catalog](https://www.amministrazionedigitalesvizzera.ch/application/files/8317/8999/7309/Pre-Study_Swiss_Ecosystem_Discovery_Catalog_DPSS_June_2026.pdf), DPSS iSVC / Accelerate.swiss, June 2026
