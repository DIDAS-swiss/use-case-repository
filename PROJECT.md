---
title: Project board
---

# Project board

**👉 [Open the project board](https://github.com/orgs/DIDAS-swiss/projects/6)**

The project board is the entry point to the repository's workflows: every
use-case candidate, credential signal, change request and pull request lands on
it, and its views show what is waiting for whom. It uses only GitHub Projects'
built-in fields and automations, so it needs no extra token or workflow.

**[➕ Register your use case](https://github.com/DIDAS-swiss/use-case-repository/issues/new?template=use-case-candidate.yml)** ·
[Signal a credential need](https://github.com/DIDAS-swiss/use-case-repository/issues/new?template=credential-signal.yml) ·
[Propose a change](https://github.com/DIDAS-swiss/use-case-repository/issues/new?template=change-entry.yml)

## How items move

| Status | Meaning | Moved by |
|---|---|---|
| **New** | Just filed through an issue form | automatically, when the item is added |
| **Triage** | A curator is checking scope, duplicates and labels | curator |
| **Drafting** | Accepted; an entry is being written in a pull request | curator or proposer |
| **In review** | The pull request is open and waiting for approval | curator |
| **Published** | Merged: the entry is in the catalogue | automatically, when the pull request is merged or the issue closed |
| **Not pursued** | Out of scope, duplicate or withdrawn, with the reason in the issue | curator |

The lifecycle *stage* of an entry (`signal` → `candidate` → `qualified` → …) is
not a board column: it belongs to the entry and is carried by its `stage:` label
and front matter (see [GOVERNANCE.md](GOVERNANCE.md#lifecycle-stages)).

## Setting it up

An organisation owner or a member allowed to create projects does this once.

1. **Create the project.** Organisation **DIDAS-swiss** → *Projects* → *New
   project* → *Board*. Name it **DIDAS Use Case Repository**. Short description:
   *Intake and lifecycle of business use cases for the Swiss verifiable data
   ecosystem.*
2. **Status field.** Edit the built-in *Status* field so its options are, in this
   order: `New`, `Triage`, `Drafting`, `In review`, `Published`, `Not pursued`.
3. **Type field.** Add a single-select field *Type* with `Use case`,
   `Credential need`, `Credential supply`, `Change`, `Federation update`.
4. **Built-in workflows** (project menu → *Workflows*):
   - *Auto-add to project*: repository `use-case-repository`, filter
     `is:issue,pr is:open`. Every new issue and pull request arrives on its own.
   - *Item added to project*: set Status to `New`.
   - *Item closed* and *Pull request merged*: set Status to `Published`.
   - *Auto-archive items*: `is:closed updated:<@today-30d`.
5. **Views.** Create these, from the view menu:

   | View | Layout | Filter | Group by |
   |---|---|---|---|
   | Intake | Board | `is:open` | Status |
   | Use cases | Table | `label:use-case` | Status |
   | Gap board | Board | `label:credential-need is:open` | Status |
   | Supply | Table | `label:credential-supply` | |
   | By sector | Table | `label:use-case` | (show the *Labels* column; filter by `label:"ISIC L"` etc.) |
   | Federation updates | Table | `label:federation` or `head:automation/federation-sync` | |

6. **Link it to the repository**: repository *use-case-repository* → *Projects*
   tab → *Link a project*, so it shows up there for every visitor.
7. **Point the repository at it**: `project_url` in
   [`_config.yml`](https://github.com/DIDAS-swiss/use-case-repository/blob/main/_config.yml)
   and the *Project board* button in [README.md](README.md) carry the project's
   URL, now [https://github.com/orgs/DIDAS-swiss/projects/6](https://github.com/orgs/DIDAS-swiss/projects/6).

## Project README

Paste this into the project's own README (project menu → *Settings*):

> **DIDAS Use Case Repository: intake and lifecycle.**
> Use cases for the Swiss verifiable data ecosystem, from first signal to
> published entry. Register a use case or signal a credential need with the issue
> forms in [use-case-repository](https://github.com/DIDAS-swiss/use-case-repository/issues/new/choose);
> items appear here automatically. Governance:
> [GOVERNANCE.md](https://github.com/DIDAS-swiss/use-case-repository/blob/main/GOVERNANCE.md) ·
> Catalogue: [didas-swiss.github.io/use-case-repository](https://didas-swiss.github.io/use-case-repository/)
