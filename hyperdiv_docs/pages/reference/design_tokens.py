import hyperdiv as hd
from hyperdiv.design_tokens import (
    Spacing,
    Shadow,
    BorderRadius,
    FontFamily,
    FontSize,
    FontWeight,
    LetterSpacing,
    LineHeight,
    Color,
)
from ...router import router
from ...page import page
from ...code_examples import docs_markdown

token_enums = [
    Spacing,
    Shadow,
    BorderRadius,
    FontFamily,
    FontSize,
    FontWeight,
    LetterSpacing,
    LineHeight,
    Color,
]


def render_token_enum(token_enum, example_fn):
    with page() as p:
        p.title(f"# {token_enum.__name__}")

        if token_enum.__doc__:
            hd.markdown(token_enum.__doc__)

        with hd.box(gap=1):
            for c in list(token_enum):
                with hd.scope(c.name):
                    with hd.hbox(
                        border_radius="medium",
                        align="center",
                    ):
                        hd.text(
                            f'"{c.value}"',
                            font_family="mono",
                            min_width=8,
                        )
                        with hd.box():
                            example_fn(c)


@router.route("/reference/design-tokens")
def design_tokens():
    with page() as p:
        p.title("# Design Tokens")

        docs_markdown(
            """
            Design tokens are sets of constants that can be used to style various
            aspects of a component.

            If a prop type includes the type
            [DesignToken](/reference/prop-types/DesignToken)(TokenEnum),
            it accepts values from the token enum TokenEnum.

            For example, if a prop type includes the type `DesignToken(Spacing)`,
            it will accept values like `"small"`, `"x-small"`, `"x-large"`, etc.

            Design tokens are enums exported by the `hyperdiv`
            module, and you can alternatively access the token values
            via the enum instead of using the string values.

            For example, in a prop with type `DesignToken(Color)`, you
            can pass either the string `"red-50"` or the enum field
            `hyperdiv.Color.red_50`. For values whose string starts
            with a number, for example `"2x-large"`, `"3x-large"` of
            @design_token(FontSize), the corresponding enum items are
            `FontSize.two_x_large`, `FontSize.three_x_large`, etc.
            """
        )

        with hd.box(gap=1):
            for klass in token_enums:
                with hd.scope(klass.__name__):
                    hd.link(
                        klass.__name__,
                        href=f"/reference/design-tokens/{klass.__name__}",
                        width="fit-content",
                    )


@router.route("/reference/design-tokens/Color")
def design_tokens_color():
    groups = {}

    for color in list(hd.Color):
        if "-" in color.value:
            name, num = color.value.split("-")
            groups.setdefault(name, [])
            groups[name].append(num)

    with page() as p:
        p.title("# Color")
        hd.markdown(hd.Color.__doc__)

        hd.markdown(
            """
            The table below lists the Hyperdiv colors and their variations.

            The first, numberless box represents the color without any
            variation specified. For example, `"red"` or
            `"primary"`. To get a variation on the color, you join its
            name and the variation number by a dash (`"-"`). For
            example `"red-100"`.

            Colors with unspecified variation, like `"red"` are
            typically equivalent to the `600` variation.
            """
        )

        for name, nums in groups.items():
            with hd.scope(name):
                with hd.hbox(gap=0.5):
                    hd.text(f'"{name}"', width=5, shrink=False, font_family="mono")
                    with hd.hbox(gap=0.5, wrap="wrap"):
                        hd.box(width=3, background_color=name, shrink=False)
                        for n in nums:
                            with hd.scope(n):
                                font_color = 900 if int(n) < 500 else 100
                                with hd.box(
                                    shrink=False,
                                    align="center",
                                    width=3,
                                    background_color=f"{name}-{n}",
                                    font_color=f"neutral-{font_color}",
                                ):
                                    hd.text(n, font_family="mono")


@router.route("/reference/design-tokens/Spacing")
def design_tokens_spacing():
    def example_fn(c):
        hd.box(width=c.value, height=c.value, background_color="primary")

    render_token_enum(Spacing, example_fn)


@router.route("/reference/design-tokens/Shadow")
def design_tokens_shadow():
    def example_fn(c):
        hd.box(
            width=3,
            height=3,
            background_color="neutral-50",
            shadow=c.value,
        )

    render_token_enum(Shadow, example_fn)


@router.route("/reference/design-tokens/BorderRadius")
def design_tokens_border_radius():
    def example_fn(c):
        hd.box(
            width=5,
            height=3,
            background_color="primary",
            border_radius=c.value,
        )

    render_token_enum(BorderRadius, example_fn)


@router.route("/reference/design-tokens/FontFamily")
def design_tokens_font_family():
    def example_fn(c):
        hd.text("This is some example text.", font_family=c.value)

    render_token_enum(FontFamily, example_fn)


@router.route("/reference/design-tokens/FontSize")
def design_tokens_font_size():
    def example_fn(c):
        hd.text("Hello!", font_size=c.value)

    render_token_enum(FontSize, example_fn)


@router.route("/reference/design-tokens/FontWeight")
def design_tokens_font_weight():
    def example_fn(c):
        with hd.box():
            hd.text("This is sans-serif text.", font_weight=c.value)
            hd.text("This is mono text.", font_family="mono", font_weight=c.value)
            hd.text("This is serif text.", font_family="serif", font_weight=c.value)

    render_token_enum(FontWeight, example_fn)


@router.route("/reference/design-tokens/LetterSpacing")
def design_tokens_letter_spacing():
    def example_fn(c):
        hd.text("This is some text.", letter_spacing=c.value)

    render_token_enum(LetterSpacing, example_fn)


@router.route("/reference/design-tokens/LineHeight")
def design_tokens_line_height():
    def example_fn(c):
        with hd.box(width=5):
            hd.text("Some text that wraps around.", line_height=c.value)

    render_token_enum(LineHeight, example_fn)
