# Content audit

Maintainer-facing record of the factual audit of this website against the
GLACIER repositories. **Not part of the public site navigation.**

Audit date: **14 August 2026**.
Website state audited: commit `fadb20d` ("Add google site verification").

Re-run this audit whenever the Frost or machine-data-model APIs move. The
website is the lowest-authority source about them.

---

## Evidence base

Every repository below was cloned and read at the commit shown. Default branches
were read from the GitHub API rather than assumed — **three of the repositories
that matter do not default to `main`.**

| Repository | Default branch | Inspected commit | What was read |
| --- | --- | --- | --- |
| glacier-project/frost | **`dev`** | `55e9f32c226911b9ad1a4486cce5e62f9d4aec63` | `src/lib/*.lf`, `src/python_lib/frost.py`, all 16 `test/src/*.lf`, `test/resources/config/*.yml`, `test/resources/data_model/**`, `README.md`, `Lingo.toml`, `requirements.txt`, `Makefile`, `.github/workflows/test.yml`, `CITATION.cff`, `LICENSE` |
| glacier-project/frost | `main` (release line) | `ddc512441e7dde6e33341058f6229726be1a4f8f` | `src/lib/` listing, `src/lib/FrostBus.lf` — via GitHub API, to establish what v1.0.0 contains |
| glacier-project/machine-data-model | **`dev`** | `d9f2c59701502fefb5d9d0d45052c99b992a4451` | `machine_data_model/nodes/**`, `behavior/**`, `builder/data_model_builder.py`, `protocols/**`, `README.md`, `pyproject.toml`, `examples/**` listing |
| glacier-project/frost-playground | `main` | `9f0af2cf7ec0c3eeca75da077909d76dda76697a` | `src/*.lf`, `resources/**`, `.gitmodules`, submodule pin, `README.md` |
| glacier-project/frost-template | `main` | `ef1d181024ff8478d00d2a709a55e31f8e0405e4` | `README.md`, tree |
| glacier-project/frost-planner | `main` | `7fd6e98136c538030e3e8befe53e56d040c1e835` | `README.md`, tree, tags |
| glacier-project/ice-frost | **`dev`** | `381be6f3bf7eab7a4b8277dc1a06168228329821` | `README.md`, tree, tags |
| glacier-project/xppu-frost | `main` | `ff893b10c7e40ddeefff2f592bd31613d821ce6b` | `README.md`, `src/**` imports, `CITATION.cff` |
| glacier-project/virtualice-image | `main` | `52ce3a8199adca7e86fb61d8a5615311aa9f3a20` | `README.md`, tree |

Releases and tags were read from the GitHub API: `frost` v1.0.0 (2025-10-07,
from `main`); `machine-data-model` v1.0.0, v0.0.1; `frost-planner` v0.2.4 and
five earlier; `ice-frost` v0.0.4 and three earlier. `frost-playground`,
`frost-template`, `xppu-frost` and `virtualice-image` have no tags.

`machine-data-model` is **not on PyPI** (`pypi.org/pypi/machine-data-model/json`
returns 404), contradicting nothing on the old site but worth recording, since
the upstream README says "From PyPI: Coming soon!".

---

## The finding that drives everything else

The old website documented Frost's **v1.0.0** component set while presenting it
as current, and did not mention that a release line exists.

- `frost@main` = `ddc51244` = release **v1.0.0** (7 Oct 2025) contains
  `FrostBase.lf`, `FrostBus.lf`, `FrostDataModel.lf`, `FrostInterface.lf`,
  `FrostMachine.lf`, `FrostReactor.lf`.
- `frost@dev` — **the default branch**, last pushed 29 Jul 2026 — contains
  `FrostBase.lf`, `FrostInterface.lf`, `FrostLink.lf`, `FrostNode.lf`,
  `FrostReactor.lf`, plus `scheduler/` and `simulation/`.

So `FrostBus`, `FrostDataModel` and `FrostMachine` — three of the four component
pages on the old site — document reactors that no longer exist on the current
branch. `FrostMachine` and `FrostBus` survive in the repository only under
`benchmark/INDIN/`, whose imports point at a path (`../../../../../frost/FrostBus.lf`)
that does not exist in the current tree.

