from flask_restful import Resource, request
from flask import jsonify


class TestAccess(Resource):
    @staticmethod
    def get():
        return jsonify("pong")
