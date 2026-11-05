---
id: swiss-e-id
title: Swiss e-ID
title_de: E-ID
title_fr: e-ID
title_it: Id-e
stage: candidate
supply: emerging
ambition_level: AL1
likely_issuer: Federal Office of Police (fedpol)
issuer_type: federal
schema_refs: []
used_by: [vehicle-leasing, motor-vehicle-claims-processing]
demand_issues: []
created: 2026-10-30
updated: 2026-11-05
---

# Swiss e-ID

## What it attests

The state-issued electronic proof of identity of a person under the e-ID Act
(BGEID). It is the trust anchor of ambition level 1 and the identity credential
most other use cases build on.

## Issuer and mandate

fedpol issues the e-ID under the BGEID, on the federal trust infrastructure
swiyu, which the Federal Office of Justice (FOJ) is building.

## Claims (indicative)

| Claim | Description | Needed by |
|---|---|---|
| Name, given names | | vehicle leasing, motor vehicle claims |
| Date of birth | | vehicle leasing, motor vehicle claims |

The authoritative attribute set is defined by the BGEID and its ordinance.

## Schema and semantic references

No e-ID dataset on [I14Y](https://www.i14y.admin.ch/) yet (checked
2026-11-05). The [Beta-ID](beta-id.md), the e-ID's test credential, carries the
same attributes and is published on I14Y as
[`urn:vct:ch.admin.bcs.betaid`](https://www.i14y.admin.ch/de/catalog/datasets/urn:vct:ch.admin.bcs.betaid/description); its schema is federated in
[`federation/i14y/beta-id/`](../federation/i14y/beta-id/). Reference the e-ID's
own I14Y dataset here once it is published.

## Supply status

`emerging`: the pre-study expects swiyu to go live in the first half of 2027.
This becomes `available` with a reference to the production launch.

## Demand

Used by every seeded use case. It is reused, not newly requested, in each of them.

## Sources

- [Pre-Study: Swiss Ecosystem Discovery Catalog](https://www.amministrazionedigitalesvizzera.ch/application/files/8317/8999/7309/Pre-Study_Swiss_Ecosystem_Discovery_Catalog_DPSS_June_2026.pdf), DPSS iSVC / Accelerate.swiss, June 2026: §1, §9.6
- [e-ID (eid.admin.ch)](https://www.eid.admin.ch/)
