# Tutorials

Self-paced material that builds something from beginning to end.

## Available now

There is no standalone tutorial published on this site yet. What exists today
and serves the same purpose:

### Frost worked examples

Three complete, runnable programs on this site, each covering one interaction
pattern. They are adapted from Frost's own test suite, so they are verified
against the code they document.

- [Connecting to a link](../frost/examples/link-registration.md)
- [Invoking a method](../frost/examples/method-invocation.md)
- [Subscribing to a variable](../frost/examples/variable-subscription.md)

### frost-playground

[:octicons-mark-github-16: glacier-project/frost-playground](https://github.com/glacier-project/frost-playground)

A repository of larger self-contained examples — publisher/subscriber,
sensor/alarm, a stock-market simulation and a production scheduler — with a
devcontainer so they run without installing a toolchain locally.

!!! warning "Targets Frost v1.0.0"

    The playground pins Frost at the `main` branch, so its sources use the
    v1.0.0 component names rather than the ones documented on this site. It is
    still a useful read; expect `FrostMachine` where these pages say
    `FrostReactor`. See [Versions](../reference/versions.md).

### frost-template

[:octicons-mark-github-16: glacier-project/frost-template](https://github.com/glacier-project/frost-template)

A GitHub template to start a Frost project from: directory layout, configuration
files, Frost as a submodule and a main reactor already in place.

### Larger systems to read

Two full applications, useful once the basics are familiar:

- [xppu-frost](https://github.com/glacier-project/xppu-frost) — a digital twin of
  the Extended Pick&Place Unit, with a stack, crane, stamp and conveyors, and
  physics-based variants of some components.
- [ice-frost](https://github.com/glacier-project/ice-frost) — the ICE laboratory
  production line, with a recipe-driven scheduler.

## What a published tutorial will look like

When a tutorial is published here it will be one page carrying:

- what you will have built by the end, and roughly how long it takes;
- what you need installed before starting;
- the steps, with the code inline;
- a link to a repository holding the finished result.

## Adding one

Add a section to this page following the pattern above, and link to wherever the
material lives. One Markdown file, no other change.
