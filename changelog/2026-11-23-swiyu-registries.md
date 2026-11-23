# 2026-11-23: swiyu trust and base registries

## Added

- `scripts/swiyu_sync.py` queries the swiyu trust registry and base registry
  (identifier registry) in production and in the sandbox, without
  authentication. It writes three files in `_data/`:
  - `swiyu-registry-totals.csv`: identity trust statements, active DIDs,
    verification query statements, verifiers and protected verification
    authorizations per environment;
  - `swiyu-registry.csv`: per credential with `vct_values`, the verification
    query statements that ask for it, their verifiers, and whether a type is
    on the protected issuance trust list;
  - `swiyu-organisations.csv`: organisations with an identity trust
    statement, with name and UID as published, DIDs and active DIDs in the
    base registry, verification query statements and the credentials asked
    for. Production lists every identity; the sandbox only those with a UID
    or marked as state actor. `_data/swiyu-unlisted.csv` keeps a name off.
- The *Sync federated sources* workflow runs it weekly and proposes changes as
  a pull request.
- `vct_values` in the credential front matter: set for the Beta-ID, the eLFA,
  the digital driving licence and the e-ID.
- Page [swiyu registries](../registries.md), linked in the navigation.
- `check_data.py` warns when `supply: available` has no production evidence in
  the snapshot, or `supply: missing` has.

## Changed

- VISION.md: trust registry references are referenced, with a weekly snapshot
  as evidence.
- dependencies.md and credentials/README.md link the new page.
- The swiyu test environment is called «sandbox» throughout (dependencies.md,
  credentials/README.md, credentials/beta-id.md).
