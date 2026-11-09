# 2026-11-09: Project field Kind instead of Type; Node 24 actions

## Changed

- The project board's item category is the field **Kind**: GitHub Projects
  reserve the name *Type* for issue types, so creating a field of that name
  failed. Views in `PROJECT.md` filter with `kind:"Use case"` and so on
- All workflows use `actions/checkout@v5` and `actions/github-script@v8`, which
  run on Node.js 24, the version GitHub's runners now use
