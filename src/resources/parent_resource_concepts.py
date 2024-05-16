from flask_restful import Resource


class ContentResource(Resource):
    def __init__(self, board) -> None:
        super().__init__()
        self.board = board


class ConfigResource(Resource):
    pass
