# GLACIER website

Source of <https://glacier-project.github.io/glacier-website/>.

Built with [MkDocs](https://www.mkdocs.org/) and
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/). All content
is plain Markdown.

**The published site makes no third-party requests.** No web fonts, no CDN
scripts, no client-side rendering. Keep it that way — see
[Conventions](#conventions-worth-keeping).

## Where things are

| | |
| --- | --- |
| Page content | `docs/` — one Markdown file per page |
| Images | `docs/assets/` |
| Diagrams | `docs/assets/diagrams/` — plain SVG |
| Navigation | the `nav:` block in `mkdocs.yml` |
| Colours and branding | `docs/stylesheets/extra.css` (colours), `docs/assets/` + `overrides/.icons/glacier/` (logo) |
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

## Add a diagram

Diagrams are hand-written SVG in `docs/assets/diagrams/`, inlined into the page
so they follow the light/dark theme. There is no diagram library and no
JavaScript.

1. Copy an existing file in `docs/assets/diagrams/` and edit the shapes.
   Use `var(--d-line)`, `var(--d-fill)`, `var(--d-ink)`, `var(--d-muted)`,
   `var(--d-accent)` and `var(--d-accent-soft)` for colours — those are defined
   in `extra.css` and differ per theme. Give the `<svg>` a `viewBox` and no
   `width`/`height`, and an `aria-label` describing it.
2. Drop it into the page:

   ```markdown
   <figure class="glacier-diagram" markdown="span">
   --8<-- "diagrams/your-diagram.svg"
   <figcaption>What the diagram shows.</figcaption>
   </figure>
   ```

### One rule for diagram SVGs

**No blank lines and no HTML comments inside the file.** Markdown treats
both as block terminators and will shred the SVG into paragraphs. `mkdocs build`
will not warn you; the page will just look wrong. Put explanation in the
`aria-label` instead, which doubles as the screen-reader description.

## Add a learning resource

Edit `docs/learn/tutorials.md`, `docs/learn/labs.md` or `docs/learn/lectures.md`
and add a section following the pattern already on the page. No new file, no
frontend code.

One rule: **only link to resources that exist and are publicly reachable.** If
something is planned or restricted, describe it in prose rather than presenting
it as a link.

## Change the colours

`docs/stylesheets/extra.css`. The top of the file holds the GLACIER design
system's `--glc-*` tokens for each theme, and the block under each one maps them
onto the variables Material uses. Re-branding means editing those token values
and nothing else.

The tokens come from the GLACIER design system (`glacier.css`). Keep them in
step with it rather than inventing new colours here.

## Change the logo

Two pieces, matching the design system's lockup:

- the mark is `overrides/.icons/glacier/mark.svg`, set as `theme.icon.logo` in
  `mkdocs.yml`. It is inlined as SVG and drawn in `currentColor`, so it follows
  the theme. Keep `fill="none"` on each `<path>` — Material sets
  `fill: currentColor` on the logo and would otherwise fill the shape in.
- the wordmark is live text, from `site_name` in `mkdocs.yml`.

`docs/assets/favicon.svg` is a separate copy of the mark, with fixed colours,
because a favicon renders outside the page and cannot inherit anything.

## Deployment

Pushing to `main` triggers `.github/workflows/deploy.yml`, which builds the site
and publishes it to the `gh-pages` branch, which GitHub Pages serves.

To publish from your machine instead — for instance if the workflow is broken:

```bash
mkdocs gh-deploy
```

## Conventions worth keeping

- **No third-party requests.** `theme.font: false` is deliberate: Material's
  default pulls fonts from Google, which costs a render-blocking request and
  sends visitor IPs to Google before the cookie dialogue is answered. Diagrams
  are static SVG for the same reason — the previous mermaid setup fetched 3.5 MB
  from `unpkg.com` on every page that had a diagram. If you add something that
  loads from another host, you have undone this.
- **Markdown, not HTML.** Material has built-in support for admonitions,
  content tabs, [grid cards](https://squidfunk.github.io/mkdocs-material/reference/grids/)
  and buttons. Reach for those before writing a `<div>`.
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
