---
title: swiyu registries
description: Weekly snapshot of the swiyu trust and base registries, production and sandbox, per credential and organisation.
---

# swiyu registries

The federal trust infrastructure (swiyu) publishes two registries that anyone
can query without authentication, in a production and a sandbox environment
with the same paths:

| Registry | Production | Sandbox |
|---|---|---|
| Trust registry: signed trust statements ([Trust Protocol 2.0](https://swiyu-admin-ch.github.io/specifications/trust-protocol-v2-0/), status: draft) | `trust-reg.trust-infra.swiyu.admin.ch` | `trust-reg.trust-infra.swiyu-int.admin.ch` |
| Base registry (identifier registry): DID logs, `did:webvh` | `identifier-reg.trust-infra.swiyu.admin.ch` | `identifier-reg.trust-infra.swiyu-int.admin.ch` |

The *Sync federated sources* workflow queries both every week
(`scripts/swiyu_sync.py`) and proposes any change as a pull request. The figures
below are those of the last merged sync; the
[history of the snapshot](https://github.com/{{ site.repository }}/commits/main/_data/swiyu-registry-totals.csv)
shows when each was taken. The registries remain the authoritative source.

A verification query statement is a verifier's published request: its purpose
and the credentials and claims it asks for. A DID counts as active when its log
resolves in the base registry and is not deactivated. Signatures are not
checked; the figures are evidence for curators, not a trust decision.

## Totals

<table>
<thead><tr><th>Environment</th><th>Identity trust statements</th><th>Active DIDs</th><th>Verification query statements</th><th>Verifiers</th><th>Protected verification authorizations</th></tr></thead>
<tbody>
{%- for t in site.data["swiyu-registry-totals"] %}
<tr><td>{{ t.environment }}</td><td>{{ t.identity_trust_statements }}</td><td>{{ t.active_identity_dids }}</td><td>{{ t.verification_query_statements }}</td><td>{{ t.verifiers }}</td><td>{{ t.protected_verification_authorizations }}</td></tr>
{%- endfor %}
</tbody>
</table>

## Credentials of this repository

For each credential whose entry names its credential types (`vct_values`): the
verification query statements that ask for one of them, the verifiers behind
those, and whether a type is on the protected issuance trust list. The data
check compares this with the entry's `supply`.

{% assign credentials = site.pages | where: "kind", "credential" %}
<table>
<thead><tr><th>Credential</th><th>Supply (entry)</th><th>Environment</th><th>Verification queries</th><th>Verifiers</th><th>Protected issuance trust list</th></tr></thead>
<tbody>
{%- for r in site.data["swiyu-registry"] %}
{%- assign c = credentials | where_exp: "p", "p.id == r.credential" | first %}
<tr><td>{% if c %}<a href="{{ c.url | relative_url }}">{{ c.title }}</a>{% else %}{{ r.credential }}{% endif %}</td><td>{{ c.supply }}</td><td>{{ r.environment }}</td><td>{{ r.verification_query_statements }}</td><td>{{ r.verifiers }}</td><td>{{ r.protected_issuance_trust_list }}</td></tr>
{%- endfor %}
</tbody>
</table>

## Organisations

Every identity trust statement of both environments, with name and UID exactly
as the trust registry publishes them. An entry in the sandbox shows that an
organisation tests on swiyu, not that it runs a service.
Credentials are those of this repository that the organisation's verification
query statements ask for.

{% for env in site.data["swiyu-registry-totals"] %}
### {{ env.environment | capitalize }}

<table>
<thead><tr><th>Organisation</th><th>UID</th><th>State actor</th><th>DIDs (active)</th><th>Verification queries</th><th>Credentials</th></tr></thead>
<tbody>
{%- for o in site.data["swiyu-organisations"] %}{% if o.environment == env.environment %}
<tr><td>{{ o.organisation }}</td><td>{{ o.uid }}</td><td>{{ o.state_actor }}</td><td>{{ o.dids }} ({{ o.active_dids }})</td><td>{{ o.verification_query_statements }}</td><td>{{ o.credentials }}</td></tr>
{%- endif %}{% endfor %}
</tbody>
</table>
{% endfor %}
