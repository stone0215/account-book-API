# -*- coding: UTF-8 -*-

from datetime import datetime
from flask import jsonify, request
from itertools import groupby

from api.response_format import ResponseFormat
from app.dao.model.liability.loan_model import Loan
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
from app.dao.model.setting.budget_model import Budget
from app.dao.model.setting.credit_card_model import CreditCard
from app.dao.model.dashboard.stock_price_history_model import StockPriceHistory

date_format = '%Y-%m-%dT%H:%M:%S.%fZ'


def init_journal_api(app):
    @app.route('/journal/<string:vestingMonth>', methods=['GET'])
    def getJournalsByVestingMonth(vestingMonth):
        journalList = []
        gainLoss = 0

        try:
            journals = Journal.queryByVestingMonth(Journal, vestingMonth)
            for journal in journals:
                if journal.action_main_table == 'Code':
                    gainLoss += round(journal.spending * journal.fx_rate, 2)

                journalList.append(Journal.output(Journal, journal))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, {"journalList": journalList, "gainLoss": gainLoss}))

    @app.route('/journal/expenditure-ratio/<string:vestingMonth>', methods=['GET'])
    def getExpenditureRatioByVestingMonth(vestingMonth):

        try:
            journals = Journal.queryForExpenditureRatio(
                Journal, vestingMonth, 'action_main_type')

            expendingInnerPie = []
            for key, groups in groupby(journals, lambda item: item.action_main_type):
                spendings = [item.spending for item in list(groups)]
                expendingInnerPie.append(
                    {'name': key, 'value': abs(round(sum(spendings), 2))})  # 取絕對值計算百分比

            # 不確定是因為 groupby 後 journals 被清空還是什麼原因導致資料表被釋放，所以需要重撈，之後可以考慮改 panda
            journals = Journal.queryForExpenditureRatio(
                Journal, vestingMonth, 'action_main')
            expendingOuterPie = []
            for key, groups in groupby(journals, lambda item: (item.action_main, item.action_main_name, item.action_main_type)):
                spendings = [item.spending for item in list(groups)]
                expendingOuterPie.append({'name': key[1],
                                          'type': key[2],
                                          'value': abs(round(sum(spendings), 2))})

        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, {'expendingInnerPie': expendingInnerPie, 'expendingOuterPie': expendingOuterPie}))

    @app.route('/journal/invest-ratio/<string:vestingMonth>', methods=['GET'])
    def getInvestRatioByVestingMonth(vestingMonth):

        try:
            assets = Journal.queryForInvestRatio(
                Journal, vestingMonth)
            assetOuterPie = []
            for key, groups in groupby(assets, lambda item: (item.action, item.target)):
                spendings = [item.spending for item in list(groups)]
                assetOuterPie.append({'name': key[1],
                                      'type': key[0],
                                      'value': round(sum(spendings), 2)})

        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, assetOuterPie))

    @app.route('/journal/expenditure-budget/<string:vestingMonth>', methods=['GET'])
    def getExpenditureBudgetByVestingMonth(vestingMonth):
        output = []

        try:
            budgets = Budget.queryForExpenditureBudget(Budget, vestingMonth)
            for budget in budgets:
                output.append(Budget.outputForBudget(Budget, budget))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/journal/liability/<string:vestingMonth>', methods=['GET'])
    def getLiabilityByVestingMonth(vestingMonth):
        output = []

        try:
            liabilities = CreditCardBalance.queryForLiabilities(
                CreditCardBalance, vestingMonth)
            for liability in liabilities:
                output.append(CreditCardBalance.outputForLiability(
                    CreditCardBalance, liability))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/stock/price/<string:vestingMonth>', methods=['GET'])
    def getStockPriceByVestingMonth(vestingMonth):
        output = []

        try:
            stocks = StockPriceHistory.queryByVestingMonth(
                StockPriceHistory, vestingMonth)
            for stock in stocks:
                output.append(StockPriceHistory.output(
                    StockPriceHistory, stock))
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

    @app.route('/stock/price', methods=['POST'])
    def updateStockPrice():

        try:
            inputData = request.get_json(force=True)
            inputData['fetch_date'] = datetime.strptime(
                inputData['fetch_date'], '%Y-%m-%d %H:%M:%S')
            stock = StockPriceHistory(inputData)

            if StockPriceHistory.add(StockPriceHistory, stock):
                return jsonify(ResponseFormat.true_return(ResponseFormat, True))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add stock price data'))
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
                journal.action_main_type = inputData['action_main_type']
                journal.action_main_table = inputData['action_main_table']
                journal.action_sub = inputData['action_sub']
                journal.action_sub_type = inputData['action_sub_type']
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
            estateOrLiabilityRecords = Journal.queryEstateOrLiabilityRecord(
                Journal, vestingMonth).fetchall()  # fetchall 可關閉資料庫 cursor 狀態，避免 table lock，導致後續無法 delete
            for record in estateOrLiabilityRecords:
                if record.name == 'Estate':
                    # 清掉已存在的資料重塞
                    if record.has_record != 0:
                        EstateNetValueHistory.deleteByVestingMonth(
                            EstateNetValueHistory, vestingMonth)

                    estates = Estate.query4Summary(Estate, vestingMonth)
                    for estate in estates:
                        obj = EstateNetValueHistory(estate)
                        obj.vesting_month = vestingMonth
                        EstateNetValueHistory.add(
                            EstateNetValueHistory, obj)
                elif record.name == 'Insurance':
                    # 清掉已存在的資料重塞
                    if record.has_record != 0:
                        InsuranceNetValueHistory.deleteByVestingMonth(
                            InsuranceNetValueHistory, vestingMonth)

                    insurances = Insurance.query4Summary(
                        Insurance, vestingMonth)
                    for insurance in insurances:
                        obj = InsuranceNetValueHistory(insurance)
                        obj.vesting_month = vestingMonth
                        InsuranceNetValueHistory.add(
                            InsuranceNetValueHistory, obj)
                elif record.name == 'Loan':
                    # 清掉已存在的資料重塞
                    if record.has_record != 0:
                        LoanBalance.deleteByVestingMonth(
                            LoanBalance, vestingMonth)

                    loans = Loan.query4Summary(Loan, vestingMonth)
                    for loan in loans:
                        obj = LoanBalance(loan)
                        obj.vesting_month = vestingMonth
                        LoanBalance.add(LoanBalance, obj)
                elif record.name == 'Stock':
                    # 清掉已存在的資料重塞
                    if record.has_record != 0:
                        StockNetValueHistory.deleteByVestingMonth(
                            StockNetValueHistory, vestingMonth)

                    stocks = StockJournal.query4Summary(
                        StockJournal, vestingMonth)
                    for stock in stocks:
                        obj = StockNetValueHistory(stock)
                        obj.amount = round(
                            stock.positive_amount, 6)+round(stock.negative_amount, 6)
                        obj.price = stock.close_price*obj.amount
                        obj.cost = stock.positive_cost+stock.negative_cost
                        if obj.amount != 0:
                            obj.vesting_month = vestingMonth
                            StockNetValueHistory.add(StockNetValueHistory, obj)

            lastMonth = int(vestingMonth) - \
                1 if (int(vestingMonth) -
                      1) % 100 != 0 else (int(vestingMonth[:4])-1)*100+12
            # 先清掉含本月份之後的資料
            AccountBalance.delete(AccountBalance, vestingMonth)
            CreditCardBalance.delete(CreditCardBalance, vestingMonth)
            journals = Journal.queryByVestingMonth(
                Journal, vestingMonth).fetchall()
            journalList = []
            for journal in journals:
                journalList.append({
                    'spend_way_table': journal.spend_way_table,
                    'spend_way': journal.spend_way,
                    'spending': journal.spending,
                    'action_sub_table': journal.action_sub_table,
                    'action_sub': journal.action_sub,
                    'spend_way_type': journal.spend_way_type,
                    'action_sub_type': journal.action_sub_type,
                    'note': journal.note
                })
            journalList.sort(key=lambda item: (
                item['spend_way_table'], item['spend_way']))
            accounts = Account.query4Summary(
                Account, lastMonth, vestingMonth).fetchall()
            cards = CreditCard.query4Summary(
                CreditCard, lastMonth, vestingMonth).fetchall()

            accountArray = AccountBalance.culculateBalance(
                AccountBalance, vestingMonth, journalList, accounts)

            cardArray = CreditCardBalance.culculateBalance(
                CreditCardBalance, vestingMonth, journalList, cards)

            result = False
            if (len(accountArray) > 0):
                result = AccountBalance.bulkInsert(
                    AccountBalance, accountArray)

            if (len(cardArray) > 0):
                result = CreditCardBalance.bulkInsert(
                    CreditCardBalance, cardArray)

            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, None, 'Success'))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to process summary data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
