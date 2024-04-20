import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import docs_markdown


@router.route("/extending-hyperdiv/new-components")
def new_components():
    with page() as p:
        p.title("# Creating New Components")

        docs_markdown(
            """

            In addition to being able to extend existing components
            with custom CSS props, you can create simple components
            targeting HTML tags that are currently unsupported by core
            Hyperdiv. Note that this technique only works when you
            don't need to run custom Javascript. If you need custom
            Javascript, build a [plugin](/extending-hyperdiv/plugins).

            For example, Hyperdiv does not include a built-in
            [`iframe`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe)
            component, but we can create one:

            ```py
            class iframe(hd.Component, hd.Styled):
                _tag = "iframe"

                src = hd.Prop(hd.PureString)

            iframe(
                src="/assets/iframe-example.html",
                border="1px solid neutral",
                height=10,
            )
            ```

            We create a new component by inheriting from Hyperdiv's
            component base class, @component(Component). Hyperdiv
            expects a component's HTML tag to be set using the `_tag`
            class variable. In this case the tag is `iframe`, causing
            Hyperdiv to render this component in the browser using an
            `<iframe>` tag.

            In the example above, we also inherit from
            @component(Styled), allowing us to use style props to
            style the outer `<iframe>` container with style props like
            `width` and `border`.

            Iframes work by loading a web page specified by the `src`
            attribute, so we define a string prop named `src`.

            The example above will be rendered in the browser as:

            ```html
            <iframe id="..." src="/assets/iframe-example.html"></iframe>
            ```

            Obviously, additional props can be defined, targeting
            additional HTML attributes supported by `iframe`.

            """
        )
