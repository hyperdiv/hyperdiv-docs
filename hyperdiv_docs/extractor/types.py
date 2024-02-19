import inspect
import importlib
import hyperdiv
from .dirutils import get_modules_recursively
from .hyperdiv_module_path import get_hyperdiv_module_path


def get_types():
    """
    Returns a dict type_name -> type of all Hyperdiv types, by
    dynamically importing all the relevant Hyperdiv modules, iterating
    over their variables, and collecting the ones with type
    HyperdivType.
    """

    types = dict()

    hyperdiv_path = get_hyperdiv_module_path()

    modules = (
        get_modules_recursively(
            hyperdiv_path / "component_mixins",
            "hyperdiv.component_mixins",
        )
        + get_modules_recursively(
            hyperdiv_path / "prop_types",
            "hyperdiv.prop_types",
        )
        + get_modules_recursively(
            hyperdiv_path / "components",
            "hyperdiv.components",
        )
    )

    for module_string in modules:
        m = importlib.import_module(module_string)
        for name, typ in sorted(vars(m).items()):
            if isinstance(typ, hyperdiv.prop_types.HyperdivType):
                types[name] = typ
            elif (
                inspect.isclass(typ)
                and issubclass(typ, hyperdiv.prop_types.HyperdivType)
                and not typ.__name__.endswith("Def")
            ):
                types[name] = typ

    return types
