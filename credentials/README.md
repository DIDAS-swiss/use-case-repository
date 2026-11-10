# Credentials

Every credential type that a use case relies on, published or still a
candidate in the [backlog](../backlog.md), with its supply status, plus test
credentials to build them with. Schemas are **not** defined
here. Where a credential is published on [I14Y](https://www.i14y.admin.ch/),
the entry references the I14Y dataset and its schema is federated into
[`federation/i14y/`](../federation/i14y/); otherwise it links eCH or a sectoral
repository once a schema is published.

Supply status: **available** means issued in production; **emerging** means
announced, piloted or in build; **missing** means no known issuer.

## Gap board

These credentials are needed by use cases in the backlog but have no issuer in
production. They are the open opportunities for potential issuers, ranked by the
number of use cases they block. Live demand signals are the
[open `credential-need` issues](https://github.com/DIDAS-swiss/use-case-repository/issues?q=is%3Aissue+is%3Aopen+label%3Acredential-need).
To offer to issue one, open a
[Credential need / supply signal](https://github.com/DIDAS-swiss/use-case-repository/issues/new?template=credential-signal.yml) issue.

| Credential | Supply | Likely issuer | Blocks use cases (candidates) |
|---|---|---|---|
| [Digital driving licence](digital-driving-licence.md) | emerging | Cantonal road traffic office | 7: [traffic control](https://github.com/DIDAS-swiss/use-case-repository/issues/40), [carsharing](https://github.com/DIDAS-swiss/use-case-repository/issues/45), [car rental](https://github.com/DIDAS-swiss/use-case-repository/issues/23), [corporate carsharing](https://github.com/DIDAS-swiss/use-case-repository/issues/55), [fleet](https://github.com/DIDAS-swiss/use-case-repository/issues/63), [age proof](https://github.com/DIDAS-swiss/use-case-repository/issues/52), [learner carsharing](https://github.com/DIDAS-swiss/use-case-repository/issues/76) |
| [Vehicle registration](vehicle-registration.md) | missing | Cantonal road traffic office | 2: [leasing](https://github.com/DIDAS-swiss/use-case-repository/issues/123), [claims](https://github.com/DIDAS-swiss/use-case-repository/issues/83) |
| [Motor vehicle liability insurance confirmation](motor-vehicle-liability-insurance-confirmation.md) | missing | Insurers / SVV | 2: [leasing](https://github.com/DIDAS-swiss/use-case-repository/issues/123), [claims](https://github.com/DIDAS-swiss/use-case-repository/issues/83) |
| [Salary and employment confirmation](salary-employment-confirmation.md) | missing | Employers / sector body | 1: [leasing](https://github.com/DIDAS-swiss/use-case-repository/issues/123) |
| [Accident report](accident-report.md) | missing | Cantonal police | 1: [claims](https://github.com/DIDAS-swiss/use-case-repository/issues/83) |
| [Repair assessment](repair-assessment.md) | missing | Certified garage or expert | 1: [claims](https://github.com/DIDAS-swiss/use-case-repository/issues/83) |
| [Immunization record](immunization-record.md) | emerging | The vaccinator that administered the dose | 1: [vaccination](https://github.com/DIDAS-swiss/use-case-repository/issues/122) |
| [Residence confirmation](residence-confirmation.md) ([I14Y](https://www.i14y.admin.ch/de/catalog/datasets/urn:vct:ch.egovernment.residency-permit-simple/description)) | emerging | Municipal residents' office | 1: [leasing](https://github.com/DIDAS-swiss/use-case-repository/issues/123) |
| [Debt enforcement register extract](debt-enforcement-extract.md) | emerging | Debt enforcement office | 1: [leasing](https://github.com/DIDAS-swiss/use-case-repository/issues/123) |
| [Swiss e-ID](swiss-e-id.md) | emerging | fedpol | 2: [leasing](https://github.com/DIDAS-swiss/use-case-repository/issues/123), [claims](https://github.com/DIDAS-swiss/use-case-repository/issues/83) |

## All credentials

| Credential | Ambition level | Issuer type | Supply | Stage | Needed by (candidates) | Schema |
|---|---|---|---|---|---|---|
| [Accident report](accident-report.md) | AL2 | cantonal | missing | signal | 1 | none |
| [Beta-ID](beta-id.md) (test credential) | AL1 | federal | available (Public Beta) | candidate | test stand-in for the e-ID | on I14Y (Recorded): [`urn:vct:ch.admin.bcs.betaid`](https://www.i14y.admin.ch/de/catalog/datasets/urn:vct:ch.admin.bcs.betaid/description) · [schema](../federation/i14y/beta-id/) |
| [Debt enforcement register extract](debt-enforcement-extract.md) | AL2 | cantonal | emerging | signal | 1 | none |
| [Digital driving licence](digital-driving-licence.md) | AL2 | cantonal | emerging | signal | 7 | none; announced on [swiyu](https://swiyu.admin.ch/de/oekosystem) |
| [Electronic learner's permit (eLFA)](learner-permit-elfa.md) | AL2 | cantonal | available (live; about 100,000 active, DIDAS 10.11.2026) | signal | 2 | emerging: issuer-side schema, not on I14Y (checked 2026-11-10) |
| [Immunization record](immunization-record.md) | AL3 | private | emerging | signal | 1 | emerging: showcase type `urn:vct:ch.didas.health.immunization:1.0`, not on I14Y |
| [Motor vehicle liability insurance confirmation](motor-vehicle-liability-insurance-confirmation.md) | AL3 | private | missing | signal | 2 | none |
| [Repair assessment](repair-assessment.md) | AL3 | private | missing | signal | 1 | none |
| [Residence confirmation](residence-confirmation.md) | AL2 | municipal | emerging | signal | 1 | on I14Y (Candidate): [`urn:vct:ch.egovernment.residency-permit-simple`](https://www.i14y.admin.ch/de/catalog/datasets/urn:vct:ch.egovernment.residency-permit-simple/description) · [schema](../federation/i14y/residence-confirmation/) |
| [Salary and employment confirmation](salary-employment-confirmation.md) | AL3 | private | missing | signal | 1 | none |
| [Swiss e-ID](swiss-e-id.md) | AL1 | federal | emerging | candidate | 2 | none; attribute set as [Beta-ID](https://www.i14y.admin.ch/de/catalog/datasets/urn:vct:ch.admin.bcs.betaid/description) |
| [Vehicle registration](vehicle-registration.md) | AL2 | cantonal | missing | signal | 2 | none |

"None" means no schema is known; for each, no credential dataset was found on I14Y on 2026-11-05 (learner's permit and driving licence: 2026-11-10). All credential datasets on I14Y are listed on the [Anchors page](../anchors.md#credential-datasets-on-i14y).
