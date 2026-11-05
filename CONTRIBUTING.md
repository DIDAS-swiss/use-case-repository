---
title: Contributing
---

# Contributing

You do not need to write an entry to contribute. A *Use-case candidate* or
*Credential need* issue is a complete contribution, and a curator will help
structure it. This guide is for anyone who opens the pull request.

## Two kinds of entry

| | Use case | Credential |
|---|---|---|
| Folder | `use-cases/` | `credentials/` |
| Template | [`use-cases/_template.md`](https://github.com/DIDAS-swiss/use-case-repository/blob/main/use-cases/_template.md) | [`credentials/_template.md`](https://github.com/DIDAS-swiss/use-case-repository/blob/main/credentials/_template.md) |
| Answers | What must be proven, by whom, with which credentials, under which rules | What a credential attests, who could issue it, and whether anyone does yet |
| Index | [`use-cases/README.md`](use-cases/README.md) | [`credentials/README.md`](credentials/README.md) |

A use case lists the credentials it relies on by their `id`. A credential lists
the use cases that rely on it in `used_by`. Keep both sides in step in the same
pull request.

## File names and ids

- The file name is the `id` plus `.md`, in lowercase kebab case and in English:
  `motor-vehicle-claims-processing.md`.
- Name a use case after the **outcome**, not the organisation:
  `vehicle-leasing`, not `acme-leasing-onboarding`.
- Name a credential after **what it attests**, not the paper document it
  replaces, where the two differ.

## Front matter

Each file opens with YAML front matter. GitHub renders it as a table at the top of
the page, and it is the part a future Catalog would import, so keep the field names
exactly as in the template. Keep values flat (text, or a list of text); the
detail belongs in the body.

### Use case

| Field | Required | Values |
|---|---|---|
| `id` | yes | same as the file name |
| `title` | yes | short English title |
| `title_de`, `title_fr`, `title_it` | no | the title in the other working languages |
| `stage` | yes | `signal` · `candidate` · `qualified` · `active` · `maintained` · `deprecated` |
| `ambition_levels` | yes | one or more of `AL1`, `AL2`, `AL3` |
| `sectors` | yes | ISIC Rev. 5 ids from [`_data/sectors.csv`](https://github.com/DIDAS-swiss/use-case-repository/blob/main/_data/sectors.csv), for example `ISIC-65`, `ISIC-84`. See *Sectors* below |
| `domain_steward` | yes | a name from [STEWARDS.md](STEWARDS.md), or `vacant` |
| `proposed_by` | yes | person or organisation |
| `intake_issue` | no | issue number of the candidate |
| `credentials_reused` | no | credential ids taken over from another use case or from an existing issuer |
| `credentials_new` | no | credential ids this use case newly requires |
| `credentials_excluded` | no | credential ids deliberately **not** requested, which makes data minimisation explicit |
| `related_use_cases` | no | use-case ids |
| `glossary_terms` | no | DIDAS Glossary term anchors, for example `issuer`, `verifier` |
| `created`, `updated` | yes | `YYYY-MM-DD` |

### Credential

| Field | Required | Values |
|---|---|---|
| `id`, `title` | yes | as above |
| `title_de`, `title_fr`, `title_it` | no | as above |
| `stage` | yes | as above |
| `supply` | yes | `available` (issued in production) · `emerging` (announced, piloted or in build) · `missing` (no known issuer) |
| `ambition_level` | yes | `AL1`, `AL2` or `AL3` |
| `likely_issuer` | yes | the organisation or kind of organisation with the mandate or the data |
| `issuer_type` | yes | `federal` · `cantonal` · `municipal` · `sectoral` · `private` |
| `i14y_dataset` | where published | the I14Y dataset identifier, usually the credential type (`vct`), for example `urn:vct:ch.admin.bcs.betaid` |
| `i14y_id` | where published | the dataset's I14Y id (a uuid, the `id` in the I14Y API). With it, the schema is federated (see *Credentials on I14Y* below) |
| `schema_refs` | no | further links: eCH standards, sectoral schemas, specifications. **Never** invent an identifier |
| `used_by` | yes | use-case ids |
| `demand_issues` | no | `credential-need` issue numbers |
| `created`, `updated` | yes | `YYYY-MM-DD` |

## Credentials on I14Y

I14Y is the reference for credential schemas. Wherever a credential is
published there, its entry points to I14Y and nowhere else for the schema:

1. Find the dataset on [I14Y](https://www.i14y.admin.ch/de/catalog/datasets),
   usually under its credential type, for example `urn:vct:ch.admin.bcs.betaid`.
2. Set `i14y_dataset` and `i14y_id` in the credential's front matter, and link the
   dataset under *Schema and semantic references*.
3. The **Sync schemas from I14Y** workflow then federates the schema into
   `federation/i14y/<credential-id>/`: the dataset record, the structure as
   SHACL (Turtle and JSON-LD), a compact attribute list and a rendered table,
   which the site shows on the credential's page. To do it locally, run
   `python3 scripts/i14y_sync.py` (standard library only).
4. In use cases and indexes, reference the credential's I14Y dataset next to the
   credential, as the existing entries do.

Files under `federation/i14y/` and `_includes/i14y/` are generated: never edit
them by hand. Where a credential has no I14Y dataset, write "Not published on
I14Y (checked YYYY-MM-DD)", so the next reader knows someone looked.

## Sectors

Sectors use **ISIC Rev. 5**, exactly as the
[DIDAS Industry Function Graph](https://github.com/DIDAS-swiss/industry-function-graph)
does, so a use case here and a use case pattern there can be joined on the same
code.

- Use the graph's ids: `ISIC-L` for a section, `ISIC-65` for a division,
  `ISIC-6512` for a class. Divisions and classes drop the section letter,
  because letters moved between ISIC revisions while the numbers held.
- Pick the most specific level that is on the list. A section is fine where no
  division fits.
- List every sector the use case **applies to**, which can be broader than where
  it has been piloted.
- The list in `_data/sectors.csv` is a copy of the graph's `data/sectors.csv`.
  If a code is missing, propose it in the graph first, then refresh the copy here.
  Do not add codes only here.
- Sector is context, not identity: the same use case in two sectors stays one
  entry with two sector codes.

The division number is also the join key to NOGA 2025, the Swiss implementation
of NACE Rev. 2.1, at section and division level.

## The body

Use the headings in the template, in that order, so every entry reads the same
way. A heading may say "Not yet known". Leaving it out hides the gap, and the gaps
are what this repository is meant to show.

## Sources and facts

- Cite a source for legal bases, issuer mandates and supply status. A link is enough.
- Do not mark a credential `available` without a public reference to the issuer
  or the deployment.
- Statements from illustrative material, such as pre-study mockups, are labelled as
  illustrative until confirmed.
- Use the vocabulary of the [DIDAS Glossary](https://didas-swiss.github.io/didas-glossary/).
  Link a term the first time it appears:
  `[issuer](https://didas-swiss.github.io/didas-glossary/#term:issuer)`.

## Checklist for a pull request

- [ ] Front matter fields match the template
- [ ] Index row added or updated (`use-cases/README.md`, `credentials/README.md`)
- [ ] Cross-references kept in step (`credentials_*` ↔ `used_by`)
- [ ] Sources given for legal bases and supply status
- [ ] Changelog entry in `changelog/`
- [ ] `Closes #N` for the intake issue
