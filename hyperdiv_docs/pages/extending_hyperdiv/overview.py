import hyperdiv as hd
from ...router import router
from ...page import page


@router.route("/extending-hyperdiv")
def overview():
    with page() as p:
        p.title("# Extending Hyperdiv")

        hd.markdown(
            """

            Hyperdiv can be extended in multiple ways, with new
            functionality that isn't already built-in.

            The sub-sections of this part of the documentation explore
            the various ways Hyperdiv can be extended with new
            functionality:

            * [Building Plugins](/extending-hyperdiv/plugins) -
              building new, self-contained, reusable components with
              custom Javascript, CSS, and other assets.

            * [Loading Custom Assets](/extending-hyperdiv/assets) -
              Loading custom Javascript and CSS assets into the
              top-level application.

            * [Extending Built-In
              Components](/extending-hyperdiv/built-in-components) -
              Subclassing and extending existing Hyperdiv components.

            * [Creating New
              Components](/extending-hyperdiv/new-components) - An
              alternative way to define new, simple components without
              building plugins.

            """
        )
