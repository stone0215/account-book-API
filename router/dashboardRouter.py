from datetime import datetime
from flask import jsonify, request
from itertools import groupby
from dateutil.relativedelta import relativedelta

from api.response_format import ResponseFormat
from app.dao.model.monthlyReport.journal_model import Journal
# from app.dao.model.liability.loan_model import Loan
# from app.dao.model.monthlyReport.credit_card_balance_model import CreditCardBalance
# from app.dao.model.setting.credit_card_model import CreditCard
from app.dao.model.otherAsset.other_asset_model import OtherAsset
from app.dao.model.monthlyReport.loan_balance_model import LoanBalance
from app.dao.model.setting.budget_model import Budget
from app.dao.model.dashboard.target_setting_model import TargetSetting
from app.dao.model.setting.alarm_model import Alarm
from router.yearReport.reportRouter import getBalanceSheetByNow


def init_dashboard_api(app):
    @app.route('/dashboard/summary/<string:type>/<string:period>', methods=['GET'])
    def getSummary(type, period):
        output = {}

        try:
            strFormat = '%Y%m' if type == 'month' else '%Y'

            # 取得收入與支出
            journals = Journal.queryForSpendingReport(
                Journal, period, period, strFormat)
            groupedJournalValues = []
            for key, groups in groupby(journals, lambda item: item.action_main_type):
                spendings = [item.spending for item in list(groups)]
                groupedJournalValues.append(
                    {'name': key, 'value': abs(sum(spendings))})  # 取絕對值計算百分比

            if len(groupedJournalValues) > 0:
                floatValue = [data for data in groupedJournalValues if data.get(
                    'name') == 'Floating'][0]['value']
                fixValue = [data for data in groupedJournalValues if data.get(
                    'name') == 'Fixed'][0]['value']
                passiveValue = [data for data in groupedJournalValues if data.get(
                    'name') == 'Passive'][0]['value']
                IncomeValue = [data for data in groupedJournalValues if data.get(
                    'name') == 'Income'][0]['value']

                output['spending'] = floatValue+fixValue
                output['workFreedom'] = round(
                    (passiveValue/(passiveValue+IncomeValue))*100, 2)

            # 取得歷史資料--年度則撈每年12月，共十年，月份直接將 period 帶進去撈12個月
            inputDate = datetime.strptime(period, strFormat)
            start = (inputDate+(relativedelta(months=-11) if type ==
                                'month' else relativedelta(years=-10)))
            end = inputDate.strftime(strFormat)

            # 歷史資產
            assets = OtherAsset.getAssetBalanceHistory(
                OtherAsset, start.strftime(strFormat), end, type)
            groupedAssetValues = []
            mappedDate = start
            for key, groups in groupby(assets, lambda item: item.dateString):
                balances = [round(item.balance*item.fx_rate, 2)
                            for item in list(groups)]
                while mappedDate.strftime(strFormat) != key:
                    groupedAssetValues.append({'dateString': mappedDate.strftime(strFormat),
                                               'type': 'asset',
                                               'value': 0})
                    mappedDate = (mappedDate+(relativedelta(months=1) if type ==
                                              'month' else relativedelta(years=1)))

                groupedAssetValues.append({'dateString': key,
                                           'type': 'asset',
                                           'value': sum(balances)})
                mappedDate = (mappedDate+(relativedelta(months=1) if type ==
                                          'month' else relativedelta(years=1)))
            # 歷史負債
            debts = LoanBalance.getDebtBalanceHistory(
                LoanBalance, start.strftime(strFormat), end, type)
            groupedDebtValues = []
            mappedDate = start
            for key, groups in groupby(debts, lambda item: item.dateString):
                balances = [round(abs(item.balance)*item.fx_rate, 2)
                            for item in list(groups)]
                while mappedDate.strftime(strFormat) != key:
                    groupedDebtValues.append({'dateString': mappedDate.strftime(strFormat),
                                              'type': 'asset',
                                              'value': 0})
                    mappedDate = (mappedDate+(relativedelta(months=1) if type ==
                                              'month' else relativedelta(years=1)))

                groupedDebtValues.append({'dateString': key,
                                          'type': 'debt',
                                          'value': sum(balances)})
                mappedDate = (mappedDate+(relativedelta(months=1) if type ==
                                          'month' else relativedelta(years=1)))

            lastPeriod = period if type == 'month' else period+'12'
            # 有資產的資料就代表負債也關帳了
            thisPeriodData = [data for data in groupedAssetValues if data.get(
                'dateString') == lastPeriod]
            assetValue = 0
            liabilityValue = 0
            # 取得 period 條件下的資產與負債--如果上面的資料有 period 的資料，那就不用做下面這段
            if len(thisPeriodData) == 0:
                balanceSheetValue = getBalanceSheetByNow()

                for item in balanceSheetValue['assets']:
                    assetValue += item['amount']

                for item in balanceSheetValue['debts']:
                    liabilityValue += item['amount']

                groupedAssetValues.append({'dateString': period,
                                           'type': 'asset',
                                           'value': assetValue})
                groupedDebtValues.append({'dateString': period,
                                          'type': 'debt',
                                          'value': liabilityValue})
            else:
                assetValue = thisPeriodData[0]['value']
                liabilityValue = [data for data in groupedDebtValues if data.get(
                    'dateString') == lastPeriod][0]['value']

            thisNetAssetValue = assetValue-liabilityValue
            lastNetAssetValue = groupedAssetValues[len(
                groupedAssetValues)-2]['value']-groupedDebtValues[len(groupedDebtValues)-2]['value']

            if len(groupedJournalValues) > 0:
                output.freedom = round(
                    (thisNetAssetValue/(floatValue+fixValue))*100, 2)

            output['debt'] = liabilityValue
            output['asset'] = assetValue
            output['assetBalanceChart'] = groupedAssetValues
            output['debtBalanceChart'] = groupedDebtValues
            output['netAssetGrowth'] = round(
                ((thisNetAssetValue-lastNetAssetValue)/lastNetAssetValue)*100, 2)

        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat,  output))

    @app.route('/dashboard/budget/<string:type>/<string:period>', methods=['GET'])
    def getBudgetUsed(type, period):
        try:
            budgetValue = 0
            budgets = Budget.query4Summary(
                Budget, period[0:4] if type == 'month' else period)

            row = budgets.fetchone()
            if type == 'month':
                budgetValue = row['expected'+period[4:]]
            else:
                for key, value in row.items():
                    budgetValue += value

        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, abs(budgetValue)))

    @app.route('/dashboard/alarm', methods=['GET'])
    def getAlarmList():
        try:
            thisMonth = datetime.now().strftime("%Y%m")
            lastMonth = (datetime.now()+(relativedelta(months=6))
                         ).strftime("%Y%m")

            output = []
            # 用六個月跑撈出來的資料，如果到期日小於六個月的某個月就不塞，只塞到期日還沒到的
            alarms = Alarm.queryByPeriod(Alarm, thisMonth, lastMonth)
            for alarm in alarms:
                if (alarm.alarm_type == 'M'):
                    for i in range(0, 6):
                        month = (datetime.now() +
                                 (relativedelta(months=i)))
                        # 目前要跑得月份小於到期日才加
                        if alarm.due_date == None or (alarm.due_date and month.strftime('%Y%m') <= datetime.strptime(alarm.due_date, '%Y-%m-%d').strftime('%Y%m')):
                            output.append({
                                'date': month.strftime('%m') + '/' + alarm.alarm_date,
                                'content': alarm.content
                            })
                else:
                    output.append({
                        'date': alarm.alarm_date,
                        'content': alarm.content
                    })

        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/dashboard/gift/<string:year>', methods=['GET'])
    def getGiftedList(year):
        gifts = Journal.getGiftedList(Journal, year)
        output = []
        for gift in gifts:
            output.append(Journal.outputForGifted(Journal, gift))
        return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/dashboard/target', methods=['GET'])
    def getTargets():
        targets = TargetSetting.get_all(TargetSetting)
        output = []
        for target in targets:
            output.append(TargetSetting.output(TargetSetting, target))
        return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/target', methods=['POST'])
    def addTarget():
        global date_format

        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)
            inputData['target_year'] = datetime.now().strftime("%Y")
            inputData['is_done'] = 'N'
            target = TargetSetting(inputData)

            result = TargetSetting.add(TargetSetting, target)
            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, TargetSetting.output(TargetSetting, result)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add journal data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/target/<int:id>', methods=['PUT'])
    def updateTarget(id):
        try:
            target = TargetSetting.queryByKey(TargetSetting, id)
            if target is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                target.setting_value = inputData['setting_value']
                target.is_done = inputData['is_done']

                if TargetSetting.update(TargetSetting):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update account data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/target/<int:id>', methods=['DELETE'])
    def deleteTarget(id):
        target = TargetSetting.queryByKey(TargetSetting, id)
        if target is None:
            return jsonify(ResponseFormat.false_return(ResponseFormat, None, '找不到要删除的数据'))
        else:
            TargetSetting.delete(TargetSetting, id)

            if TargetSetting.delete(TargetSetting, id):
                return jsonify(ResponseFormat.true_return(ResponseFormat, None))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, '删除失败'))
