# 2026-11-09: The project board stays in step with the repository

## Added

- `project-sync.yml` (*Sync project board*): adds every issue and pull request to
  [project 6](https://github.com/orgs/DIDAS-swiss/projects/6), sets its Type from
  the labels and its Status from what happens (opened, pull request in review,
  merged, completed, not pursued, reopened), without overriding a status a curator
  set by hand. Run by hand, it creates the Status options and the Type field,
  writes the board's description and README, and adds existing items
- `PROJECT.md`: how the automation works and the one-time setup (a token stored as
  `PROJECT_TOKEN`, the views, public visibility)

## Notes for review

- The board was empty because GitHub Projects can only be written with a token
  that has project rights, which the repository's Actions token does not have.
  Without `PROJECT_TOKEN` the workflow only logs a warning
- Views cannot be created through GitHub's API and are set up by hand once
