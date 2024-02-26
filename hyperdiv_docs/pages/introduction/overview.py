import hyperdiv as hd
from ...router import router
from ...page import page


def feature(title):
    with hd.box(
        gap=1,
        padding=1,
        border="1px solid neutral-100",
        border_radius="large",
        background_color="neutral-50",
    ) as box:
        hd.markdown(f"### {title}", font_color="blue")
    return box


@router.route("/introduction/overview", redirect_from=("/", "/introduction"))
def overview():
    with page() as p:
        p.title("# Hyperdiv Overview")

        hd.markdown(
            """

            Hyperdiv is a Python framework that aims to minimize tool
            complexity and the amount of code you have to type when
            building a reactive browser UI app.

            """
        )

        hd.link(
            "Jump to Getting Started",
            href="/guide/getting-started",
            font_color="neutral-100",
            padding=1,
            align="center",
            justify="center",
            border="1px solid neutral-100",
            border_radius="large",
            background_gradient=(30, "pink", "blue"),
        )

        hd.markdown("## Features")

        with feature("Pure Python"):
            hd.markdown(
                """

                A Hyperdiv app is written in pure Python, in a single
                Python program that seamlessly blends UI and backend
                logic. There are no extraneous tools or build steps,
                and you can run your app with `python my-app.py`.

                """
            )

        with feature("Batteries Included"):
            hd.markdown(
                """

                Hyperdiv ships with a rich set of built-in UI
                components based on the excellent Web Components
                library [Shoelace](https://shoelace.style), which
                includes forms with a full set of input components,
                dialogs, drawers, menus, and more. Thanks to Shoelace,
                Hyperdiv apps automatically support light and dark
                modes and follow the user's system mode by default.

                Hyperdiv also ships with data table components, charts
                based on [Chart.js](https://www.chartjs.org/), and
                Markdown support based on
                [Mistune](https://mistune.lepture.com) and
                [Pygments](https://pygments.org/).

                """
            )

        hd.markdown("## Technical Features")

        with feature("Immediate Mode"):
            hd.markdown(
                """

                Hyperdiv syntax is inspired by immediate mode GUI
                frameworks like [Dear
                ImGui](https://github.com/ocornut/imgui). Immediate
                mode provides a very minimal and terse syntax for
                expressing UIs and handling UI events.

                """
            )

        with feature("Reactive"):
            hd.markdown(
                """

                Hyperdiv is implicitly reactive. When application
                state changes, Hyperdiv automatically re-runs your app
                and updates the UI.

                A core innovation of Hyperdiv's design is the seamless
                blending of immediate mode with a reactive state model
                that borrows from [React
                hooks](https://react.dev/reference/react/hooks) and
                [Preact
                signals](https://preactjs.com/guide/v10/signals/).

                """
            )

        with feature("Managed"):
            hd.markdown(
                """

                Hyperdiv automatically manages frontend-backend
                communication under the hood. You are not exposed to
                handling HTTP requests or interacting with a
                Websocket.

                Hyperdiv also does not expose users to frontend
                technologies like HTML, Javascript, node, rollup/vite,
                etc., and has no dependencies on the Javascript
                ecosystem.

                """
            )

        with feature("Over-The-Wire Dom Patching"):
            hd.markdown(
                """

                Hyperdiv uses Virtual Dom diffing and sends
                minimal virtual Dom patches to the browser, which
                applies them to the actual in-browser Dom.

                """,
            )

        with feature("Fixed JS"):
            hd.markdown(
                """

                The Javascript code that runs in the browser is a
                piece of fixed, generic boilerplate that applies
                incoming diffs to the Dom and sends UI events back
                to Python. Hyperdiv does not expose the internal
                logic of your app, or your raw data, to the
                browser. The in-browser JS only receives virtual
                Dom diffs and translates them into real Dom
                modifications.

                """
            )
