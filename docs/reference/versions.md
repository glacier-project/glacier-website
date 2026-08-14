# Versions

## What this documentation follows

These pages document the **default branch** of each repository, which is the
current line of development.

| Repository | Documented branch | Latest release |
| --- | --- | --- |
| [frost](https://github.com/glacier-project/frost) | `dev` | v1.0.0 (7 October 2025) |
| [machine-data-model](https://github.com/glacier-project/machine-data-model) | `dev` | v1.0.0 |
| [frost-planner](https://github.com/glacier-project/frost-planner) | `main` | v0.2.4 |

Where the released version behaves differently from what is documented, the page
says so.

## Frost renamed its components after v1.0.0

This is the difference that matters most, because it changes the name of
everything you write.

Frost v1.0.0 — the `main` branch — had six components. The `dev` branch
reorganised them into a cleaner hierarchy, splitting the data model out as a
port-less mixin so that the two concrete components can combine it with the
communication interface independently.

| v1.0.0 (`main`) | Current (`dev`) | What changed |
| --- | --- | --- |
| `FrostBase` | `FrostBase` | Unchanged in role. |
| `FrostInterface` | `FrostInterface` | No longer performs bus registration; that moved to `FrostReactor`. Now splits incoming messages onto four logical actions. |
| `MessageFilter` | `MessageFilter` | Unchanged in role. |
| `FrostDataModel` | **`FrostNode`** | Renamed, and turned into a mixin with no ports of its own. |
| `FrostMachine` | **`FrostReactor`** | Merged. v1.0.0 had a separate `FrostReactor` for communication only and `FrostMachine` for communication plus a data model; there is now one component. |
| `FrostReactor` | *(merged into `FrostReactor`)* | — |
| `FrostBus` | **`FrostLink`** | Renamed. Its data model paths changed from `FrostBus/#Machines` and `FrostBus/MachineInfo` to `FrostLink/#Nodes` and `FrostLink/NodeInfo`. |

Other differences on `dev`:

- **Registration is symmetric.** v1.0.0 had components send a registration
  request to the bus and retry on a timeout. Components now broadcast to the
  marker `"__target__"` on every output port, and record peers both from replies
  to their own broadcast and from broadcasts they receive — so direct
  point-to-point wiring works without a router.
- **A default route by name.** Messages for unknown targets are sent to a peer
  named `frost_link`.
- **New subsystems.** `dev` adds `FrostScheduler` (job-shop scheduling driven by
  `frost-planner`) and a simulation package with an `Orchestrator`, `SimModel`
  and an FMI/FMU wrapper, `FrostFmu`. None of these existed in v1.0.0.

### Which one should I use?

**`dev`.** It is Frost's default branch, it is what its CI tests on every push,
and it is what the current applications — [xppu-frost](https://github.com/glacier-project/xppu-frost),
[ice-frost](https://github.com/glacier-project/ice-frost) — are built against.

Use `main` only if you have an existing project pinned to v1.0.0. Note that
[frost-playground](https://github.com/glacier-project/frost-playground) is such
a project: its submodule tracks `main`, so its examples will not compile against
`dev` unchanged.

## machine-data-model

v1.0.0 is the latest release. These pages document `dev`, which is the default
branch.

The library is **not on PyPI**. Install it from source, or let Frost's
`requirements.txt` pull it in — which is how Frost gets it:

```text
git+https://github.com/glacier-project/machine-data-model.git@dev
```

Note the `@dev`: Frost depends on the development branch, not on the release.

MQTT connector support is recent, merged in June 2026. If you are working from
an older checkout, only the OPC UA connector will be present.

## Toolchain

| | Version |
| --- | --- |
| Python (Frost) | 3.12 or later — CI tests 3.12 and 3.13 |
| Python (machine-data-model) | 3.11 or later |
| Java | 17, for the Lingua Franca compiler |
| Lingua Franca | installed via `curl -Ls https://install.lf-lang.org \| bash -s cli` |

## Checking for yourself

The authoritative answer is always the repository. Two commands settle most
questions:

```bash
# What is the default branch, and what has been released?
gh repo view glacier-project/frost --json defaultBranchRef,latestRelease

# Which components exist on the branch I am using?
gh api "repos/glacier-project/frost/contents/src/lib?ref=dev" --jq '.[].name'
```
