import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import code_example, docs_markdown


@router.route("/guide/loops")
def loops():
    with page() as p:
        p.title("# Rendering in Loops")

        docs_markdown(
            """

            When rendering components in loops, we have to take a bit
            of extra precaution. For example, if we want to render 5
            sliders in a loop, this code will not work:

            ```py
            for i in range(5):
                slider = hd.slider()
                hd.text(slider.value)
            ```

            The reason for the failure is that Hyperdiv internally
            assigns each component a unique ID (key), based roughly on
            the position in the code where that component is
            instantiated.

            The fix is to wrap the loop body in @component(scope), and
            pass to each scope a value that is unique per loop
            iteration. In this case `i` is unique per loop iteration:

            ```py
            for i in range(5):
                with hd.scope(i):
                    slider = hd.slider()
                    hd.text(slider.value)
            ```

            Passing `i` to `scope` gives Hyperdiv the extra
            information it needs to generate unique IDs for all
            components.

            """
        )

        with hd.alert(
            opened=True,
            background_color="neutral-0",
            border="1px solid neutral-100",
        ):
            hd.markdown(
                """

                In general, when rendering lists of components in
                loops, always wrap the loop body in `with
                hd.scope(loop_id)`, where `loop_id` is unique per loop
                iteration.

                When rendering a list of database records by iterating
                over the list, the `loop_id` is naturally the primary
                key of the record.

                """
            )

        docs_markdown(
            """

            `scope` is covered more extensively in the [scope reference
            documentation](/reference/components/scope).

            """
        )
