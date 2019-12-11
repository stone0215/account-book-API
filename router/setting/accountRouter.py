# -*- coding: UTF-8 -*-

from flask import jsonify, request

from api.response_format import ResponseFormat
from app.dao.model.setting.account_model import Account
from app.dao.model.setting.initial_model import InitialSetting


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
            account = Account(name=inputData['name'], account_type=inputData['account_type'],
                              fx_code=inputData['fx_code'], is_calculate=inputData['is_calculate'],
                              in_use=inputData['in_use'], discount=inputData['discount'], account_index=inputData['account_index'])
            outputData = Account.add(Account, account)

            # 新增初始值
            initial = InitialSetting(code_id=account.account_id, code_name=account.name,
                                     initial_type='A', setting_value=0)
            result = InitialSetting.add(InitialSetting, initial)

            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, Account.output(Account, outputData)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add account data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/account/<int:account_id>', methods=['PUT'])
    def updateAccount(account_id):
        try:
            account = Account.queryByKey(Account, account_id)
            if account is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                account.name = inputData['name']
                account.account_type = inputData['account_type']
                account.fx_code = inputData['fx_code']
                account.is_calculate = inputData['is_calculate']
                account.in_use = inputData['in_use']
                account.discount = inputData['discount']
                account.account_index = inputData['account_index']
                if Account.update(Account):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update account data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/account/<int:account_id>', methods=['DELETE'])
    def deleteAccount(account_id):
        try:
            account = Account.queryByKey(Account, account_id)
            if account is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if Account.delete(Account, account_id):
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
