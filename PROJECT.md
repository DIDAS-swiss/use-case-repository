---
title: Project board
---

# Project board

**👉 [Open the project board](https://github.com/orgs/DIDAS-swiss/projects/6)**

The project board is the entry point to the repository's workflows: every
use-case candidate, credential signal, change request and pull request lands on
it, and its views show what is waiting for whom. A workflow keeps it up to date
(see *Keeping it up to date*).

**[➕ Register your use case](https://github.com/DIDAS-swiss/use-case-repository/issues/new?template=use-case-candidate.yml)** ·
[Signal a credential need](https://github.com/DIDAS-swiss/use-case-repository/issues/new?template=credential-signal.yml) ·
[Propose a change](https://github.com/DIDAS-swiss/use-case-repository/issues/new?template=change-entry.yml)

## How items move

| Status | Meaning | Moved by |
|---|---|---|
| **New** | Just filed through an issue form | automatically |
| **Triage** | A curator is checking scope, duplicates and labels | curator |
| **Drafting** | Accepted; an entry is being written in a pull request | curator or proposer |
| **In review** | The pull request is open and waiting for approval | automatically |
| **Published** | Merged: the entry is in the catalogue | automatically, when the pull request is merged or the issue completed |
| **Not pursued** | Out of scope, duplicate or withdrawn, with the reason in the issue | automatically when closed as such, or curator |

The lifecycle *stage* of an entry (`signal` → `candidate` → `qualified` → …) is
not a board column: it belongs to the entry and is carried by its `stage:` label
and front matter (see [GOVERNANCE.md](GOVERNANCE.md#lifecycle-stages)).

## Working groups take candidates

Candidates arrive one at a time through the form, or as a batch through
[`intake/`](intake/README.md). The **Up for grabs** view lists the open candidates
no working group has taken yet, by sector. A working group takes one by adding
its `wg: <group>` label and assigning a member; the board then shows it under
that group, and the group details the candidate and drafts the entry
([GOVERNANCE.md](GOVERNANCE.md#working-groups)).

## Keeping it up to date

The **Sync project board** workflow (`.github/workflows/project-sync.yml`) keeps
the board in step with the repository:

- every issue and pull request is added, including the ones that existed before
- **Type** follows the labels: `use-case` → Use case, `credential-need` → Credential
  need, `credential-supply` → Credential supply, `change` and other pull requests →
  Change, the sync branch `automation/…` → Federation update
- **Status** follows what happens: a new issue starts at New, an open pull request
  is In review, merged or completed is Published, closed as not planned, duplicate
  or out of scope is Not pursued, reopened goes back to Triage. A status a curator
  set by hand (Triage, Drafting) is never overwritten by a label change or edit

- **Sector** is the item's primary sector as an ISIC Rev. 5 section: the first
  sector chosen in the form, otherwise its first `ISIC <letter>` label. Every
  sector of a cross-sector use case remains filterable through the labels, for
  example `label:"ISIC P"`
- **Working group** follows the `wg: <group>` label, once the groups are listed in
  [`_data/working-groups.csv`](https://github.com/DIDAS-swiss/use-case-repository/blob/main/_data/working-groups.csv)

- **Lighthouse** is set while the item carries the `lighthouse` label, and cleared
  when the label is removed. Curators or working groups add the label to select a
  use case as a lighthouse; a batch file can set it with a `lighthouse` column

Run by hand, it also sets up the board: the Status options and the Type, Sector,
Working group and Lighthouse fields, the short description and the project README.

### One-time setup

GitHub Projects can only be written with a token that has project rights; the
repository's own Actions token does not, which is why the board stays empty
without this.

1. **Create a token.** As a member with write access to project 6:
   GitHub → *Settings* → *Developer settings* → *Personal access tokens* →
   *Fine-grained tokens* → *Generate new token*.
   - Resource owner: **DIDAS-swiss**
   - Repository access: *Only select repositories* → `use-case-repository`;
     repository permissions *Issues* and *Pull requests*: **Read-only**
   - Organization permissions → *Projects*: **Read and write**

   The organisation may have to approve fine-grained tokens. A classic token with
   the `project` and `public_repo` scopes works as well.
2. **Store it** in the repository: *Settings* → *Secrets and variables* →
   *Actions* → *New repository secret*, name **`PROJECT_TOKEN`**.
3. **Run the workflow once**: *Actions* → *Sync project board* → *Run workflow*.
   It creates the fields, writes the description and README, and adds the
   existing issues and pull requests. From then on it runs on every issue and
   pull request event.
4. **Views** cannot be created through GitHub's API. Create them once, from the
   board's view menu:

   | View | Layout | Filter | Group by |
   |---|---|---|---|
   | Intake | Board | `is:open` | Status |
   | Use cases | Table | `type:"Use case"` | Status |
   | Gap board | Board | `type:"Credential need" is:open` | Status |
   | Supply | Table | `type:"Credential supply"` | |
   | By sector | Board | `type:"Use case"` | Sector |
   | Up for grabs | Table | `type:"Use case" no:"Working group" is:open` | Sector |
   | Working groups | Board | `type:"Use case" has:"Working group"` | Working group |
   | Lighthouses | Table | `type:"Use case" lighthouse:Lighthouse` | Sector |
   | Federation updates | Table | `type:"Federation update"` | |

   In any view, filter by sector with the field (`sector:"L · Financial and
   insurance activities"`, or pick it from the filter menu) or by any of an item's
   sectors with its labels (`label:"ISIC L"`), and by lighthouse with
   `lighthouse:Lighthouse` or `label:lighthouse`.

5. **Visibility and link**: in the board's *Settings*, set visibility to
   *Public*, so the links from the README and the site work for everyone. Then
   link the board in the repository's *Projects* tab.

The board is at [https://github.com/orgs/DIDAS-swiss/projects/6](https://github.com/orgs/DIDAS-swiss/projects/6); `project_url` in
[`_config.yml`](https://github.com/DIDAS-swiss/use-case-repository/blob/main/_config.yml)
and the *Project board* buttons point to it.

## Project README

The workflow writes the board's README and short description when run by hand;
the text is in `project-sync.yml`.
