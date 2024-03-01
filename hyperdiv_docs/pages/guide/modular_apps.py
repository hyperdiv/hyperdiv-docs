import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import code_example, docs_markdown


@router.route("/guide/modular-apps")
def modular_apps():
    with page() as p:
        p.title("# Building Modular Apps")

        docs_markdown(
            """

            If you want to break up your Hyperdiv app into multiple
            modular units, you can just use Python functions and
            classes.

            """
        )

        code_example(
            """
            import hyperdiv as hd

            def fancy_slider(name, value=0):
                with hd.box(
                    gap=1,
                    padding=1,
                    background_color="neutral-50",
                    border="1px solid neutral-100",
                    border_radius="large",
                ):
                    hd.markdown(f"### {name}")
                    slider = hd.slider(value=value)
                    hd.text(slider.value)
                return slider.value

            def my_bar_chart(name1, value1, name2, value2):
                hd.bar_chart(
                    (value1, value2),
                    x_axis=(name1, name2)
                )

            def main():
                with hd.box(gap=1):
                    value1 = fancy_slider("A Slider", value=10)
                    value2 = fancy_slider("Another Slider", value=5)
                    my_bar_chart("A Slider", value1, "Another Slider", value2)

            hd.run(main)
            """,
            code_to_execute=(
                """
                def fancy_slider(name, value=0):
                    with hd.box(
                        gap=1,
                        padding=1,
                        background_color="neutral-50",
                        border="1px solid neutral-100",
                        border_radius="large",
                    ):
                        hd.markdown(f"### {name}")
                        slider = hd.slider(value=value)
                        hd.text(slider.value)
                    return slider.value

                def my_bar_chart(name1, value1, name2, value2):
                    hd.bar_chart(
                        (value1, value2),
                        x_axis=(name1, name2)
                    )

                with hd.box(gap=1):
                    value1 = fancy_slider("A Slider", value=10)
                    value2 = fancy_slider("Another Slider", value=5)
                    my_bar_chart("A Slider", value1, "Another Slider", value2)
                """
            ),
        )

        hd.markdown(
            """

            In this example, we wrote two functions, `fancy_slider`
            and `bar_chart`, that are effectively custom Hyperdiv
            components.

            Each call to `fancy_slider()` or `my_bar_chart()` renders
            a UI with independent internal state. In the example
            above, we call `fancy_slider()` twice, creating two
            separate and independent sliders.

            """
        )

        p.heading("## Encapsulating Custom State")

        hd.markdown(
            """

            Component functions can naturally define their own private
            custom state internally:

            """
        )

        code_example(
            """
            import hyperdiv as hd

            def counter(name):
                state = hd.state(count=0)

                with hd.box(
                    padding=1,
                    gap=1,
                    border="1px solid neutral-100",
                    background_color="neutral-50",
                    border_radius="large"
                ):
                    hd.markdown(f"### {name}")
                    hd.text("Count:", state.count)
                    if hd.button("Increment").clicked:
                        state.count += 1

            def main():
                with hd.box(gap=1):
                    counter("First Counter")
                    counter("Second Counter")

            hd.run(main)
            """,
            code_to_execute=(
                """

                def counter(name):
                    state = hd.state(count=0)

                    with hd.box(
                        padding=1,
                        gap=1,
                        border="1px solid neutral-100",
                        background_color="neutral-50",
                        border_radius="large"
                    ):
                        hd.markdown(f"### {name}")
                        hd.text("Count:", state.count)
                        if hd.button("Increment").clicked:
                            state.count += 1

                with hd.box(gap=1):
                    counter("First Counter")
                    counter("Second Counter")

                """
            ),
        )

        docs_markdown(
            """

            In this example app, we define a component function
            `counter` that uses @component(state) to define internal,
            custom state. We can call this component function multiple
            times, and each call will render a counter UI with its own
            independent count.

            """
        )

        p.heading("## Global State")

        docs_markdown(
            """

            When modularizing our app into several component functions
            and classes, and several of those components share custom
            state, we normally have to instantiate the state at the
            top level and pass it down into all of those components.

            To reduce the burden of having to pass state everywhere it
            is needed, Hyperdiv provides the @component(global_state)
            decorator, which makes a state component global, so that
            all instances of that component share the same underlying
            state.

            See @component(global_state) for more.

            """
        )
