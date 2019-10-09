from flask import jsonify

from api.response_format import ResponseFormat

from .accountRouter import init_account_api
from .alarmRouter import init_alarm_api
from .budgetRouter import init_budget_api
from .codeRouter import init_code_api
from .creditCardRouter import init_credit_card_api
from .otherAssetRouter import init_other_asset_api


def init(app):
    @app.route('/')
    def index():
        return jsonify(ResponseFormat.true_return(ResponseFormat, 'Hello Flask!'))

    @app.route('/util/server-alive')
    def serverAlive():
        return jsonify(ResponseFormat.true_return(ResponseFormat, True))

    init_account_api(app)
    init_alarm_api(app)
    init_budget_api(app)
    init_code_api(app)
    init_credit_card_api(app)
    init_other_asset_api(app)
