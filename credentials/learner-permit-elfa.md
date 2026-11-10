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
schema_refs: []
used_by: []
demand_issues: []
created: 2026-11-10
updated: 2026-11-10
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
of March 2027.

## Claims (indicative)

| Claim | Description | Needed by |
|---|---|---|
| Holder identity | Name, date of birth, photo | carsharing for learner drivers, traffic control |
| Category | Vehicle category of the permit, for example B | carsharing for learner drivers |
| Validity | Valid from and until, status | all |

These claims are indicative. The authoritative schema is the issuer's.

## Schema and semantic references

Not published on [I14Y](https://www.i14y.admin.ch/): no learner's permit or
driving licence dataset is in the I14Y catalogue (checked 2026-11-10, 2,669
datasets). A schema exists on the issuer side and has been shared with DIDAS;
it is not public, so `schema_status` is `emerging`. Once it is on I14Y, set
`i14y_dataset` and `i14y_id` and the schema is federated into this repository.

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
- DIDAS, 10 November 2026: about 100,000 active eLFA
