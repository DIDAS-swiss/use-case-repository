---
id: vaccination-record
title: Vaccination record and evidence of doses
title_de: Impfnachweis und Nachweis verabreichter Dosen
title_fr: Carnet de vaccination et preuve des doses administrées
title_it: Certificato di vaccinazione e prova delle dosi somministrate
stage: signal
ambition_levels: [AL3]
sectors: [ISIC-86, ISIC-47]
domain_steward: vacant
proposed_by: DIDAS (from the digital-health_swiyu showcase, Accelerate GmbH)
intake_issue:
credentials_reused: []
credentials_new: [immunization-record]
credentials_excluded: [swiss-e-id, beta-id]
related_use_cases: []
trust_flows: [health/immunization/F-01, health/immunization/F-02, health/immunization/F-03, health/immunization/F-06]
ifm_patterns: []
implementations: ["https://github.com/DIDAS-swiss/digital-health_swiyu (sandbox demo, mocked swiyu components)"]
glossary_terms: [issuer, verifier, wallet, claim, selective-disclosure, status-list, ebpi]
created: 2026-11-05
updated: 2026-11-05
---

# Vaccination record and evidence of doses

> **From a working showcase.** This entry describes the immunisation journey of
> [digital-health_swiyu](https://github.com/DIDAS-swiss/digital-health_swiyu)
> ([showcase portal](https://didas-swiss.github.io/digital-health_swiyu/)),
> developed by Accelerate GmbH out of the Swiss GovTech Hackathons and published
> by DIDAS. Issuance (flow F-02) and minimal-disclosure presentation (F-03) are
> implemented and tested there **against a mock of the swiyu components, in the
> Sandbox only**. Nothing has run against production. Legal readings are the
> showcase's own and need legal review.

## Summary

Whoever administers a vaccination issues one verifiable credential per dose
into the patient's [wallet](https://didas-swiss.github.io/didas-glossary/#term:wallet).
The patient later presents evidence of the doses received to a practice, a
pharmacy or a travel clinic, releasing only the
[claims](https://didas-swiss.github.io/didas-glossary/#term:claim) that the
requesting role is entitled to. A travel clinic, for example, receives 4 of the
credential's 18 claims. Today a vaccination history is scattered across GPs,
pharmacies and travel clinics or kept in a paper booklet, and since
meineimpfungen.ch closed in 2021 there has been no national electronic record.
With credentials, the patient keeps a copy whether or not the issuing
organisation stays in service.

## Outcome: what must be proven

The relying party decides whether, and what, to vaccinate or advise. To do so it
needs proof that:

- a dose of a given vaccine against a given disease was administered on a given date
- it was dose *n* of a series of *m*
- an organisation authorised to vaccinate asserted this

The credential proves that doses were given. **It does not prove protection.**
Whether a person is protected is a clinical inference over the schedule, the
elapsed time and judgement, made by the clinician; only the dose record is signed.

## Actors and roles

| Role | Actor | Organisation type | Notes |
|---|---|---|---|
| Holder | Patient | person | Holds one credential per dose |
| Issuer | Vaccinator: GP practice, pharmacy with a vaccination permit, company medical service | private / public | Showcase role `ch.didas.health.role.vaccinator` |
| Verifier | Practice | private / public | Entitled to 18 of 18 claims |
| Verifier | Pharmacy | private | Entitled to 7 of 18 claims, to check the series before the next dose |
| Verifier | Travel clinic | private | Entitled to 4 of 18 claims, as input to travel advice |
| Verifier | Research | academic | Entitled to 4 of 18, only under explicit, revocable consent (roadmap) |
| Verifier | Statistics: national vaccination coverage monitoring, e.g. [EBPI](https://didas-swiss.github.io/didas-glossary/#term:ebpi) | academic / public | Entitled to 5 of 18 (roadmap, F-11) |
| Governing authority | **None exists** for the health domain | | Would grant the vaccinator role and the request entitlements |

## Process flow

| # | Actor | Action | Credential |
|---|---|---|---|
| 1 | Vaccinator | Is onboarded to swiyu and granted the vaccinator role (F-01, partial) | |
| 2 | Vaccinator | Administers a dose and issues one credential for it (F-02) | Immunization record (new) |
| 3 | Patient | Stores the credential in the wallet | |
| 4 | Travel clinic | Requests evidence of doses against one disease; the query is built from its entitlement, so it can only ask for 4 claims (F-03) | |
| 5 | Patient | Sees the purpose and the four claims, and releases or declines | Immunization record |
| 6 | Travel clinic | Verifies signature, status and trust markers; the clinician draws the clinical conclusion | |
| 7 | Vaccinator | Revokes a dose credential only to correct a recording error, never to withdraw a dose that took place (F-06, partial) | |

## Credentials

| Credential | In this use case | Claims needed | Supply | Why |
|---|---|---|---|---|
| [Immunization record](../credentials/immunization-record.md) | new | travel clinic: `target_disease`, `occurrence_date`, `dose_number`, `doses_in_series` | emerging | Signed evidence of each dose, by its author |
| [Swiss e-ID](../credentials/swiss-e-id.md) | **excluded** | | | The travel clinic already knows the patient from the appointment; the immunization record carries name and date of birth |
| [Beta-ID](../credentials/beta-id.md) ([I14Y](https://www.i14y.admin.ch/de/catalog/datasets/urn:vct:ch.admin.bcs.betaid/description)) | **excluded** | | | Used in the showcase's practice check-in (F-04), not in this journey |

The exclusions make data minimisation explicit: the travel clinic receives four
claims and no identity credential.

## Governance and trust context

- **Legal basis** *(the showcase's reading; legal review required)*: the
  Epidemics Act (EpG/LEp, SR 818.101) for the federal and cantonal vaccination
  framework, with professional, therapeutic-products and cantonal law deciding who
  may administer. The e-ID Act (BGEID) governs the trust infrastructure, but not
  the content of a health credential or what a practice may request; its
  proportionality rule (Art. 23) applies to the e-ID only.
- **Trust frameworks and registries**: swiyu Trust Registry and Trust Protocol
  2.0. The immunization record is a *governed* credential type: a verifier should
  accept it only with a Governed Use Case Authorization Trust Marker for the
  issuer. No health-domain governing authority exists to issue that marker, so
  the showcase uses configured lists of accepted issuers. That works for a pilot
  and does not scale.
- **Verifier governance**: each role's query is published as a Verification
  Query Public Statement, and a request outside the role's entitlement is refused
  when it is built, before it reaches the wallet.
- **Sensitive attributes**: health data. Selective disclosure narrows each
  presentation, but unlinkability is not claimed: credential identifier, holder
  key, status-list reference and timing still allow correlation.

## Demand and value

- **Relying parties**: GP practices, pharmacies, travel clinics; later research
  and national coverage monitoring
- **Indicative scale**: not yet known
- **Value**: a vaccination history the patient can actually produce, instead of
  guessing and being vaccinated again; fewer re-recorded doses; no dependence on a
  single central service; minimal disclosure per role

## Coordination needs and open questions

- **A governing authority for the health domain** is the decisive dependency. It
  would grant the vaccinator role and the per-role request entitlements, and back
  the trust markers verifiers need.
- **Schema**: the credential type `urn:vct:ch.didas.health.immunization:1.0` is
  the showcase's own, mapped to the FHIR CH VACD profile. It is not on I14Y.
  Bringing it there, through eCH or the eHealth Suisse community, is the step
  towards a formally maintained schema.
- **Holder notification on correction**: the current swiyu profiles define no
  mechanism for telling the holder that a credential was superseded.
- **Related journeys** in the same showcase that could become use cases here:
  practice check-in with identity and insurance credentials (F-04), single-use
  prescription redemption (F-05) and the national vaccination coverage survey
  (F-11).
- Is there a domain steward for health (AL3)?

## Sources

- [digital-health_swiyu](https://github.com/DIDAS-swiss/digital-health_swiyu),
  README and [business case](https://github.com/DIDAS-swiss/digital-health_swiyu/blob/main/docs/business-case.md), at commit `6636357`
- [F-02 Recording an administered dose](https://github.com/DIDAS-swiss/digital-health_swiyu/blob/main/flows/F-02-immunization-issuance.md)
- [F-03 Presenting vaccination evidence with minimal disclosure](https://github.com/DIDAS-swiss/digital-health_swiyu/blob/main/flows/F-03-immunization-minimal-disclosure.md)
- [Immunization Record credential definition](https://github.com/DIDAS-swiss/digital-health_swiyu/blob/main/docs/credentials/immunization.md)
- [Governance framework](https://github.com/DIDAS-swiss/digital-health_swiyu/blob/main/docs/governance-framework.md)
