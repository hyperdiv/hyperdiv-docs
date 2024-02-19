import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import code_example, docs_markdown


@router.route("/reference/cli")
def cli():
    with page() as p:

        p.title("# The Hyperdiv CLI")

        hd.markdown(
            """

            When you install Hyperdiv, a command-line utility named
            `hyperdiv` will be automatically installed.

            Currently, the CLI provides only one command, which opens
            this documentation app when run:

            ```sh
            hyperdiv docs
            ```

            The CLI will provide additional commands in the future.

            """
        )
