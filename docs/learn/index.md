# Learn

This is the catalogue of teaching and training material that uses GLACIER tools.

GLACIER is developed inside a university department, and a good deal of it
exists because it is used to teach — manufacturing systems, cyber-physical
systems, control software engineering. This section is where that material is
published as it becomes publicly available.

!!! tip "Attending the FDL 2026 Summer School?"

    The GLACIER hands-on session has its own preparation page: what to install,
    what to download, and how to check that your laptop is ready before the
    session starts.

    [:octicons-arrow-right-24: Prepare for FDL 2026](events/fdl-2026.md)

!!! info "The catalogue is being populated"

    Several of the categories below have no public entries yet. Rather than
    list placeholders, each page says what it is for and what a published entry
    will look like. Nothing here links to a resource that does not exist.

<div class="grid cards" markdown>

-   :material-book-open-variant: __Tutorials__

    ---

    Step-by-step, self-paced material: build something with GLACIER from
    beginning to end.

    [:octicons-arrow-right-24: Tutorials](tutorials.md)

-   :material-flask-outline: __Labs and exercises__

    ---

    Hands-on sessions and exercise sets, usually taught alongside a course.

    [:octicons-arrow-right-24: Labs and exercises](labs.md)

-   :material-presentation: __Lectures__

    ---

    Slide decks and recorded talks on the ideas behind GLACIER.

    [:octicons-arrow-right-24: Lectures](lectures.md)

-   :material-calendar-star: __Events__

    ---

    Preparation pages for sessions taught in person at conferences and summer
    schools.

    [:octicons-arrow-right-24: Events](events/index.md)

</div>

## Start here instead

If you are looking to learn the tools rather than take a course, the fastest
route today is the documentation itself:

1. [What is GLACIER?](../overview/index.md) — the problem and the approach, in
   about five minutes.
2. [Architecture](../overview/architecture.md) — how the pieces fit together.
3. [Connecting to a link](../frost/examples/link-registration.md) — the smallest
   Frost program that does something.
4. [Invoking a method](../frost/examples/method-invocation.md) and
   [Subscribing to a variable](../frost/examples/variable-subscription.md) — the
   two interaction patterns everything else is built from.
5. [frost-template](https://github.com/glacier-project/frost-template) — start
   your own project from a working skeleton.

## Contributing a resource

This site catalogues resources; it does not host them. A lecture lives in
whatever repository or archive its author publishes it to, and the entry here
points at it.

Adding one means editing a single Markdown file — `docs/learn/tutorials.md`,
`docs/learn/labs.md` or `docs/learn/lectures.md` — and adding a section
following the pattern already on the page. No frontend code is involved. An
event preparation page is the one exception: it is a new file under
`docs/learn/events/`, plus one line in `nav:`.

The only rule is the one stated above: **an entry must point at something that
exists and is publicly reachable.** A resource that is planned, or that is
restricted to enrolled students, can be described as such in prose, but must not
be presented as a link a visitor can follow.
