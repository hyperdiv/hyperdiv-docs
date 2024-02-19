import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import code_example, docs_markdown


@router.route("/guide/layout")
def layout():
    with page() as p:

        p.title("# Style & Layout")

        docs_markdown(
            """

            Hyperdiv components are pre-styled and look good out of
            the box. In general you don't need to worry about styling
            in order to achieve a good-looking app. That said,
            Hyperdiv components can be styled using a limited set of
            style props based on CSS.

            Hyperdiv also includes a @component(box) component that
            can be used to create nested layouts, with control for how
            the box's children are laid out.

            """
        )

        p.heading("## Component Style")

        docs_markdown(
            """

            Hyperdiv components support a limited form of visual
            customization, controlling the font size and family,
            colors, borders, and sizes of components. For example:

            ```py
            hd.text(
                "Hello, Green World",
                padding=2,
                width="fit-content",
                font_color="green-700",
                background_color="green-200",
                border="1px solid green-400",
                border_radius="large"
            )
            ```

            The style props are defined by the @component(Styled)
            class and any component that inherits from
            @component(Styled) can be styled. Almost all Hyperdiv
            components inherit from @component(Styled).

            The color constants you see in this example are
            documented here: @design_token(Color).

            The syntax of the values accepted by each style prop is
            determined by that prop's type. For example, the prop
            `border` has type @prop_type(Border), and `width` has
            type @prop_type(Size).

            The degree to which components can be styled can vary. For
            built-in [Shoelace](https://shoelace.style) components,
            the style props may only affect the "outer" container
            of those components, as they may consist of an outer
            container containing multiple inner containers.

            An approach to fully controlling the styles of Shoelace
            components, including the styles of internal containers,
            is currently being investigated.

            See @component(Styled) for more.

            """
        )

        p.heading("## The `box` Component")

        docs_markdown(
            """

            Hyperdiv includes a @component(box) component that
            supports nested layouts. We can create a `box` and place
            "child" components inside it, using a Python `with` block:

            ```py
            with hd.box():
                hd.text("Hello")
                hd.text("World")
            ```

            `box` stacks it children vertically. `hbox` is a `box`
            whose children are laid out horizontally. (`hbox()` is
            equivalent to `box(direction="horizontal")`).

            ```py
            with hd.hbox():
                hd.text("Hello")
                hd.text("World")
            ```

            """
        )

        docs_markdown(
            """

            We can insert a gap between the children using the `gap` prop:

            ```py
            with hd.hbox(gap=1):
                hd.text("Hello")
                hd.text("World")
            ```

            """
        )

        p.heading("## Styling Boxes")

        docs_markdown(
            """

            The @component(box) component inherits from
            @component(Styled) and can be styled using those style
            props.

            ```py
            with hd.box(
                width=8,
                height=5,
                border="1px solid yellow",
                background_color="yellow-50",
                border_radius=1,
                align="center",
                justify="center",
            ):
                hd.text("Hello")
            ```

            """
        )

        p.heading("## Box Alignment")

        docs_markdown(
            """

            @component(box) inherits from @component(Boxy), which
            provides props that let you control how the children of
            the box are aligned inside the box.

            A right-justified vertical box:

            ```py
            with hd.box(
                padding=1,
                gap=1,
                border="1px solid yellow",
                align="end"
            ):
                hd.button("Button 1")
                hd.button("Button 2")
            ```

            A horizontal box with equal space between its children:

            ```py
            with hd.hbox(
                padding=1,
                gap=1,
                border="1px solid yellow",
                justify="space-between"
            ):
                hd.button("Button 1")
                hd.button("Button 2")
                hd.button("Button 3")
            ```

            See @component(box) and @component(Boxy) for more.

            """
        )

        p.heading("## Nesting")

        docs_markdown(
            """

            Almost any Hyperdiv UI component can be placed inside a
            box (except overlay components, like @component(drawer)
            and @component(dialog), which are naturally parentless),
            and boxes can be nested arbitrarily:

            ```py
            with hd.hbox(
                gap=1,
                padding=1,
                justify="center",
                border="1px solid red",
            ):
                with hd.box(
                    gap=1,
                    padding=1,
                    border="1px solid green"
                ):
                    hd.button("Button 1")
                    hd.button("Button 2")
                    hd.button("Button 3")
                with hd.box(
                    gap=1,
                    padding=1,
                    border="1px solid blue"
                ):
                    hd.button("Button 4")
                    hd.button("Button 5")
                    hd.button("Button 6")
            ```

            In this example, we created two side by side columns of
            buttons, by nesting two child boxes within a parent
            horizontal box, and nesting buttons inside the two child
            boxes.

            """
        )
