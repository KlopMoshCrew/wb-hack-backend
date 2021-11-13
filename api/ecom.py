from flask_restful import Resource, reqparse


class Ecom(Resource):

    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument("id", type=str, required=True, location="args")

    def get(self, id=None):
        # args = self.get_parser.parse_args()

        return {"message": "ok"}, 200
