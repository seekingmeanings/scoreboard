import os
import ast


def extract_values(cmp_node):
    node = cmp_node.body
    id_value: str
    attr_value: str
    args = []
    kwargs = {}

    if not isinstance(node, ast.Call):
        raise TypeError(f"cant parse {type(node)} as an ast.Call obj")

    # get the id and stuff
    id_value = node.keywords[0].value.keywords[0].value.keywords[0].value.keywords[0].value.value

    attr_value = node.keywords[0].value.keywords[1].value.value

    def parse_vals(val_tree):
        if val_tree.func.id == 'Dict':
            keys = [key.keywords[0].value.value for key in
                    val_tree.keywords[0].value.elts
                    ]

            values = [value.keywords[0].value.value for value in
                      val_tree.keywords[1].value.elts

                      ]

            return dict(zip(keys, values))
        elif val_tree.func.id == 'Constant':
            return val_tree.keywords[0].value.value

        else:
            raise NotImplementedError(f"just dont use keyword arguments pls in the decorator")

    args = [parse_vals(arg) for arg in node.keywords[1].value.elts]

    # TODO: make it intelligent with scanning

    # parse any kwargs
    for kwarg in node.keywords[2].value.elts:
        raise NotImplementedError("im to lazy")

    return {
        'id': id_value,
        'wrapper_name': attr_value,
        'args': args,
        'kwargs': kwargs,
    }



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
