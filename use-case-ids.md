---
title: Use-case ids
---

# Use-case ids

Every use case by its id: the published entries and the candidates of the
intake batches. Use these ids in the *Related*, *Upstream* and *Downstream* fields
of the [use-case form](https://github.com/DIDAS-swiss/use-case-repository/issues/new?template=use-case-candidate.yml).
The list is built from the repository with the form.

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
