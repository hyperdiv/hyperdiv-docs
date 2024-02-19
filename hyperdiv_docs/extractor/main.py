import os
import json
import inspect
import pathlib
import hyperdiv as hd
from hyperdiv.prop_types import HyperdivType
from .extractor import Extractor

extracted = None
json_path = pathlib.Path(os.path.dirname(__file__), "extracted.json")


def extract():
    """
    Extracts metadata from the Hyperdiv repo, which is used to
    dynamically render the docs components and prop types pages.

    If a json file exists at `json_path`, this function will load that
    json file. If not, it creates an Extractor and extracts docs
    metadata from the hyperdiv repo, starting with all the components
    and types exported by hyperdiv at the top level.

    The output is cached in the global variable `extracted` and
    returned on subsequent calls.
    """
    global extracted

    # If globally cached, return.
    if extracted:
        return extracted

    # If the json file exists, load it, cache it, and return.
    if json_path.exists():
        with open(json_path) as f:
            extracted = json.loads(f.read())
            return extracted

    # Otherwise extract metadata from the Hyperdiv repo.
    ctx = Extractor()

    # Iterate over all the attributes exported by `hyperdiv`
    for name, attr in vars(hd).items():
        # Skip internal attributes and modules
        if name.startswith("__") or inspect.ismodule(attr):
            continue

        # If it's a type, extract the type.
        is_type = False

        try:
            if isinstance(attr, HyperdivType):
                is_type = True
        except Exception:
            pass

        try:
            if issubclass(attr, HyperdivType):
                is_type = True
        except Exception:
            pass

        if is_type:
            ctx.extract_prop_type(attr, toplevel=True)
            continue

        # Skip definitions like hbox, vbox which are functools.partial
        # aliases.
        try:
            attr.__name__
        except AttributeError:
            continue

        # The rest of the attributes must be component classes or
        # functions.
        ctx.extract_component(attr)

    # Extract all the types in Hyperdiv
    for typ in ctx.types.values():
        ctx.extract_prop_type(typ)

    # Cache the output
    extracted = ctx.output
    return extracted


def create_json_file():
    """
    (Re)-creates the stored JSON file containing docs metadata.
    """
    if os.path.exists(json_path):
        os.unlink(json_path)
    data = extract()
    with open(json_path, "w") as f:
        f.write(json.dumps(data, indent=2))
