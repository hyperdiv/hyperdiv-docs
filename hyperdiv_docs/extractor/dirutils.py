import os
import re


def get_files_recursively(path):
    paths = path.iterdir()
    files = []
    for path in paths:
        if os.path.isdir(path):
            files.extend(get_files_recursively(path))
        elif path.name.endswith(".py") and os.path.exists(path):
            files.append(str(path))
    return files


def get_modules_recursively(path, module_name):
    paths = path.iterdir()
    modules = []
    for path in paths:
        if os.path.isdir(path):
            modules.extend(
                get_modules_recursively(path, f"{module_name}.{os.path.split(path)[1]}")
            )
        elif (
            path.name.endswith(".py")
            and path.name != "__init__.py"
            and os.path.exists(path)
        ):
            nested_module_name = re.split(r"\.py$", path.name)[0]
            modules.append(f"{module_name}.{nested_module_name}")
    return modules
