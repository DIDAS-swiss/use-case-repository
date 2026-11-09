---
title: Backlog
---

# Backlog

Every use case, from the first signal to the published entry: the candidates
filed through the [use-case form](https://github.com/DIDAS-swiss/use-case-repository/issues/new?template=use-case-candidate.yml),
the ones a working group has taken, the drafts under review and the published
entries. The list is read live from GitHub each time the page opens.

<div id="backlog-app" class="backlog">
  <p class="note">Loading the use cases from GitHub…</p>
</div>

<script id="backlog-entries" type="application/json">
[{%- assign entries = site.pages | where: "kind", "use-case" | where_exp: "p", "p.stage" -%}
{%- for e in entries -%}{"id":{{ e.name | remove: ".md" | jsonify }},"title":{{ e.title | jsonify }},"stage":{{ e.stage | jsonify }},"lighthouse":{{ e.lighthouse | default: "" | jsonify }},"url":{{ e.url | relative_url | jsonify }}}{% unless forloop.last %},{% endunless %}{%- endfor -%}]
</script>
<script id="backlog-groups" type="application/json">
[{%- for g in site.data["working-groups"] -%}{"id":{{ g.id | jsonify }},"name":{{ g.name | jsonify }}}{% unless forloop.last %},{% endunless %}{%- endfor -%}]
</script>
<script src="{{ '/assets/backlog.js' | relative_url }}"></script>

## How a use case moves

| Step | What it means | How it gets there |
|---|---|---|
| **Candidate** | Filed, waiting for a working group | the use-case form, or a batch in `intake/` |
| **Taken** | A working group details it | the group adds its `wg: <group>` label |
| **Drafting** | The entry is written and reviewed in a pull request | the label `drafting` opens the pull request |
| **Published** | The entry is in the catalogue, at its lifecycle stage | a curator merges the pull request |
| **Not pursued** | Closed as out of scope, duplicate or withdrawn | a curator closes the issue |

Published entries then move through the lifecycle stages `signal` → `candidate`
→ `qualified` → `active` → `maintained`, or `deprecated`
([GOVERNANCE.md](GOVERNANCE.md#lifecycle-stages)). The
[project board](https://github.com/orgs/DIDAS-swiss/projects/6) shows the same
items with the curators' working status.
