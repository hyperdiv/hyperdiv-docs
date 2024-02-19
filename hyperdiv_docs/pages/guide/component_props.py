import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import code_example, docs_markdown


@router.route("/guide/props")
def component_props():
    with page() as p:

        p.title("# Component Props")

        hd.markdown(
            """

            Virtually every Hyperdiv component exports *props*. Props
            determine the component's state at any given time and are
            a fundamental piece of how Hyperdiv works.

            """
        )

        p.heading("## Initializing Props")

        docs_markdown(
            """

            A component's props are initialized by passing prop values
            into the component's constructor. For example:

            ```py
            hd.checkbox(checked=True)
            ```

            Here, we initialize the checkbox's `checked` prop to
            `True`, and the checkbox renders in checked state. In
            general, any prop can be initialized by passing a kwarg
            with the prop's name to the constructor.

            """
        )

        p.heading("## Accessing Props")

        docs_markdown(
            """

            The current value of a component's prop can be accessed
            via an attribute with the prop's name:

            ```py
            ch = hd.checkbox(checked=True)
            hd.markdown(
                "The value of `checked` is",
                ch.checked
            )
            ```

            In this example, we access the value of the `checked` prop
            using `ch.checked`, and render it in a markdown
            component. In general, every prop exported by a component
            can be accessed via a component attribute with the prop's
            name.

            """
        )

        p.heading("## Mutating Props")

        docs_markdown(
            """

            Notice that in the example above, the markdown component
            updates as we check and uncheck the checkbox.

            When we click the checkbox, the value of the `checked`
            prop is *mutated*. In response to the mutation, Hyperdiv
            re-runs the app function, which generates an updated UI
            reflecting the new value of the `checked` prop.

            Props can also be mutated in code, in reponse to events:

            ```py
            ch = hd.checkbox(checked=True)
            hd.markdown(
                "The value of `checked` is",
                ch.checked
            )
            button = hd.button("Toggle")
            if button.clicked:
                ch.checked = not ch.checked
            ```

            When we click the button, `button.clicked` becomes `True`
            for one run, and our code toggles the value of the
            `checked` prop. We will expand on how the `clicked` prop
            works, further down on this page.
            """
        )

        p.heading("## Prop Lifecycle")

        docs_markdown(
            """

            In Hyperdiv, props start off in "initialized" state, and
            transition to "mutated" state when they are first mutated.

            Props are initialized using keyword-arguments passed to
            the constructor. While in "initialized" state, a prop is
            updated with the value of its keyword argument, every time
            the app function runs. When first mutated, the prop enters
            "mutated" state: it begins ignoring the value of the
            constructor keyword argument, and instead remembers its
            mutated value.

            Here's an example:

            ```py
            slider = hd.slider()
            hd.text_input(value=slider.value)
            ```

            In the example above, the text input's `value` prop is
            initialized with the slider's `value` prop, updating as
            you move the slider. But as soon as you type into the box,
            the text input's `value` prop enters "mutated" state and
            stops taking its value from the slider.

            A prop's "mutated" state can be reset back to
            "initialized" by calling `component.reset_prop(prop_name)`:

            ```py
            slider = hd.slider()
            text_input = hd.text_input(value=slider.value)
            reset_button = hd.button("Reset")
            if reset_button.clicked:
                text_input.reset_prop("value")
            ```

            This design strikes a balance between being able to build
            dataflow UIs, where components dynamically take their prop
            values from other components' props, and honoring user
            intent by "sticking" to the value set by the user.

            As a related side note, resetting a @component(form) is
            implemented by calling `reset_prop()` on the form's input
            components. Resetting a form causes all of its input
            components to "forget" their mutated states caused by
            the user editing the inputs.

            """
        )

        p.heading("## Event Props")

        docs_markdown(
            """

            Some props are *event props*, the most prominent of which
            is the `clicked` prop of @component(button) and @component(link).

            Event props are props that:

            * Cannot be initialized. You cannot create a button with
              `hd.button(clicked=True)`.
            * Cannot be directly mutated by app Python code. You
              cannot do `button.clicked = True`.
            * Are "set" for only one run of the application when the
              corresponding event triggers.
            * Are automatically reset to their default value after the run.

            ```py
            slider = hd.slider(min_value=0, max_value=10)
            hd.text("Value:", slider.value)
            button = hd.button("Increment")
            if button.clicked:
                if slider.value < 10:
                    slider.value += 1
            ```

            In this example, the part of the code guarded by `if
            button.clicked` is executed exactly once per click. When
            you click the button, `clicked` becomes `True`. Hyperdiv
            then re-runs the app function with `clicked` set to
            `True`, which causes the slider `value` prop to be
            incremented. At at the end of that run, `clicked` is
            automatically reset back to `False`.

            """
        )

        with hd.alert(
            opened=True,
            background_color="neutral-0",
            border="1px solid neutral-50",
        ):
            hd.markdown(
                """

                When checking an event's prop value, you should only
                perform state mutations under that conditional. You
                should not attempt to render components. This will not
                work:

                ```py
                if hd.button("Show Text").clicked:
                    hd.text("The Text")
                ```

                The text component `"The Text"` will not be
                rendered. This is because `button.clicked` is only
                `True` for a single run, so the text component will
                disappear on subsequent runs.

                Instead, this pattern will work:

                ```py
                state = hd.state(visible=False)
                if state.visible:
                    hd.text("The Text")
                if hd.button("Show Text").clicked:
                    state.visible = True
                ```
                """
            )

        p.heading("## Prop Types")

        docs_markdown(
            """

            Hyperdiv has a custom, dynamic type system for props, that
            controls which kinds of values a prop accepts. For
            example, if a prop has type @prop_type(Int), it only
            accepts integer values, and if you attempt to set an
            integer prop to a non-integer value, an exception will be
            raised at runtime.

            The prop types used in Hyperdiv are documented
            [here](/reference/prop-types).

            """
        )
