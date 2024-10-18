import importlib

from typing import Union, List

import flask_restful
import functools
import ast
import logging

from src.helper import get_wrapped_classes as wrap_scan
from src.things.scoreboard.controls import Control, ControlManager


class ApiEndpointManager:
    """
    this has to have an instance before ??
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ApiEndpointManager, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def singleton_init(init_func):
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, '_initialized'):
                init_func(self, *args, **kwargs)

                # can't use _instance cause its already been set at that point
                self._initialized = True

        return wrapper

    @singleton_init
    def __init__(
            self,
            api: flask_restful.Api,
            resources,
            control_manager: ControlManager,
    ):
        self.lg = logging.getLogger(self.__class__.__name__)
        self.test = None
        self.api = api
        self.resource = resources
        self.control_manager = control_manager

    def import_endpoint_module(self, module: str) -> None:

        # TODO: every file has to be imported
        self.lg.debug(f"importing module: {module} in api endpoint manager")
        self.lg.warning(f"the module needs a sufficient __init__.py file to recognize api endpoints")
        importlib.import_module(module)

    @staticmethod
    def auto_add_endpoints_not_needed() -> None:
        import src.api.endpoints
        print("added endpoints module")
        endpoints = wrap_scan.find_wrappers_in_module_path(src.api.endpoints)

        for endpoint in endpoints:
            for decorator in [ast.parse(dec_str, mode='eval') for dec_str in endpoint['decorators']]:
                print(decorator)

    def add_resources(self,
                      resources: dict = None,
                      url: str = None,
                      control: Union[Control, List[Control]] = None,
                      ):
        sself = self

        def decorator(cls):
            class WrappedClass(cls):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.lg = logging.getLogger(cls.__name__)
                    if resources:
                        for name, res_name in resources.items():
                            setattr(
                                self,
                                name,
                                sself.resource[res_name]
                            )
            if url:
                # does it init itself??
                self.lg.debug(f"adding resource {cls} to {url} as {WrappedClass}")
                sself.api.add_resource(
                    WrappedClass,
                    sself.api.base_url + url,
                    endpoint=f"{cls.__name__.lower()}_endpoint"
                )

            if control:
                if isinstance(control, list):
                    for c in control:
                        c.api_call.make_call(url)

                        self.lg.debug(f"adding control {c}")
                        self.control_manager.add_control(c)
                else:
                    control.api_call.make_call(url)
                    self.lg.debug(f"adding control {control}")
                    self.control_manager.add_control(control)

        return decorator