Corroboration that `dev` is the live line: `frost@dev`'s own README describes
`FrostReactor` and `FrostLink`; `ice-frost`'s README says "we developed each
machine by extending the **FrostReactor** and we connected them through the
**FrostLink**"; `xppu-frost/src/XPPU.lf` imports `FrostReactor`.

**Action taken:** the site now documents `dev`, states which branch it follows
on every relevant page, and carries a
[Versions](docs/reference/versions.md) page with the full v1.0.0 → `dev` mapping.

---

## Ledger

Verdicts: `CURRENT` · `STALE` · `UNSUPPORTED` · `AMBIGUOUS` · `OVERSTATED` ·
`BROKEN LINK` · `LEGACY REFERENCE`.

### Architecture and terminology

| Claim (old site) | Evidence | Branch/commit | Verdict | Action |
| --- | --- | --- | --- | --- |
| Frost's key components are Data Model, FrostMachine, Actor, FrostBus | `src/lib/` contains FrostBase, FrostInterface, FrostNode, FrostReactor, FrostLink | frost `dev` `55e9f32` | **STALE** | Rewritten: `FrostReactor` and `FrostLink` are the two you instantiate |
| `FrostBus` is the communication infrastructure / message router | No `FrostBus.lf` on `dev`; `FrostLink.lf` holds the routing logic | frost `dev` `55e9f32` | **STALE** | Renamed throughout; documented as `FrostLink` |
| `FrostDataModel` reactor integrates a data model, extends `FrostInterface` | `FrostNode.lf` docstring: "It is a pure mixin: it has no communication ports of its own"; `extends FrostBase` | frost `dev` `55e9f32` | **STALE** | Renamed to `FrostNode`; corrected from "extends FrostInterface" to "extends FrostBase, is a port-less mixin" |
| `FrostMachine` inherits from both `FrostDataModel` and `FrostReactor` | `FrostReactor.lf`: `extends FrostInterface, FrostNode`. No `FrostMachine.lf` | frost `dev` `55e9f32` | **STALE** | Merged into `FrostReactor`; inheritance diagram corrected |
| "Actor: components that interact with the machines or other actors" | No actor concept in `src/lib/`; `dev` uses "target"/"peer". `FrostInterface` state is `targets` | frost `dev` `55e9f32` | **STALE** | Term removed. Both machines and control software are `FrostReactor`s |
| `FrostReactor`'s bus connection is "handled by the parent `FrostInterface`" via a `connect_to_bus` logical action | `grep -rn connect_to_bus` over `frost@dev` returns nothing. Registration is `check_targets`/`explore_targets` in `FrostReactor.lf` | frost `dev` `55e9f32` | **STALE** | Rewritten; registration documented where it now lives |
| `FrostInterface` "includes a handshake mechanism that repeatedly attempts to connect until it succeeds or times out" (code sample with `SEC(9)`/`SEC(3)`) | That code is not in `FrostInterface.lf`. `FrostReactor` retries every `update_step`, giving up after **10** attempts | frost `dev` `55e9f32` | **STALE** | Snippet removed; the real retry policy documented, including that it only warns on failure |
| `MessageFilter` routes by type into requests/responses/errors, with custom callbacks and a `discarded_messages` port | `MessageFilter.lf` matches | frost `dev` `55e9f32` | **CURRENT** | Kept; added that `discarded_messages` carries registration traffic, which the old page did not mention |
| `FrostBase` provides logging, parameter overriding, message-passing utilities | `FrostBase.lf` matches | frost `dev` `55e9f32` | **CURRENT** | Kept and extended with the logical-time helpers, which were undocumented |
| Config dictionary "is passed to the reactor, typically during its initialization" | `frost.py` reads `FROST_CONFIG` from an environment variable into a module global; `FrostBase` reads that global in a startup reaction | frost `dev` `55e9f32` | **STALE** | Corrected; `FROST_CONFIG` and its `resources/frost_config.yml` default documented |
| Config example shows a flat `reactors: <name>: {logging_level, parameters}` | Real files nest `reactors:` inside a component for contained reactors, and carry a top-level `time_precision` | `test/resources/config/*.yml` | **AMBIGUOUS** | Not wrong, but incomplete. Replaced with a real config file from the test suite |

### API and code claims

