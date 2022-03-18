from flask import jsonify, request
from itertools import groupby

from api.response_format import ResponseFormat
from app.dao.model.setting.account_model import Account
from app.dao.model.setting.credit_card_model import CreditCard
from app.dao.model.liability.loan_model import Loan
from app.dao.model.setting.code_model import Code
from app.dao.model.otherAsset.insurance_model import Insurance


def init_util_api(app):
    @app.route('/util/wallet-selection-group', methods=['GET'])
    def getWalletSelectionGroups():
        output = []
        selections = []
        tempSelections = []

        try:
            # 取得帳戶選項
            tempSelections = Account.query4Selection(Account)

            for account in tempSelections:
                selections.append(Account.output4Selection(Account, account))

            # 要先 sort 才能 groupby
            selections.sort(key=lambda item: item['type'])
            # Group By Age Field
            for key, groups in groupby(selections, lambda item: item['type']):
                output.append({
                    'title': key,
                    'selections': list(groups)
                })
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/util/credit-card-selection-group', methods=['GET'])
    def getCreditCardSelectionGroups():
        output = []
        selections = []
        tempSelections = []

        try:
            # 取得信用卡選項
            tempSelections = CreditCard.query4Selection(CreditCard)
            for card in tempSelections:
                selections.append(
                    CreditCard.output4Selection(CreditCard, card))

            if len(selections) > 0:
                output.append({
                    'title': 'Credit_Card',
                    'name': '信用卡',
                    'selections': selections
                })
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/util/loan-selection-group', methods=['GET'])
    def getLoanSelectionGroups():
        output = []
        selections = []
        tempSelections = []

        try:
            # 取得貸款選項
            tempSelections = Loan.query4Selection(Loan)
            if tempSelections.count() > 0:
                for loan in tempSelections:
                    selections.append(Loan.output4Selection(Loan, loan))
                output.append({
                    'title': 'Loan',
                    'name': '貸款',
                    'selections': selections
                })
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/util/insurance-selection-group', methods=['GET'])
    def getInsuranceSelectionGroups():
        output = []
        selections = []
        tempSelections = []

        try:
            # 取得保險選項
            tempSelections = Insurance.query4Selection(Insurance)
            for insurance in tempSelections:
                selections.append(
                    Insurance.output4Selection(Insurance, insurance))
            output.append({
                'title': 'Insurance',
                'name': '保險',
                'selections': selections
            })
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/util/code-selection-group', methods=['GET'])
    def getCodeSelectionGroups():
        output = []
        selections = []
        tempSelections = []

        try:
            # 取得選單選項
            tempSelections = Code.query4Selection(Code)

            for code in tempSelections:
                selections.append(Code.output4Selection(Code, code))

            # 要先 sort 才能 groupby
            selections.sort(key=lambda item: item['type'])
            # Group By Age Field
            for key, groups in groupby(selections, lambda item: item['type']):
                output.append({
                    'title': key,
                    'selections': list(groups)
                })
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/util/code-selection-group/<int:code_group>', methods=['GET'])
    def getSubCodeSelectionGroups(code_group):
        output = []
        selections = []
        tempSelections = []

        try:
            # 取得副選單選項
            tempSelections = Code.query4SubSelection(Code, code_group)
            for code in tempSelections:
                selections.append(Code.output4SubSelection(Code, code))
            output.append({
                'title': '副選單',
                'selections': selections
            })
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))
