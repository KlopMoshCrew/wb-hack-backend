import os

from flask import Flask, current_app
from flask_restful import Api
from flask_cors import CORS
from api.ecom import Ecom
from api.heatmap import Heatmap


def create_app():
    app = Flask(__name__)

    cors = CORS(app, resources={r"*": {"origins": "*"}})

    # with app.app_context():
    #     current_app.db_wrapper = DBWrapper(DATABASE, USER, PASSWORD, HOST, PORT, SCHEMA)

    api = Api(app)
    api.add_resource(Ecom, "/ecom/<string:id>")
    api.add_resource(Heatmap, "/get_heatmap")

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
