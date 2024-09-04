import importlib

import flask_restful
import functools
import ast

from src.helper import get_wrapped_classes as wrap_scan


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
            #endpoint_modules: list,
            resources
    ):
        self.test = None
        self.api = api
        self.resource = resources

    @staticmethod
    def import_endpoint_module(module: str) -> None:

        # TODO: every file has to be imported, or the __init__.py has to take care
        importlib.import_module(module)
        import src.api.endpoints

    def auto_add_endpoints(self) -> None:
        import src.api.endpoints
        print("added endpoints module")
        endpoints = wrap_scan.find_wrappers_in_module_path(src.api.endpoints)

        return
        for endpoint in endpoints:
            for decorator in [ast.parse(dec_str, mode='eval') for dec_str in endpoint['decorators']]:
                print(decorator)

    # just api, make resource another one
    # so all resource is sepereate and tihs is just api class
    # so it can be a subclass of flask_restful.api ??????????????s
    def add_resources(self,
                      resources: dict = None,
                      url: str = None
                      ):
        sself = self
        print("called the decorator")

        def decorator(cls):
            class WrappedClass(cls):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    if resources:
                        for name, res_name in resources.items():
                            setattr(
                                self,
                                name,
                                sself.resource[res_name]
                            )

            if url:
                # does it init itself??
                print(url)
                print(WrappedClass)
                sself.api.add_resource(
                    WrappedClass,
                    sself.api.base_url + url,
                    endpoint=f"{cls.__name__.lower()}_endpoint"
                )

        return decorator
