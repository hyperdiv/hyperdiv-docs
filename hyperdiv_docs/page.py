from functools import cache
import re
import contextlib
import hyperdiv as hd


def make_anchor(s):
    """Makes a hash link name from a heading name."""
    return re.sub(r"[^a-zA-Z0-9]+", "-", s.lower())


class Heading:
    """
    Renders a heading with an anchor and a link button that copies
    that anchor location to the clipboard when clicked.
    """

    def __init__(self, title):
        self.level = 0
        for i, char in enumerate(title):
            if char == "#":
                self.level += 1
            else:
                break

        self.title = title[i:].strip()
        self.anchor = make_anchor(self.title)

        with hd.box():
            hd.anchor(self.anchor)
            with hd.hbox(gap=0.5, align="center", padding_top=2):
                hd.markdown(title, font_color="blue")
                with hd.tooltip("Copy Link") as tooltip:
                    if hd.icon_button("link").clicked:
                        # When the `copy link` button is clicked, copy
                        # the full location, including the anchor
                        # hash, into the clipboard.
                        loc = hd.location()
                        url = f"{loc.protocol}//{loc.host}{loc.path}#{self.anchor}"
                        hd.clipboard().write(url)
                        tooltip.content = "Copied!"
                        tooltip.set_prop_delayed("content", "Copy Link", 1)


class HeadingsCollector:
    """
    A collector of headings. Used to render the `On This Page`
    section.
    """

    def __init__(self):
        self.page_title = None
        self.headings = []

    def heading(self, h):
        self.headings.append(Heading(h))

    def title(self, t):
        self.page_title = t


@contextlib.contextmanager
def page():
    """
    The base "page" abstraction in this documentation app. It yields a
    `HeadingsCollector` that can be used to render and simultaneously
    collect headings, which are then used to render the "On This Page"
    section responsively.

    It also automatically renders prev and next links at the bottom of
    the content box.
    """
    window = hd.window()
    wide = window.width > 1400
    headings_collector = HeadingsCollector()

    # Yield the collector in a delayed content box, to be rendered
    # later. During this phase, the caller can render any components
    # into the content box, as well as call `.title()` and
    # `.heading()` on the collector to simultaneously render and
    # collect headings.
    with hd.box(collect=False, gap=2) as content_box:
        yield headings_collector

    # Render the "On This Page" section, but do not collect it yet.
    if len(headings_collector.headings) > 0:
        with hd.box(
            background_color="neutral-50",
            border="1px solid neutral-100",
            border_radius="large",
            padding=1,
            gap=1,
            font_size=0.9,
            collect=False,
            height="fit-content",
            shrink=0,
        ) as on_this_page:
            hd.text("On This Page", font_weight="bold")

            with hd.box():
                for h in headings_collector.headings:
                    with hd.scope(h.anchor):
                        with hd.hbox(
                            gap=0.3,
                            padding=(0, 0, 0, h.level - 2),
                        ):
                            hd.markdown("&bullet;")
                            with hd.link(
                                href=f"#{h.anchor}",
                                width="fit-content",
                            ):
                                hd.markdown(h.title)

    if wide and len(headings_collector.headings) > 0:
        # When the window is wide, render a horizontal box with two
        # children, with the content box on the left, and the "On This
        # Page" box on the right.
        with hd.hbox(vertical_scroll=False):
            with hd.box(gap=2, padding=(4, 2, 2, 2), vertical_scroll=True):
                if headings_collector.page_title:
                    hd.markdown(headings_collector.page_title)
                content_box.collect()
                render_prev_and_next_links()
            with hd.box(width=14, shrink=0, padding=(4, 2, 2, 0)):
                on_this_page.collect()
    else:
        # When the window is narrow, render a single vertical box
        # containing the title, followed by the "On This Page"
        # section, followed by the content box.
        with hd.box(gap=2, padding=(4, 2, 2, 2)):
            if headings_collector.page_title:
                hd.markdown(headings_collector.page_title)
            if len(headings_collector.headings) > 0:
                on_this_page.collect()
            content_box.collect()
            render_prev_and_next_links()


@cache
def get_flat_menu():
    from .menu import menu

    flat_menu = []

    for section, links in menu.items():
        for link_name, info in links.items():
            flat_menu.append((section, link_name, info))

    return flat_menu


def get_prev_and_next_links():
    """
    Compute the prev and next navigation links, relative to the
    current location, from the navigation menu data structure.
    """
    flat_menu = get_flat_menu()

    loc = hd.location()

    for i in range(len(flat_menu)):
        _, _, info = flat_menu[i]
        if info["href"] == loc.path:
            if i == 0:
                return (None, flat_menu[i + 1])
            elif i == len(flat_menu) - 1:
                return (flat_menu[i - 1], None)
            else:
                return (flat_menu[i - 1], flat_menu[i + 1])

    return None, None


def link_box(section, title, href, prev=True):
    """
    Render a prev or a next link box. If `prev` is `True` it renders a
    prev box, otherwise a next box.
    """
    w = hd.window()
    with hd.link(href=href, grow=1, basis=0, cursor="pointer", font_color="neutral"):
        with hd.hbox(
            background_color="neutral-50",
            border_radius=(0.5, 0.5, 0, 0),
            padding=(0.3, 0.9, 0.1, 0.9),
            font_size=0.7,
            font_weight="bold",
            align="center",
            justify=("start" if prev else "end"),
            gap=0.4,
        ):
            if prev:
                hd.icon("arrow-left")
                hd.text("PREVIOUS SECTION")
            else:
                hd.text("NEXT SECTION")
                hd.icon("arrow-right")
        with hd.box(
            grow=1,
            border="1px solid neutral-50",
            border_radius=(0, 0, 0.5, 0.5),
            padding=(0.5, 0.9, 0.5, 0.9),
            align=("start" if prev else "end"),
            font_size=0.7 if w.width < 700 else None,
        ):
            hd.text(section, font_weight="light")
            hd.text(title, text_align=("start" if prev else "end"), font_weight="bold")


def render_prev_and_next_links():
    """
    Renders the prev and next link boxes, side by side.
    """
    prev_link, next_link = get_prev_and_next_links()

    if prev_link or next_link:
        with hd.hbox(gap=1, padding=(2, 0, 2, 0)):
            if prev_link:
                (section, title, info) = prev_link
                link_box(section, title, info["href"])
            if next_link:
                (section, title, info) = next_link
                link_box(section, title, info["href"], prev=False)
