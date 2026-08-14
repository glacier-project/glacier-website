# About GLACIER

GLACIER is a research project at the **Department of Engineering for Innovation
Medicine** of the **University of Verona**, Italy, in the Section of Engineering
and Physics.

It builds open-source tools for designing, prototyping, monitoring and
optimising cyber-physical production systems, and it uses them in its own
research and teaching.

## Status

GLACIER is under active development, and the documentation on this site tracks
the current development branches of its repositories rather than fixed releases.
See [Versions](../reference/versions.md) for what has been released and how it
differs.

## Contact

For technical support, collaborations or further information:

**Sebastiano Gaiardelli** — [sebastiano.gaiardelli@univr.it](mailto:sebastiano.gaiardelli@univr.it)
Department of Engineering for Innovation Medicine, University of Verona,
Section of Engineering and Physics, Italy

## Contributing

Contributions are welcome across the GLACIER repositories. Each repository takes
issues and pull requests directly:

- [frost](https://github.com/glacier-project/frost/issues)
- [machine-data-model](https://github.com/glacier-project/machine-data-model/issues)
- [frost-planner](https://github.com/glacier-project/frost-planner/issues)

For this website — a broken link, a stale claim, something that does not match
the code — open an issue on
[glacier-website](https://github.com/glacier-project/glacier-website/issues).
Every page has an edit link in its top right corner that goes straight to the
Markdown source on GitHub.

The repositories run their own checks before merging: Frost builds and runs its
Lingua Franca test suite in CI, and `machine-data-model` runs `ruff`, `mypy` and
`pytest` through `tox` with pre-commit hooks. Their READMEs have the details.

## Citing GLACIER

If you use Frost in academic work, cite the INDIN 2025 paper introducing it. The
[frost repository](https://github.com/glacier-project/frost) carries a
`CITATION.cff`, so GitHub's "Cite this repository" button gives you a correct
entry. See [Lectures](../learn/lectures.md) for the full list of papers.

## Licence

The GLACIER libraries are released under permissive BSD licences — BSD 2-Clause
for [frost](https://github.com/glacier-project/frost),
[machine-data-model](https://github.com/glacier-project/machine-data-model) and
[frost-planner](https://github.com/glacier-project/frost-planner), and BSD
3-Clause for [ice-frost](https://github.com/glacier-project/ice-frost) and this
website. Each repository's `LICENSE` file is authoritative; see
[Repositories](../reference/repositories.md) for a per-repository summary.

## Privacy

This site uses Google Analytics to understand which pages are read. Analytics
cookies are only set after you accept them in the consent dialogue, and you can
change that choice at any time through the **Change cookie settings** link in the
footer.
