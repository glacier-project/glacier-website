# GLACIER website

Source for the public GLACIER website at
<https://glacier-project.github.io/glacier-website/>. It is a static
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/) site; all
content is plain Markdown. This README is the maintenance manual — the site's
own content is under `docs/`.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

make serve      # preview at http://127.0.0.1:8000, reloads as you edit
```

`make help` lists every maintenance command. The Makefile uses `.venv/bin/python`
when it exists, so the commands work whether or not the venv is activated.

## Where does this go?

| I want to... | Edit/add here |
| --- | --- |
| Change the homepage | `docs/index.md` |
| Add overview content | `docs/overview/` |
| Document Frost | `docs/frost/` |
| Add a tutorial, lab or lecture | `docs/learn/tutorials.md`, `labs.md`, `lectures.md` |
| Add repository/version reference | `docs/reference/` |
| Add an image | `docs/assets/` |
| Add a diagram | `docs/assets/diagrams/` (hand-written SVG) |
| Change navigation | `nav:` in `mkdocs.yml` |
| Change colours or styles | `docs/stylesheets/extra.css` (the `--glc-*` tokens at the top) |
| Change the logo | `overrides/.icons/glacier/mark.svg`, favicon in `docs/assets/` |
| Change header/footer templates | `overrides/` — keep these minimal |
| Change anything else configurable | `mkdocs.yml` |
| Change deployment | `.github/workflows/deploy.yml` |

## Repository layout

```
docs/               Public website content, one Markdown file per page.
  index.md            Homepage.
  overview/           What GLACIER is, its architecture and ecosystem.
  frost/              Frost technical documentation.
  learn/              Tutorials, labs and lectures.
  reference/          Repositories, versions, generated site map.
  project/            About the project.
  assets/             Images, diagrams (SVG) and the favicon.
  stylesheets/        extra.css — GLACIER colours and small customisations.
overrides/          MkDocs Material template overrides and the logo mark.
scripts/            Maintenance scripts (see below).
mkdocs.yml          Navigation and all MkDocs configuration.
requirements.txt    Pinned Python dependencies.
Makefile            Maintenance commands.
.github/workflows/  CI and deployment.
```

## Common tasks

**Add a page.** Create the Markdown file under the right `docs/` section, add
one line to `nav:` in `mkdocs.yml`, then run `make check`. The sidebar, table of
contents, previous/next links and search index all follow from those two steps.

**Add an image.** Put it in `docs/assets/` and reference it relative to the
page: `![xPPU layout](../assets/xppu-layout.png)`.

**Add a diagram.** Diagrams are hand-written SVG in `docs/assets/diagrams/`,
inlined so they follow the light/dark theme. Copy an existing file, use the
`var(--d-*)` colour variables from `extra.css`, then include it with
`--8<-- "diagrams/your-diagram.svg"`. **No blank lines and no HTML comments
inside the SVG file** — Markdown treats both as block terminators and will
shred it, silently.

**Add a tutorial, lab or lecture.** Edit `docs/learn/tutorials.md`,
`docs/learn/labs.md` or `docs/learn/lectures.md` and add a section following the
pattern already there. No new file. Only link to resources that exist and are
publicly reachable.

**Rename or move a page.** That breaks its URL — add an entry to
`redirect_maps` in `mkdocs.yml`.

**See every public page.** `make site-tree` prints the whole navigation:

```
glacier
├── Home
├── Overview
│   ├── Architecture
│   └── Ecosystem
...
```

**Update the public site map.** `make site-map` regenerates
`docs/reference/site-map.md` from `nav:`. That file is generated and committed;
never edit it by hand. `make check` fails if it is stale.

**Validate before committing.** `make check` — a strict MkDocs build plus the
navigation consistency checks.

## Maintenance tools

`scripts/site_tree.py` — reads the `nav:` block from `mkdocs.yml` (the single
source of truth for the public site structure) and:

- prints the navigation tree (`make site-tree`);
- regenerates `docs/reference/site-map.md` (`make site-map`);
- reports missing nav targets, pages unreachable from nav, duplicate nav
  references and a stale site map (`--check`, run by `make check`).

A page that should exist but stay out of the public navigation goes in the
`NAV_EXEMPT` set at the top of that script, with a reason. It is currently
empty.

There are no other custom maintenance scripts.

## Deployment

Pushing to `main` runs `.github/workflows/deploy.yml`, which builds with
`--strict` and publishes to the `gh-pages` branch that GitHub Pages serves.
Pull requests run the build only. To publish by hand if the workflow is broken:
`mkdocs gh-deploy`.

## Conventions worth keeping

- **No third-party requests.** No web fonts (`theme.font: false` is
  deliberate), no CDN scripts, no JavaScript. Anything loading from another host
  undoes this.
- **Markdown, not HTML.** Material has admonitions, content tabs, grid cards and
  buttons built in. Reach for those before writing a `<div>`.
- **Verify technical claims against the repositories.** The GLACIER libraries
  move and this website is the lowest-authority source about them. See
  `CONTENT_AUDIT.md` for the source and commit provenance already checked.

## Before committing

```bash
make check
git diff --check
```
