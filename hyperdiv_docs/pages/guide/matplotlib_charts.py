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
                ax.plot([1, 2, 3, 4], [10, 11, 12, 13])

                # Render the image bytes in the UI:
                hd.image(get_chart_image(fig), width=20)
            ```

            Note that `matplotlib.use("Agg")` is important. It tells
            Matplotlib to run headless, without depending on a
            GUI. Without this setting, attempting to add a Matplotlib
            chart to Hyperdiv will fail.

            More on this [here](https://matplotlib.org/stable/users/explain/figure/backends.html#selecting-a-backend).

            """
        )

        p.heading("## Asynchronous Chart Creation with `task`")

        docs_markdown(
            """

            In the example above, The chart is re-created on every run
            of the app function. We can use a @component(task) to
            create the chart only once and cache its result:

            ```py-nodemo
            def get_chart():
                fig, ax = plt.subplots()
                ax.plot([1, 2, 3, 4], [10, 11, 12, 13])

                return get_chart_image(fig)

            def main():
                task = hd.task()
                task.run(get_chart)
                if task.result:
                    hd.image(task.result, width=20)
            ```

            In this example, the function `get_chart` is called only
            once and the image bytes are cached in `task.result`.

            """
        )

        p.heading("## Dynamically Updating Charts")

        docs_markdown(
            """

            We can also re-create a chart on demand, with new data.

            ```py-nodemo
            def get_chart(data):
                fig, ax = plt.subplots()
                ax.plot(*data)

                return get_chart_image(fig)

            def main():
                state = hd.state(
                    chart_data=([1, 2, 3, 4], [10, 11, 12, 13])
                )

                task = hd.task()
                task.run(get_chart, state.chart_data)
                if task.result:
                    hd.image(task.result, width=20)

                if hd.button("Update Chart").clicked:
                    state.chart_data = ([1, 2, 3, 4], [5, 20, 8, 10])
                    task.clear()
            ```

            In this example, we store the chart's line data in
            @component(state). When the `Update Chart` button is
            clicked, we update the chart data and clear the task. The
            task will then re-run with the new chart data, and an
            updated chart will be rendered.

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
            def get_chart(data, is_dark):
                if is_dark:
                    with plt.style.context("dark_background"):
                        fig, ax = plt.subplots()
                        ax.plot(*data)
                else:
                    fig, ax = plt.subplots()
                    ax.plot(*data)

                return get_chart_image(fig)

            def main():
                theme = hd.theme()
                task = hd.task()
                task.run(
                    get_chart,
                    ([1, 2, 3, 4], [5, 20, 8, 10]),
                    # Pass the current theme mode to the task:
                    theme.is_dark
                )

                if task.result:
                    hd.image(task.result, width=20)

                # When the Hyperdiv theme changes, re-render the chart
                # in the new theme mode:
                if theme.changed:
                    task.clear()
            ```

            """
        )
