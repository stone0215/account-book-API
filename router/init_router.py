from flask import jsonify

from api.response_format import ResponseFormat

from .alarmRouter import init_alarm_api


def init(app):
    init_alarm_api(app)

    @app.route('/')
    def index():
        return jsonify(ResponseFormat.true_return(ResponseFormat, 'Hello Flask!'))

    @app.route('/util/server-alive')
    def serverAlive():
        return jsonify(ResponseFormat.true_return(ResponseFormat, True))
