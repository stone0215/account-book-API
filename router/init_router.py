from flask import jsonify

from api.response_format import ResponseFormat

from .setting.accountRouter import init_account_api
from .setting.alarmRouter import init_alarm_api
from .setting.budgetRouter import init_budget_api
from .setting.codeRouter import init_code_api
from .setting.creditCardRouter import init_credit_card_api
from .setting.initialRouter import init_initial_api
from .setting.loanRouter import init_loan_api
from .otherAsset.estateAssetRouter import init_estate_asset_api
from .otherAsset.insuranceAssetRouter import init_insurance_asset_api
from .otherAsset.otherAssetRouter import init_other_asset_api
from .otherAsset.stockAssetRouter import init_stock_asset_api
from .utilRouter import init_util_api


def init(app):
    @app.route('/')
    def index():
        return jsonify(ResponseFormat.true_return(ResponseFormat, 'Hello Flask!'))

    @app.route('/global/server-alive')
    def serverAlive():
        return jsonify(ResponseFormat.true_return(ResponseFormat, True))

    init_account_api(app)
    init_alarm_api(app)
    init_budget_api(app)
    init_code_api(app)
    init_credit_card_api(app)
    init_estate_asset_api(app)
    init_initial_api(app)
    init_loan_api(app)
    init_other_asset_api(app)
    init_stock_asset_api(app)
    init_insurance_asset_api(app)
    init_util_api(app)
