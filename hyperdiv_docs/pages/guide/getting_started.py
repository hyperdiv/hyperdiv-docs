import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import code_example, docs_markdown


@router.route("/guide/getting-started", redirect_from=("/guide",))
def getting_started():
    with page() as p:

        p.title("# Getting Started")

        hd.markdown(
            """

            This Guide section of the documentation aims to give a
            high level taste for how Hyperdiv works and how Hyperdiv
            apps are structured. It is not a complete description of
            Hyperdiv. The Hyperdiv API is documented in detail in the
            Reference section.

            """
        )

        p.heading("## Hello World")

        hd.markdown("The simplest possible Hyperdiv app:")

        code_example(
            """
            import hyperdiv as hd

            def main():
                hd.text("Hello, World!")

            hd.run(main)
            """,
            code_to_execute=(
                """
                hd.text("Hello World")
                """
            ),
        )

        hd.markdown(
            """

            The running app is rendered to the right of the code block
            (or below, on small screens). This code example pattern is
            used throughout this documentation app.

            """
        )

        with hd.alert(
            opened=True,
            background_color="neutral-0",
            border="1px solid neutral-100",
        ):
            docs_markdown(
                """

                Note that to avoid repetition, the rest of this
                documentation app will often only show the body of the app
                function, and assume you'll fill in the rest. Like this:

                ```py
                hd.text("Hello World")
                ```

                """
            )

        p.heading("### Running the App")

        hd.markdown(
            """

            You can click the clipboard icon to the top-right of the
            code block to copy the code, and paste it into a new file
            called `hello.py`. Then, you can run the app at the
            command line with:

            ```sh
            python hello.py
            ```

            Hyperdiv will print the local URL where the app is
            running, which is typically `http://localhost:8888`. You
            can open this URL in a browser to view the running app.

            As you make modifications to the source code, the app will
            automatically reload when you save the file.

            """
        )

        with hd.alert(
            opened=True,
            background_color="neutral-0",
            border="1px solid neutral-100",
        ):
            hd.markdown(
                """

                When you ship an app to be run locally by users, or
                deploy it on a server, you can put it in [production
                mode](/reference/env-variables), so that a browser tab
                automatically opens with the app in it when you run
                the app script.

                """
            )

        p.heading("### Changing the Port")

        docs_markdown(
            """

            By default, Hyperdiv uses port `8888`, and will fail to
            start if this port is occupied. To run the app on a
            different port, use the `HD_PORT` environment variable:

            ```sh
            HD_PORT=9000 python hello.py
            ```

            """
        )

        p.heading("## App Structure")

        hd.markdown(
            """

            Getting started with writing a Hyperdiv app has three simple steps:
            1. Import the `hyperdiv` module.
            2. Define the app function. Here, it is called `main`.
            3. Run the app function with `hyperdiv.run(main)`.

            Inside the app function, you lay out the app's UI and
            logic, using components exported by the `hyperdiv`
            module.

            In this example, when you call `hd.text("Hello, World!")`,
            a text component with the contents `"Hello World"` is
            automatically rendered in the browser.

            """
        )
