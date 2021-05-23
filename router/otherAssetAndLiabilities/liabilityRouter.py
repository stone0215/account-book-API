# -*- coding: UTF-8 -*-

from datetime import datetime
from flask import jsonify, request

from api.response_format import ResponseFormat
from app.dao.model.liability.loan_journal_model import LoanJournal
from app.dao.model.liability.loan_modely import Loan

date_format = '%Y-%m-%dT%H:%M:%S.%fZ'


def init_liability_api(app):
    @app.route('/liability/loan', methods=['GET'])
    def getLoans():
        output = []

        try:
            liabilitys = Loan.query4Summary(Loan)
            for liability in liabilitys:
                output.append(Loan.output4View(
                    Loan, liability))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/liability/loan', methods=['POST'])
    def addLoan():
        global date_format

        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)

            liability = Loan(loan_name=inputData['loan_name'], loan_type=inputData['loan_type'],
                             account_id=inputData['account_id'], account_name=inputData['account_name'],
                             interest_rate=inputData['interest_rate'], perid=inputData['perid'],
                             apply_date=datetime.strptime(
                                 inputData['apply_date'], date_format),
                             pay_day=inputData['pay_day'], amount=inputData['amount'],
                             repayed=inputData['repayed'], loan_index=inputData['loan_index'])

            result = Loan.add(Loan, liability)

            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, Loan.output(Loan, result)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add estate data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/liability/loan/<int:estate_id>', methods=['PUT'])
    def updateLoan(estate_id):
        global date_format

        try:
            liability = Loan.queryByKey(
                Loan, estate_id)
            if liability is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                liability.loan_name = inputData['loan_name']
                liability.loan_type = inputData['loan_type']
                liability.account_id = inputData['account_id']
                liability.apply_date = datetime.strptime(
                    inputData['apply_date'], date_format)
                liability.down_payment = inputData['down_payment']
                liability.loan_id = inputData['loan_id'] if inputData['loan_id'] else None
                liability.amount = inputData['amount']
                if Loan.update(Loan):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update estate data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/liability/loan/<int:estate_id>', methods=['DELETE'])
    def deleteLoan(estate_id):
        try:
            liability = Loan.queryByKey(
                Loan, estate_id)
            if liability is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if Loan.delete(Loan, estate_id):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete estate data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/liability/loan/detail/<int:estate_id>', methods=['GET'])
    def getLoanJournals(estate_id):
        output = []

        try:
            estate_journals = LoanJournal.queryByLoanId(
                LoanJournal, estate_id)
            for estate_journal in estate_journals:
                output.append(LoanJournal.output(
                    LoanJournal, estate_journal))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/liability/loan/detail', methods=['POST'])
    def addLoanJournal():
        global date_format

        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)

            estate_journal = LoanJournal(estate_id=inputData['estate_id'], estate_excute_type=inputData['estate_excute_type'],
                                         excute_price=inputData['excute_price'], excute_date=datetime.strptime(
                inputData['excute_date'], date_format),
                memo=inputData['memo'])
            result = LoanJournal.add(LoanJournal, estate_journal)

            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, LoanJournal.output(LoanJournal, result)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add estate detail data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/liability/loan/detail/<int:distinct_number>', methods=['PUT'])
    def updateLoanJournal(distinct_number):
        global date_format

        try:
            estate_journal = LoanJournal.queryByKey(
                LoanJournal, distinct_number)
            if estate_journal is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                estate_journal.estate_excute_type = inputData['estate_excute_type']
                estate_journal.excute_price = inputData['excute_price']
                estate_journal.excute_date = datetime.strptime(
                    inputData['excute_date'], date_format)
                estate_journal.memo = inputData['memo']

                if LoanJournal.update(LoanJournal):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update estate detail data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/liability/loan/detail/<int:distinct_number>', methods=['DELETE'])
    def deleteLoanJournal(distinct_number):
        try:
            estate_journal = LoanJournal.queryByKey(
                LoanJournal, distinct_number)
            if estate_journal is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if LoanJournal.delete(LoanJournal, distinct_number):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete estate detail data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
