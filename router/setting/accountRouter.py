# -*- coding: UTF-8 -*-

from flask import jsonify, request

from api.response_format import ResponseFormat
from app.dao.model.setting.account_model import Account
# from app.dao.model.setting.initial_model import InitialSetting


def init_account_api(app):
    @app.route('/account/query', methods=['GET'])
    def getAccounts():
        output = []

        try:
            accounts = Account.queryByConditions(
                Account, request.args)
            for account in accounts:
                output.append(Account.output(Account, account))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/account', methods=['POST'])
    def addAccount():
        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)

            # 新增帳戶
            account = Account(inputData)
            result = Account.add(Account, account)

            # 新增初始值
            # initial = InitialSetting(code_id=account.account_id, code_name=account.name,
            #                          initial_type='Account', setting_value=0)
            # result = InitialSetting.add(InitialSetting, initial)

            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, Account.output(Account, result)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add account data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/account/<int:id>', methods=['PUT'])
    def updateAccount(id):
        try:
            account = Account.queryByKey(Account, id)
            if account is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                account.account_id = inputData['account_id']
                account.name = inputData['name']
                account.account_type = inputData['account_type']
                account.fx_code = inputData['fx_code']
                account.is_calculate = inputData['is_calculate']
                account.in_use = inputData['in_use']
                account.discount = inputData['discount']
                account.memo = inputData['memo']
                account.owner = inputData['owner']
                account.owner = inputData['carrier_no']
                account.account_index = inputData['account_index']
                if Account.update(Account):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update account data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/account/<int:id>', methods=['DELETE'])
    def deleteAccount(id):
        try:
            account = Account.queryByKey(Account, id)
            if account is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if Account.delete(Account, id):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete account data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/account/selection', methods=['GET'])
    def getAccountSelections():
        output = []

        try:
            accounts = Account.query4Selection(Account)
            for account in accounts:
                output.append(Account.output4Selection(Account, account))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))
