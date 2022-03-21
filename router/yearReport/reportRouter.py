from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask import jsonify

from api.response_format import ResponseFormat
from app.dao.model.monthlyReport.journal_model import Journal
from app.dao.model.setting.account_model import Account
from app.dao.model.monthlyReport.account_balance_model import AccountBalance
from app.dao.model.otherAsset.stock_journal_model import StockJournal
from app.dao.model.monthlyReport.stock_net_value_model import StockNetValueHistory
from app.dao.model.otherAsset.insurance_model import Insurance
from app.dao.model.monthlyReport.insurance_net_value_model import InsuranceNetValueHistory
from app.dao.model.otherAsset.estate_model import Estate
from app.dao.model.monthlyReport.estate_net_value_model import EstateNetValueHistory
from app.dao.model.setting.credit_card_model import CreditCard
from app.dao.model.monthlyReport.credit_card_balance_model import CreditCardBalance
from app.dao.model.liability.loan_model import Loan
from app.dao.model.monthlyReport.loan_balance_model import LoanBalance
from app.dao.model.liability.loan_journal_model import LoanJournal


def init_report_api(app):
    @app.route('/report/balance', methods=['GET'])
    def getBalanceSheet():
        try:
            result = getBalanceSheetByNow()
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, result))

    @app.route('/report/expenditure/<string:type>/<string:vestingMonth>', methods=['GET'])
    def getSpendingReport(type, vestingMonth):
        try:
            strFormat = '%Y%m' if type == 'month' else '%Y'
            inputDate = datetime.strptime(vestingMonth, strFormat)
            start = (inputDate+(relativedelta(months=-11) if type ==
                                'month' else relativedelta(years=-10))).strftime(strFormat)
            end = inputDate.strftime(strFormat)

            # 取得收入與支出
            journals = Journal.queryForSpendingReport(
                Journal, start, end, strFormat)
            # 取得貸款
            loans = LoanJournal.queryForSpendingReport(
                LoanJournal, start, end, strFormat)

            output = []
            for journal in journals:
                output.append(Journal.outputForReport(Journal, journal))
            for loan in loans:
                output.append(LoanJournal.outputForReport(LoanJournal, loan))

        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/report/asset', methods=['GET'])
    def getAssetReport():
        try:
            thisMonth = datetime.now().strftime("%Y%m")
            lastMonth = (datetime.now().replace(day=1) -
                         timedelta(days=1)).strftime("%Y%m")

            output = []
            # 取得現金資產
            journals = Journal.queryByVestingMonth(Journal, thisMonth)
            accounts = Account.query4Summary(Account, '', thisMonth)
            accountArray = AccountBalance.culculateBalance(
                AccountBalance, thisMonth, journals, accounts)
            for account in accountArray:
                if account.is_calculate == 'Y':
                    output.append(AccountBalance.outputForReport(
                        AccountBalance, account))

            # 取得不動產資產
            estates = Estate.query4Summary(Estate, thisMonth)
            for asset in estates:
                output.append(EstateNetValueHistory.outputForReport(
                    EstateNetValueHistory, asset))

            # 取得保險資產
            insurances = Insurance.query4Summary(Insurance, thisMonth)
            for insurance in insurances:
                output.append(InsuranceNetValueHistory.outputForReport(
                    InsuranceNetValueHistory, insurance))

            # 取得股票資產
            stocks = StockJournal.query4Summary(StockJournal, thisMonth)
            for stock in stocks:
                if stock.amount > 0:
                    output.append(StockNetValueHistory.outputForReport(
                        StockNetValueHistory, stock))

        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))


def getBalanceSheetByNow():
    try:
        thisMonth = datetime.now().strftime("%Y%m")
        lastMonth = (datetime.now().replace(day=1) -
                     timedelta(days=1)).strftime("%Y%m")

        journals = Journal.queryByVestingMonth(Journal, thisMonth)
        if journals.rowcount == -1:
            journals = []
        else:
            journals.sort(key=lambda item: (
                item.spend_way_table, item.spend_way))
        accounts = Account.query4Summary(Account, '', thisMonth).fetchall()

        # 取得現金資產
        accountBalances = AccountBalance.culculateBalance(
            AccountBalance, accounts[0]['vesting_month'] if len(accounts) else thisMonth, journals, accounts)
        # 取得股票資產
        stocks = StockJournal.query4Summary(StockJournal, thisMonth)
        # 取得儲蓄險資產
        insurances = Insurance.query4Summary(Insurance, thisMonth)
        # 取得不動產資產
        estates = Estate.query4Summary(Estate, thisMonth)

        assets = []
        assets.append(AccountBalance.outputForBalanceSheet(
            AccountBalance, accountBalances))
        assets.append(StockNetValueHistory.outputForBalanceSheet(
            StockNetValueHistory, stocks))
        assets.append(InsuranceNetValueHistory.outputForBalanceSheet(
            InsuranceNetValueHistory, insurances))
        assets.append(EstateNetValueHistory.outputForBalanceSheet(
            EstateNetValueHistory, estates))

        cards = CreditCard.query4Summary(CreditCard, '', thisMonth)

        # 取得信用卡負債
        cardBalances = CreditCardBalance.culculateBalance(
            CreditCardBalance, thisMonth, journals, cards)
        # 取得貸款負債
        loans = Loan.query4Summary(Loan, thisMonth)

        debts = []
        debts.append(CreditCardBalance.outputForBalanceSheet(
            CreditCardBalance, cardBalances))
        debts.append(LoanBalance.outputForBalanceSheet(LoanBalance, loans))

    except Exception as error:
        raise
    else:
        return {'assets': assets, 'debts': debts}
