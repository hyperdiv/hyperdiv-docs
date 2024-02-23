import hyperdiv as hd
from ...router import router
from ...page import page
from ...code_examples import docs_markdown


@router.route("/reference/env-variables")
def env_variables():
    with page() as p:
        p.title("# Environment Variables")

        docs_markdown(
            """

            Hyperdiv's behavior can be controlled with the following
            environment variables.

            With the exception of `HD_HOST` and `HD_PORT`, these
            environment variables are all boolean variables and take
            the values `"1"` or `"true"`, or `"0"` or `"false"`. `"0"`
            or `"false"` is equivalent to leaving the environment
            variable unset.

            """
        )

        p.heading("## Core Config")

        docs_markdown(
            """

            ### `HD_HOST`

            This environment variable allows setting the host that a
            Hyperdiv app runs on. The value should be a string
            representing a valid IP address or hostname, e.g.
            `"0.0.0.0"` (default value=`"localhost"`).

            ### `HD_PORT`

            This environment variable allows setting the port that a
            Hyperdiv app runs on. The value should be an integer in
            valid port range, e.g. `8000`.

            ### `HD_PRODUCTION`

            When set to a true value, this environment disables "debug
            mode" in the internal Tornado server, which normally
            watches for file changes and auto-reloads the app when a
            dependent file is modified, and limits logging output.

            Setting this environment variable causes all the
            environment variables in the [Development
            Mode](#development-mode) section below to be ignored,
            regardless of their values.

            ### `HD_PRODUCTION_LOCAL`

            Works exactly like `HD_PRODUCTION` but in addition:

            1. It causes @component(run) to automatically open a
               browser tab with the app running in it.

            2. Hyperdiv automatically finds an open port on which to
               run the app when `HD_PORT` is left unset. The port
               search starts and `8988` and goes upward.

            This environment variable is meant to be set when shipping
            apps that users can run locally on their computers. For
            example, when distributing an app on
            [PyPI](https://pypi.org).

            """
        )

        p.heading("## Development Mode")

        docs_markdown(
            """

            These environment variables are useful when developing
            Hyperdiv itself, and may be useful when improving the
            performance of apps.

            ### `HD_DEBUG`

            When set, this environment variable causes Hyperdiv to log
            a lot of debugging statements, useful when developing
            Hyperdiv itself. This output may be inscrutible to
            developers who aren't working on Hyperdiv itself.

            Automatically disabled if `HD_PRODUCTION` is enabled.

            ### `HD_PRINT_OUTPUT`

            Causes Hyperdiv to log each message sent to the
            browser. Note that some of these messages can be very
            large. In particular, when connecting to an app, the
            entire dom is logged to the console.

            Automatically disabled if `HD_DEBUG` is disabled.

            """
        )

        p.heading("## Setting Environment Variables")

        docs_markdown(
            """

            In bash-like shells, you can set environment variables like this:

            ```sh
            export HD_PORT=9000
            export HD_PRODUCTION=1
            python app.py
            ```

            Using `export` will set the environment variable for the
            rest of the terminal session, or until set again.

            You can also set the variable for a single execution of
            the app, without exporting it to the session.

            ```sh
            HD_PORT=9000 HD_PRODUCTION=1 python start.py
            ```

            In non-bash-like shells, you can use `setenv`, which works
            like the `export` command from bash-like shells:

            ```sh
            setenv HD_PORT 9000
            setenv HD_PRODUCTION 1
            python app.py
            ```

            """
        )
