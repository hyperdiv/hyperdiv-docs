import hyperdiv as hd
from ...router import router
from ...page import page


@router.route("/guide/deploying")
def deploying():
    with page() as p:

        p.title("# Deploying Hyperdiv")

        p.heading("## Deploying as a local tool")

        hd.markdown(
            """

            A Hyperdiv app can be deployed as a local tool, that runs
            locally on the user's computer and automatically opens in
            a browser tab. This approach can be used to for example
            ship a Hyperdiv UI with a Python tool that is
            `pip`-installable.

            In this approach we want to set the `HD_PRODUCTION_LOCAL`
            to `"1"`, so when the app runs, it automatically chooses
            an open port and opens a browser tab when invoked. (See
            [Environment Variables](/reference/env-variables)).

            Suppose you deploy a tool on PyPI whose code bundle
            structure looks like:

            ```
            my_tool/
                my_hyperdiv_app/
                    start.py
                    ...other app code...
                launch.py
                ...
            ```

            Then `launch.py` could look like this:

            ```py
            import os
            import shutil

            def launch_app():
                app_path = os.path.join(
                    os.path.dirname(__file__),
                    "my_hyperdiv_app",
                    "start.py"
                )
                python = shutil.which("python3")
                os.environ["HD_PRODUCTION_LOCAL"] = "1"
                os.execl(python, "python", app_path)
            ```

            Then, you can point your packaging system's config to
            automatically convert this function into a command-line
            tool. For example, using
            [`console_scripts`](https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html#the-console-scripts-entry-point)
            in `setuptools` or Poetry
            [`scripts`](https://python-poetry.org/docs/pyproject/#scripts).

            For reference, Hyperdiv itself provides a command-line
            tool called `hyperdiv` based on
            [Click](https://click.palletsprojects.com/). Its
            implementation is
            [here](https://github.com/hyperdiv/hyperdiv/blob/main/hyperdiv/cli.py)
            and its Poetry `scripts` config is
            [here](https://github.com/hyperdiv/hyperdiv/blob/main/pyproject.toml). See
            the `[tool.poetry.scripts]` section.

            """
        )

        with hd.alert(opened=True):
            hd.markdown(
                """

                Note that on Windows, this strategy using `os.execl`
                may not work as expected. See
                https://bugs.python.org/issue9148. Instead, you may
                have to use
                [Popen](https://docs.python.org/3/library/subprocess.html)
                and maintain a subprocess.

                """
            )

        p.heading("## Deploying on the web or local network")

        hd.markdown(
            """

            A Hyperdiv app can be deployed as a web app on the world
            wide web or a host on a local network.

            Suppose you have a host `foo.com` and want to deploy a
            Hyperdiv app there.

            """
        )

        p.heading("### Simplest Case")

        hd.markdown(
            """

            In the simplest case, you can just install Hyperdiv on the
            host and run an app there, on a port of your choice:

            ```
            $ HD_PORT=9000 python my-app.py
            ```

            Then, provided that port `9000` is open externally, you
            can navigate to `http://foo.com:9000` to use the
            app, and share this URL with users.

            """
        )

        p.heading("### Using Nginx as a Reverse Proxy")

        hd.markdown(
            """

            In the case above, The Hyperdiv app does not support TLS,
            so traffic is unencrypted. This may be ok when deploying
            Hyperdiv on a local, private network.

            A more robust setup uses a reverse-proxy like Nginx to
            terminate TLS and forward traffic to the actual Hyperdiv
            app. In this setup, you can also run the Hyperdiv app in
            multiple processes, on multiple ports, and let Nginx play
            the role of a load balancer, forwarding user connections
            to one of the available Hyperdiv processes.

            """
        )

        p.heading("#### Nginx Config")

        hd.markdown(
            """

            Here's a basic Nginx config that sets up the Hyperdiv app
            on `my-app.foo.com`:

            ```nginx
            server {
                server_name my-app.foo.com;
                listen 80;

                location / {
                    proxy_pass http://my-hyperdiv-app;
                    proxy_http_version 1.1;
                    proxy_set_header Host $http_host;
                    proxy_set_header X-Real-IP $remote_addr;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header X-Forwarded-Proto $scheme;

                    proxy_connect_timeout 3600;
                    proxy_send_timeout 3600;
                    proxy_read_timeout 3600;
                }

                # Websocket config:
                location /ws {
                    proxy_pass http://my-hyperdiv-app;
                    proxy_http_version 1.1;
                    proxy_set_header Host $http_host;
                    proxy_set_header X-Real-IP $remote_addr;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header X-Forwarded-Proto $scheme;

                    proxy_connect_timeout 3600;
                    proxy_send_timeout 3600;
                    proxy_read_timeout 3600;

                    proxy_set_header Upgrade $http_upgrade;
                    proxy_set_header Connection "Upgrade";
                }
            }

            upstream my-hyperdiv-app {
                server 127.0.0.1:9000 max_fails=0;
            }
            ```

            In this setup, the Hyperdiv app runs on port `9000`, Nginx
            runs on port `80`, and Nginx forwards connections to the
            app.

            You can run the Hyperdiv app in multiple processes on
            multiple ports and let Nginx play the role of a load
            balancer, forwarding a new user connection to one of the
            processes:

            ```nginx
            upstream my-hyperdiv-app {
                server 127.0.0.1:9000 max_fails=0;
                server 127.0.0.1:9001 max_fails=0;
                server 127.0.0.1:9002 max_fails=0;
                server 127.0.0.1:9003 max_fails=0;
            }
            ```

            """
        )

        p.heading("#### TLS Setup")

        hd.markdown(
            """

            For a basic TLS setup, using
            [Certbot](https://certbot.eff.org) is recommended. After
            setting up the Nginx config, Certbot will automatically
            modify your config to listen on port 443 with valid TLS
            certificates.

            """
        )

        p.heading("### Using Supervisor")

        hd.markdown(
            """

            To manage the Hyperdiv processes of the app running behind
            Nginx, using [Supervisor](http://supervisord.org) is
            recommended. Supervisor monitors the running processes and
            restarts them if they crash, captures their logs, and
            offers a command-line interface for bulk-starting/stopping
            the processes.

            Suppose user `bob` is deploying an app called `my-app` on
            Linux. The app's code will be stored in
            `/home/bob/apps/my-app`. This directory will have the
            following structure:

            ```
            my-app/
                start.py
                start.sh
                ... other app code ...
                logs/
            ```

            `start.py` is the app's entrypoint, that you'd normally
            run with `python start.py` to run your app.

            `start.sh` is a script that enters the virtualenv in which
            Hyperdiv is you installed, and then executes the app's
            script:

            ```sh
            # start.sh
            source {path to virtualenv}/bin/activate
            exec python start.py
            ```

            If you're using Pyenv and installed Hyperdiv in a Pyenv
            virtualenv called `"hyperdiv-env"`, the script would be:

            ```sh
            # start.sh
            pyenv activate hyperdiv-env
            exec python start.py
            ```

            Then, here's a Supervisor config for this setup:

            ```ini
            [program:my-app]
            process_name=my-app
            numprocs=1
            command=/bin/bash /home/bob/apps/my-app/start.sh
            directory=/home/bob/apps/my-app
            environment=HD_PRODUCTION=1,HD_PORT=9000
            startretries=3
            stopasgroup=true
            killasgroup=true
            stderr_logfile=/home/bob/apps/my-app/logs/err.log
            stdout_logfile=/home/bob/apps/my-app/logs/out.log
            user=bob
            autostart=true
            autorestart=true
            ```

            This config runs the app in a single process on port
            `9000` and captures its output in `logs/err.log` and
            `logs/out.log` inside the app directory.


            """
        )

        p.heading("#### Multiple Processes")

        hd.markdown(
            """

            We can make minor modifications to the config to make
            Supervisor spawn multiple processes on different ports:

            ```ini
            [program:my-app]
            process_name=my-app-%(process_num)s
            numprocs=4
            command=/bin/bash /home/bob/apps/my-app/start.sh
            directory=/home/bob/apps/my-app
            environment=HD_PRODUCTION=1,HD_PORT=900%(process_num)s
            startretries=3
            stopasgroup=true
            killasgroup=true
            stderr_logfile=/home/bob/apps/my-app/logs/err.log
            stdout_logfile=/home/bob/apps/my-app/logs/out.log
            user=bob
            autostart=true
            autorestart=true
            ```

            These are the modified lines:

            ```ini
            process_name=my-app-%(process_num)s
            numprocs=4
            environment=HD_PRODUCTION=1,HD_PORT=900%(process_num)s
            ```

            In this config, we tell supervisor to start and maintain 4
            processes running the app, and use the `%(process_num)s`
            Supervisor variable to give unique names and ports to each
            process. The `%(process_num)s` variable starts at `0` and
            increments by `1` with each added process.

            In this case, the app will run in 4 processes on ports
            `9000`, `9001`, `9002`, `9003`. Using the Nginx config
            above, with Certbot set up, we can access our app at
            `https://my-app.foo.com`, and Nginx will round-robin
            incoming connections into one of the four underlying
            processes.

            """
        )
