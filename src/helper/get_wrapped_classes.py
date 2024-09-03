import os
import ast


def file_wrapped_classes_in_file_path(file_path):
    with open(file_path, "r") as source:
        tree = ast.parse(source.read())

    wrapped_classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if node.decorator_list:
                class_info = {
                    "class_name": node.name,
                    "decorators": [ast.dump(decorator) for decorator in node.decorator_list]
                }
                wrapped_classes.append(class_info)
    return wrapped_classes


def find_wrappers_in_module_path(module_path):
    wrapped_classes = []

    for root, dirs, files in os.walk(module_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                wrapped_classes.extend(file_wrapped_classes_in_file_path(file_path))

    return wrapped_classes


def get_module_path(module):
    return os.path.dirname(module.__file__)
