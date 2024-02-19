"""
A custom global definition doc parser that extracts documentation from
all the global definitions in a set of given directories.

If we define global variables like:

# x is the sum of 1 and 2
x = 1 + 2

'''
y is the product
of 4 and 5
'''
y = 4 * 5

This custom parser will create a mapping like:

{
  'x': 'x is the sum of 1 and 2',
  'y': 'y is the product\nof 4 and 5'
}
"""

import symtable
import ast
from .docstring_extractor import extract_docstring
from .dirutils import get_files_recursively
from .hyperdiv_module_path import get_hyperdiv_module_path


class TopLevelAssignmentVisitor(ast.NodeVisitor):
    def __init__(self, source_lines, sym_table):
        self.source_lines = source_lines
        self.docs = {}
        self.sym_table = sym_table

    def visit_Assign(self, node):
        docstring = extract_docstring(self.source_lines, node.lineno - 2)
        if docstring:
            for item in node.targets:
                if isinstance(item, ast.Name):
                    self.docs[item.id] = docstring

    def generic_visit(self, node):
        # Using symtable to detect scoped nodes
        if hasattr(node, "name") and isinstance(node.name, str):
            try:
                if self.sym_table.lookup(node.name).is_namespace():
                    # Skip over nodes that introduce a new scope
                    return
            except KeyError:
                return
        super().generic_visit(node)


def extract_top_level_docs_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()
    sym_table = symtable.symtable(source_code, "<string>", "exec")
    tree = ast.parse(source_code)
    visitor = TopLevelAssignmentVisitor(source_code.splitlines(), sym_table)
    visitor.visit(tree)

    return visitor.docs


def extract_top_level_docs_from_files(file_paths):
    all_docs = {}
    for file_path in file_paths:
        docs = extract_top_level_docs_from_file(file_path)
        if docs:  # Only add entries for classes that have docs
            all_docs.update(docs)
    return all_docs


def get_top_level_docs():
    """
    A dict name -> doc mapping top-level names to their docs in all
    Hyperdiv component files. For example if there's a definition like
    this:

        # This is a doc
        x = 1

    The dict will contain {'x': 'This is a doc'}.

    This dict is used to get the prop type docs from top-level type
    definitions like:

        # This is the color type
        Color = Optional(DesignToken(tokens.Color))

    But since it's hard to statically determine if the type of a
    top_level definition is HyperdivType, this dict includes all
    top-level definitions.
    """

    hyperdiv_path = get_hyperdiv_module_path()

    file_paths = (
        get_files_recursively(hyperdiv_path / "prop_types")
        + get_files_recursively(hyperdiv_path / "component_mixins")
        + get_files_recursively(hyperdiv_path / "components")
    )

    return extract_top_level_docs_from_files(file_paths)
