import hyperdiv as hd
from ...router import router
from ...page import page


@router.route("/guides/templates")
def using_the_app_template():
    with page() as p:
        p.title("# Using the App Template")

        p.heading("## Introduction")

        hd.markdown(
            """
            To help quickly build basic apps and tools, Hyperdiv comes
            bundled with a template that features:

            * A top bar that can hold
                * a top-left logo and title.
                * a top-right theme switcher and optional navigation links.

            * A sidebar that can hold an optional navigation menu or any
              other components. The sidebar becomes a togglable drawer on
              small screens and the responsive threshold can be
              customized.

            * A main content area.

            This documentation app is built using the app template.
            """
        )

        p.heading("## Example")

        hd.markdown(
            """
            ```py
            import hyperdiv as hd

            router = hd.router()

            # Define the pages of the app:

            @router.route("/app-template-demo")
            def home():
                hd.markdown("# Welcome")


            @router.route("/app-template-demo/users")
            def users():
                hd.markdown("# Users")


            def main():
                template = hd.template(logo="/assets/hd-logo-white.svg", title="My App")

                # Sidebar menu linking to the app's pages:
                template.add_sidebar_menu(
                    {
                        "Home": {"icon": "house", "href": home.path},
                        "Users": {"icon": "people", "href": users.path},
                    }
                )

                # A topbar contact link:
                template.add_topbar_links(
                    {"Contact": {"icon": "envelope", "href": "mailto:hello@hyperdiv.io"}}
                )

                # Render the active page in the body:
                with template.body:
                    router.run()

            hd.run(main)
            ```
            """
        )

        with hd.link(
            href="/app-template-demo",
            align="center",
            background_color="primary",
            font_color="neutral-0",
            padding=1,
            border_radius="large",
        ):
            hd.text("Run This App"),
            hd.text(
                "Click the browser back button to return here.",
                font_size="small",
                font_color="primary-200",
            )

        p.heading("## Responsive Thresholds")

        hd.markdown(
            """

            In wide browser windows, the sidebar is rendered in-line,
            and the topbar links show both the link icon and the link
            name. In narrow browser windows, the sidebar is rendered
            in a togglable drawer, and the topbar links show only the
            link icon, with the link name in a tooltip.

            The threshold when a browser window is considered "wide"
            can be controlled with two kwargs:

            * `responsive_threshold`: (Default `1000`.) Controls the
              threshold, in pixels, at which the sidebar is rendered
              in a drawer vs. inline.

            * `responsive_topbar_links_threshold`: (Default `600`.)
              Controls the threshold, in pixels, at which topbar links
              are rendered as icons vs. icon + name.

            ```py
            template = hd.template(
                title="My App",
                # When the window is narrower than 1200 pixels,
                # render the sidebar in a drawer.
                responsive_threshold=1200,
                # When the window is narrower than 700 pixels,
                # render the topbar links as icon-only.
                responsive_topbar_links_threshold=700
            )
            ```
            """
        )

        p.heading("## Custom Sidebar and Topbar Contents")

        hd.markdown(
            """

            The typical usage of the app template is:

            ```py
            template = hd.template(
                logo="/assets/my-logo.svg",
                title="My App",
            )
            template.add_sidebar_menu(my_menu)
            template.add_topbar_links(my_links)
            with template.body:
                my_app_body()
            ```

            This will render the logo, along with the app title, in
            the top-left of the topbar, and at the top of the sidebar
            drawer (on small screens). It will also render a series of
            links in the top-right of the topbar.

            However, arbitrary contents can be placed in the sidebar,
            topbar title area, and topbar links area.

            ```py
            template = hd.template()
            # The main app title.
            with template.app_title:
                hd.text("Custom title")
            # The app title at the top of the drawer.
            # Relevant only when a drawer is present.
            with template.drawer_title:
                hd.text("Custom title")
            # Custom topbar links content.
            with template.topbar_links:
                hd.text("Custom topbar")
            # Custom sidebar content.
            with template.sidebar:
                hd.text("Custom sidebar")
            ```

            Note that you can add stuff to the sidebar before or after
            you render a menu:

            ```py
            template.add_sidebar_menu(my_menu)
            with template.sidebar:
                hd.text(
                    '''
                    Custom sidebar content,
                    Rendered, below the menu.
                    '''
                )
            ```
            """
        )

        p.heading("## Optional Sidebar")

        hd.markdown(
            """

            The sidebar is optional and you can make a simple app
            without a sidebar by passing `sidebar=False`:

            ```py
            template = hd.template(
                logo="/assets/logo.svg",
                title="My App",
                sidebar=False
            )
            with template.body:
                hd.markdown("# Hello")
            ```

            Without a sidebar, there will be no drawer or drawer
            toggle button rendered on small screens.
            """
        )
