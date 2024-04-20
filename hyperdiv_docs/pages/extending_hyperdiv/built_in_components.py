import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import docs_markdown


@router.route("/extending-hyperdiv/built-in-components")
def built_in_components():
    with page() as p:
        p.title("# Extending Built-In Components")

        docs_markdown(
            """

            Hyperdiv built-in components can be extended with new
            style props. Also, if a built-in style prop doesn't expose
            CSS attributes that you need, you can override/replace
            that prop with a prop that does.

            Hyperdiv's prop and type system enables defining props
            that are compiled to CSS and applied to the component in
            the browser. For example, we can create a new component
            type that extends @component(box) with an
            [opacity](https://developer.mozilla.org/en-US/docs/Web/CSS/opacity)
            prop:

            ```py
            class opacity_box(hd.box):
                opacity = hd.Prop(
                    hd.CSSField(
                        "opacity",
                        hd.Optional(hd.ClampedFloat(0, 1))
                    ),
                    None
                )

            with opacity_box(
                opacity=0.3,
                border="1px solid green",
                padding=1,
                gap=1,
            ) as box:
                hd.text("A low-opacity box.")
                hd.button("A button")

            ```

            Hyperdiv provides a type, @prop_type(CSSField), that
            enables defining new CSS attributes. In the example above,
            we define a new prop, `opacity`. Its type,
            `CSSField("opacity", hd.Optional(hd.ClampedFloat(0, 1)))`,
            specifies that

            1. this prop will be compiled to CSS
            2. the CSS attribute name is `"opacity"`
            3. the allowed values are floats between 0 and 1. The
               value of the prop will be rendered directly in the CSS
               `opacity` field.

            The CSS `opacity: 0.3;` will be added to instances of this
            component.

            CSS props work like normal Hyperdiv props and can be read
            and mutated by Python code. For example, we can control
            the box opacity with a slider:

            ```py
            class opacity_box(hd.box):
                opacity = hd.Prop(
                    hd.CSSField(
                        "opacity",
                        hd.Optional(hd.ClampedFloat(0, 1))
                    ),
                    None
                )

            opacity = hd.slider(
                min_value=0,
                max_value=1,
                value=1,
                step=0.01
            )

            with opacity_box(
                opacity=opacity.value,
                border="1px solid green",
                padding=1,
                gap=1,
            ) as box:
                hd.text("Drag the slider to change the opacity.")
                hd.button("A button")

            ```

            Note that when the value of a CSS prop is `None`, its
            corresponding CSS field will not be sent to the browser at
            all. `None` corresponds to default browser behavior.

            The props defined by @component(Styled), from which most
            Hyperdiv components inherit, are defined in this way.

            """
        )
