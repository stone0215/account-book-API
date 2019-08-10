from flask import jsonify

from api.response_format import ResponseFormat
from .userRouter import init_api


def init(app):
    init_api(app)

    @app.route('/util/server-alive')
    def serverAlive():
        return jsonify(ResponseFormat.true_return(ResponseFormat, True))