| Claim (old site) | Evidence | Branch/commit | Verdict | Action |
| --- | --- | --- | --- | --- |
| `new ControlQuality(model_path="models/control_quality.yml")` | Parameter is `_data_model_path`; every test supplies it via `parameters.data_model_path` in the config file | frost `dev` `55e9f32` | **STALE** | All examples now set the path in the configuration file |
| `new FrostBus(model_path=..., width=2)` | `FrostLink` takes no `model_path`; `width` is inherited from `FrostInterface` | frost `dev` `55e9f32` | **STALE** | Replaced with `new FrostLink(name="frost_link", width=2)` |
| `get_cm_msg(target=..., method_name=..., args=[...])` | No such function in `frost.py` or `src/lib/`. Messages are built with `self.message_builder.build_*` | frost `dev` `55e9f32` | **UNSUPPORTED** | Removed; replaced with `build_invoke_method_message` as used in `TestMethodInvoke.lf` |
| Method path used as `control_quality/statistics/check_quality`, matching the machine `name:` | Paths start at the **root node's** `name`, not the machine's. Test models are named `worker` with root `Machine`, and paths are `Machine/Square` | frost `dev` `55e9f32`; `test/resources/data_model/**` | **STALE** | Corrected, and the distinction called out explicitly |
| Machine callbacks bound as `node.callback = self.method` | `TestMethodInvoke.lf` does exactly this | frost `dev` `55e9f32` | **CURRENT** | Kept |
| A `MethodNode` invocation is answered automatically | `FrostReactor._process_data_model_requests` queues plain `MethodNode` calls on `new_method_request` and leaves invocation to the concrete reactor | frost `dev` `55e9f32` | **STALE (by omission)** | Documented; the required reaction is shown, and the contrast with async/composite methods stated |
| `FrostMessage(...)` constructed by hand with `FrostHeader(type=..., version=(1,0,0), ...)` | Type exists, but no current test or example builds one this way; all use `FrostMessageBuilder` | frost `dev` `55e9f32` | **STALE** | Replaced with builder calls throughout |
| Website's four examples (Stock Market, Publisher/Subscriber, Target/Initiator, Sensor/Alarm) | Derived from `frost-playground`, whose Frost submodule is pinned to `ddc51244` = `main` = v1.0.0. They use `FrostMachine`/`FrostBus`/`FrostDataModel` | frost-playground `9f0af2c` | **STALE** | All four removed. Replaced by three examples adapted from `frost@dev`'s CI-run tests |

### Data model claims

