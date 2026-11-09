# 2026-11-10: The e-ID is not a login

## Changed

- `epd-access-eid-agov` (#2): the e-ID verifies the identity once, when the
  record or the AGOV account used for it is opened; later logins use the AGOV
  account's means. Title, summary, outcome, actors, process flow, credentials and
  trust frameworks corrected; marked as the DIDAS reading of the BJ and BAG
  statements
- #2 adds a representation proof for parents, legal representatives and powers
  of attorney, with `guardianship-delegation` upstream, and names
  `health-professional-credential`, `health-facility-identity` and
  `patient-summary-ips` as related
- Review notes on `agov-login-eid`, `justitia-court-authentication` and
  `card-payment-3ds-eid`, which describe the e-ID as a login or payment
  authenticator
- The intake finds an existing issue by its short id before its title, so a
  corrected title keeps the same issue
