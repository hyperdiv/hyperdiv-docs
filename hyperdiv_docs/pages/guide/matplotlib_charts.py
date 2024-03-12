from ...router import router
from ...page import page
from ...code_examples import docs_markdown


@router.route("/guide/matplotlib-charts")
def matplotlib_charts():
    with page() as p:
        p.title("# Matplotlib Charts")

        docs_markdown(
            """

            Hyperdiv does not have a specific component for
            [Matplotlib](https://matplotlib.org) charts but a
            Matplotlib chart can be added to a Hyperdiv app by
            rendering the chart to image bytes and passing the bytes
            to the @component(image) component.

            """
        )

        p.heading("## Basic Use")

        docs_markdown(
            """

            ```py-nodemo
            import io
            import matplotlib
            import matplotlib.pyplot as plt
            import hyperdiv as hd

            matplotlib.use("Agg")

            def get_chart_image(fig):
                '''
                Renders the chart to png image bytes.
                '''
                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                buf.seek(0)
                image_bytes = buf.getvalue()
                buf.close()
                plt.close(fig)
                return image_bytes

            def main():
                # Create a chart:
                fig, ax = plt.subplots()
                ax.plot((1, 2, 3, 4), (10, 11, 12, 13))

                # Render the image bytes in the UI:
                hd.image(get_chart_image(fig), width=20)

            hd.run(main)
            ```

            Note that `matplotlib.use("Agg")` is important. It tells
            Matplotlib to run headless, without depending on a
            GUI. Without this setting, attempting to add a Matplotlib
            chart to Hyperdiv will fail.

            More on this [here](https://matplotlib.org/stable/users/explain/figure/backends.html#selecting-a-backend).

            """
        )

        p.heading("## Responding to Theme Mode")

        docs_markdown(
            """

            By default, Matplotlib chart images are rendered on white
            background. There's currently no easy way to match the
            chart's color scheme to Hyperdiv's theme exactly, but
            Matplotlib provides a basic way to render a chart in dark
            or light mode. We can then sync the chart's theme mode to
            Hyperdiv's theme mode.

            ```py-nodemo
            def main():
                theme = hd.theme()

                line_data = ((1, 2, 3, 4), (10, 11, 12, 13))

                if theme.is_dark:
                    # Render the matplotlib chart in dark mode:
                    with plt.style.context("dark_background"):
                        fig, ax = plt.subplots()
                        ax.plot(*line_data)
                else:
                    # Render it in light mode:
                    fig, ax = plt.subplots()
                    ax.plot(*line_data)

                # Render the image bytes in the UI:
                hd.image(get_chart_image(fig), width=20)
            ```

            """
        )

        p.heading("## Caching Chart Components with `@cached`")

        docs_markdown(
            """

            Using the pattern above, the chart will be re-created on
            every unrelated run of the app function. We can use the
            @component(cached) decorator to avoid re-creating the
            chart on every run.

            ```py-nodemo
            @hd.cached
            def chart():
                theme = hd.theme()

                line_data = ((1, 2, 3, 4), (10, 11, 12, 13))

                if theme.is_dark:
                    with plt.style.context("dark_background"):
                        fig, ax = plt.subplots()
                        ax.plot(*line_data)
                else:
                    fig, ax = plt.subplots()
                    ax.plot(*line_data)

                hd.image(get_chart_image(fig), width=20)

            def main():
                chart()

                state = hd.state(count=0)
                if hd.button("Click Me").clicked:
                    state.count += 1
                hd.text(state.count)
            ```

            In this example, when the app first loads, `chart()` is
            called and its resulting virtual DOM is cached.

            For demonstration, there's an unrelated click counter on
            the page. When we click the `Click Me` button, the app
            re-runs but the call to `chart()` does not re-run the
            `chart` function, and instead uses its cached virtual DOM.

            Also, when the theme mode is switched between light and
            dark, the `chart` function's dependency on theme mode will
            be invalidated and the function will re-run, rendering the
            chart in the new theme mode.

            """
        )

        p.heading("## Dynamically Updating Charts")

        docs_markdown(
            """

            We can re-create the chart on demand, with new data:

            ```py-nodemo
            @hd.cached
            def chart():
                theme = hd.theme()
                state = hd.state(
                    line_data=((1, 2, 3, 4), (10, 11, 12, 13))
                )

                if theme.is_dark:
                    with plt.style.context("dark_background"):
                        fig, ax = plt.subplots()
                        ax.plot(*state.line_data)
                else:
                    fig, ax = plt.subplots()
                    ax.plot(*state.line_data)

                hd.image(get_chart_image(fig), width=20)

                if hd.button("Update Chart").clicked:
                    state.line_data = ((1, 2, 3, 4), (5, 20, 8, 10))
            ```

            In this example, we store the chart's line data in
            @component(state). When the `Update Chart` button is
            clicked, an updated chart will be rendered.
            """
        )
