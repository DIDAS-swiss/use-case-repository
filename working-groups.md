---
title: Working groups
---

# Working groups

DIDAS working groups take use-case candidates and develop them into entries
([GOVERNANCE.md](GOVERNANCE.md#working-groups)). Each group is responsible for
one or more ISIC Rev. 5 sectors. The assignment is one table,
[`_data/working-group-sectors.csv`](https://github.com/DIDAS-swiss/use-case-repository/blob/main/_data/working-group-sectors.csv),
with one row per group and sector code.

**Rules.** A sector code belongs to at most one group. The most specific
assignment wins: a group holding a division takes it over from the group
holding its section. A code without an assignment of its own inherits the group
of the nearest broader code that has one. The *Check data* workflow enforces
this on every change.

{%- assign groups = site.data["working-groups"] -%}
{%- assign assignments = site.data["working-group-sectors"] -%}

## Groups and their sectors

<table>
<thead><tr><th>Working group</th><th>Label</th><th>ISIC sectors</th><th>Open candidates</th></tr></thead>
<tbody>
{%- for g in groups -%}
{%- assign mine = assignments | where: "group", g.id -%}
<tr>
<td><strong>{{ g.name }}</strong><br><span class="note">{{ g.description }}</span></td>
<td><code>wg: {{ g.id }}</code></td>
<td>{%- for a in mine -%}{%- assign s = site.data.sectors | where: "id", a.sector | first -%}<code>{{ a.sector | remove: "ISIC-" }}</code> {{ s.label }}{% unless forloop.last %}<br>{% endunless %}{%- endfor -%}{% if mine.size == 0 %}<span class="pill supply-missing">none</span>{% endif %}</td>
<td><a href="https://github.com/{{ site.repository }}/issues?q=is%3Aissue+is%3Aopen+label%3A%22wg%3A+{{ g.id }}%22">taken</a></td>
</tr>
{%- endfor -%}
</tbody>
</table>

## Who is responsible for a sector

Every sector in the list the repository uses, with the group responsible for it.
*Inherited* means the group holds a broader code.

<table>
<thead><tr><th>ISIC sector</th><th>Working group</th></tr></thead>
<tbody>
{%- for s in site.data.sectors -%}
{%- assign hit = nil -%}{%- assign via = nil -%}
{%- assign cur = s -%}
{%- for step in (1..3) -%}
  {%- if cur == nil -%}{%- break -%}{%- endif -%}
  {%- assign a = assignments | where: "sector", cur.id | first -%}
  {%- if a -%}{%- assign hit = groups | where: "id", a.group | first -%}{%- assign via = cur.id -%}{%- break -%}{%- endif -%}
  {%- assign cur = site.data.sectors | where: "id", cur.broader | first -%}
{%- endfor -%}
<tr>
<td>{% if s.level == "division" %}&nbsp;&nbsp;&nbsp;{% elsif s.level == "class" %}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{% endif %}<code>{{ s.id | remove: "ISIC-" }}</code> {{ s.label }}</td>
<td>{% if hit %}{{ hit.name }}{% if via != s.id %} <span class="tag">inherited from {{ via | remove: "ISIC-" }}</span>{% endif %}{% else %}<span class="pill supply-missing">no working group</span>{% endif %}</td>
</tr>
{%- endfor -%}
</tbody>
</table>

## Changing the assignment

Open a pull request that adds, moves or removes rows in
`_data/working-group-sectors.csv` (and, for a new group, a row in
`_data/working-groups.csv`). Curators review it; the *Check data* workflow
rejects a code assigned twice or a code that is not in the sector list. Then run
*Sync labels* so a new group gets its `wg:` label.

Codes are taken from the sector list the repository shares with the
[Industry Function Graph](https://github.com/DIDAS-swiss/industry-function-graph):
all 22 sections and the divisions and classes the graph uses. A group can always
be assigned a section; a more specific code that is missing is added in the graph
first, then reaches this repository with the next sync.
