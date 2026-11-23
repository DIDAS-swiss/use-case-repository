---
title: Anchors
description: For each trust flow, Industry Function Graph pattern and I14Y credential dataset, the use cases that reference it.
---

# Anchors

For each trust flow of the DIDAS Trust Flow Diagram Repository, each pattern of
the DIDAS Industry Function Graph and each credential dataset on I14Y, this page
lists the use cases that reference it. A use case records these references in
its fields `trust_flows`, `ifm_patterns` and, through its credentials,
`i14y_dataset`. An item that no use case references is marked *no use case yet*.

The *Sync federated sources* workflow updates the three lists from their
sources every week.

{% assign usecases = site.pages | where: "kind", "use-case" | where_exp: "p", "p.stage" %}

## Trust flows

From the [DIDAS Trust Flow Diagram Repository](https://github.com/DIDAS-swiss/Trust-Flow-Diagram-Repository).

<table>
<thead><tr><th>Trust flow</th><th>Status</th><th>Sector</th><th>Use cases</th></tr></thead>
<tbody>
{%- for f in site.data["trust-flows"] -%}
{%- assign hits = "" -%}
{%- for u in usecases -%}{%- if u.trust_flows contains f.id -%}{%- capture hits %}{{ hits }}<a href="{{ u.url | relative_url }}">{{ u.title }}</a><br>{% endcapture -%}{%- endif -%}{%- endfor -%}
<tr>
<td><a href="{{ f.url }}">{{ f.title }}</a><br><code>{{ f.id }}</code></td>
<td>{{ f.status }}</td>
<td>{{ f.isic_division }}</td>
<td>{% if hits != "" %}{{ hits }}{% else %}<span class="pill supply-missing">no use case yet</span>{% endif %}</td>
</tr>
{%- endfor -%}
</tbody>
</table>

## Use case patterns

From the [DIDAS Industry Function Graph](https://github.com/DIDAS-swiss/industry-function-graph).

<table>
<thead><tr><th>Pattern</th><th>Use cases</th></tr></thead>
<tbody>
{%- for pat in site.data["ifm-patterns"] -%}
{%- assign hits = "" -%}
{%- for u in usecases -%}{%- if u.ifm_patterns contains pat.id -%}{%- capture hits %}{{ hits }}<a href="{{ u.url | relative_url }}">{{ u.title }}</a><br>{% endcapture -%}{%- endif -%}{%- endfor -%}
<tr>
<td><a href="{{ pat.url }}">{{ pat.name }}</a><br><code>{{ pat.id }}</code></td>
<td>{% if hits != "" %}{{ hits }}{% else %}<span class="pill supply-missing">no use case yet</span>{% endif %}</td>
</tr>
{%- endfor -%}
</tbody>
</table>

## Credential datasets on I14Y

Every dataset on [I14Y](https://www.i14y.admin.ch/) identified by a credential
type (`urn:vct:…`), published or still a candidate.

<table>
<thead><tr><th>I14Y dataset</th><th>Publisher</th><th>Registration status</th><th>Credential entry</th></tr></thead>
<tbody>
{%- assign creds = site.pages | where_exp: "p", "p.i14y_dataset" -%}
{%- for d in site.data["i14y-credentials"] -%}
{%- assign c = creds | where: "i14y_dataset", d.identifier | first -%}
<tr>
<td><a href="{{ d.url }}">{{ d.title }}</a><br><code>{{ d.identifier }}</code></td>
<td>{{ d.publisher_name }}</td>
<td>{{ d.registration_status }}</td>
<td>{% if c %}<a href="{{ c.url | relative_url }}">{{ c.title }}</a>{% else %}<span class="pill supply-missing">no entry yet</span>{% endif %}</td>
</tr>
{%- endfor -%}
</tbody>
</table>

## Implementations

<table>
<thead><tr><th>Implementation</th><th>Use case</th></tr></thead>
<tbody>
{%- for u in usecases -%}{%- for impl in u.implementations -%}
{%- assign url = impl | split: " " | first -%}
<tr><td><a href="{{ url }}">{{ url | remove: "https://" }}</a>{{ impl | remove_first: url }}</td><td><a href="{{ u.url | relative_url }}">{{ u.title }}</a></td></tr>
{%- endfor -%}{%- endfor -%}
</tbody>
</table>
