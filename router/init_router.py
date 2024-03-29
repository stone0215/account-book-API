from flask import jsonify

from api.response_format import ResponseFormat

from .monthlyReport.cashFlowRouter import init_journal_api
from .setting.accountRouter import init_account_api
from .setting.alarmRouter import init_alarm_api
from .setting.budgetRouter import init_budget_api
from .setting.codeRouter import init_code_api
from .setting.creditCardRouter import init_credit_card_api
from .setting.initialRouter import init_initial_api
from .otherAssetAndLiabilities.estateAssetRouter import init_estate_asset_api
from .otherAssetAndLiabilities.insuranceAssetRouter import init_insurance_asset_api
from .otherAssetAndLiabilities.liabilityRouter import init_liability_api
from .otherAssetAndLiabilities.otherAssetRouter import init_other_asset_api
from .otherAssetAndLiabilities.stockAssetRouter import init_stock_asset_api
from .utilRouter import init_util_api
from .yearReport.reportRouter import init_report_api
from .dashboardRouter import init_dashboard_api
from .globalRouter import init_global_api


def init(app):
    @app.route('/')
    def index():
        return jsonify(ResponseFormat.true_return(ResponseFormat, 'Hello Flask!'))

    init_account_api(app)
    init_alarm_api(app)
    init_budget_api(app)
    init_code_api(app)
    init_credit_card_api(app)
    init_estate_asset_api(app)
    init_initial_api(app)
    init_other_asset_api(app)
    init_stock_asset_api(app)
    init_insurance_asset_api(app)
    init_util_api(app)
    init_liability_api(app)
    init_journal_api(app)
    init_report_api(app)
    init_dashboard_api(app)
    init_global_api(app)
