---
id: motor-vehicle-liability-insurance-confirmation
title: Motor vehicle liability insurance confirmation
title_de: Versicherungsnachweis Motorfahrzeug-Haftpflicht
title_fr: Attestation d'assurance responsabilité civile véhicule
title_it: Attestato d'assicurazione responsabilità civile veicoli
stage: signal
supply: missing
ambition_level: AL3
likely_issuer: Motor vehicle liability insurers; schema coordination by the Swiss Insurance Association (SVV)
issuer_type: private
schema_refs: []
used_by: [vehicle-leasing, motor-vehicle-claims-processing]
demand_issues: []
created: 2026-10-30
updated: 2026-10-30
---

# Motor vehicle liability insurance confirmation

## What it attests

That a vehicle is covered by the mandatory motor vehicle liability insurance, by which insurer, under which policy and for which period.

## Issuer and mandate

Insurers issue the cover. Liability insurance is mandatory under the Road Traffic Act (SVG). A shared schema would need sector coordination, for example through the SVV.

## Claims (indicative)

| Claim | Description | Needed by |
|---|---|---|
| Insurer | | both use cases |
| Policy | Policy number | both use cases |
| Vehicle | Plate or vehicle identification | both use cases |
| Validity | Period of cover | both use cases |

These claims are indicative. The authoritative schema is defined in I14Y, eCH or
a sectoral repository, not here.

## Schema and semantic references

None published yet.

## Supply status

`missing`: no issuer known. It appears on the pre-study's gap-board mockup as an open request (illustrative score 88, "blocks 2 use cases"). Today insurers already transmit cover electronically to the road traffic offices; whether that becomes a holder credential is open.

## Demand

Created in [vehicle leasing](../use-cases/vehicle-leasing.md) and **reused** in [motor vehicle claims processing](../use-cases/motor-vehicle-claims-processing.md).

## Sources

- [Pre-Study: Swiss Ecosystem Discovery Catalog](https://www.amministrazionedigitalesvizzera.ch/application/files/8317/8999/7309/Pre-Study_Swiss_Ecosystem_Discovery_Catalog_DPSS_June_2026.pdf), DPSS iSVC / Accelerate.swiss, June 2026
