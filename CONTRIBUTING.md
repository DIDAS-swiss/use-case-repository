# Contributing

You do not need to write an entry to contribute. A *Use-case candidate* or
*Credential need* issue is a complete contribution, and a curator will help
structure it. This guide is for anyone who opens the pull request.

## Two kinds of entry

| | Use case | Credential |
|---|---|---|
| Folder | `use-cases/` | `credentials/` |
| Template | [`use-cases/_template.md`](use-cases/_template.md) | [`credentials/_template.md`](credentials/_template.md) |
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
| `sectors` | yes | for example `mobility`, `insurance`, `finance`, `health`, `education`, `public-administration` |
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
| `schema_refs` | no | links to I14Y, eCH or sectoral schema publications. **Never** invent an identifier |
| `used_by` | yes | use-case ids |
| `demand_issues` | no | `credential-need` issue numbers |
| `created`, `updated` | yes | `YYYY-MM-DD` |

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
