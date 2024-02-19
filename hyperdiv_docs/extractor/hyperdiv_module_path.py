import os
import pathlib


def get_hyperdiv_module_path():
    """
    We assume that the `hyperdiv` repo exists alongside the
    `hyperdiv-docs` repo.
    """
    return (
        pathlib.Path(os.path.dirname(__file__))
        / ".."
        / ".."
        / ".."
        / "hyperdiv"
        / "hyperdiv"
    ).resolve()
