import inspect
import hyperdiv as hd
from hyperdiv.prop_types import HyperdivType
from .extractor import Extractor


def extract():
    """
    Extracts metadata from the Hyperdiv repo, which is used to
    dynamically render the docs components and prop types pages.
    """

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

    return ctx.output