| Claim (old site) | Evidence | Branch/commit | Verdict | Action |
| --- | --- | --- | --- | --- |
| Node types: FolderNode, VariableNode, ObjectNode, MethodNode, AsyncMethodNode, CompositeMethodNode | `_register_yaml_constructors()` registers `FolderNode`, `NumericalVariableNode`, `StringVariableNode`, `BooleanVariableNode`, `ObjectVariableNode`, `MethodNode`, `AsyncMethodNode`, `CompositeMethodNode`, plus CFG and connector tags | mdm `dev` `d9f2c59` | **STALE** | `ObjectNode` corrected to `ObjectVariableNode`. `VariableNode` documented as the abstract base, not a YAML tag — with an explicit warning, since the old site invited people to write it |
| `MethodNode` is synchronous and returns after completion | `MethodNode` / README agree | mdm `dev` `d9f2c59` | **CURRENT** | Kept |
| `AsyncMethodNode` returns immediately; completion signalled by variable updates | Class docstring: "the result is obtained asynchronously, typically through variable monitoring or event-based mechanisms" | mdm `dev` `d9f2c59` | **CURRENT** | Kept |
| `CompositeMethodNode` "returns immediately, returning an acceptance value, while when it is completed, an update message is sent to the caller" | README: "A **synchronous** method composed of a sequence of operations specified in a Control Flow Graph… returns the result only when all operations are completed. If the execution does not terminate… it returns the id of execution instance" | mdm `dev` `d9f2c59` | **STALE** | Corrected: synchronous, returns results on completion, returns an execution id only when suspended at a wait condition |
| Composite method operations "may include the execution of asynchronous methods, reading and writing variables, and waiting for specific conditions" | `ReadVariableNode`, `WriteVariableNode`, `WaitConditionNode`, `CallMethodNode` registered | mdm `dev` `d9f2c59` | **CURRENT** | Kept, and the four tags plus their keys documented |
| — (not on old site) | `CallRemoteMethodNode`, `ReadRemoteVariableNode`, `WriteRemoteVariableNode`, `WaitRemoteEventNode` registered | mdm `dev` `d9f2c59` | **CURRENT** | Newly documented: composite methods can orchestrate other components |
| — (not on old site) | `OpcuaConnector`, `MqttConnector`, `OpcuaRemoteResourceSpec`, `MqttRemoteResourceSpec`; MQTT merged 19 Jun 2026 (PR #64) | mdm `dev` `d9f2c59` | **CURRENT** | Newly documented, including the two stated limitations: MQTT supports no method calls, and no topic wildcards |
| — (not on old site) | `DataChangeSubscription`, `RangeSubscription`, `EventType.{DATA_CHANGE,IN_RANGE,OUT_OF_RANGE,ANY}` | mdm `dev` `d9f2c59` | **CURRENT** | Newly documented |
| Example YAML uses `!!NumericalVariableNode` with over-indented children | The malformed indentation in the old `control_quality.yaml` would not parse | mdm `dev` `d9f2c59` | **STALE** | Example replaced with YAML copied from Frost's test resources |
| — (not on old site) | `_build_kwargs` raises `ValueError: Unexpected keys: …` for unknown node keys | mdm `dev` `d9f2c59` | **CURRENT** | Newly documented — useful failure mode for authors |

### Overclaims

| Claim (old site) | Evidence | Verdict | Action |
| --- | --- | --- | --- |
| "software and physical components are **seamlessly** integrated" | Nothing in the source establishes seamlessness; it is a design aspiration | **OVERSTATED** | Removed |
| Frost "allows users to create **high-fidelity** digital twins… **replicating** the APIs exposed by real systems" | Frost supplies interface, messaging and execution; fidelity is entirely a property of user-written behaviour. `machine-data-model` connectors do map a model onto a real OPC UA/MQTT endpoint | **OVERSTATED** | Split apart. The site now distinguishes the interface model, the simulated behaviour, the communication behaviour and deployment, and states plainly that Frost supplies no validated physical models |
| "GLACIER supports different levels of fidelity, from simple data-mirroring models to complex predictive simulations" | `FrostFmu`/`SimModel` exist on `dev` and wrap FMI/FMU co-simulation; `xppu-frost` has physics-based components. "Predictive simulation" is not demonstrated | **AMBIGUOUS** | Softened to what is implemented; FMI support noted under Versions as a `dev` addition |
| Lingua Franca supports programs "deployed on the Cloud, the Edge, and even on bare-metal architectures" | True of Lingua Franca; not demonstrated for Frost, which targets Python and whose CI runs on `ubuntu-latest` only | **OVERSTATED** (about Frost) | Attributed to Lingua Franca where relevant; no deployment-target claim made for Frost |
| "reduces the time spent adapting and deploying prototype software on the target system" | Plausible project goal, not a measured result on this site | **OVERSTATED** | Reframed as a design goal, with an explicit "what GLACIER does not claim" section |
| Determinism presented alongside physical-twin language | Lingua Franca guarantees deterministic event ordering in logical time; it says nothing about matching real timing | **AMBIGUOUS** | Separated explicitly on the Overview page |
| Roadmap with dated milestones through 2026-03-31, most already past | No release, tag or CI evidence for "SysML v2 integration", "Physic-based machine simulation", "FMI/FMU integration" as delivered milestones on those dates. FMI code does exist on `dev` | **UNSUPPORTED** | Roadmap removed. Restating dates that have passed with nothing to point at is worse than having no roadmap |

### Links

| Link (old site) | Evidence | Verdict | Action |
| --- | --- | --- | --- |
| `github.com/esd-univr/frost` (used twice) | API: redirects to `glacier-project/frost` | **LEGACY REFERENCE** | → `github.com/glacier-project/frost` |
| `github.com/esd-univr/frost-machine-data-model` (used twice) | API: redirects to `glacier-project/machine-data-model` — repository was renamed as well as moved | **LEGACY REFERENCE** | → `github.com/glacier-project/machine-data-model` |
| `lf-lang.org`, `icelab.di.univr.it` | Reachable | **CURRENT** | Kept |

Legacy references found in **upstream** repositories, reported rather than
fixed here — the website no longer repeats them, but the repositories should be
corrected by their maintainers:

- `frost-template/README.md` links to `esd-univr/frost`, `esd-univr/frost-template`
  and `esd-univr/glacier`. The last is a repository that no longer exists under
  that name — it now redirects to `glacier-project/frost`.
- `frost-template/README.md` lists "Extensible components (FrostMachine,
  FrostBus, FrostReactor, etc.)", which is the v1.0.0 set.
