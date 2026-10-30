# 2026-10-30: Published as a GitHub Pages site

## Added

- The repository is published at https://didas-swiss.github.io/use-case-repository/
  by GitHub Pages' built-in Jekyll, from the same Markdown files and with no
  separate build step (`_config.yml`)
- A page layout with the shared DIDAS masthead, section navigation, a facts panel
  built from each entry's front matter (stage, supply, ambition level, sectors,
  steward, titles in DE/FR/IT), and links to the source and to the change form
  (`_layouts/default.html`, `assets/`)

## Changed

- `CONTRIBUTING.md` carries a one-line front matter, without which GitHub Pages
  does not render it; links to the entry templates point to GitHub, because
  Jekyll does not publish files whose names start with `_`
