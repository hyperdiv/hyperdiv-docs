"""
A custom class attribute doc parser that extracts documentation
from all the classes in a set of given directories. This is in lieu of
an acceptable Python built-in solution for documenting class attributes.

If we have a class definition like:

class Foo:

  # The foo attribute
  foo = 1

  '''
  The bar attribute.
  It does bar things.
  '''
  bar = 2

This custom parser will create a mapping like:

{
  Foo: {
    'foo': 'The foo attribute',
    'bar': 'The bar attribute\n  It does bar things.'
  }
}

(give or take whitespace).
"""

import ast
from .docstring_extractor import extract_docstring
from .dirutils import get_files_recursively
from .hyperdiv_module_path import get_hyperdiv_module_path


class ClassAttributeVisitor(ast.NodeVisitor):
    def __init__(self, source_lines):
        self.source_lines = source_lines
        self.docs = {}
        self.current_class = None

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None

    def visit_Assign(self, node):
        if self.current_class:  # Only consider class-level attributes
            docstring = extract_docstring(self.source_lines, node.lineno - 2)
            if docstring:
                for item in node.targets:
                    if isinstance(item, ast.Name):
                        if self.current_class not in self.docs:
                            self.docs[self.current_class] = {}
                        self.docs[self.current_class][item.id] = docstring


def extract_class_attribute_docs_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()
    source_lines = source_code.splitlines()
    tree = ast.parse(source_code)
    visitor = ClassAttributeVisitor(source_lines)
    visitor.visit(tree)
    return visitor.docs


def extract_class_attribute_docs_from_files(file_paths):
    all_docs = {}
    for file_path in file_paths:
        docs = extract_class_attribute_docs_from_file(file_path)
        if docs:  # Only add entries for classes that have docs
            all_docs.update(docs)
    return all_docs


def get_class_attribute_docs():
    """
    A dict name -> doc mapping prop names to their docs. Similar to the
    above, but restricted to class attributes of type `Prop`.
    """
    hyperdiv_path = get_hyperdiv_module_path()

    mixins_path = hyperdiv_path / "component_mixins"
    components_path = hyperdiv_path / "components"

    file_paths = get_files_recursively(mixins_path) + get_files_recursively(
        components_path
    )

    return extract_class_attribute_docs_from_files(file_paths)
