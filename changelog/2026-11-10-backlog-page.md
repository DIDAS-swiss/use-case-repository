# 2026-11-10: Backlog page with the whole lifecycle

## Added

- A [Backlog page](https://didas-swiss.github.io/use-case-repository/backlog.html)
  with every use case and its step: candidate, taken by a working group,
  drafting, published (with its lifecycle stage) or not pursued. Counts per step,
  filters for sector, working group, lighthouse and text, and links to each
  issue, draft pull request and entry
- The page reads the use-case issues and open pull requests from the public
  GitHub API when it opens, so it is always current without a build; published
  entries come from the site. The project board's working status (Triage,
  In review) needs a token and is not shown
- *Backlog* in the site navigation and a *See the backlog* button on the home page
