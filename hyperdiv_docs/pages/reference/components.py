import hyperdiv as hd
from ...router import router
from ...code_examples import docs_markdown
from ...utils import render_value
from ...page import page
from ...docs_metadata import get_docs_metadata


def render_methods(methods):
    hd.markdown("### Methods")

    with hd.box(gap=1):
        for method in methods:
            with hd.scope(method["sig"]):
                with hd.box(
                    border="1px solid neutral-100",
                    border_radius="large",
                ):
                    with hd.box(
                        background_color="neutral-50",
                        border_radius=("large", "large", 0, 0),
                    ):
                        hd.code(method["sig"], grow=1)
                    if method.get("overrides"):
                        with hd.box(padding=(0.6, 1, 0.6, 1)):
                            hd.markdown(
                                f"Overrides `{method['method_name']}` from "
                                f"[`{method['overrides']}`](/reference/components/{method['overrides']}/).",
                            )
                    if method["doc"]:
                        with hd.box(padding=(0.6, 1, 0.6, 1)):
                            docs_markdown(method["doc"])


def render_props(props):
    hd.markdown("### Props")
    with hd.box(gap=1):
        for prop in props:
            with hd.scope(prop["prop_name"]):
                with hd.box(gap=0.2, border="1px solid neutral-100", border_radius=0.4):
                    default_value = render_value(prop["default_value"])
                    with hd.hbox(
                        gap=0.5,
                        background_color="neutral-50",
                        justify="space-between",
                        border_radius=(0.3, 0.3, 0, 0),
                        padding=(0.5, 1, 0.5, 1),
                        align="center",
                    ):
                        hd.text(
                            f"{prop['prop_name']} = {default_value}", font_family="mono"
                        )
                        if prop["immutable"]:
                            hd.badge(
                                "read-only",
                                variant="neutral",
                                padding=(0, 0.3, 0, 0.3),
                                height=1.2,
                            )

                    with hd.box():
                        hd.markdown(
                            f"type: {prop['markdown']}",
                            font_family="mono",
                            padding=(0.5, 1, 0.5, 1),
                        )
                        prop_doc = prop["prop_doc"]
                        if prop_doc:
                            hd.divider(color="neutral-100")
                            with hd.box(padding=(0.5, 1, 0.5, 1)):
                                docs_markdown(prop_doc)


def render_slots(slots):
    # TODO: Nicer rendering of slots
    hd.markdown("### Slots")
    hd.markdown(", ".join([f"`{slot['slot_name']}`" for slot in slots]))


@router.route("/reference/components/{component_name}")
def reference_component(component_name):
    data = get_docs_metadata()
    component = data["components"].get(component_name)
    if not component:
        router.render_not_found()
        return

    tag = component.get("tag")

    with page():
        with hd.hbox(justify="space-between", align="center", wrap="wrap", gap=1):
            hd.markdown(f"# `{component_name}`")
            if tag:
                with hd.tooltip("The HTML tag of this component"):
                    if tag.startswith("sl-"):
                        hd.markdown(
                            f"[`<{tag}>`](https://shoelace.style/components/{tag[3:]})"
                        )
                    else:
                        hd.markdown(f"`<{tag}>`")

        if component["component_type"] == "class" and component["class_doc"]:
            if component["superclasses"]:
                hd.markdown(
                    "Inherits from:",
                    ", ".join(
                        f"[`{s}`](/reference/components/{s})"
                        for s in component["superclasses"]
                    ),
                    padding=0.5,
                    background_color="neutral-50",
                    border_radius="large",
                )

            docs_markdown(component["class_doc"])

        with hd.box(gap=2):
            if component["component_type"] == "class":
                hd.markdown("### Call Signature", margin_top=1)

            hd.code(component["sig"])

            if component["doc"]:
                docs_markdown(component["doc"])

            if component["component_type"] == "class":
                if component["props"]:
                    render_props(component["props"])
                if component["slots"]:
                    render_slots(component["slots"])
                if component["methods"]:
                    render_methods(component["methods"])


core_api = {
    "Top-Level Functions": ["run", "router", "index_page"],
    "Top-Level Decorators": [
        "cached",
        "global_state",
    ],
}

non_ui_components = {
    "System": [
        "state",
        "BaseState",
        "lifecycle",
        "scope",
        "task",
        "style",
    ],
    "Browser": [
        "window",
        "theme",
        "location",
        "clipboard",
        "local_storage",
    ],
}

ui_components = {
    "App Utilities": [
        "template",
        "navigation_menu",
        "theme_switcher",
        "icon_link",
    ],
    "Text": ["plaintext", "markdown", "code", "text", "h1", "h2", "h3", "h4", "h5"],
    "Lists": ["ordered_list", "list", "list_item", "box_list", "box_list_item"],
    "Navigation": ["nav", "link", "breadcrumb", "breadcrumb_item", "anchor"],
    "Layout": [
        "box",
        "card",
        "details",
        "divider",
        "split_panel",
        "tab_group",
        "tab",
        "tree",
        "tree_item",
        "carousel",
        "carousel_item",
    ],
    "Table": ["data_table", "table", "thead", "tbody", "tfoot", "tr", "td"],
    "Charts": [
        "line_chart",
        "bar_chart",
        "scatter_chart",
        "bubble_chart",
        "pie_chart",
        "polar_chart",
        "radar_chart",
        "cartesian_chart",
        "chart",
    ],
    "Overlays": ["drawer", "dialog", "dropdown", "popup"],
    "User Feedback": [
        "progress_bar",
        "progress_ring",
        "spinner",
        "alert",
        "badge",
        "tag",
        "tooltip",
    ],
    "Media": [
        "audio",
        "video",
        "media_source",
        "image",
        "image_comparer",
        "avatar",
        "icon",
        "icon_button",
    ],
    "Forms and Input": [
        "form",
        "button",
        "button_group",
        "textarea",
        "text_input",
        "checkbox",
        "switch",
        "radio_group",
        "radio",
        "radio_button",
        "radios",
        "radio_buttons",
        "slider",
        "select",
        "option",
        "color_picker",
    ],
    "Menus": [
        "menu",
        "menu_item",
        "menu_label",
    ],
    "Animation": ["animation", "keyframe"],
}


def render_menu(menu):
    for section_name, component_names in menu.items():
        with hd.scope(section_name):
            with hd.box(
                padding=1,
                gap=1,
                border="1px solid neutral-100",
                border_radius="large",
                background_color="neutral-50",
            ):
                hd.markdown(f"### {section_name}")
                hd.markdown(
                    " ".join(
                        [
                            f"[`{component_name}`](/reference/components/{component_name})"
                            for component_name in component_names
                        ]
                    )
                )


@router.route("/reference/components")
def components():
    with page() as p:
        p.title("# Hyperdiv API")

        with hd.box(gap=3):
            with hd.box(gap=1):
                hd.markdown(
                    """
                    ## Core API
                    """
                )

                render_menu(core_api)

            with hd.box(gap=1):
                hd.markdown(
                    """
                    ## State Components

                    Hyperdiv components that do not render
                    user-visible components in the browser. The
                    components in the "Browser" subsection provide
                    access to browser state in Python.

                    """
                )

                render_menu(non_ui_components)

            with hd.box(gap=1):
                hd.markdown(
                    """
                    ## UI Components

                    Hyperdiv components that render user-visible,
                    interactive UI components in the browser.
                    """
                )

                render_menu(ui_components)
