import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import docs_markdown


@router.route("/guide/plugins")
def plugins():
    with page() as p:
        p.title("# Building Custom Components")

        docs_markdown(
            """

            Hyperdiv provides a @component(Plugin) base class that can
            be subclassed to create custom components with custom
            Javascript, CSS, and other assets, such as images, text
            files, etc.

            Plugins work like built-in Hyperdiv components. They can
            define props, and when the props are updated by the Python
            app, the updates are sent to the browser. And when the
            browser updates props, they are automatically updated on
            the Python side.

            Plugin instances are wrapped in [Web
            Components](https://developer.mozilla.org/en-US/docs/Web/API/Web_components). As
            such, plugin CSS is naturally isolated to the plugin, and
            does not interfere with other CSS in the app. However,
            plugin Javascript assets are *not isolated*. They are
            inserted in the global `<head>` tag of the Hyperdiv
            app. As such, plugin Javascript assets should be careful
            to not pollute the global scope or modify other objects in
            the global scope.

            A plugin can be instantiated multiple times in the same
            app, and each plugin instance has its own independent
            state.

            A plugin has two parts:

            1. A Python class that inherits from @component(Plugin)
               and defines the plugin's props as well as the plugin's
               static assets, so Hyperdiv can load them in the
               browser.

            2. The plugin's assets. One of the provided assets is a
               special piece of Javascript that uses the Hyperdiv
               Javascript API to register a plugin with the Hyperdiv
               frontend.

            """
        )

        p.heading("## Defining a Plugin")

        docs_markdown(
            """

            We will build a basic counter plugin that renders a count
            and a button that increments the count by 1 when
            clicked. The plugin stores the count in a `count` prop
            that can be read and written in Python.

            The counter plugin implementation is available
            [here](https://github.com/hyperdiv/hyperdiv-docs/tree/main/hyperdiv_docs/demos/counter_plugin).

            Here's the plugin's Python definition:

            ```py-nodemo
            import os
            import hyperdiv as hd

            class counter(hd.Plugin):
                _assets_root = os.path.join(os.path.dirname(__file__), "assets")
                _assets = ["counter.css", "counter.js"]

                count = hd.Prop(hd.Int, 0)
            ```

            The directory structure of this plugin looks like this:

            ```
            counter_plugin/
                __init__.py
                counter.py
                assets/
                    counter.css
                    counter.js
            ```

            `counter.py` contains the Python code above and defines
            the plugin. The `assets` directory contains the Javascript
            and CSS assets of the plugin. `counter.js` contains the
            plugin's HTML/Javascript implementation and the code that
            registers the plugin with the Hyperdiv Javascript
            frontend. `counter.css` styles the plugin.

            """
        )

        p.heading("### Local Assets")

        docs_markdown(
            """

            If the plugin provides local asset files, it must define the
            class variable `_assets_root`. This is the root directory
            where the plugin's assets are stored. In the code above,
            `os.path.join(os.path.dirname(__file__), "assets")` means
            "the directory named `assets` in the same directory as
            this Python module."

            Then, the plugin specifies its static assets in the
            `_assets` class variable. This is a list of paths,
            relative to the assets root.

            The `_assets` variable supports Python
            [glob](https://docs.python.org/3/library/glob.html)
            syntax, so we could rewrite the plugin like this:

            ```py-nodemo
            import os
            import hyperdiv as hd

            class counter(hd.Plugin):
                _assets_root = os.path.join(os.path.dirname(__file__), "assets")
                _assets = ["*"]

                count = hd.Prop(hd.Int, 0)
            ```

            Using `glob` syntax, `"*"` means "include all the files in
            the assets directory". Other examples using glob syntax:

            ```py-nodemo
            # All the .js files, and all the .css files:
            _assets = ["*.js", "*.css"]

            # Recursively include all the .js and .css files in all
            # subdirectories:
            _assets = ["**/*.js", "**/*.css"]

            # Recursively include all the .js files from the `js`
            # subdirectory, and all the .css files from the `css`
            # subdirectory:
            _assets = ["js/**/*.js", "css/**/*.css"]
            ```
            """
        )

        p.heading("### Remote Assets")

        docs_markdown(
            """

            In addition to local assets, a plugin can load remote
            assets. For example, a plugin for
            [Leaflet](https://leafletjs.com) could look like this:

            ```py-nodemo
            class leaflet(hd.Plugin):
                _assets_root = os.path.join(os.path.dirname(__file__), "assets")
                _assets = [
                    "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
                    "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js",
                    "leaflet-plugin.js"
                ]
                # ...
            ```

            This plugin will load Leaflet's CSS and Javascript bundles
            remotely from `unpkg.com`, and then provide the plugin
            registration in the local asset `leaflet-plugin.js`.

            More about this Leaflet plugin [below](#a-leaflet-plugin).

            """
        )

        p.heading("### Nonstandard File Extensions")

        docs_markdown(
            """

            When loading a local or remote asset file, Hyperdiv infers
            its type from its extension. Hyperdiv recognizes the
            extensions `.css` for CSS files and `.js` for Javascript
            files.

            If a file does not have one of these extensions, Hyperdiv
            will raise an error.

            If your plugin contains Javascript or CSS files with a
            different extension, you can use `hd.Plugin.css_link` and
            `hd.Plugin.js_link` to tell Hyperdiv whether a file is a
            CSS file or a Javascript file:

            ```py-nodemo
            class my_plugin(hd.Plugin):
                # ...
                _assets = [
                    # A CSS asset
                    hd.Plugin.css_link("https://foo.com/bar.style")
                    # A Javascript asset
                    hd.Plugin.js_link("foo.stuff")
                ]
            ```

            """
        )

        p.heading("## Registering a Plugin in Javascript")

        docs_markdown(
            """

            The Hyperdiv frontend exports a function,
            `window.hyperdiv.registerPlugin`, that a plugin must use
            to register itself with Hyperdiv.

            A plugin *must* provide a Javascript asset that registers
            the plugin with Hyperdiv. If the registration is missing,
            attempting to use a plugin will cause Hyperdiv to crash
            with Javascript errors.

            The registration looks like this:

            ```js
            window.hyperdiv.registerPlugin(pluginName, registrationFunction);
            ```

            By default, the `pluginName` is the name of the Python
            class that defines the plugin. In our counter example, the
            plugin name would be `"counter"`. A plugin can provide an
            explicit name by setting the `_name` class variable:

            ```py-nodemo
            class my_counter(hd.Plugin):
                _name = "counter"
                ...
            ```

            `registrationFunction` is a function that takes a single
            parameter, a plugin context object, and sets up the plugin
            instance.

            """
        )

        p.heading("### The Plugin Context Object")

        docs_markdown(
            """

            When you instantiate a plugin in Python, the Hyperdiv
            frontend will invoke the registration function and pass it
            an object with the following attributes and methods:

            **Attributes:**

            * `domElement` - The DOM element that this plugin instance
              should mount into. This is the plugin wrapper's [shadow
              root](https://developer.mozilla.org/en-US/docs/Web/API/ShadowRoot).

            * `initialProps` - The prop values with which the plugin
              was instantiated in Python. This is a dictionary that
              maps prop names (the names of the plugin's props as
              defined in Python) to their values.

            * `assetsRoot` - The root path from which the plugin's
              assets are served. The plugin can use this path to load
              additional assets, like images, text files, etc.

            **Methods:**

            * `onPropUpdate(callback)` - Registers a prop update
              handler, to handle incoming prop updates from
              Python. The callback will be called with the arguments
              `(propName, propValue)`, with the name and value of the
              prop that was updated.

            * `updateProp(propName, propValue)` - Sends a prop update
              to Python.

            Note that when a plugin calls `ctx.updateProp(propName,
            propValue)` to tell Python to update a prop, this update
            *will not* be echoed back to the plugin. That is, the
            update callback registered with `ctx.onPropUpdate()` will
            not be called for this particular update. Therefore the
            plugin should update its own internal state to reflect
            the update, before sending it to Python.

            """
        )

        p.heading("## Counter Implementation")

        docs_markdown(
            """

            Here are the contents of `counter.js`, which implements
            and registers our counter plugin:

            ```js
            window.hyperdiv.registerPlugin("counter", (ctx) => {
              let count = 0;
              const button = document.createElement("button");
              button.innerText = "Increment";
              const countDiv = document.createElement("div");

              const updateCount = (newCount) => {
                count = newCount;
                countDiv.innerText = count;
              };

              // On click, increment the count and send the updated
              // prop value to Python:
              button.addEventListener("click", () => {
                updateCount(count + 1);
                ctx.updateProp("count", count);
              });

              // Handle incoming prop updates from Python. We ignore
              // `propName` because there is only one prop, "count".
              ctx.onPropUpdate((propName, propValue) => {
                updateCount(propValue);
              });

              // Add the dom elements to the shadow root.
              ctx.domElement.appendChild(button);
              ctx.domElement.appendChild(countDiv);

              // Initialize the plugin with the initial count.
              updateCount(ctx.initialProps.count);
            });
            ```

            Here is the plugin in action:

            ```py
            counter()
            ```

            We can initialize, read, and write the `count` prop from
            Python. We can also style the plugin's outer container,
            since @component(Plugin) inherits from @component(Styled).

            ```py
            c = counter(
                count=30,
                padding=1,
                border="1px solid neutral-100",
                background_color="neutral-50",
                border_radius="large"
            )

            hd.markdown('**Prop access in Python**:')

            hd.text(c.count)
            if hd.button("Increment").clicked:
                c.count += 1
            if hd.button("Decrement").clicked:
                c.count -= 1

            """
        )

        p.heading("## Using Shoelace In Plugins")

        docs_markdown(
            """

            All the [Shoelace](https://shoelace.style) components and
            Shoelace CSS variables used by Hyperdiv are available to
            plugins.

            For example, a plugin could create a Shoelace button like
            this:

            ```js
            const button = document.createElement("sl-button")
            ```

            When styling elements in plugins, Shoelace's CSS variables
            can be used. For example:

            ```css
            .my-class {
                border-radius: var(--sl-border-radius-large);
                background-color: var(--sl-color-blue-100);
            }
            ```

            """
        )

        p.heading("## A Leaflet Plugin")

        docs_markdown(
            """

            Finally, here is a barebones [Leaflet
            plugin](https://github.com/hyperdiv/hyperdiv-docs/tree/main/hyperdiv_docs/demos/leaflet_plugin)
            for the [Leaflet](https://leafletjs.com) map library,
            which exposes `lat`, `lng`, and `zoom` props.

            In this example, we instantiate the plugin and render a
            list of controls below it, to modify its props from
            Python.

            ```py
            leaf = leaflet(
                # NYC:
                lat=40.713955826286046,
                lng=-73.99944305419923,
                zoom=14
            )

            with hd.hbox(gap=1, justify="center"):
                if hd.icon_button("plus").clicked:
                    leaf.zoom += 1
                if hd.icon_button("dash").clicked:
                    leaf.zoom -= 1
                if hd.icon_button("arrow-up").clicked:
                    leaf.lat += 0.01
                if hd.icon_button("arrow-down").clicked:
                    leaf.lat -= 0.01
                if hd.icon_button("arrow-left").clicked:
                    leaf.lng -= 0.01
                if hd.icon_button("arrow-right").clicked:
                    leaf.lng += 0.01

            ```
            """
        )
