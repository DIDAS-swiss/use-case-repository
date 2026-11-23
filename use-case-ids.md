---
title: Use-case ids
description: The id of every published entry and candidate, for the relation fields of the use-case form.
---

# Use-case ids

The id of every use case, published entry or candidate. The fields *Related*,
*Upstream*, *Downstream* and *Variant of* of the
[use-case form](https://github.com/DIDAS-swiss/use-case-repository/issues/new?template=use-case-candidate.yml)
take these ids. The list is built from `use-cases/` and the batch files in
`intake/` whenever the form is rebuilt.

<table>
<thead><tr><th>Id</th><th>Use case</th><th></th></tr></thead>
<tbody>
{%- for u in site.data["use-case-index"] -%}
<tr>
<td><code>{{ u.id }}</code></td>
<td>{% if u.kind == "entry" %}<a href="{{ '/use-cases/' | append: u.id | append: '.html' | relative_url }}">{{ u.title }}</a>{% else %}<a href="https://github.com/{{ site.repository }}/issues?q=is%3Aissue+label%3Ause-case+%22{{ u.id }}%22">{{ u.title }}</a>{% endif %}</td>
<td><span class="tag">{% if u.kind == "entry" %}published{% else %}candidate{% endif %}</span></td>
</tr>
{%- endfor -%}
</tbody>
</table>
