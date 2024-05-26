from flask_restful import Resource


class ContentResource(Resource):
    def __init__(self, board) -> None:
        super().__init__()
        self.board = board

    # TODO: make this a class wrapper
    # TODO: move flask_restful.Resource to the resource files


class ConfigResource(Resource):
    def __init__(self, config) -> None:
        pass
