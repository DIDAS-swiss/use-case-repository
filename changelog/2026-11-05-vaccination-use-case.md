# 2026-11-05: Vaccination use case from digital-health_swiyu

## Added

- `use-cases/vaccination-record.md`: the immunisation journey of the
  [digital-health_swiyu](https://github.com/DIDAS-swiss/digital-health_swiyu)
  showcase (Accelerate GmbH, published by DIDAS): one credential per
  administered dose, presented with minimal disclosure per requesting role
  (a travel clinic receives 4 of 18 claims). Stage `signal`; sectors `ISIC-86`
  and `ISIC-47`
- `credentials/immunization-record.md`: the showcase's credential type
  `urn:vct:ch.didas.health.immunization:1.0`, supply `emerging`, linked to its
  JSON Schema, Type Metadata, OCA bundle and the FHIR CH VACD profile. Not
  published on I14Y (checked 2026-11-05)

## Notes for review

- The showcase runs against a mock of the swiyu components, in the Sandbox only;
  its legal readings (EpG/LEp, BGEID) are its own and need legal review
- The entry records the showcase's main open dependency: no governing authority
  exists for the health domain to grant the vaccinator role and the request
  entitlements
- The e-ID and the Beta-ID are recorded as deliberately excluded: the journey
  needs no identity credential
