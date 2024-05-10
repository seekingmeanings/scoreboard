from flask_restful import Resource


class ContentResource(Resource):
    def __init__(self, thing) -> None:
        super().__init__()
        self.thing = thing


class ConfigResource(Resource):
    pass
