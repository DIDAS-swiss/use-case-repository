# Vision: an early use-case section of the Ecosystem Discovery Catalog

## Where this comes from

In June 2026 the DPSS working group iSVC (*inhaltliche Standardisierung Verifiable
Credentials*) published the
[Pre-Study: Swiss Ecosystem Discovery Catalog](https://www.amministrazionedigitalesvizzera.ch/application/files/8317/8999/7309/Pre-Study_Swiss_Ecosystem_Discovery_Catalog_DPSS_June_2026.pdf).
Accelerate.swiss wrote it on the working group's mandate. It recommends building an **Ecosystem
Discovery Catalog** as Switzerland's coordination, discovery and transparency
layer for the verifiable data ecosystem, across all three ambition levels (AL1 for the e-ID,
AL2 for public-sector credentials and AL3 for private and other non-state
credentials).

The pre-study's central finding is that **the primary bottleneck is coordination,
not core technology** (§4.4). Verifiers cannot see which credentials exist, and issuers
cannot see who needs one. Reuse happens only when it is made explicit at use-case level.

It also notes that the term "credential catalog" is interpreted inconsistently
(§2.4), and that **concrete use-case flows were what made the Catalog tangible**.

This repository starts on the use-case side now, in the open, before the Catalog
is procured.

## What this repository is

An early version of the parts of the Catalog that the pre-study says should be
**stored natively** (§6.1). It is built only from what GitHub already offers:
Markdown files, issue forms, labels and pull requests.

| Pre-study artefact | Catalog role (pre-study §6.1) | Here |
|---|---|---|
| Use-case entries | Stored natively | `use-cases/*.md` |
| Demand signals | Stored natively | `credential-need` issues, plus `credentials/*.md` with `supply: missing` or `emerging`. Together they form the gap board |
| Use-case lifecycle and maturity state | Stored natively | the `stage` field and `stage:` label, advanced by pull request |
| Schema metadata | Federated from I14Y | **referenced only** (`schema_refs`) |
| Trust registry references | Linked to the swiyu Trust Registry | **referenced only** |
| Governance framework references | Linked, with summary metadata stored | `governance` block: link plus one-line summary |
| OCA overlays | Linked to source repository | **referenced only** |

It covers five of the MVP's functional priorities (§9.3) at repository scale:

1. **Structured use-case entries**: a schema-validated format following the
   four parts of the conceptual model (§3.3.1)
2. **Visibility of existing, emerging and missing credentials**: every
   credential carries a supply status
3. **Demand and supply signalling**: the credential-need issue form and the gap
   board
4. **Lifecycle and maturity visibility**: the six stages of §8.10, applied to
   every entry
5. **Explicit reuse and deliberate exclusion at use-case level**: each credential
   in a use case is marked `reused`, `new` or `excluded`

Issuer and verifier discovery and live federation with I14Y and the swiyu Trust
Registry need a running system. In this repository they appear only as links.

## How the entry format maps to the conceptual model

| Conceptual model part (§3.3.1) | Entry field(s) |
|---|---|
| Part 1: Decision context (trust domains and use cases) | `outcome`, `sectors`, `ambition_levels`, `trust_domain`, `governance` |
| Part 2: Trust resolution | `governance.trust_frameworks`, `governance.legal_basis` |
| Part 3: Semantic layer (claims and schemas) | `credentials[].claims`, credential `schema_refs` |
| Part 4: Operational interaction patterns | `flow` |
| Roles | `actors` (issuers, holders, verifiers, governing authorities) |

## Who it serves

These are the pre-study's archetypes (§3.3.2), as they would use this repository today:

- **Demand / supply signaller**: files a credential-need issue and watches the gap board
- **Policy navigator**: reads `governance` and the legal basis of a use case
- **Domain steward**: owns the use cases of a sector and advances their stage
- **Schema builder**: finds a missing credential and takes the schema work to I14Y
- **Implementer**: reads the flow and the credentials of a qualified use case
- **Curator**: triages intake and keeps entries coherent

## Path to the Catalog

The pre-study's phasing names the use cases as an input in every phase: priority
AL2 credentials and use cases in Phase 1, and at least 10 structured use-case
entries with full actor, credential and governance context as an MVP acceptance
criterion (§9.4.3).

This repository can be that input. The entry format is meant to be **importable**:
each file opens with plain YAML front matter in fixed fields (see
[CONTRIBUTING.md](CONTRIBUTING.md)), so whichever system is procured can ingest
the entries rather than re-collecting them.

Version one deliberately stays within GitHub. Tooling such as validation, a
rendered catalog or an automatically computed gap board comes later, once the
format has proven itself on real entries.

| Pre-study phase | What this repository contributes |
|---|---|
| Phase 1: Decision and procurement readiness | A body of structured candidates from which to choose priority AL2 use cases and 1–2 AL3 sectoral ecosystems |
| Phase 2: MVP and pilot activation | Initial catalog population, plus the entry format as one input to the metadata model |
| Phase 3: Version 1 | Archive, or a mirror that the Catalog federates |

## Non-goals

- **No schema authoring or schema lifecycle management.** That belongs to I14Y,
  eCH and sectoral repositories (pre-study, Executive Summary and §6.1).
- **No trust decisions.** Issuer recognition and verifier registration belong to the
  swiyu Trust Registry and the FOJ.
- **No runtime policy, conformance testing or runtime binding.** These are later-stage
  capabilities (§9.5).
- **No claim to be the Catalog.** This is a community precursor. The Catalog's
  governance, operator and curator roles are for the readiness phase to decide.
