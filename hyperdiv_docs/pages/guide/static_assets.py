import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import code_example, docs_markdown


@router.route("/guide/static-assets")
def static_assets():
    with page() as p:

        p.title("# Static Assets")

        hd.markdown(
            """

            Apps will in general want to display images or provide
            links to static documents.

            To make static assets available to your app, you can
            create a directory called `assets` in the same directory
            as the application's start script. If you store your
            application in a directory called `my_app`, you can create
            a directory structure like this:

            ```sh
            my_app/
              assets/
                my-image.png
                a-text-file.txt
                ...
              start.py
              ...
            ```

            Then, the app whose entrypoint is `start.py` will be able
            to refer to these static assets using paths prefixed by
            `"/assets"`. For example:

            ```py
            hd.image("/assets/my-image.png")
            hd.link("A text file", href="/assets/a-text-file.txt")
            ```

            Note that the assets directory must be named `assets`, and
            must have the same parent directory as the app script, in
            order for Hyperdiv to detect it.

            """
        )
