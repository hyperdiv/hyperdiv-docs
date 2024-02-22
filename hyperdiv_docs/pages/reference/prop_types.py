import hyperdiv as hd
from ...router import router
from ...code_examples import docs_markdown
from ...page import page
from ...docs_metadata import get_docs_metadata


@router.route("/reference/prop-types")
def prop_types():
    data = get_docs_metadata()

    top_level_types = []
    concrete_types = []

    for pt in data["prop_types"].values():
        if pt["toplevel"]:
            top_level_types.append(pt)
        else:
            concrete_types.append(pt)

    with page() as p:
        p.title("# Prop Types")

        hd.markdown(
            """
            Hyperdiv has a custom dynamic type system (unrelated to
            Python's [type
            annotations](https://docs.python.org/3/library/typing.html))
            for controlling the values that are accepted by component
            props. When you assign a value into a prop, and the value
            does not match the prop's type, an error will be
            raised. This helps catch typos immediately instead of
            propagating incorrect values into the browser and causing
            hard-to-debug behaviors.

            Hyperdiv types may accept values in multiple formats. The
            various formats are transformed into a *canonical form*
            that is ultimately stored in the prop. For example, the
            type `Size` may accept values like `10`, `"10rem"` or `(10,
            "rem")`, but the stored value will always look like `(10,
            "rem")`.
            """
        )

        p.heading("## User-Facing State Types")

        docs_markdown(
            """

            You can use the following types to define your own typed
            @component(BaseState) components, or adding additional props
            to component subclasses.

            """
        )

        with hd.box(gap=0.5):
            for pt in top_level_types:
                with hd.scope(pt["name"]):
                    hd.link(
                        pt["name"],
                        href=f"/reference/prop-types/{pt['name']}",
                        width="fit-content",
                    )

        p.heading("## Other Types")

        hd.markdown(
            """
            The following is a list of prop types specific to
            built-in Hyperdiv components.
            """
        )

        with hd.box(gap=0.5):
            for pt in concrete_types:
                with hd.scope(pt["name"]):
                    hd.link(
                        pt["name"],
                        href=f"/reference/prop-types/{pt['name']}",
                        width="fit-content",
                    )


@router.route("/reference/prop-types/{prop_type}")
def prop_type(prop_type_name):
    if prop_type_name == "Icon":
        with page() as p:
            p.title("# `Icon`")
            hd.markdown(
                """
                The `Icon` type accepts icon names.

                Head to the [icons reference page](/reference/icons)
                to browse the available icons.
                """
            )
        return

    data = get_docs_metadata()
    if prop_type_name not in data["prop_types"]:
        router.render_not_found()
        return

    prop_type = data["prop_types"][prop_type_name]

    with page() as p:
        p.title(f"# `{prop_type_name}`")

        if prop_type["doc"]:
            docs_markdown(prop_type["doc"])

        if prop_type["is_alias"]:
            with hd.box(gap=1):
                hd.markdown("### Type Definition:")
                hd.markdown(
                    f"{prop_type_name} = {prop_type['markdown']}", font_family="mono"
                )
