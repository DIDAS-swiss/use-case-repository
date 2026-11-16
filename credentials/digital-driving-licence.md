---
id: digital-driving-licence
title: Digital driving licence
title_de: Digitaler Führerausweis
title_fr: Permis de conduire numérique
title_it: Licenza di condurre digitale
stage: signal
supply: emerging
schema_status: none
ambition_level: AL2
likely_issuer: Cantonal road traffic office (Strassenverkehrsamt); federal coordination by FEDRO (ASTRA)
issuer_type: cantonal
schema_refs: []
used_by: []
demand_issues: []
created: 2026-11-10
updated: 2026-11-10
---

# Digital driving licence

## What it attests

That the holder is entitled to drive vehicles of the listed categories, with
any restrictions, as recorded by the issuing road traffic office. It is the
digital counterpart of the driving licence card; the paper licence is to be
kept.

## Issuer and mandate

Driving licences are issued by the road traffic office of the canton of
residence (SVG Art. 22). Motion 25.4402, asking for a digital driving licence,
was transferred to the Federal Council on 3 June 2026.

## Claims (indicative)

| Claim | Description | Needed by |
|---|---|---|
| Holder identity | Name, date of birth, photo | all |
| Categories | Licence categories and restrictions | traffic control, carsharing, rental, fleet |
| Issue date | Date of first issue per category | rental (licence tenure) |
| Status | Valid, suspended, withdrawn | all |

These claims are indicative. The authoritative schema is defined in I14Y, eCH or
by the issuer, not here.

## Schema and semantic references

Not published on [I14Y](https://www.i14y.admin.ch/) (checked 2026-11-10). The
learner's permit ([eLFA](learner-permit-elfa.md)) is its live predecessor in the
same wallet.

## Supply status

`emerging`: announced as "soon available" on swiyu.admin.ch ("Strassenverkehrsämter
stellen den Führerausweis jetzt auch digital aus"), with traffic control,
carsharing and car rental as the federal use-case examples. No issuance to
licence holders is confirmed yet.

## Demand

Needed by the candidates for traffic control
([#40](https://github.com/DIDAS-swiss/use-case-repository/issues/40)), carsharing
registration ([#45](https://github.com/DIDAS-swiss/use-case-repository/issues/45)),
car rental ([#23](https://github.com/DIDAS-swiss/use-case-repository/issues/23)),
corporate carsharing ([#55](https://github.com/DIDAS-swiss/use-case-repository/issues/55)),
fleet management ([#63](https://github.com/DIDAS-swiss/use-case-repository/issues/63)),
the age-proof option ([#52](https://github.com/DIDAS-swiss/use-case-repository/issues/52))
and, for the accompanying driver, learner-driver carsharing
([#76](https://github.com/DIDAS-swiss/use-case-repository/issues/76)).

## Sources

- [swiyu – Ökosystem](https://swiyu.admin.ch/de/oekosystem), accessed 2026-11-10: "Bald verfügbar: Digitaler Führerausweis"
- [swiyu – Anwendungsbeispiele](https://swiyu.admin.ch/de/anwendungsbeispiele), accessed 2026-11-10: traffic control, carsharing, car rental