- `frost-playground/README.md` clone instructions use `esd-univr/frost-playground`.
- `xppu-frost/README.md` links to `esd-univr/machine-data-model`.
- `virtualice-image/README.md` clone instructions use `esd-univr/virtualice-image`.
- `frost/README.md` points at `examples/ICE`, a directory that does not exist on
  `dev` — **BROKEN LINK** upstream.
- `machine-data-model/README.md` shows `node.subscribe("New User")`, but the
  current signature is `subscribe(self, subscription: VariableSubscription)`.
  The website does not repeat this form.
- `machine-data-model/README.md` gives a `poetry build` install command producing
  `machine_data_model-0.0.1-py3-none-any.whl`, while `pyproject.toml` declares
  version `1.0.0`.

### Site mechanics

| Item | Evidence | Verdict | Action |
| --- | --- | --- | --- |
| `theme.features` declared `navigation.instant.prefetch` and `content.code.select` | Neither string appears anywhere in `mkdocs-material` 9.6.8; both are Insiders-only | **UNSUPPORTED** | Removed. `navigation.path` was considered and rejected for the same reason |
| `requirements.txt` pinned `mkdocs-material[imaging]` | No `social` plugin is configured, so the extra's Cairo/Pillow dependencies were never used — and they are a common cause of failed installs | **UNSUPPORTED** | Extra dropped |
| Banner styled `background-color: #e2c15d; color: #fff` | Contrast ratio 1.81:1, below WCAG AA (4.5:1) | **ACCESSIBILITY DEFECT** | Restyled: neutral surface with an amber rule |
| `extra.css` forced the footer white with eight `!important` rules | Would have made the footer unreadable in dark mode — which the site did not have | **STALE** | Removed; the footer follows the theme |
| Palette declared one scheme (`default`, `primary: white`) | No dark mode, no system-preference support | **STALE** | Three-way light/dark/system palette added |
| `docs/diagrams/sequence/{read,write,subscribe}_variable.md` | Empty files (0 bytes) | **STALE** | Deleted |
| `docs/diagrams/sequence/{method,async_method,composite_method}.md` | Not referenced from `nav:` or any page, but built and published as pages | **STALE** | Deleted; the useful one is redrawn on the Architecture page |
| `docs/index.md` contained ~200 lines including the whole Frost manual | — | — | Split across Overview, Frost and Reference |

---

## Example classification

Every code example that was on the old site, and every example now on it.

### Removed

| Example | Why |
| --- | --- |
| `ControlQuality.lf` machine (home page) | `extends FrostMachine`; `model_path=` constructor argument; data model path `control_quality/statistics/...` rooted at the machine name |
| `ControlQualityActor.lf` (home page) | `extends FrostMachine` for something described as an actor; `get_cm_msg()` does not exist; `import FrostBus from "FrostBus.lf"` |
| `control_quality.yaml` (home page) | Malformed indentation under `!!NumericalVariableNode`; would not parse |
| Stock Market | `extends FrostDataModel` / `FrostBase` with hand-declared `channel_in`/`channel_out`; no such wiring on `dev` |
| Publisher and Subscriber | `extends FrostDataModel`; hand-built `FrostMessage` with `FrostHeader(version=(1,0,0))` |
| Target and Initiator | `extends FrostMachine`; hand-built `MethodPayload`; `message.payload.ret['response']` where the declared return name is different |
| Alarm and Sensor | `extends FrostMachine`; `new FrostBus(...)` |
| `FrostBase` parameter-override snippet | Accurate against `dev`, but shown with `//` comments inside a Python-target method body |
| `FrostBus` registration and routing snippets | Reference `FrostBus`, `routing_map` on a component that no longer exists under that name |
| `FrostDataModel` startup/request/update snippets | Reference a reactor that no longer exists; `handle_request` is now `handle_message` |
| `FrostInterface` `connect_to_bus` snippet | No such action on `dev` |
| `FrostReactor` startup snippet | Replaced by `check_targets`/`explore_targets` |

