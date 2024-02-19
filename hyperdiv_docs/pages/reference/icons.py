import hyperdiv as hd
from hyperdiv.icons import icon_names as hyperdiv_icon_names
from ...router import router
from ...page import page
from ...code_examples import docs_markdown


@router.route("/reference/icons")
def icons():
    per_page = 100
    s = hd.state(page=0)

    with page() as p:
        p.title("# Icons")

        docs_markdown(
            """
            The following is the list of icons available to a Hyperdiv
            app. A prop with type @prop_type(Icon) will accept an icon's
            name as a string. The most common use of icons is via
            the [icon](/reference/components/icon) and
            [icon_button](/reference/components/icon_button)
            components, which you can use to render an icon by
            calling `icon(icon_name)` or `icon_button(icon_name)`.

            Hover over an icon to see its name in a tooltip. Click
            the icon to copy its name to the clipboard.

            Use the search box to narrow to the list of icons whose names
            match the search text.
            """
        )

        with hd.hbox(gap=1, wrap="wrap"):
            search_box = hd.text_input(
                clearable=True,
                prefix_icon="search",
                grow=10,
            )
            icon_family = hd.select(
                options=("Outline", "Solid", "All Icons"),
                value="Outline",
                grow=1,
            )

        if search_box.changed:
            s.page = 0

        if icon_family.changed:
            s.page = 0

        icon_names = [
            icon_name
            for icon_name in hyperdiv_icon_names
            if search_box.value in icon_name
            and (
                "fill" in icon_name
                if icon_family.value == "Solid"
                else "fill" not in icon_name
                if icon_family.value == "Outline"
                else True
            )
        ]

        num_pages = (len(icon_names) / per_page) - 1
        low = s.page * per_page
        high = min(len(icon_names), (s.page + 1) * per_page)

        with hd.hbox(wrap="wrap"):
            for icon_name in icon_names[low:high]:
                with hd.scope(icon_name):
                    with hd.tooltip(icon_name) as tooltip:
                        if hd.icon_button(
                            icon_name,
                            cursor="pointer",
                            padding=0.5,
                            font_size=1.5,
                            font_color="neutral-800",
                        ).clicked:
                            hd.clipboard().write(icon_name)
                            tooltip.content = "Copied!"
                            tooltip.reset_prop_delayed("content", 1)

        with hd.hbox(justify="space-between", align="center"):
            with hd.button(disabled=s.page <= 0) as prev_button:
                hd.icon("chevron-left")
            if prev_button.clicked:
                s.page -= 1

            hd.text(f"{s.page+1}/{(len(icon_names)//per_page)+1}")

            with hd.button(disabled=s.page >= num_pages) as next_button:
                hd.icon("chevron-right")
            if next_button.clicked:
                s.page += 1
