import inspect
from black import format_str, FileMode
from hyperdiv.component_base import Component
from hyperdiv.prop import Prop
from hyperdiv.prop_types import (
    HyperdivType,
    CSS,
    Optional,
    Union,
    OneOf,
    DesignToken,
    Event,
    List,
    CSSField,
    ClampedNumber,
    ClampedInt,
    ClampedFloat,
    Constant,
    Native,
    OneOrMoreOf,
)
from hyperdiv.style_part import StylePart
from hyperdiv.design_tokens import TokenEnum
from hyperdiv.slot import Slot
from .types import get_types
from .top_level_docs import get_top_level_docs
from .class_attribute_docs import get_class_attribute_docs
from ..utils import render_value, render_value_list


class Extractor:
    """
    Extracts the core documentation metadata used to render component
    and prop type doc pages. Collects the metadata in `self.output`,
    which is a JSON-renderable data structure.

    This metadata can be dumped to a JSON file in a build process, so
    the docs app can just load the JSON instead of re-extracting docs
    every time it starts.
    """

    def __init__(self):
        self.types = get_types()
        self.top_level_docs = get_top_level_docs()
        self.class_attribute_docs = get_class_attribute_docs()
        self.parametric_types = {
            name: typ
            for name, typ in self.types.items()
            if inspect.isclass(typ)
            and not name.endswith("Def")
            and typ != HyperdivType
            and typ != CSS
        }

        self.output = dict(
            prop_types=dict(),
            design_tokens=[],
            components={},
        )

    def is_parametric(self, cls):
        for name, typ in self.parametric_types.items():
            if issubclass(cls, typ):
                return True
        return False

    def get_prop_type_doc(self, typ):
        """
        Returns doc info for a prop type definition.

        If the prop type is not parametric (a class/type constructor),
        it looks up its docs in `self.top_level_docs` which contains
        custom-parsed docs of all global variable definitions in
        Hyperdiv.

        We have a convention that type constructors whose names end in
        'Def' are not generally usable type constructors, but are
        intended to be instantiated only once.

        E.g.

        class MyTypeDef(HyperdivType):
            '''
            My docs
            '''
            ...

        MyType = MyTypeDef()

        In this case, the doc for `MyType` will be grabbed from its
        class definition.  The doc for `MyType` will be 'My docs'.
        """
        name = None
        for k, v in self.types.items():
            if typ == v:
                name = k
                break
        if name:
            typ = self.types.get(name)

            if not typ:
                return

            if inspect.isclass(typ):
                return dict(doc=typ.__doc__, typ=typ, name=name)
            else:
                if typ.__class__.__name__.endswith("Def"):
                    return dict(doc=typ.__class__.__doc__, name=name, typ=typ)
                else:
                    doc = self.top_level_docs.get(name, "")
                    return dict(doc=doc, name=name, typ=typ)

    def get_prop_doc(self, klass, prop_name):
        """
        Returns doc info for a prop definition, as a class attribute of `klass`.

        The prop docstring is taken from `self.class_attribute_docs`,
        which is created by our custom parser which grabs custom docs
        for all class attributes in Hyperdiv.
        """
        return self.class_attribute_docs.get(klass.__name__, {}).get(prop_name)

    def extract_prop_type(self, prop_type, toplevel=False):
        """
        Extracts info about `prop_type` and puts it in
        `self.output['prop_types']`.  `toplevel` indicates whether
        this type is directly exported by hyperdiv, or otherwise is an
        internally-used type.
        """
        doc = self.get_prop_type_doc(prop_type)

        if not doc:
            return

        if doc["name"] in self.output["prop_types"]:
            return

        if not inspect.isclass(prop_type) and self.is_parametric(prop_type.__class__):
            is_alias = True
            markdown = self.get_prop_type_markdown(doc["typ"], lookup_alias=False)
        else:
            is_alias = False
            markdown = self.get_prop_type_markdown(doc["typ"])

        self.output["prop_types"][doc["name"]] = dict(
            name=doc["name"],
            markdown=markdown,
            doc=doc["doc"],
            is_parametric=inspect.isclass(prop_type),
            is_alias=is_alias,
            toplevel=toplevel,
        )

    def format_code(self, code_text):
        try:
            return format_str(code_text, mode=FileMode())
        except Exception:
            return code_text

    def get_component_signature(self, klass_or_fn):
        sig = f"{klass_or_fn.__name__}{str(inspect.signature(klass_or_fn))}"
        if inspect.isclass(klass_or_fn):
            return sig, klass_or_fn.__init__.__doc__
        else:
            return sig, klass_or_fn.__doc__

    def extract_component(self, comp):
        """
        Populates `self.output` with info extracted from `comp`. `comp`
        can be either a Hyperdiv exported function, like
        `hd.global_state` or `hd.cache`, or a component class.
        """

        # If already extracted, do nothing.
        if comp.__name__ in self.output["components"]:
            return

        sig, doc = self.get_component_signature(comp)
        sig = self.format_code(sig)

        is_class = inspect.isclass(comp)

        # If it's a function, we're done
        if not is_class:
            self.output["components"][comp.__name__] = dict(
                component_type="function", sig=sig, doc=doc
            )
            return

        # If it's a design token, we're done
        if issubclass(comp, TokenEnum):
            if comp.__name__ not in self.output["design_tokens"]:
                self.output["design_tokens"].append(comp.__name__)
            return

        # Otherwise, it's a component class
        tag = getattr(comp, "_tag", None)
        class_doc = comp.__doc__

        props = []
        style_parts = []
        slots = []
        methods = []
        is_mixin = not issubclass(comp, Component)

        # Collect info for all the class attributes
        for name, attr in vars(comp).items():
            if name.startswith("_"):
                continue

            # The class attribute is a prop
            if isinstance(attr, Prop):
                prop_doc = self.get_prop_doc(comp, attr.name)
                # A prop can be either a style part prop,
                if isinstance(attr.prop_type, StylePart):
                    style_parts.append(dict(prop_name=attr.name, prop_doc=prop_doc))
                # Or a normal prop.
                else:
                    markdown = self.get_prop_type_markdown(attr.prop_type)
                    props.append(
                        dict(
                            prop_name=attr.name,
                            default_value=attr.default_value,
                            immutable=attr.backend_immutable,
                            markdown=markdown,
                            prop_doc=prop_doc,
                        )
                    )

            # The class attribute is a slot
            elif isinstance(attr, Slot):
                slot_doc = self.get_prop_doc(comp, attr.name)
                slots.append(dict(slot_name=attr.name, slot_doc=slot_doc))

            # The class attribute is a method or property
            elif callable(attr) or (type(attr) is property):
                method_doc = attr.__doc__
                # A property:
                if type(attr) is property:
                    if attr.fget and attr.fset:
                        method_sig = f"{attr.fget.__name__} # read/write property"
                    else:
                        method_sig = f"{attr.fget.__name__} # read-only property"

                    # If both getter and setter have public docs, put
                    # them both in the description.
                    setter_doc = attr.fset.__doc__

                    if setter_doc:
                        method_doc = f"*Getter:* {doc}\n\n*Setter:* {setter_doc}"

                    attr = attr.fget
                # A normal method:
                else:
                    method_sig = f"{attr.__name__}{inspect.signature(attr)}"

                methods.append(dict(method_name=name, sig=method_sig, doc=method_doc))

        # Collects the superclasses
        superclasses = []

        for base in comp.__bases__:
            if base != object:
                # Recursively extract info for each superclass
                self.extract_component(base)
                if base.__name__ in self.output["components"]:
                    # If the current class overrides any methods from
                    # the superclass, mark each of those methods with
                    # the superclass whose method it overrides.
                    superclass_methods = self.output["components"][base.__name__][
                        "methods"
                    ]
                    for m in superclass_methods:
                        overridden_method = next(
                            (
                                method
                                for method in methods
                                if method["method_name"] == m["method_name"]
                            ),
                            None,
                        )
                        if overridden_method:
                            overridden_method["overrides"] = base.__name__

                    superclasses.append(base.__name__)

        self.output["components"][comp.__name__] = dict(
            component_type="class",
            sig=sig,
            doc=doc,
            class_doc=class_doc,
            tag=tag,
            props=props,
            style_parts=style_parts,
            slots=slots,
            methods=methods,
            superclasses=superclasses,
            is_mixin=is_mixin,
        )

    def get_prop_type_markdown(self, prop_type, lookup_alias=True):
        """
        Recursively compiles `prop_type` to Markdown where each type is
        compiled to a link to its docs page.
        """
        if isinstance(prop_type, CSSField):
            prop_type = prop_type.typ

        if lookup_alias:
            doc = self.get_prop_type_doc(prop_type)

            if doc:
                name = doc["name"]
                return f"[{name}](/reference/prop-types/{name})"

        def make_link(prop_type_class):
            name = prop_type_class.__name__
            return f"[{name}](/reference/prop-types/{name})"

        if isinstance(prop_type, Optional):
            return (
                make_link(Optional)
                + "("
                + self.get_prop_type_markdown(prop_type.typ)
                + ")"
            )
        elif isinstance(prop_type, OneOf):
            return make_link(OneOf) + "(" + render_value_list(prop_type.values) + ")"
        elif isinstance(prop_type, OneOrMoreOf):
            return (
                make_link(OneOrMoreOf) + "(" + render_value_list(prop_type.values) + ")"
            )
        elif isinstance(prop_type, CSSField):
            return self.get_prop_type_markdown(prop_type.typ)
        elif isinstance(prop_type, DesignToken):
            link = make_link(DesignToken)
            enum_name = prop_type.enum.__name__
            return f"{link}([{enum_name}](/reference/design-tokens/{enum_name}))"
        elif isinstance(prop_type, Event):
            return (
                make_link(Event)
                + "("
                + self.get_prop_type_markdown(prop_type.typ)
                + ")"
            )
        elif isinstance(prop_type, Union):
            link = make_link(Union)
            typ1_md = self.get_prop_type_markdown(prop_type.typ1)
            typ2_md = self.get_prop_type_markdown(prop_type.typ2)
            return f"{link}({typ1_md}, {typ2_md})"
        elif isinstance(prop_type, Native):
            link = make_link(Native)
            typ = prop_type.typ.__name__
            args = [typ]
            if prop_type.coercible_types:
                args.append(
                    "coercible_types=["
                    + ", ".join([t.__name__ for t in prop_type.coercible_types])
                    + "]"
                )
            args = ", ".join(args)
            return f"{link}({args})"
        elif isinstance(prop_type, StylePart):
            return make_link(StylePart)
        elif isinstance(prop_type, ClampedNumber):
            typ_md = None
            if isinstance(prop_type, ClampedInt):
                link = make_link(ClampedInt)
            elif isinstance(prop_type, ClampedFloat):
                link = make_link(ClampedFloat)
            else:
                link = make_link(ClampedNumber)
                typ_md = self.get_prop_type_markdown(prop_type.typ)
            args = []
            if prop_type.low is not None:
                args.append(f"low={prop_type.low}")
            if prop_type.high is not None:
                args.append(f"high={prop_type.high}")
            args_str = ", ".join(args)
            if typ_md:
                return f"{link}({typ_md}, {args_str})"
            else:
                return f"{link}({args_str})"
        elif isinstance(prop_type, Constant):
            link = make_link(Constant)
            const = prop_type.constant
            return f"{link}({repr(const)})"
        elif isinstance(prop_type, List):
            link = make_link(List)
            typ_md = self.get_prop_type_markdown(prop_type.typ)
            return f"{link}({typ_md})"

        name = repr(prop_type)
        return f"[{name}](/reference/prop-types/{name})"
