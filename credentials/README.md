# Credentials

Every credential type that a published use case relies on, with its supply
status, plus test credentials to build them with. Schemas are **not** defined
here. Where a credential is published on [I14Y](https://www.i14y.admin.ch/),
the entry references the I14Y dataset and its schema is federated into
[`federation/i14y/`](../federation/i14y/); otherwise it links eCH or a sectoral
repository once a schema is published.

Supply status: **available** means issued in production; **emerging** means
announced, piloted or in build; **missing** means no known issuer.

## Gap board

These credentials are needed by published use cases but have no issuer in
production. They are the open opportunities for potential issuers, ranked by the
number of use cases they block. Live demand signals are the
[open `credential-need` issues](https://github.com/DIDAS-swiss/use-case-repository/issues?q=is%3Aissue+is%3Aopen+label%3Acredential-need).
To offer to issue one, open a
[Credential need / supply signal](https://github.com/DIDAS-swiss/use-case-repository/issues/new?template=credential-signal.yml) issue.

| Credential | Supply | Likely issuer | Blocks use cases |
|---|---|---|---|
| [Vehicle registration](vehicle-registration.md) | missing | Cantonal road traffic office | 2: [leasing](../use-cases/vehicle-leasing.md), [claims](../use-cases/motor-vehicle-claims-processing.md) |
| [Motor vehicle liability insurance confirmation](motor-vehicle-liability-insurance-confirmation.md) | missing | Insurers / SVV | 2: [leasing](../use-cases/vehicle-leasing.md), [claims](../use-cases/motor-vehicle-claims-processing.md) |
| [Salary and employment confirmation](salary-employment-confirmation.md) | missing | Employers / sector body | 1: [leasing](../use-cases/vehicle-leasing.md) |
| [Accident report](accident-report.md) | missing | Cantonal police | 1: [claims](../use-cases/motor-vehicle-claims-processing.md) |
| [Repair assessment](repair-assessment.md) | missing | Certified garage or expert | 1: [claims](../use-cases/motor-vehicle-claims-processing.md) |
| [Residence confirmation](residence-confirmation.md) ([I14Y](https://www.i14y.admin.ch/de/catalog/datasets/urn:vct:ch.egovernment.residency-permit-simple/description)) | emerging | Municipal residents' office | 1: [leasing](../use-cases/vehicle-leasing.md) |
| [Debt enforcement register extract](debt-enforcement-extract.md) | emerging | Debt enforcement office | 1: [leasing](../use-cases/vehicle-leasing.md) |
| [Swiss e-ID](swiss-e-id.md) | emerging | fedpol | 2: [leasing](../use-cases/vehicle-leasing.md), [claims](../use-cases/motor-vehicle-claims-processing.md) |

## All credentials

| Credential | Ambition level | Issuer type | Supply | Stage | Used by | I14Y |
|---|---|---|---|---|---|---|
| [Accident report](accident-report.md) | AL2 | cantonal | missing | signal | 1 | not published |
| [Beta-ID](beta-id.md) (test credential) | AL1 | federal | available (Public Beta) | candidate | test stand-in for the e-ID | [`urn:vct:ch.admin.bcs.betaid`](https://www.i14y.admin.ch/de/catalog/datasets/urn:vct:ch.admin.bcs.betaid/description) · [schema](../federation/i14y/beta-id/) |
| [Debt enforcement register extract](debt-enforcement-extract.md) | AL2 | cantonal | emerging | signal | 1 | not published |
| [Motor vehicle liability insurance confirmation](motor-vehicle-liability-insurance-confirmation.md) | AL3 | private | missing | signal | 2 | not published |
| [Repair assessment](repair-assessment.md) | AL3 | private | missing | signal | 1 | not published |
| [Residence confirmation](residence-confirmation.md) | AL2 | municipal | emerging | signal | 1 | [`urn:vct:ch.egovernment.residency-permit-simple`](https://www.i14y.admin.ch/de/catalog/datasets/urn:vct:ch.egovernment.residency-permit-simple/description) · [schema](../federation/i14y/residence-confirmation/) |
| [Salary and employment confirmation](salary-employment-confirmation.md) | AL3 | private | missing | signal | 1 | not published |
| [Swiss e-ID](swiss-e-id.md) | AL1 | federal | emerging | candidate | 2 | not published; attribute set as [Beta-ID](https://www.i14y.admin.ch/de/catalog/datasets/urn:vct:ch.admin.bcs.betaid/description) |
| [Vehicle registration](vehicle-registration.md) | AL2 | cantonal | missing | signal | 2 | not published |

"Not published" means no credential dataset was found on I14Y on 2026-11-05.
