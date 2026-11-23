---
id: learner-permit-elfa
title: Electronic learner's permit (eLFA)
title_de: Elektronischer Lernfahrausweis (eLFA)
title_fr: Permis d'élève conducteur électronique
title_it: Licenza per allievo conducente elettronica
stage: signal
supply: available
schema_status: emerging
ambition_level: AL2
likely_issuer: Cantonal road traffic office (Strassenverkehrsamt), in the federal pilot run with asa
issuer_type: cantonal
vct_values: ["urn:vct:ch.admin.astra.vz.elfa"]
schema_refs: ["https://vz-api.astra.admin.ch/public/issuer/oid4vci/json-schema/elfa"]
claims: [lastName, firstName, dateOfBirth, hometown, photoImage, signatureImage, categoryCode, categoryIcon, categoryRestrictions, restrictionsA, restrictionsB, licenceNumber, faberPin, issuerEntity, issuerEntityDate, dateOfExpiration, policeQRImage, vct, iss, sub, iat, nbf, exp, cnf, status]
used_by: []
demand_issues: []
created: 2026-11-10
updated: 2026-11-16
---

# Electronic learner's permit (eLFA)

## What it attests

That the holder has a valid learner's permit for a vehicle category, issued by
the cantonal road traffic office after the theory test. It is the digital form
of the paper learner's permit and is valid in all of Switzerland and in
Liechtenstein.

## Issuer and mandate

The cantonal road traffic offices issue it into the swiyu wallet, by QR code or
SMS link, after the theory test. The eLFA is a pilot of the Confederation,
developed with the association of road traffic offices (asa) under an ASTRA
directive in effect since 1 September 2024; its evaluation runs until the end
of March 2027. Under that directive (section C) the eLFA alone proves the entitlement to
drive within Switzerland and Liechtenstein, not across other borders; the paper
permit need not be carried.

## Claims

From the issuer's published JSON Schema (draft 2020-12), as fetched on
16 November 2026. *Required* is the schema's own `required` list.

| Claim | Type | Required | Meaning (DIDAS reading of the name) |
|---|---|---|---|
| `lastName` | string | yes | Holder's name |
| `firstName` | string | yes | Holder's name |
| `dateOfBirth` | string | yes | Holder's date of birth |
| `hometown` | string | yes | Place of origin (Heimatort) |
| `photoImage` | string | yes | Holder's photo |
| `signatureImage` | string | yes | Holder's signature image |
| `categoryCode` | string | yes | Vehicle category of the permit, for example B |
| `categoryIcon` | string | yes | Pictogram of the category |
| `categoryRestrictions` | string | yes | Restrictions on the permit |
| `restrictionsA` | string | yes | Restrictions on the permit |
| `restrictionsB` | string | yes | Restrictions on the permit |
| `licenceNumber` | string | yes | Permit number |
| `faberPin` | number | yes | Holder's number in the federal register of driving licences (FABER) |
| `issuerEntity` | string | yes | Issuing road traffic office and issue date |
| `issuerEntityDate` | string | yes | Issuing road traffic office and issue date |
| `dateOfExpiration` | string | yes | End of validity |
| `policeQRImage` | string | no | QR code for police checks |
| `vct` | string | yes | Credential type and issuer (SD-JWT VC registered claims) |
| `iss` | string | yes | Credential type and issuer (SD-JWT VC registered claims) |
| `sub` | string / number | no | Subject, issued at, not before, expiry |
| `iat` | string / number | no | Subject, issued at, not before, expiry |
| `nbf` | string / number | no | Subject, issued at, not before, expiry |
| `exp` | string / number | no | Subject, issued at, not before, expiry |
| `cnf` | object | no | Holder key binding |
| `status` | object | no | Status reference (revocation) |

What the schema means for the use cases:

- There is **no age-over claim** (such as `age_over_18`): a verifier that needs
  only an age threshold receives the full `dateOfBirth` if it asks for age
  ([#52](https://github.com/DIDAS-swiss/use-case-repository/issues/52)).
- `categoryCode` and the restriction claims carry what a carsharing provider
  checks for a learner driver
  ([#76](https://github.com/DIDAS-swiss/use-case-repository/issues/76)); the
  accompanying driver is not part of this credential.
- The meanings in the last column are read from the claim names; the schema
  gives types only. The issuer's documentation is authoritative.

## Schema and semantic references

- **Published by the issuer:** [JSON Schema for the eLFA](https://vz-api.astra.admin.ch/public/issuer/oid4vci/json-schema/elfa) at ASTRA's
  OpenID4VCI issuer endpoint (`application/schema+json`). This repository keeps
  the reference, not a copy.
- **Not on [I14Y](https://www.i14y.admin.ch/):** no learner's permit or driving
  licence dataset is in the I14Y catalogue (rechecked 2026-11-16, 2,673
  datasets; still only two credential datasets). So `schema_status` is
  `emerging`: a schema is published, but not on the national catalogue.
  Publication on I14Y is being clarified (noted on
  [#76](https://github.com/DIDAS-swiss/use-case-repository/issues/76),
  13 November 2026). Once it
  is on I14Y, set `i14y_dataset` and `i14y_id` and the schema is federated into
  this repository.

## Supply status

`available`: in live use in all cantons since 1 December 2025 (BJ,
participation meeting of 5 December 2025: about 27,000 issued by then). DIDAS
reports about **100,000 active eLFA** as of 10 November 2026; no public source
for that figure is linked yet. The Confederation still calls it a pilot. Anyone
can check an eLFA with ASTRA's [LicenceCheck](https://licencecheck.astra.admin.ch/).

## Demand

Needed by [learner-driver carsharing](https://github.com/DIDAS-swiss/use-case-repository/issues/76).
Checked at traffic stops through LicenceCheck; the traffic-control use case
([#40](https://github.com/DIDAS-swiss/use-case-repository/issues/40)) is about
the full driving licence and lists the eLFA as excluded. Also considered as an
age-proof option ([#52](https://github.com/DIDAS-swiss/use-case-repository/issues/52)).

## Sources

- [eid.admin.ch – Elektronischer Lernfahrausweis (eLFA)](https://www.eid.admin.ch/de/pilotprojekte), accessed 2026-11-10 (site no longer maintained since 27 October 2026): "Der eLFA ist ein Pilotprojekt des Bundes. Er wurde zusammen mit der Vereinigung der Strassenverkehrsämter asa erarbeitet."
- [swiyu – Anwendungsbeispiele](https://swiyu.admin.ch/de/anwendungsbeispiele), accessed 2026-11-10: digital driving licence and learner's permit
- [ASTRA LicenceCheck](https://licencecheck.astra.admin.ch/)
- [ASTRA – eLFA JSON Schema](https://vz-api.astra.admin.ch/public/issuer/oid4vci/json-schema/elfa), accessed 2026-11-16
- DIDAS, 10 November 2026: about 100,000 active eLFA
