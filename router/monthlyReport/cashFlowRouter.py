# -*- coding: UTF-8 -*-

from datetime import datetime
from flask import jsonify, request
from itertools import groupby

from api.response_format import ResponseFormat
from app.dao.model.liability.loan_modely import Loan
from app.dao.model.monthlyReport.journal_model import Journal
from app.dao.model.monthlyReport.account_balance_model import AccountBalance
from app.dao.model.monthlyReport.credit_card_balance_model import CreditCardBalance
from app.dao.model.monthlyReport.estate_net_value_model import EstateNetValueHistory
from app.dao.model.monthlyReport.insurance_net_value_model import InsuranceNetValueHistory
from app.dao.model.monthlyReport.loan_balance_model import LoanBalance
from app.dao.model.monthlyReport.stock_net_value_model import StockNetValueHistory
from app.dao.model.otherAsset.estate_model import Estate
from app.dao.model.otherAsset.insurance_model import Insurance
from app.dao.model.otherAsset.stock_journal_model import StockJournal
from app.dao.model.setting.account_model import Account
from app.dao.model.setting.credit_card_model import CreditCard

date_format = '%Y-%m-%dT%H:%M:%S.%fZ'


def init_journal_api(app):
    @app.route('/journal/<string:vestingMonth>', methods=['GET'])
    def getJournalsByVestingMonth(vestingMonth):
        output = []

        try:
            journals = Journal.queryByVestingMonth(Journal, vestingMonth)
            for journal in journals:
                output.append(Journal.output(Journal, journal))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/journal', methods=['POST'])
    def addJournal():
        global date_format

        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)
            inputData['spend_date'] = datetime.strptime(
                inputData['spend_date'], date_format)
            journal = Journal(inputData)

            result = Journal.add(Journal, journal)
            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, Journal.output(Journal, result)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add journal data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/journal/<int:journalId>', methods=['PUT'])
    def updateJournal(journalId):
        global date_format

        try:
            journal = Journal.queryByKey(Journal, journalId)
            if journal is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                journal.spend_date = datetime.strptime(
                    inputData['spend_date'], date_format)
                journal.spend_way = inputData['spend_way']
                journal.spend_way_type = inputData['spend_way_type']
                journal.spend_way_table = inputData['spend_way_table']
                journal.action_main = inputData['action_main']
                journal.action_main_table = inputData['action_main_table']
                journal.action_sub = inputData['action_sub']
                journal.action_sub_table = inputData['action_sub_table']
                journal.spending = inputData['spending']
                journal.note = inputData['note']

                if Journal.update(Journal):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update journal data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/journal/<int:journalId>', methods=['DELETE'])
    def deleteJournal(journalId):
        try:
            journal = Journal.queryByKey(Journal, journalId)
            if journal is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if Journal.delete(Journal, journalId):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete journal data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/balance/<string:vestingMonth>', methods=['PUT'])
    def setMonthlySummary(vestingMonth):
        try:

            lastMonth = int(vestingMonth) - \
                1 if int(vestingMonth) - \
                1 % 10 != 0 else (int(vestingMonth[:4])-1)*100+12

            # 其他資產若是沒有本月份資料才塞，因為不會漏掉補帳
            estateOrLiabilityRecords = Journal.queryEstateOrLiabilityRecord(
                Journal, vestingMonth)
            for record in estateOrLiabilityRecords:
                if record.name == 'Estate' and record.has_record == 0:
                    estates = Estate.query4Summary(Estate, str(lastMonth))
                    for estate in estates:
                        obj = EstateNetValueHistory(estate)
                        obj.vesting_month = vestingMonth
                        EstateNetValueHistory.add(
                            EstateNetValueHistory, obj)
                elif record.name == 'Insurance' and record.has_record == 0:
                    insurances = Insurance.query4Summary(
                        Insurance, str(lastMonth))
                    for insurance in insurances:
                        obj = InsuranceNetValueHistory(insurance)
                        obj.vesting_month = vestingMonth
                        InsuranceNetValueHistory.add(
                            InsuranceNetValueHistory, obj)
                elif record.name == 'Loan' and record.has_record == 0:
                    loans = Loan.query4Summary(Loan, str(lastMonth))
                    for loan in loans:
                        obj = LoanBalance(loan)
                        obj.vesting_month = vestingMonth
                        LoanBalance.add(LoanBalance, obj)
                elif record.name == 'Stock' and record.has_record == 0:
                    stocks = StockJournal.query4Summary(
                        StockJournal, str(lastMonth))
                    for stock in stocks:
                        obj = StockNetValueHistory(stock)
                        obj.vesting_month = vestingMonth
                        StockNetValueHistory.add(StockNetValueHistory, obj)

            # 先清掉含本月份之後的資料
            AccountBalance.delete(AccountBalance, vestingMonth)
            CreditCardBalance.delete(CreditCardBalance, vestingMonth)
            journals = Journal.queryByVestingMonth(Journal, vestingMonth)
            journals.sort(key=lambda item: (
                item.spend_way_table, item.spend_way))
            accounts = Account.query4Summary(Account, str(lastMonth))
            cards = CreditCard.query4Summary(CreditCard, str(lastMonth))

            accountArray = []
            for account in accounts:
                obj = AccountBalance(account)
                obj.vesting_month = vestingMonth
                for journal in journals:
                    # 處理扣項金額
                    if journal.spend_way_table == 'Account' and obj.id == int(journal.spend_way):
                        obj.balance += journal.spending
                    # 處理加項金額
                    elif journal.action_sub_table == 'Account' and obj.id == int(journal.action_sub):
                        obj.balance -= journal.spending

                accountArray.append(obj)

            cardArray = []
            for card in cards:
                obj = CreditCardBalance(card)
                obj.vesting_month = vestingMonth
                for journal in journals:
                    # 處理扣項金額
                    if journal.spend_way_table == 'Credit_Card' and obj.id == int(journal.spend_way):
                        obj.balance += journal.spending
                    # 處理加項金額
                    elif journal.action_sub_table == 'Credit_Card' and obj.id == int(journal.action_sub):
                        obj.balance -= journal.spending
                print('123', journal.spend_way_table,
                      obj.id, journal.spend_way, journal.action_sub)

                cardArray.append(obj)

            result = AccountBalance.bulkInsert(
                AccountBalance, accountArray) and CreditCardBalance.bulkInsert(CreditCardBalance, cardArray)

            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, None, 'Success'))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to process summary data'))
        except Exception as error:
            print('789', error)
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
