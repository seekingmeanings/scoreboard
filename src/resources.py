class ContentResource:
    pass


class ConfigResource:
    pass


class ResourceManager:
    """
    Manage Resources (api functions linked to requests)
    giving them access to the right physical or virtual thing
    eg. an LED
    """
    def __init__(self):
        self.resources: dict = dict()

    def register(
            self,
            res_type: ContentResource | ConfigResource,
            resource: any,
            res_name: str,
    ) -> None:
        self.resources[res_name] = (res_type, resource)

    def retrieve(self, res_name):
        return self.resources[res_name]

    def get_resource_for_class(
            self,
            query: list[tuple[str, str]]
    ):
        """

        :param query: list of tuples with the name in the wrapped fun and the name of the content
        :return: wrapper
        """

        def wrapper(cls):
            return cls

        return wrapper
