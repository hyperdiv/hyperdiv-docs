from ...router import router
from ...page import page
from ...code_examples import code_example, docs_markdown


@router.route("/guide/tasks")
def tasks():
    with page() as p:

        p.title("# Asynchronous Tasks")

        docs_markdown(
            """

            When you start Hyperdiv with `hyperdiv.run(main)`,
            Hyperdiv will begin running and re-running `main()` over
            and over as props change. The calls to `main()` are
            scheduled *synchronously*, meaning the next call to
            `main()` won't happen until the previous call finished.

            This is a nice property because you don't have to worry
            about concurrent calls to `main()` causing data races.

            But the app function will likely need to perform I/O calls
            to the network or filesystem. Sometimes it may be fine to
            make those calls directly and let them re-run
            synchronously. For example if accessing a local Sqlite
            database, the latency may be imperceptible.

            But if a call has to block on I/O for a significant amount
            of time, or is otherwise slow, that call will introduce
            perceptible latency, causing the UI to feel sluggish.

            To address this, Hyperdiv provides an *asynchronous task
            functions* interface, allowing special functions to be run
            in the background, without blocking the `main()` thread.

            """
        )

        p.heading("## Launching One-Time Tasks")

        code_example(
            """
            import time
            import hyperdiv as hd

            def slow_function(state):
                time.sleep(3)
                state.count += 1

            def main():
                state = hd.state(count=0)
                hd.text(state.count)

                task = hd.task()

                if hd.button(
                    "Slow Increment",
                    disabled=task.running
                ).clicked:
                    task.rerun(slow_function, state)

                if hd.button("Fast Increment").clicked:
                    state.count += 1

            hd.run(main)
            """,
            code_to_execute=(
                """
                def slow_function(state):
                    import time
                    time.sleep(3)
                    state.count += 1

                state = hd.state(count=0)
                hd.text(state.count)

                task = hd.task()

                if hd.button(
                    "Slow Increment",
                    disabled=task.running
                ).clicked:
                    task.rerun(slow_function, state)

                if hd.button("Fast Increment").clicked:
                    state.count += 1
                """
            ),
        )

        docs_markdown(
            """

            The example above uses @component(task) to create a task
            component, and when you click the "Slow Increment" button,
            it calls `task.rerun(slow_function, state)`, which
            launches a call `slow_function(state)` in the
            background. After 3 seconds, the call increments
            `state.count`, which causes the UI to update with the new
            count.

            In that example, we also use the task's `running` prop to
            disable the button while the task is running, preventing
            the launching of multiple concurrent `slow_function`
            calls.

            Note that after you click "Slow Increment", while the
            button is disabled, you can freely click "Fast Increment"
            and the UI updates immediately, showing that tasks don't
            block the UI.

            """
        )

        p.heading("## Locking")

        docs_markdown(
            """

            Concurrent writes to any prop are serialized by using an
            internal lock. In the previous example, the write
            performed by the task and the write performed when you
            click "Fast Increment" may happen concurrently, and those
            writes are automatically serialized.

            You may need explicit locking if you need coarser
            granularity serialization.

            """
        )

        p.heading("## Read Tasks")

        docs_markdown(
            """

            The previous example shows how to run a one-time task in
            response to an event, in this case `clicked`.

            Another core use of task is for slow reads. For example,
            running a heavy database query:

            """
        )

        code_example(
            """
            import asyncio
            import hyperdiv as hd

            async def get_users():
                await asyncio.sleep(2)
                return ((0, "Amy"), (1, "John"))

            def main():
                users_task = hd.task()
                users_task.run(get_users)

                if users_task.running:
                    hd.spinner()
                elif users_task.done:
                    for user_id, user_name in users_task.result:
                        with hd.scope(user_id):
                            hd.text(user_name)

                if hd.button("Reload").clicked:
                    users_task.clear()

            hd.run(main)
            """,
            code_to_execute=(
                """
                async def get_users():
                    import asyncio
                    await asyncio.sleep(1)
                    return ((0, "Amy"), (1, "John"))

                users_task = hd.task()
                users_task.run(get_users)
                if users_task.running:
                    hd.spinner()
                elif users_task.done:
                    for user_id, user_name in users_task.result:
                        with hd.scope(user_id):
                            hd.text(user_name)

                if hd.button("Reload").clicked:
                    users_task.clear()
                """
            ),
        )

        docs_markdown(
            """

            In the example above, we use `run` to launch the function
            performing a slow read. Then, we check its state using the
            `running` and `done` props. If the task is still running,
            we render a loading spinner. When the function call is
            done running, its return value will be stored in the
            task's `result` prop. We can then render the users list.

            Once a task is done running, the return value of the
            function will remain cached in `result`, and the task will
            stay in `done` state. As Hyperdiv re-runs the `main`
            function, the task *does not* rerun.

            To cause the task to re-run, we call `clear()`. This will
            reset the task's `done` and `running` props, causing
            Hyperdiv to re-run the app function, which then causes the
            task to run again.

            Also note that @component(task) supports both normal
            Python functions as well as `async def` functions.

            """
        )

        p.heading("## Very Long-Running Tasks")

        docs_markdown(
            """

            You can launch tasks that run indefinitely. A task may,
            for example, listen to some external I/O channel, and when
            that channel is updated, the task updates a prop with new
            data.

            A potential issue with indefinitely-running tasks is that
            they should exit when the user closes the browser
            connection to the app. If they don't exit, they may cause
            memory leaks and prevent Hyperdiv from shutting down
            cleanly.

            One way for indefinite tasks to exit cleanly is to use the
            `app_stopped` prop of @component(lifecycle):

            ```py-nodemo
            def my_long_task(state):
                while True:
                    # Exit the task
                    if state.stopped:
                        break
                    # Otherwise, listen for external I/O data
                    # and update a prop if there's any new data.
                    result = listen_to_external_io(timeout=0.5)
                    if result:
                        state.my_prop = result

            def main():
                state = hd.state(stopped=False, my_prop=None)
                lifecycle = hd.lifecycle()
                if lifecycle.app_stopped:
                    # Tell the task to exit
                    state.stopped = True
                ...
            ```

            This hypothetical task function runs an infinite loop that
            listens to some external I/O, and if there is any data, it
            updates a prop. In the same loop, it checks
            `state.stopped` periodically and exits shortly after
            `state.stopped` is set to `True` by the app function.

            The `app_stopped` prop of @component(lifecycle) is an
            event prop, set to `True` for one run when the user has
            closed the associated browser connection, or when Hyperdiv
            has been signaled to shut down.

            """
        )

        p.heading("## Guidelines")

        docs_markdown(
            """

            When you need to launch a task in response to an event,
            every time the event happens, use `task.rerun(slow_fn)`
            when that event happens.

            When you need to read and cache the result of a heavy
            call, use `task.run(slow_fn)` and inspect the task's props
            to determine when the call is done. And then use
            `task.clear()` to cause the task to re-run when
            appropriate.

            """
        )
