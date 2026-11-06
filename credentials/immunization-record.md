---
id: immunization-record
title: Immunization record
title_de: Impfeintrag
title_fr: Vaccination
title_it: Vaccinazione
stage: signal
supply: emerging
schema_status: emerging
ambition_level: AL3
likely_issuer: The vaccinator that administered the dose (GP practice, pharmacy with a vaccination permit, company medical service)
issuer_type: private
schema_refs: [https://github.com/DIDAS-swiss/digital-health_swiyu/blob/main/docs/credentials/immunization.md, https://github.com/DIDAS-swiss/digital-health_swiyu/blob/main/config/praxis/credentials/health-immunization-sd-jwt/schema.json, http://fhir.ch/ig/ch-vacd/StructureDefinition/ch-vacd-immunization]
used_by: [vaccination-record]
demand_issues: []
created: 2026-11-05
updated: 2026-11-05
---

# Immunization record

## What it attests

That one dose of a vaccine against one or more diseases was administered to a
person on a date, as dose *n* of a series, by a named practitioner and
organisation. **One credential per dose**, so each dose keeps its own author and
each issuer can revoke only its own assertion. It replaces the entry in the paper
vaccination booklet.

## Issuer and mandate

The party that administered the dose. Who may vaccinate follows from the
Epidemics Act (EpG/LEp) together with professional, therapeutic-products and
cantonal law: GP practices, pharmacies with a vaccination permit, company
medical services. No governing authority yet grants the vaccinator role on the
trust infrastructure (see the use case).

## Claims (indicative)

| Claim | Description | Needed by |
|---|---|---|
| `target_disease` | Diseases protected against (SNOMED CT) | vaccination record (travel clinic) |
| `occurrence_date` | Date given | vaccination record (travel clinic) |
| `dose_number`, `doses_in_series` | Position in the series | vaccination record (travel clinic) |
| `vaccine_code`, `vaccine_name`, `lot_number`, `route`, `site`, `next_dose_due` | The product and its administration | practice, pharmacy |
| `patient_given_name`, `patient_family_name`, `patient_birth_date` | The subject | practice |
| `performer_name`, `performer_gln`, `organization_name`, `country`, `immunization_id` | Who recorded it, where | practice |

18 claims in all, every one selectively disclosable under the Swiss Profile.

## Schema and semantic references

- **Not published on [I14Y](https://www.i14y.admin.ch/)** (checked 2026-11-05).
- **Showcase definition**: credential type `urn:vct:ch.didas.health.immunization:1.0`,
  SD-JWT VC under `swiss-profile-vc:1.0.0`, with
  [definition](https://github.com/DIDAS-swiss/digital-health_swiyu/blob/main/docs/credentials/immunization.md),
  [JSON Schema](https://github.com/DIDAS-swiss/digital-health_swiyu/blob/main/config/praxis/credentials/health-immunization-sd-jwt/schema.json),
  [Type Metadata](https://github.com/DIDAS-swiss/digital-health_swiyu/blob/main/config/praxis/credentials/health-immunization-sd-jwt/vct.json) and
  [OCA bundle](https://github.com/DIDAS-swiss/digital-health_swiyu/blob/main/config/praxis/credentials/health-immunization-sd-jwt/oca.json).
- **Clinical models**: HL7 FHIR `Immunization`, profile
  [CH VACD](http://fhir.ch/ig/ch-vacd/StructureDefinition/ch-vacd-immunization);
  openEHR `openEHR-EHR-ACTION.medication.v1`. The mappings are the showcase's own
  and unreviewed by the standards bodies.

## Supply status

`emerging`: implemented and tested in the showcase against a mock of the swiyu
components, Sandbox only. No vaccinator issues it in production.

## Demand

Needed by [vaccination record](../use-cases/vaccination-record.md), requested by
practices, pharmacies and travel clinics, later by research and coverage
monitoring.

## Sources

- [Immunization Record credential definition](https://github.com/DIDAS-swiss/digital-health_swiyu/blob/main/docs/credentials/immunization.md), digital-health_swiyu at commit `6636357`
- [F-02](https://github.com/DIDAS-swiss/digital-health_swiyu/blob/main/flows/F-02-immunization-issuance.md) and [F-03](https://github.com/DIDAS-swiss/digital-health_swiyu/blob/main/flows/F-03-immunization-minimal-disclosure.md)
