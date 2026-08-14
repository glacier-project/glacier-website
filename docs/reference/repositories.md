# Repositories

All GLACIER code lives in the
[glacier-project](https://github.com/glacier-project) organisation on GitHub.

This page lists the **public** repositories that are part of the platform or
demonstrate it. The organisation also contains private repositories for work in
progress; those are not listed here.

## Core libraries

### frost

[:octicons-mark-github-16: glacier-project/frost](https://github.com/glacier-project/frost)

The simulation and control framework: a library of Lingua Franca reactors
providing messaging, registration, routing and data-model integration. Depends
on `machine-data-model` and `frost-planner`.

Default branch `dev` · latest release v1.0.0 · BSD 2-Clause · Python

### machine-data-model

[:octicons-mark-github-16: glacier-project/machine-data-model](https://github.com/glacier-project/machine-data-model)

The interface library: declares a machine's variables and methods as a YAML
tree, and connects them to OPC UA servers or MQTT brokers. Usable without Frost.

Default branch `dev` · latest release v1.0.0 · BSD 2-Clause · Python

### frost-planner

[:octicons-mark-github-16: glacier-project/frost-planner](https://github.com/glacier-project/frost-planner)

A library for solving flexible job-shop scheduling problems. Frost's
`FrostScheduler` reactor uses it to decide what to invoke and when.

Default branch `main` · latest tag v0.2.4 · BSD 2-Clause · Python

## Getting started

### frost-template

[:octicons-mark-github-16: glacier-project/frost-template](https://github.com/glacier-project/frost-template)

A GitHub template for new Frost projects: directory layout, configuration files,
Frost as a submodule and a main reactor in place.

Default branch `main` · BSD 2-Clause

### frost-playground

[:octicons-mark-github-16: glacier-project/frost-playground](https://github.com/glacier-project/frost-playground)

Self-contained example applications — publisher/subscriber, sensor/alarm, a
stock-market simulation, a production scheduler — with a devcontainer.

Default branch `main` · BSD 2-Clause

!!! warning "Pinned to Frost v1.0.0"

    Its Frost submodule tracks the `main` branch, so its examples use the v1.0.0
    component names. See [Versions](versions.md).

## Applications and demonstrators

### xppu-frost

[:octicons-mark-github-16: glacier-project/xppu-frost](https://github.com/glacier-project/xppu-frost)

A digital twin of the Extended Pick&Place Unit, a widely used Industry 4.0
research demonstrator. Models a stack, crane, stamp and several conveyors, with
physics-based variants of some components, and integrates with Kafka for data
streaming.

Default branch `main` · BSD 2-Clause · built on Frost `dev`

### ice-frost

[:octicons-mark-github-16: glacier-project/ice-frost](https://github.com/glacier-project/ice-frost)

The production line of the [ICE laboratory](https://www.icelab.di.univr.it/) in
Verona, modelled with Frost. Each machine extends `FrostReactor`; a scheduler
reads a recipe from YAML and drives the line through Frost messages.

Default branch `dev` · latest tag v0.0.4 · BSD 3-Clause

### virtualice-image

[:octicons-mark-github-16: glacier-project/virtualice-image](https://github.com/glacier-project/virtualice-image)

The ICE laboratory's data-collection architecture — Kafka, RabbitMQ and
supporting services — packaged as a Docker Compose deployment.

Default branch `main`

## This site

### glacier-website

[:octicons-mark-github-16: glacier-project/glacier-website](https://github.com/glacier-project/glacier-website)

The source of these pages. Built with MkDocs and Material for MkDocs; content is
Markdown under `docs/`.

Default branch `main` · BSD 3-Clause

## A note on old links

GLACIER repositories used to live in the `esd-univr` organisation. Those URLs
still redirect, but `glacier-project` is the canonical location and the one to
link to. If you find a `github.com/esd-univr/...` link on this site, it is a bug
worth [reporting](https://github.com/glacier-project/glacier-website/issues).

Two renames happened alongside the move: `frost-machine-data-model` became
`machine-data-model`, and the repository once called `glacier` is now `frost`.
