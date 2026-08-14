#!/usr/bin/env python3
"""Print and validate the public navigation of the GLACIER website.

The `nav:` block in mkdocs.yml is the single source of truth for the public site
structure. This script only reads it -- nothing here is hardcoded.

    python scripts/site_tree.py             print the public navigation tree
    python scripts/site_tree.py --check     report nav/file inconsistencies
    python scripts/site_tree.py --site-map  rewrite docs/reference/site-map.md

Exit codes: 0 fine, 1 problems found, 2 the configuration could not be read.
"""

from __future__ import annotations

import argparse
import posixpath
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, NoReturn

REPO = Path(__file__).resolve().parent.parent
CONFIG = REPO / "mkdocs.yml"
SITE_MAP = "reference/site-map.md"
GENERATED_BY = "<!-- GENERATED from mkdocs.yml by scripts/site_tree.py. Do not edit manually. -->"

# Markdown files under docs/ that are deliberately outside the public
# navigation. Everything listed here needs a reason next to it.
NAV_EXEMPT: set[str] = set()

H1 = re.compile(r"^#\s+(.*?)\s*#*\s*$")


@dataclass
class Node:
    """One entry in the navigation: a page, a section, or an external link."""

    title: str
    path: str | None = None  # docs-relative Markdown path, if any
    url: str | None = None  # external URL, if any
    children: list["Node"] = field(default_factory=list)


def fail(message: str, code: int = 2) -> NoReturn:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def load_mkdocs_config() -> Any:
    """Load mkdocs.yml through MkDocs itself, so its custom YAML tags resolve."""
    try:
        from mkdocs.config import load_config
    except ImportError:
        fail("MkDocs is not installed. Run: pip install -r requirements.txt")
    try:
        return load_config(str(CONFIG))
    except Exception as exc:  # MkDocs raises many config-error types
        fail(f"could not read {CONFIG.name}: {exc}")


def page_title(docs_dir: Path, path: str) -> str:
    """The page's first H1, which is the title MkDocs would use."""
    file = docs_dir / path
    if not file.is_file():
        return path
    in_fence = False
    for line in file.read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        elif not in_fence and (match := H1.match(line)):
            return match.group(1).replace("`", "")
    return path


def build_nodes(items: list, docs_dir: Path) -> list[Node]:
    """Turn a MkDocs nav list into Nodes, resolving implicit titles."""
    nodes = []
    for item in items:
        if isinstance(item, str):  # bare page, title comes from its H1
            nodes.append(Node(page_title(docs_dir, item), path=item))
            continue
        (title, value), = item.items()
        if isinstance(value, list):
            nodes.append(as_section(title, build_nodes(value, docs_dir)))
        elif "://" in value:
            nodes.append(Node(title, url=value))
        else:
            nodes.append(Node(title, path=value))
    return nodes


def as_section(title: str, children: list[Node]) -> Node:
    """Fold a leading `<section>/index.md` into the section itself.

    This mirrors the theme's `navigation.indexes` feature: such a section header
    is a link to its own landing page rather than a separate child entry.
    """
    if children and children[0].path and children[0].path.endswith("index.md"):
        return Node(title, path=children[0].path, children=children[1:])
    return Node(title, children=children)


def walk(nodes: list[Node]):
    for node in nodes:
        yield node
        yield from walk(node.children)


# --- printing ---------------------------------------------------------------


def render_tree(nodes: list[Node], prefix: str = "") -> list[str]:
    lines = []
    for index, node in enumerate(nodes):
        last = index == len(nodes) - 1
        lines.append(f"{prefix}{'└── ' if last else '├── '}{node.title}")
        lines += render_tree(node.children, prefix + ("    " if last else "│   "))
    return lines


# --- checking ---------------------------------------------------------------


def check(nodes: list[Node], docs_dir: Path) -> list[str]:
    """Return one message per inconsistency between nav and docs/."""
    problems = []
    seen: dict[str, list[str]] = {}

    for node in walk(nodes):
        if node.path is None:
            continue
        if not (docs_dir / node.path).is_file():
            problems.append(
                f"nav entry '{node.title}' points to missing file docs/{node.path}"
            )
        seen.setdefault(node.path, []).append(node.title)

    for path, titles in sorted(seen.items()):
        if len(titles) > 1:
            labels = ", ".join(f"'{title}'" for title in titles)
            problems.append(f"docs/{path} is referenced {len(titles)} times in nav ({labels})")

    for file in sorted(docs_dir.rglob("*.md")):
        path = file.relative_to(docs_dir).as_posix()
        if path not in seen and path not in NAV_EXEMPT:
            problems.append(
                f"docs/{path} is not reachable from nav "
                "(add it to nav: in mkdocs.yml, or to NAV_EXEMPT in scripts/site_tree.py)"
            )
    return problems


# --- site map ---------------------------------------------------------------


def render_site_map(nodes: list[Node]) -> str:
    """The Markdown body of the public Site map page."""
    lines = [
        GENERATED_BY,
        "",
        "# Site map",
        "",
        "Every public page on this website, in navigation order.",
        "",
    ]
    lines += render_site_map_list(nodes, depth=0)
    return "\n".join(lines) + "\n"


def render_site_map_list(nodes: list[Node], depth: int) -> list[str]:
    here = posixpath.dirname(SITE_MAP)
    lines = []
    for node in nodes:
        target = node.url or (node.path and posixpath.relpath(node.path, here))
        label = f"[{node.title}]({target})" if target else node.title
        lines.append(f"{'    ' * depth}- {label}")
        lines += render_site_map_list(node.children, depth + 1)
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Print and validate the public navigation.")
    parser.add_argument("--check", action="store_true",
                        help="report nav/file inconsistencies and a stale site map")
    parser.add_argument("--site-map", action="store_true",
                        help=f"rewrite docs/{SITE_MAP} from the navigation")
    args = parser.parse_args()

    config = load_mkdocs_config()
    docs_dir = Path(config["docs_dir"])
    if not config["nav"]:
        fail("mkdocs.yml has no nav: block, so there is no site structure to read")
    nodes = build_nodes(config["nav"], docs_dir)
    site_map_file = docs_dir / SITE_MAP
    site_map_text = render_site_map(nodes)

    if args.site_map:
        changed = not site_map_file.is_file() or site_map_file.read_text(encoding="utf-8") != site_map_text
        site_map_file.write_text(site_map_text, encoding="utf-8")
        print(f"{'updated' if changed else 'unchanged'}: docs/{SITE_MAP}")
        return 0

    if args.check:
        problems = check(nodes, docs_dir)
        if site_map_file.is_file() and site_map_file.read_text(encoding="utf-8") != site_map_text:
            problems.append(f"docs/{SITE_MAP} is out of date (run: make site-map)")
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        pages = sum(1 for node in walk(nodes) if node.path)
        count = len(problems)
        print(f"{pages} public pages, {count} problem{'' if count == 1 else 's'}")
        return 1 if problems else 0

    print(config["site_name"])
    print("\n".join(render_tree(nodes)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
