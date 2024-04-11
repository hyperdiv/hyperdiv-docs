import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import docs_markdown


@router.route("/reference/plugins")
def plugins():
    with page() as p:
        p.title("# Plugins")

        docs_markdown(
            """

            Hyperdiv provides a @component(Plugin) base class that can
            be subclassed to create custom components with custom
            Javascript, CSS, and other assets, such as images.

            Plugins work like built-in Hyperdiv components. They can
            define props, and when the props are updated by the Python
            app, the updates are sent the browser. And when the
            browser updates props, they are automatically updated on
            the Python side.

            A plugin can be instantiated multiple times in the same
            app, and each plugin instance has its own independent
            state.

            A plugin has two parts:

            1. A Python class that inherits from @component(Plugin)
               and defines the plugin's props as well as the plugin's
               static assets, so Hyperdiv can load them in the
               browser.

            2. One of the provided assets is a special piece of
               Javascript that uses the Hyperdiv Javascript API to
               register a plugin with the Hyperdiv frontend.

            """
        )

        p.heading("## Defining a Plugin")

        p.heading("## Registering a Plugin in Javascript")
