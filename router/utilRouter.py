from flask import jsonify, request

from api.response_format import ResponseFormat
from app.dao.model.setting.account_model import Account
from app.dao.model.setting.credit_card_model import CreditCard


def init_util_api(app):
    @app.route('/util/wallet-selection-group', methods=['GET'])
    def getSelectionGroups():
        output = []
        selections = []
        tempSelections = []

        try:
            # 取得帳戶選項
            tempSelections = Account.query4Selection(Account)
            for account in tempSelections:
                selections.append(Account.output4Selection(Account, account))
            output.append({
                'title': '帳戶',
                'type': 'A',
                'selections': selections
            })

            # 取得信用卡選項
            selections = []
            tempSelections = CreditCard.query4Selection(CreditCard)
            for card in tempSelections:
                selections.append(
                    CreditCard.output4Selection(CreditCard, card))
            output.append({
                'title': '信用卡',
                'type': 'C',
                'selections': selections
            })

            # 取得貸款選項 todo:
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))
