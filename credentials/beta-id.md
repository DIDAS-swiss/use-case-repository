---
id: beta-id
title: Beta-ID
title_de: Beta-ID
title_fr: Bêta-ID
title_it: Beta-ID
stage: candidate
supply: available
schema_status: i14y
ambition_level: AL1
likely_issuer: Federal Office of Police (fedpol), through the Beta Credential Service (BCS)
issuer_type: federal
vct_values: ["urn:vct:ch.admin.bcs.betaid", "betaid-sdjwt"]
i14y_dataset: urn:vct:ch.admin.bcs.betaid
i14y_id: f7223759-b198-41eb-96be-3f3bd54689fb
schema_refs: [https://swiyu-admin-ch.github.io/cookbooks/how-to-use-beta-id/]
claims: [family_name, given_name, birth_date, age_over_16, age_over_18, age_over_65, age_birth_year, sex, place_of_origin, birth_place, nationality, portrait, personal_administrative_number, additional_person_info, document_number, issuance_date, expiry_date, reference_id_type, referende_id_expiry_date, verification_type, verification_organization, issuing_authority, issuing_country]
used_by: []
demand_issues: []
created: 2026-11-05
updated: 2026-11-05
---

# Beta-ID

> **Test credential.** The Beta-ID is a pseudo-credential of the swiyu Public
> Beta. Its values are self-declared and unchecked, so it is **not a proof of
> identity** and must not be used as one in productive business cases. It is
> listed here because it carries the same attributes as the
> [Swiss e-ID](swiss-e-id.md), which makes it the credential to build and pilot
> use cases with until the e-ID is issued.

## What it attests

Nothing about the person. A verified Beta-ID presentation establishes only that
the Beta Credential Service issued it, that it is unaltered and that it has not
been revoked. Its value lies in its **structure**: the attribute set of the
coming e-ID, so that verifiers can integrate, test and simulate use cases early.

## Issuer and mandate

Issued, verified and revoked by the Beta Credential Service
([BCS](https://www.bcs.admin.ch/bcs-web)) of the e-ID implementation programme.
The I14Y dataset is published by fedpol. After issuance the BCS keeps only the
Beta-ID number, for revocation; revocation cannot be reverted.

## Claims (indicative)

| Claim | Description | Needed by |
|---|---|---|
| `family_name` | Surname | testing the identification step of any use case |
| `given_name` | Given name(s) | testing the identification step of any use case |
| `birth_date` | Date of birth | testing the identification step of any use case |
| `age_over_16` | Over the age of 16 | testing age checks |
| `age_over_18` | Over the age of 18 | testing age checks |
| `age_over_65` | Over the age of 65 | testing age checks |
| `age_birth_year` | Year of birth | testing age checks |
| `sex` | Sex |  |
| `place_of_origin` | Place of origin |  |
| `birth_place` | Place of birth |  |
| `nationality` | Nationality |  |
| `portrait` | Face image | testing the identification step of any use case |
| `personal_administrative_number` | AHV number (protected field) |  |
| `additional_person_info` | Additional information about the person |  |
| `document_number` | Beta-ID number |  |
| `issuance_date` | Date of issuance |  |
| `expiry_date` | Date of expiry |  |
| `reference_id_type` | Identification document type |  |
| `referende_id_expiry_date` | Identification document date of expiry (I14Y spelling) |  |
| `verification_type` | Identity verification process |  |
| `verification_organization` | Identity verification by |  |
| `issuing_authority` | Issuing authority |  |
| `issuing_country` | Issuing country |  |

The full attribute list, with labels, types and the I14Y concepts each attribute
conforms to, is the federated schema below.

## Schema and semantic references

- **I14Y**: dataset
  [`urn:vct:ch.admin.bcs.betaid`](https://www.i14y.admin.ch/de/catalog/datasets/urn:vct:ch.admin.bcs.betaid/description),
  published by fedpol. The schema is federated into this repository:
  [`federation/i14y/beta-id/`](../federation/i14y/beta-id/).
- **Credential type** (`vct`): `urn:vct:ch.admin.bcs.betaid`, active since
  2026-06-25. The earlier value `betaid-sdjwt` remains in use during migration,
  so verifier queries list both.
- **Format**: SD-JWT VC under the Swiss Profile. The technical claims `vct`,
  `iss`, `cnf`, `iat` and `status` are not selectively disclosable and are not
  part of the I14Y structure.
- **Naming difference**: I14Y publishes the attribute as `referende_id_expiry_date`;
  the issued credential, per the swiyu cookbook, uses `reference_id_expiry_date`.
  Verifiers should query the name the credential carries. Worth reporting to
  the dataset's I14Y contact.
- **Glossary**: [Beta-ID](https://didas-swiss.github.io/didas-glossary/#term:beta-id).

## Supply status

`available` in the swiyu **Public Beta** (test environment): anyone can obtain a
Beta-ID from the BCS. There is no production issuance, by design.

## Demand

Not relied on by any use case as evidence. It is the test stand-in for the
[Swiss e-ID](swiss-e-id.md) in pilots of
[vehicle leasing](https://github.com/DIDAS-swiss/use-case-repository/issues/123) and
[motor vehicle claims processing](https://github.com/DIDAS-swiss/use-case-repository/issues/83).

## Sources

- [I14Y dataset urn:vct:ch.admin.bcs.betaid](https://www.i14y.admin.ch/de/catalog/datasets/urn:vct:ch.admin.bcs.betaid/description), retrieved through the public I14Y API on 2026-11-05
- [How to use Beta-ID for my business](https://swiyu-admin-ch.github.io/cookbooks/how-to-use-beta-id/), swiyu cookbook
- [swiyu release note, 2026-06-25](https://swiyu-admin-ch.github.io/2026/06/25/new-versions-released.html): `vct` activation
- [DIDAS Glossary: Beta-ID](https://didas-swiss.github.io/didas-glossary/#term:beta-id)