### Verified

Adapted from `frost@dev` tests that CI builds and runs on every push. Changes
limited to trimming test assertions and renaming files.

| Example | Source |
| --- | --- |
| [Connecting to a link](docs/frost/examples/link-registration.md) | `test/src/TestFrostLink.lf` + `test/resources/config/test_frost_link.yml` + `test/resources/common/data_model/link.yml` |
| [Invoking a method](docs/frost/examples/method-invocation.md) | `test/src/TestMethodInvoke.lf` + `test/resources/config/test_method_invoke.yml` + `test/resources/data_model/test_method_invoke/{worker,caller}.yml` |
| [Subscribing to a variable](docs/frost/examples/variable-subscription.md) | `test/src/TestSubscription.lf` + `test/resources/config/test_subscription.yml` + `test/resources/data_model/test_subscription/*.yml` |
| `FrostLink` data model YAML | `test/resources/common/data_model/link.yml`, verbatim |
| `FrostBase` configuration YAML | `test/resources/config/test_frost_reactor.yml` |

### Updated

Rewritten from current sources rather than carried over.

| Example | Basis |
| --- | --- |
| Frost "shape of a program" skeleton (`frost/index.md`) | Composed from `TestMethodInvoke.lf` |
| Machine skeleton (`frost/components/frost-reactor.md`) | Composed from `TestSubscription.lf` and `TestMethodInvoke.lf` |
| Connection-wait pattern | `TestMethodInvoke.lf`, `TestSubscription.lf` |
| Variable YAML by type | `machine-data-model` README + builder `default_kwargs` |
| OPC UA and MQTT connector YAML | `machine-data-model` README, cross-checked against `data_model_builder.py` constructors |
| Python data model usage | `machine-data-model` README, minus the stale `subscribe("New User")` form |

### Conceptual

Illustrative, not copied from a runnable source. Marked as such in prose.

| Example | Note |
| --- | --- |
| `stamp_workpiece` composite method YAML | Tags and keys verified against the registered constructors; the specific machine is invented |
| `start_cycle` async method YAML | Same |
| Object / string / boolean variable snippets | Shapes verified against builder `default_kwargs` |
| Architecture and inheritance mermaid diagrams | Redrawn from `src/lib/` imports and `extends` clauses |

---

## Counts

| Verdict | Count |
| --- | --- |
| CURRENT | 12 |
| STALE | 20 |
| UNSUPPORTED | 5 |
| AMBIGUOUS | 3 |
| OVERSTATED | 5 |
| BROKEN LINK | 1 (upstream, in `frost/README.md`) |
| LEGACY REFERENCE | 3 on the site + 6 upstream |

| Example class | Count |
| --- | --- |
| VERIFIED | 5 |
| UPDATED | 6 |
| CONCEPTUAL | 4 |
| REMOVED | 12 |

---

## Open questions for the maintainers

1. **Will `dev` be merged to `main`?** The website documents `dev` because it is
   the default branch and the live line of development, but the only *release*
   is a year old and describes a different API. A v2.0.0 from `dev` would remove
   the need for most of the Versions page.
2. **`frost-playground` is stale.** Its submodule tracks `main`, so its examples
   no longer match the framework. Either repoint the submodule at `dev` and
   update the sources, or say on the repository itself that it targets v1.0.0.
3. **Upstream `esd-univr` links.** Listed above. The redirects work, so nothing
   is broken, but the links are wrong.
4. **`frost/README.md` points at `examples/ICE`**, which does not exist on `dev`.
   The ICE model lives in `glacier-project/ice-frost`.
5. **Analytics property `G-W9HHV0Z1Z5`** was carried over unchanged, along with
   the cookie-consent configuration, as neither showed evidence of a defect. The
   contrast bug in the banner was fixed; the analytics and consent behaviour was
   deliberately left alone.
