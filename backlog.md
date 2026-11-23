---
title: Backlog
description: All use cases with their step, working group, source and evidence status.
---

# Backlog

All use cases of the repository: open candidates from the
[use-case form](https://github.com/DIDAS-swiss/use-case-repository/issues/new?template=use-case-candidate.yml)
or an intake batch, candidates a working group has taken, entries in drafting and
published entries. The page reads the issues from GitHub each time it opens; the
published entries come from the site build.

<div id="backlog-app" class="backlog">
  <p class="note">Loading the use cases from GitHub…</p>
</div>

<script id="backlog-entries" type="application/json">
[{%- assign entries = site.pages | where: "kind", "use-case" | where_exp: "p", "p.stage" -%}
{%- for e in entries -%}{"id":{{ e.name | remove: ".md" | jsonify }},"title":{{ e.title | jsonify }},"stage":{{ e.stage | jsonify }},"evidence":{{ e.evidence_status | default: "" | jsonify }},"source":{{ e.proposed_by | default: "" | jsonify }},"lighthouse":{{ e.lighthouse | default: "" | jsonify }},"url":{{ e.url | relative_url | jsonify }}}{% unless forloop.last %},{% endunless %}{%- endfor -%}]
</script>
<script id="backlog-groups" type="application/json">
[{%- for g in site.data["working-groups"] -%}{"id":{{ g.id | jsonify }},"name":{{ g.name | jsonify }},"status":{{ g.status | default: "active" | jsonify }}}{% unless forloop.last %},{% endunless %}{%- endfor -%}]
</script>
<script src="{{ '/assets/backlog.js' | relative_url }}"></script>

## How a use case moves

| Step | What it means | How it gets there |
|---|---|---|
| **Candidate** | Filed, waiting for a working group | the use-case form, or a batch in `intake/` |
| **Taken** | A working group details it | the group adds its `wg: <group>` label |
| **Drafting** | The entry is written and reviewed in a pull request | the label `drafting` opens the pull request |
| **Published entry** | The entry is in the catalogue, at its lifecycle stage | a curator merges the pull request |
| **Not pursued** | Closed as out of scope, duplicate or withdrawn | a curator closes the issue |

Publication is not qualification, endorsement or production readiness: a
published entry starts at stage `signal`, and the **Evidence** column shows how far
the evidence for the proposed exchange goes (hypothesis, documented need, design,
prototype, pilot, production). Only the files in
[`use-cases/`](use-cases/README.md) count as published; the page lists them from
the site build and everything else from the issues. Published entries then move
through the lifecycle stages `signal` → `candidate`
→ `qualified` → `active` → `maintained`, or `deprecated`
([GOVERNANCE.md](GOVERNANCE.md#lifecycle-stages)). The
[project board](https://github.com/orgs/DIDAS-swiss/projects/6) shows the same
items with the curators' working status.
