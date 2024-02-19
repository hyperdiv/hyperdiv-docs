import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import code_example, docs_markdown


@router.route("/guide/conditional-rendering")
def conditional_rendering():
    with page() as p:
        p.title("# Conditional Rendering")

        hd.markdown(
            """

            So far, we've seen how to render UIs where all
            instantiated components are on the screen all the
            time. But in general, UIs are rendered differently based
            on how the states of components evolve.

            """
        )

        p.heading("## Basic Example")

        docs_markdown(
            """

            To render UI conditionally, you just use built-in Python
            conditionals, like so:

            ```py
            ch = hd.checkbox("Check Me")
            if ch.checked:
                hd.text("It is checked")
            ```

            In this example, the @component(checkbox) component
            exposes a `checked` prop that lets us determine if the
            checkbox is checked. The value of this prop changes as we
            check and uncheck the checkbox in the UI. The value of the
            prop effectively *stays synchronized* with the state of
            the checkbox in the UI.

            Then, we can render UI conditionally based on the current
            value of this prop.

            """
        )

        p.heading("## Arbitrary UI Under Conditionals")

        docs_markdown(
            """

            We can render any Hyperdiv UI under conditionals:

            ```py
            ch = hd.checkbox("Check Me")
            if ch.checked:
                radios = hd.radios("One", "Two", "Three")
                hd.text(radios.value)
            else:
                with hd.box(
                    border="1px solid neutral-100", 
                    padding=2,
                    gap=1,
                ):
                    slider = hd.slider()
                    hd.text(slider.value)
            ```

            Notice how Hyperdiv remembers the states of the components
            under conditionals, across runs in which they may be
            absent from the UI.

            """
        )
