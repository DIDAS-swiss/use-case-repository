# 2026-11-05: Credential schemas federated from I14Y, Beta-ID added

## Added

- `credentials/beta-id.md`: the Beta-ID, the swiyu Public Beta test credential
  that carries the e-ID's attribute set, with its I14Y dataset
  `urn:vct:ch.admin.bcs.betaid`
- Schema federation from I14Y: `scripts/i14y_sync.py` fetches each referenced
  dataset record and its structure from the public I14Y API into
  `federation/i14y/<credential-id>/` (dataset record, SHACL structure as Turtle
  and JSON-LD, compact attribute list, rendered table)
- Credential pages on the site show the federated schema, with each attribute's
  labels in four languages, type, cardinality and the I14Y concept it conforms to
- `i14y-sync.yml`: refreshes the federation weekly and on changes to credential
  entries, and proposes upstream changes as a pull request
- `i14y_dataset` and `i14y_id` front-matter fields for credentials

## Changed

- `credentials/residence-confirmation.md` references its I14Y dataset
  `urn:vct:ch.egovernment.residency-permit-simple` (DVS, status *Candidate*), and
  its claims use the attribute names of that schema
- Credential references in the use cases and in the credentials index point to
  I14Y where a dataset exists; the e-ID entry points to the Beta-ID dataset until
  an e-ID dataset is published
- Every other credential records that it is not published on I14Y (checked
  2026-11-05)

## Notes for review

- I14Y publishes the Beta-ID attribute as `referende_id_expiry_date`, while the
  issued credential uses `reference_id_expiry_date`. Recorded in the Beta-ID entry
- The glossary records the Beta-ID's attribute-level structure view as
  access-restricted on the I14Y website; the structure export of the public API
  is reachable, and is the source used here
