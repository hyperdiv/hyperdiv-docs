import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import code_example, docs_markdown


@router.route("/guide/components")
def components():
    with page() as p:

        p.title("# Component Basics")

        docs_markdown(
            """

            Hyperdiv includes a rich set of [UI
            components](/reference/components) from the
            [Shoelace](https://shoelace.style) component library,
            charts, tables, and markdown.

            """
        )

        p.heading("## UI Components Overview")

        docs_markdown(
            '''

            To add components to your app, you just instantiate them
            with relevant arguments. Here are some examples:

            ```py
            hd.checkbox("Check Me", checked=True)
            hd.alert("This is an alert", opened=True)
            hd.button("Click Me")
            hd.radio_buttons("One", "Two", "Three", value="Three")
            hd.text_input(placeholder="Enter Some Text")
            hd.progress_bar("75%", value=75)
            hd.tab_group("Tab 1", "Tab 2", "Tab 3")
            ```

            Hyperdiv provides many more UI components, found in the
            [reference](/reference/components).

            Hyperdiv comes bundled with charts and tables, too:

            ```py
            hd.bar_chart(
                (3, 18, 6),
                (20, 1, 24),
                x_axis=("Oats", "Corn", "Beef"),
                labels=(2022, 2023)
            )
            hd.line_chart(
                (3, 5, 9, 4, 20, 50, 4, 9),
                (1, 8, 4, 31, 30, 15, 80, 20),
                labels=("Trend A", "Trend B")
            )
            hd.data_table(dict(
                Name=("Lisa", "John", "Amy"),
                Age=(28, 25, 31)
            ))
            ```

            Hyperdiv also includes a Markdown component, based on
            [Mistune](https://mistune.lepture.com) and
            [Pygments](https://pygments.org).

            ```py
            hd.markdown(
                """
                ## A Heading

                * Item 1
                * Item 2

                ```js
                const add = (a, b) => a + b;
                ```
                """
            )
            ```
            '''
        )

        p.heading("## Component Props")

        docs_markdown(
            """

            Props will be covered in subsequent sections of this
            guide, but it's worth mentioning here that almost all
            Hyperdiv components export *props*. Props are special
            component attributes that hold a component's state, and
            are at the foundation of how Hyperdiv works.

            For example `checked` is a prop of @component(checkbox),
            giving read/write access to the checkbox's checked state.

            Props are initialized by passing a keyword-argument to the
            component constructor (e.g. `hd.checkbox(checked=True)`
            and accessed via a component attribute with the same name
            (e.g. `my_checkbox.checked`).

            """
        )

        p.heading("## Container Components")

        docs_markdown(
            """

            Some Hyperdiv components, including those based on
            Shoelace, are "containers" that can have child components
            nested inside them.

            For example:

            ```py
            alert = hd.alert(opened=True)
            with alert:
                hd.plaintext("This is an alert")
            ```

            In this example, @component(alert) is a container, and we
            nest a @component(plaintext) component inside it using the
            `with` keyword. In Hyperdiv, the `with` keyword is
            universally used to nest children inside a container.

            Note that for convenience, @component(alert) accepts a
            text label argument and if you pass it, it
            automatically creates a child text component with that
            label. This pattern is common across Hyperdiv:

            ```py
            hd.alert("This is an alert", opened=True)
            # Is equivalent to
            alert = hd.alert(opened=True)
            with alert:
                hd.plaintext("This is an alert")
            ```

            """
        )

        p.heading("### Slots")

        docs_markdown(
            """

            In the example above, when we nested a text component
            inside an alert component, we say that we placed the text
            component inside the alert's "default slot".

            Many Hyperdiv components export additional, named slots,
            which target various internal containers within those
            components.

            For example, the @component(button) component exports
            `prefix` and `suffix` slots that can be used to nest
            prefix and suffix icons within the button:

            ```py
            with hd.button() as button:
                # Default slot
                hd.plaintext("The label")
                # 'prefix' slot
                hd.icon("gear", slot=button.prefix)
                # 'suffix' slot
                hd.icon("chevron-right", slot=button.suffix)
            ```

            Child components can be "slotted" into a parent by passing
            the parent slot into the child's `slot` prop.

            In many cases, for convenience, components accept keyword
            arguments that will automatically fill in those slots. The
            example above is equivalent to:

            ```py
            hd.button(
                "The label",
                prefix_icon="gear",
                suffix_icon="chevron-right"
            )
            ```

            """
        )
