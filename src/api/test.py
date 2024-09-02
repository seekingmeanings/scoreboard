from flask_restful import Resource, request
from flask import jsonify


class TestAccess(Resource):
    # TODO: add test for virtual
    @staticmethod
    def get():
        return jsonify("pong")
