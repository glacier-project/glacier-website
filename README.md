# GLACIER website

Source of <https://glacier-project.github.io/glacier-website/>.

Built with [MkDocs](https://www.mkdocs.org/) and
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/). All content
is plain Markdown.

## Where things are

| | |
| --- | --- |
| Page content | `docs/` — one Markdown file per page |
| Images | `docs/assets/` |
| Navigation | the `nav:` block in `mkdocs.yml` |
| Colours and branding | `docs/stylesheets/extra.css` (colours), `docs/assets/` (logo, favicon) |
| Everything else configurable | `mkdocs.yml` |
| Deployment | `.github/workflows/deploy.yml` |

## Preview

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

mkdocs serve
```

Then open <http://127.0.0.1:8000>. The site reloads as you edit.

## Build

```bash
mkdocs build --strict
```

`--strict` turns broken internal links and other warnings into errors. This is
what CI runs, so run it before pushing.

## Add a page

1. Create a Markdown file under `docs/`, in the section it belongs to —
   `docs/frost/components/frost-scheduler.md`, say.
2. Add one line to `nav:` in `mkdocs.yml`:

   ```yaml
     - Frost:
         - Components:
             - FrostScheduler: frost/components/frost-scheduler.md
   ```

3. `mkdocs serve` and look at it.

That is the whole procedure. The sidebar, the table of contents, the
previous/next links and the search index all follow from those two steps.

## Add an image

Put the file in `docs/assets/` and reference it with a path relative to the page:

```markdown
![xPPU layout](../assets/xppu-layout.png)
```

## Add a learning resource

Edit `docs/learn/tutorials.md`, `docs/learn/labs.md` or `docs/learn/lectures.md`
and add a section following the pattern already on the page. No new file, no
frontend code.

One rule: **only link to resources that exist and are publicly reachable.** If
something is planned or restricted, describe it in prose rather than presenting
it as a link.

## Change the colours

`docs/stylesheets/extra.css`. The GLACIER brand colours are at the top of the
file with a comment explaining why each theme uses a different shade of them.
It is the only stylesheet on the site.

## Deployment

Pushing to `main` triggers `.github/workflows/deploy.yml`, which builds the site
and publishes it to the `gh-pages` branch, which GitHub Pages serves.

To publish from your machine instead — for instance if the workflow is broken:

```bash
mkdocs gh-deploy
```

## Conventions worth keeping

- **Markdown, not HTML.** Material has built-in support for admonitions,
  content tabs, [grid cards](https://squidfunk.github.io/mkdocs-material/reference/grids/)
  and mermaid diagrams. Reach for those before writing a `<div>`.
- **One custom stylesheet.** If a page needs styling, it probably needs a
  Material feature instead.
- **No JavaScript.** There is none, and the site does not need any.
- **Verify technical claims against the repositories.** The GLACIER libraries
  move; the website is the lowest-authority source about them. `CONTENT_AUDIT.md`
  records what was checked, against which commit, and when.
- **Renaming a page breaks its URL.** Add an entry to `redirect_maps` in
  `mkdocs.yml` when you move one.

## Dependencies

Four, in `requirements.txt`:

| Package | Why |
| --- | --- |
| `mkdocs` | the site generator |
| `mkdocs-material` | the theme |
| `mkdocs-redirects` | keeps old URLs working after pages move |
| `lf-pygments-lexer` | syntax highlighting for Lingua Franca code blocks (` ```lf-python `) |
