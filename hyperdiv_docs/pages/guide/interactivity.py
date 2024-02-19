import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import code_example, docs_markdown


@router.route("/guide/interactivity")
def interactivity():
    with page() as p:

        p.title("# Interactivity Basics")

        hd.markdown(
            """

            So far we've seen how to render basic components into
            non-interactive apps: apps that do nothing when you
            interact with the rendered components.

            A core Hyperdiv feature, however, is making the building
            of interactive UIs as simple as possible.

            """
        )

        p.heading("## Basic Examples")

        docs_markdown(
            """

            Here's an interactive app that renders different things
            based on the state of a checkbox:

            ```py
            checkbox = hd.checkbox("Check Me")
            if checkbox.checked:
                hd.text("It is checked.")
            ```

            Hyperdiv works by *re-running the app function* whenever a
            prop changes. In this case, when the user clicks the
            checkbox, the `checked` prop is mutated. Hyperdiv then
            re-runs the app function that you passed to
            @component(run), which may then generate an updated UI.

            Here's another example:

            ```py
            slider = hd.slider()
            hd.text(slider.value)
            ```

            When you move the slider, the slider's `value` prop is
            mutated accordingly. Hyperdiv re-runs the app, generating
            a UI with the slider's new value in the text component.

            """
        )

        p.heading("## Responding to Events")

        docs_markdown(
            """

            Here's an app that toggles a checkbox when a button is clicked:

            ```py
            checkbox = hd.checkbox("Check Me")
            if hd.button("Toggle").clicked:
                checkbox.checked = not checkbox.checked
            ```

            When the button is clicked, `clicked` is set to
            `True`. The app re-runs, generating an updated UI, and
            when the run is done the `clicked` prop is automatically
            reset back to `False`.

            `clicked` is an "event prop" and we will learn more about
            it in the next section.

            """
        )
