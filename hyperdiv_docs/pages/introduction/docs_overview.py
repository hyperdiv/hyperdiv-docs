import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import docs_markdown


@router.route("/introduction/docs-overview")
def docs_overview():
    with page() as p:
        p.title("# This Documentation App")

        hd.markdown(
            """
            The rest of this app is organized in the following sections, which
            can be accessed via the sidebar:
            """
        )

        hd.markdown("### Guide", font_color="blue")

        hd.markdown(
            """

            The [Guide](/guide/getting-started) section is a guided
            walk through some of Hyperdiv's core features. It is not
            an exhaustive explanation of Hyperdiv. Instead, it tries
            to impart a high level taste of what's currently possible
            with Hyperdiv.

            """
        )

        hd.markdown("### Reference", font_color="blue")

        hd.markdown(
            """

            The [Reference](/reference/components) section documents
            each Hyperdiv component and function in detail.

            """
        )
