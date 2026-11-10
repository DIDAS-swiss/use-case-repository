---
title: Shared dependencies
---

# Shared dependencies

Many use cases depend on the same infrastructure. Its timing is kept here once,
with its source and the date it was last checked, instead of in every use case.
A use case names the dependency in its batch row (`dependencies`) and its issue
links this page; dependencies that only concern one project stay in that use
case.

## E-ID and trust infrastructure

Used by the use cases whose `dependencies` say `e-id` (the state e-ID, which
also needs the trust infrastructure) or `trust-infrastructure` (the federal
trust infrastructure, swiyu, without the e-ID).

| | Status | Source |
|---|---|---|
| State e-ID | Introduction postponed on 30 June 2026 for further security work; the date will be announced once that work is largely complete. No new date announced. | Federal Council, [Neuer Zeitplan für die Einführung der E-ID und der Vertrauensinfrastruktur](https://www.admin.ch/de/newnsb/4ZNYpSk3J1-U), 30 June 2026; [BJ, Staatliche E-ID](https://www.bj.admin.ch/de/staatliche-e-id) |
| Trust infrastructure (swiyu) | Expected to start operating in the first half of 2027, independently of the e-ID. Until then the swiyu Public Beta is a test environment. | Same sources |
| Electronic signatures | The e-ID is not a signing tool. It can be used to obtain electronic signatures from certified providers under ZertES, including qualified electronic signatures (QES), and so enable or trigger a remote signing flow. Remote signing capabilities are planned; which providers integrate the e-ID, and when, is not established here. | swiyu, [Hilfe zur e-ID](https://swiyu.admin.ch/de/hilfe-e-id) ("Kann ich mit der e-ID elektronisch signieren?") |

**Last checked: 10 November 2026.** The BJ page lists no announcement after
30 June 2026. Whoever checks again updates the date and, where the status
changed, the table; the use cases follow through their link.

### What this means for a use case

- A use case that needs the e-ID is not blocked from being described, drafted or
  qualified; its pilot or production depends on the dates above.
- Where a use case needs a signature, it names what the signature is for: the
  identity verified with the e-ID, the document the person approves, the signing
  provider and the signature level the relying party requires. A signature alone
  does not satisfy notarisation or a public deed.
- Identity proofing, later authentication (for example with AGOV), signature,
  authority to act for someone, and entitlement to a benefit are different
  facts. Each use case says which of them its decision needs.
