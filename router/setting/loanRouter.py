# -*- coding: UTF-8 -*-

from flask import jsonify, request

from api.response_format import ResponseFormat
from app.dao.model.setting.loan_model import Loan


def init_loan_api(app):
    @app.route('/loan/query', methods=['GET'])
    def getLoans():
        output = []

        try:
            loans = Loan.getAll(Loan)
            for loan in loans:
                output.append(Loan.output(Loan, loan))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/loan', methods=['POST'])
    def addLoan():
        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)

            # 新增其他資產
            loan = Loan(loan_name=inputData['loan_name'], account_id=inputData['account_id'],
                        account_name=inputData['account_name'], interest_rate=inputData[
                            'interest_rate'], apply_date=inputData['apply_date'],
                        pay_day=inputData['pay_day'], loan_index=inputData['loan_index'])

            if Loan.add(Loan, loan):
                return jsonify(ResponseFormat.true_return(ResponseFormat, Loan.output(Loan, outputData)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add asset data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/loan/<int:loan_id>', methods=['PUT'])
    def updateLoan(loan_id):
        try:
            loan = Loan.queryByKey(Loan, loan_id)
            if loan is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                loan.loan_name = inputData['loan_name']
                loan.account_id = inputData['account_id']
                loan.account_name = inputData['account_name']
                loan.interest_rate = inputData['interest_rate']
                loan.apply_date = inputData['apply_date']
                loan.pay_day = inputData['pay_day']
                loan.loan_index = inputData['loan_index']
                if Loan.update(Loan):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update asset data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/loan/<int:loan_id>', methods=['DELETE'])
    def deleteLoan(loan_id):
        try:
            loan = Loan.queryByKey(Loan, loan_id)
            if loan is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if Loan.delete(Loan, loan_id):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete asset data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
