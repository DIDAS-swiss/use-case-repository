---
id: beta-id
title: Beta-ID
title_de: Beta-ID
title_fr: Bêta-ID
title_it: Beta-ID
stage: candidate
supply: available
ambition_level: AL1
likely_issuer: Federal Office of Police (fedpol), through the Beta Credential Service (BCS)
issuer_type: federal
i14y_dataset: urn:vct:ch.admin.bcs.betaid
i14y_id: f7223759-b198-41eb-96be-3f3bd54689fb
schema_refs: [https://swiyu-admin-ch.github.io/cookbooks/how-to-use-beta-id/]
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
| Person attributes | `given_name`, `family_name`, `birth_date`, `birth_place`, `place_of_origin`, `sex`, `nationality`, `personal_administrative_number`, `portrait`, `additional_person_info` | testing the identification step of any use case |
| Derived age attributes | `age_over_16`, `age_over_18`, `age_over_65`, `age_birth_year` | testing age checks |
| Document and verification metadata | `document_number`, `issuance_date`, `expiry_date`, `issuing_authority`, `issuing_country`, `reference_id_type`, `reference_id_expiry_date`, `verification_organization`, `verification_type` | |

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
[vehicle leasing](../use-cases/vehicle-leasing.md) and
[motor vehicle claims processing](../use-cases/motor-vehicle-claims-processing.md).

## Sources

- [I14Y dataset urn:vct:ch.admin.bcs.betaid](https://www.i14y.admin.ch/de/catalog/datasets/urn:vct:ch.admin.bcs.betaid/description), retrieved through the public I14Y API on 2026-11-05
- [How to use Beta-ID for my business](https://swiyu-admin-ch.github.io/cookbooks/how-to-use-beta-id/), swiyu cookbook
- [swiyu release note, 2026-06-25](https://swiyu-admin-ch.github.io/2026/06/25/new-versions-released.html): `vct` activation
- [DIDAS Glossary: Beta-ID](https://didas-swiss.github.io/didas-glossary/#term:beta-id)
