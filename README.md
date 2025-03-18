# GLACIER Website

This is the repository for the GLACIER website. The website is built using [mkdocs](https://www.mkdocs.org/) and the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme. 
To build the website locally, you need to have Python installed on your machine.

## Installation

To install the required dependencies, run the following command:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Development

To run the website locally, run the following command:

```bash
mkdocs serve
```

## Publishing the Website

To publish the website, run the following command:

```bash
mkdocs gh-deploy
```

