import os
import pkgutil
import importlib

# Get the directory where this __init__.py is located
package_dir = os.path.dirname(__file__)

# Iterate over all files in the directory
for module_info in pkgutil.iter_modules([package_dir]):
    module_name = module_info.name
    if module_name != '__init__':
        # Import the module
        importlib.import_module(f'.{module_name}', __name__)

# TODO: pack that up in a callable importable object
# TODO: make it part of import func in the api_manager
