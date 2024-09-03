from flask_restful import Resource
import functools


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
    def __init__(self, api, resources):
        print("lel")
        self.api = api
        self.resource = resources

    def register_api_endpoint(self, url):
        @functools.wraps(cls)
        def wrapper(*args, **kwargs):
            print(cls)
            inst = cls(*args, **kwargs)

            return inst

        return wrapper

    def add_resources(self, resources):
        def decorator(cls):
            print(cls)

            def wrapper(*args, **kwargs):
                return cls(*args, **kwargs)

            return wrapper

        return decorator


class PopulateApiResource(Resource):
    def __init__(self, board) -> None:
        super().__init__()
        self.board = board

    # TODO: make this a class wrapper

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


class ConfigResource(Resource):
    def __init__(self, config) -> None:
        pass
