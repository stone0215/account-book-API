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
            liabilitys = Loan.query4Display(Loan)
            for liability in liabilitys:
                output.append(Loan.output4View(Loan, liability))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/liability/loan/<int:loan_id>', methods=['GET'])
    def getLoanById(loan_id):
        output = {}

        try:
            liability = Loan.queryByKey(Loan, loan_id)
            output = Loan.output(Loan, liability)

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
            inputData['apply_date'] = datetime.strptime(
                inputData['apply_date'], date_format)
            inputData['grace_expire_date'] = datetime.strptime(
                inputData['grace_expire_date'], date_format) if inputData['grace_expire_date'] else None
            liability = Loan(inputData)

            result = Loan.add(Loan, liability)

            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, Loan.output(Loan, result)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add estate data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/liability/loan/<int:loan_id>', methods=['PUT'])
    def updateLoan(loan_id):
        global date_format

        try:
            liability = Loan.queryByKey(Loan, loan_id)
            if liability is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                liability.loan_name = inputData['loan_name']
                liability.loan_type = inputData['loan_type']
                liability.account_id = inputData['account_id']
                liability.account_name = inputData['account_name']
                liability.interest_rate = inputData['interest_rate']
                liability.period = inputData['period']
                liability.apply_date = datetime.strptime(
                    inputData['apply_date'], date_format)
                liability.grace_expire_date = datetime.strptime(
                    inputData['grace_expire_date'], date_format)
                liability.pay_day = inputData['pay_day']
                liability.amount = inputData['amount']
                liability.repayed = inputData['repayed']
                liability.loan_index = inputData['loan_index'] if inputData['loan_index'] else None
                if Loan.update(Loan):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update estate data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/liability/loan/<int:loan_id>', methods=['DELETE'])
    def deleteLoan(loan_id):
        try:
            liability = Loan.queryByKey(
                Loan, loan_id)
            if liability is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if Loan.delete(Loan, loan_id):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete estate data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/liability/loan/selection', methods=['GET'])
    def getLoanSelections():
        output = []

        try:
            loans = Loan.query4Selection(Loan)
            for loan in loans:
                output.append(Loan.output4Selection(Loan, loan))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/liability/loan/detail/<int:loan_id>', methods=['GET'])
    def getLoanJournals(loan_id):
        output = []

        try:
            loan_journals = LoanJournal.queryByLoanId(
                LoanJournal, loan_id)
            for loan_journal in loan_journals:
                output.append(LoanJournal.output(
                    LoanJournal, loan_journal))
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

            loan_journal = LoanJournal(loan_id=inputData['loan_id'], loan_excute_type=inputData['loan_excute_type'],
                                       excute_price=inputData['excute_price'], excute_date=datetime.strptime(inputData['excute_date'], date_format), memo=inputData['memo'])
            result = LoanJournal.add(LoanJournal, loan_journal)

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
            loan_journal = LoanJournal.queryByKey(
                LoanJournal, distinct_number)
            if loan_journal is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                loan_journal.loan_excute_type = inputData['loan_excute_type']
                loan_journal.excute_price = inputData['excute_price']
                loan_journal.excute_date = datetime.strptime(
                    inputData['excute_date'], date_format)
                loan_journal.memo = inputData['memo']

                if LoanJournal.update(LoanJournal):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update estate detail data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/liability/loan/detail/<int:distinct_number>', methods=['DELETE'])
    def deleteLoanJournal(distinct_number):
        try:
            loan_journal = LoanJournal.queryByKey(
                LoanJournal, distinct_number)
            if loan_journal is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if LoanJournal.delete(LoanJournal, distinct_number):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete estate detail data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
