import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import docs_markdown


@router.route("/guides/routing")
def pages_and_navigation():
    with page() as p:
        p.title("# Pages & Navigation")

        p.heading("## Location-Based Rendering")

        hd.markdown(
            """

            Hyperdiv includes a
            [`location`](/reference/components/location) component,
            which is used to inspect the current location in the
            browser's location bar and render different things based
            on location. It can also be used to change the location,
            though this is generally not recommended (see below).

            For example, to render different things based on the
            location path:

            ```py
            loc = hd.location()

            if loc.path == "/foo":
                render_foo_page()
            elif loc.path == "/bar":
                render_bar_page()
            ```

            """
        )

        docs_markdown(
            """

            To change the location, use the `hyperdiv.location.go()`
            method:

            ```py
            loc = hd.location()

            if hd.button("Go to /users").clicked:
                loc.go("/users")
            ```
            """
        )

        p.heading("## Links")

        docs_markdown(
            """
            Note that modifying the location like in the example above
            is not typically recommended, because it makes it
            difficult for screen readers and other accessibility
            devices to detect that the button is a navigation
            button. Instead you should use links, either by making
            markdown links or using the
            [`link`](/reference/components/link) component.

            ```py
            hd.link("Users", href="/users")
            # Or, a link embedded in markdown:
            hd.markdown("[Users](/users)")
            ```
            """
        )

        p.heading("## Router")

        hd.markdown(
            """
            Hyperdiv comes with a basic router, built on top of
            [`location`](/reference/components/location), that makes
            it easy to build apps with multiple pages. When using
            Router, you write one function for each page, decorating
            each function with its path, and then let the router
            render the right page based on the current location:

            ```py
            import hyperdiv as hd

            router = hd.router()

            # Define the app's pages and their paths:

            @router.route("/")
            def home():
                hd.markdown("# Home Page")

            @router.route("/users")
            def users():
                hd.markdown("# Users Page")

            def app():
                with hd.box(gap=1):
                    # A simple navigation menu:
                    with hd.hbox(gap=1):
                        hd.link("Home", href="/")
                        hd.link("Users", href="/users")

                    # Let the router render the right page:
                    router.run()

            hd.run(app)
            ```
            """
        )

        p.heading("## Accessible Navigation")

        hd.markdown(
            """
            When building navigation menus using links, they should be
            wrapped in [`nav`](/reference/components/nav), to provide
            a hint to accessibility devices that the contents of this
            component contain a navigation menu.

            To improve the navigation menu in the example above, we
            use a `nav` instead of an `hbox`.

            ```py
            # A simple navigation menu:
            with hd.nav(direction="horizontal", gap=1):
                hd.link("Home", href="/")
                hd.link("Users", href="/users")
            ```

            `nav` takes the same arguments as
            [`box`](/reference/components/box) and behaves identically
            to a box but generates a `<nav>` HTML tag instead of
            `<div>`.
            """
        )

        p.heading("## Built-In Navigation Menu")

        hd.markdown(
            """
            Hyperdiv provides a built-in navigation menu component
            that supports flat or hierarchical menus and optional
            icons for its menu items.
            """
        )

        with hd.alert(opened=True):
            hd.text(
                """
                Note that clicking links in these examples will lead to the 404
                page, since those paths do not exist in this
                documentation app.
                """
            )

        docs_markdown(
            """
            ```py
            hd.navigation_menu({
                "Welcome": {"href": "/welcome"},
                "Users": {"href": "/users"},
                "Settings": {"href": "/settings"}
            })
            ```
            """
        )

        p.heading("### Menu With Icons")

        docs_markdown(
            """
            The menu items can have prefix icons:

            ```py
            hd.navigation_menu({
                "Welcome": {"icon": "house", "href": "/welcome"},
                "Users": {"icon": "people", "href": "/users"},
                "Settings": {"icon": "gear", "href": "/settings"}
            })
            ```
            """
        )

        p.heading("### Hierarchical Menu")

        docs_markdown(
            """
            By adding a level of nesting, menus can have one level of
            hierarchy, with the individual sections being collapsible:

            ```py
            hd.navigation_menu({
                "Introduction": {
                    "Welcome": {"icon": "house", "href": "/welcome"},
                    "Users": {"icon": "people", "href": "/users"}
                },
                "System": {
                    "My Account": {"icon": "person", "href": "/account"},
                    "Settings": {"icon": "gear", "href": "/settings"}
                }
            })
            ```

            Note that the active route in a menu is automatically
            highlighted, and when using hierarchical menus, the
            section of the active route is automatically expanded.

            We'll demonstrate this by setting the path of the
            "Welcome" link to `"/guides/routing"`, which is the path
            of this page.

            The hierarchical menu also prevents users from collapsing
            the active section.

            ```py
            hd.navigation_menu({
                "Introduction": {
                    "Welcome": {"icon": "house", "href": "/guides/routing"},
                    "Users": {"icon": "people", "href": "/users"}
                },
                "System": {
                    "My Account": {"icon": "person", "href": "/account"},
                    "Settings": {"icon": "gear", "href": "/settings"}
                }
            })
            ```
            """
        )
