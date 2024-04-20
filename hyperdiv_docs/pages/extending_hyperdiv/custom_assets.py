import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import docs_markdown


@router.route("/extending-hyperdiv/custom-assets")
def custom_assets():
    with page() as p:
        p.title("# Loading Custom Assets")

        docs_markdown(
            """

            Hyperdiv can be extended by loading custom JS and CSS at
            the top level of the app. For example, you can [set up
            Google
            Analytics](https://www.w3schools.com/howto/howto_google_analytics.asp)
            for your app, which involves adding Google's custom
            Javascript tags to the app's top-level. Or, load your own
            custom Javascript that runs every time the app is loaded.

            To learn how to load custom assets at the top level, see
            the documentation for @component(index_page).

            """
        )
