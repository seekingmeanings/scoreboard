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

    def auto_add_endpoints(self):
        import src.api.endpoints
        print("added endpoints module")
        endpoints = wrap_scan.find_wrappers_in_module_path(src.api.endpoints)

        for endpoint in endpoints:
            print(endpoint)
            for decorator in [ast.parse(dec_str, mode='eval') for dec_str in endpoint['decorators']]:
                print(decorator)



    # just api, make resource another one
    # so all resource is sepereate and tihs is just api class
    # so it can be a subclass of flask_restful.api
    def add_resources(self,
                      resources: dict = None,
                      url: str = None
                      ):
        sself = self

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


class ResourceManager:
    pass


class PopulateApiResource(flask_restful.Resource):
    def __init__(self, board) -> None:
        print("INNNNNIOTTTTTT")
        super().__init__()
        self.board = board

    # TODO: move flask_restful.Resource to the resource files (Why?)


def register_api_endpoint(cls):
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        instance = cls(*args, **kwargs)
        return instance

    return wrapper


def add_resource(cls):
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        inst = cls(*args, **kwargs)
        return inst

    return wrapper


class ConfigResource(flask_restful.Resource):
    def __init__(self, config) -> None:
        pass
