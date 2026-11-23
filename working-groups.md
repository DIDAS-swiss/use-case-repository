---
title: Working groups
description: The DIDAS working groups, their status and the ISIC sectors each sector group is responsible for.
---

# Working groups

DIDAS working groups take use-case candidates and develop them into entries
([GOVERNANCE.md](GOVERNANCE.md#working-groups)). **Sector groups** are each
responsible for one or more ISIC Rev. 5 sectors. **Horizontal groups** work
across sectors on topics every use case shares.

{%- assign groups = site.data["working-groups"] -%}
{%- assign assignments = site.data["working-group-sectors"] -%}
{%- assign active_sector = groups | where: "kind", "sector" | where: "status", "active" -%}
{%- assign active_horizontal = groups | where: "kind", "horizontal" | where: "status", "active" -%}

**Active now**: {% for g in active_sector %}{{ g.name }}{% unless forloop.last %}, {% endunless %}{% endfor %}, and
the horizontal group {% for g in active_horizontal %}{{ g.name }}{% unless forloop.last %}, {% endunless %}{% endfor %}.
The other groups are **open**: planned, not set up yet. An open sector group
keeps its sectors below, so they are already mapped when it starts; until then
an active group or a curator can take its candidates.

## Sector groups

The assignment is one table,
[`_data/working-group-sectors.csv`](https://github.com/DIDAS-swiss/use-case-repository/blob/main/_data/working-group-sectors.csv),
with one row per group and sector code.

**Rules.** A sector code belongs to at most one group. The most specific
assignment wins: a group holding a division takes it over from the group
holding its section. A code without an assignment of its own inherits the group
of the nearest broader code that has one. The *Check data* workflow enforces
this on every change.

<table>
<thead><tr><th>Working group</th><th>Status</th><th>Label</th><th>ISIC sectors</th><th>Open candidates</th></tr></thead>
<tbody>
{%- assign sector_groups = groups | where: "kind", "sector" | sort: "status" -%}
{%- for g in sector_groups -%}
{%- assign mine = assignments | where: "group", g.id -%}
<tr>
<td><strong>{{ g.name }}</strong><br><span class="note">{{ g.description }}</span></td>
<td>{% if g.status == "active" %}<span class="pill supply-available">active</span>{% else %}<span class="pill supply-missing">open</span>{% endif %}</td>
<td><code>wg: {{ g.id }}</code></td>
<td>{%- for a in mine -%}{%- assign s = site.data.sectors | where: "id", a.sector | first -%}<code>{{ a.sector | remove: "ISIC-" }}</code> {{ s.label }}{% unless forloop.last %}<br>{% endunless %}{%- endfor -%}{% if mine.size == 0 %}<span class="pill supply-missing">none</span>{% endif %}</td>
<td><a href="https://github.com/{{ site.repository }}/issues?q=is%3Aissue+is%3Aopen+label%3A%22wg%3A+{{ g.id }}%22">taken</a></td>
</tr>
{%- endfor -%}
</tbody>
</table>

## Horizontal groups

They hold no sectors. A horizontal group takes a candidate with its `wg:` label
when the open work is about its topic, for example a credential format or a
trust-infrastructure question, alongside or instead of the sector group.

<table>
<thead><tr><th>Working group</th><th>Status</th><th>Label</th><th>Open candidates</th></tr></thead>
<tbody>
{%- assign horizontal_groups = groups | where: "kind", "horizontal" | sort: "status" -%}
{%- for g in horizontal_groups -%}
<tr>
<td><strong>{{ g.name }}</strong><br><span class="note">{{ g.description }}</span></td>
<td>{% if g.status == "active" %}<span class="pill supply-available">active</span>{% else %}<span class="pill supply-missing">open</span>{% endif %}</td>
<td><code>wg: {{ g.id }}</code></td>
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
<td>{% if hit %}{{ hit.name }}{% if hit.status == "open" %} <span class="tag">open</span>{% endif %}{% if via != s.id %} <span class="tag">inherited from {{ via | remove: "ISIC-" }}</span>{% endif %}{% else %}<span class="pill supply-missing">no working group</span>{% endif %}</td>
</tr>
{%- endfor -%}
</tbody>
</table>

## Changing the assignment

Open a pull request that adds, moves or removes rows in
`_data/working-group-sectors.csv` (and, for a new group, a row in
`_data/working-groups.csv` with its `kind`, `sector` or `horizontal`, and its
`status`). When an open group starts, its `status` changes from `open` to
`active` in the same way. Curators review it; the *Check data* workflow
rejects a code assigned twice or a code that is not in the sector list. Then run
*Sync labels* so a new group gets its `wg:` label.

Codes are taken from the sector list the repository shares with the
[Industry Function Graph](https://github.com/DIDAS-swiss/industry-function-graph):
all 22 sections and the divisions and classes the graph uses. A group can always
be assigned a section; a more specific code that is missing is added in the graph
first, then reaches this repository with the next sync.
