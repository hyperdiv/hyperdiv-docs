import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import code_example, docs_markdown


@router.route("/guide/state")
def state():
    with page() as p:
        p.title("# Custom State")

        hd.markdown(
            """

            So far, we've seen how to interact with the states of
            built-in components, but most apps will need to manage
            custom user-defined state and data.

            """
        )

        p.heading("## Using `hd.state`")

        docs_markdown(
            """

            Hyperdiv provides @component(state) for quickly defining
            custom state components:

            ```py
            state = hd.state(count=0)
            hd.text("Count:", state.count)
            if hd.button("Increment").clicked:
                state.count += 1
            ```

            In this example, we define a custom state component with a
            `count` prop that is initially set to `0`. When the button
            is clicked, we increment the count.

            @component(state) works by dynamically converting its
            kwargs into props, which can be initialized, read, and
            mutated just like normal component props. You can define
            as many props as you want on a state component:

            ```py
            state = hd.state(count=0, name="Steve")

            hd.text("Count:", state.count)
            hd.text("Name:", state.name)

            if hd.button("Increment").clicked:
                state.count += 1

            if hd.button("Toggle Name").clicked:
                state.name = (
                    "George"
                    if state.name == "Steve"
                    else "Steve"
                )
            ```

            """
        )

        p.heading("## Change Detection")

        docs_markdown(
            """

            As mentioned earlier, Hyperdiv re-runs the app when a
            prop's value is mutated to a different value. Hyperdiv
            intercepts all assignments into props and compares the
            prop's current value with the new, incoming value, in
            order to detect a change.

            When you work with custom state, and you update a custom
            state prop, you should always assign a *new value* into
            the state, as opposed to internally modifying a current
            value. For example:

            ```py
            state = hd.state(users=["Steve", "Bob"])
            hd.text(state.users)
            if hd.button("Add New User").clicked:
                state.users.append("Mary")
            ```

            In this example, Hyperdiv won't be able to detect a change
            in the prop `state.users`, because we didn't mutate the
            prop. Instead, we internally modified the list stored in
            the prop. Even though the list contents changed, the list
            itself is the same list.

            This way of modifying a list works:

            ```py
            state = hd.state(users=["Steve", "Bob"])
            hd.text(state.users)
            if hd.button("Add New User").clicked:
                state.users = state.users + ["Mary"]
            ```

            In this example, `state.users + ["Mary"]` creates a *new
            list* and assigns it into the prop. When Hyperdiv compares
            the old list to the new list, it detects a change because
            they are different lists.

            """
        )

        p.heading("## State Initial Values")

        docs_markdown(
            """

            Note that initial values to state props are recreated
            every time Hyperdiv re-runs the app. For example:

            ```py-nodemo
            import hyperdiv as hd

            class MyObject:
                ...

            def main():
                state = hd.state(my_object=MyObject())
                ...

            hd.run(main)
            ```

            As Hyperdiv re-runs this app, `MyObject()` will be
            re-created on every run.

            This is fine in many cases, e.g. when initializing state
            with primitive values or basic list/tuple literals, but if
            you need the prop value to stay unchanged across runs (for
            example if you store a `threading.Lock` object in a prop),
            you should use this pattern:

            ```py-nodemo
            import hyperdiv as hd

            class MyObject:
                ...

            def main():
                state = hd.state(my_object=None)
                if state.my_object is None:
                    state.my_object = MyObject()
                ...

            hd.run(main)
            ```

            In this example, `MyObject()` is called only once, on the
            first run of the application. On that first run, the
            object is created and assigned into `state.my_object`. On
            subsequent runs, `if state.my_object is None` will
            evaluate to `False` and the object creation will be
            skipped.

            """
        )

        p.heading("## Typed State")

        docs_markdown(
            """

            In addition to @component(state), You can define your own
            state classes with typed props. See @component(BaseState).

            """
        )
