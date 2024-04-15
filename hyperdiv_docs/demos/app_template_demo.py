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
