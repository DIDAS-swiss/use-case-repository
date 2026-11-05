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
i14y_dataset: urn:vct:ch.egovernment.residency-permit-simple
i14y_id: 49ad2ad8-6792-4902-bc0c-c2c3b41fb909
schema_refs: []
used_by: [vehicle-leasing]
demand_issues: []
created: 2026-10-30
updated: 2026-11-05
---

# Residence confirmation

## What it attests

That a person is registered as resident at an address in a municipality, and since when. It replaces the paper residence confirmation.

## Issuer and mandate

The municipal residents' registration office keeps the residents' register. Depending on the canton, a cantonal platform may issue on its behalf.

## Claims (indicative)

| Claim | Description | Needed by |
|---|---|---|
| Current address | Street, postcode, municipality (`dwellingAddress`) | vehicle leasing |
| Residence since | Date of moving in (`moveData/arrival_date`) | vehicle leasing |

The attribute names in brackets are those of the I14Y schema below.

## Schema and semantic references

Published on I14Y as **Einfache Wohnsitzbestätigung**, dataset
[`urn:vct:ch.egovernment.residency-permit-simple`](https://www.i14y.admin.ch/de/catalog/datasets/urn:vct:ch.egovernment.residency-permit-simple/description),
published by Digital Public Services Switzerland (DVS), registration status
*Candidate*. The schema is federated into this repository:
[`federation/i14y/residence-confirmation/`](../federation/i14y/residence-confirmation/).

The pre-study's mockup used the illustrative identifier `ch.schema.residence.simple.v1`;
the published credential type (`vct`) is `urn:vct:ch.egovernment.residency-permit-simple`.

## Supply status

`emerging`: a schema is published on I14Y (status *Candidate*), but no production
issuance is confirmed in this repository yet. The pre-study's illustrative
mapping shows it with a cantonal issuer.

## Demand

Needed by [vehicle leasing](../use-cases/vehicle-leasing.md). Deliberately **excluded** in [motor vehicle claims processing](../use-cases/motor-vehicle-claims-processing.md).

## Sources

- [Pre-Study: Swiss Ecosystem Discovery Catalog](https://www.amministrazionedigitalesvizzera.ch/application/files/8317/8999/7309/Pre-Study_Swiss_Ecosystem_Discovery_Catalog_DPSS_June_2026.pdf), DPSS iSVC / Accelerate.swiss, June 2026
- [I14Y dataset urn:vct:ch.egovernment.residency-permit-simple](https://www.i14y.admin.ch/de/catalog/datasets/urn:vct:ch.egovernment.residency-permit-simple/description), retrieved through the public I14Y API on 2026-11-05
