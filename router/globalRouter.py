from datetime import datetime, timedelta
from flask import jsonify
from threading import Thread
import time
import requests

from api.response_format import ResponseFormat

from app.dao.model.dashboard.fx_rate_model import FXRate
from app.dao.model.monthlyReport.journal_model import Journal
from app.dao.model.setting.credit_card_model import CreditCard

invoicePayload = {'appID': 'your app id', 'cardEncrypt': 'your password',
                  'cardNo': 'your card'}


def init_global_api(app):

    @app.route('/global/server-alive')
    def serverAlive():
        return jsonify(ResponseFormat.true_return(ResponseFormat, True))

    @app.route('/global/checkFxRate', methods=['POST'])
    def importFxRate():
        datas = []

        try:
            # 寫法一
            response = requests.get(
                'https://openapi.taifex.com.tw/v1/DailyForeignExchangeRates')

            fxRateList = response.json()
            for rate in fxRateList:
                date = None
                usd = None  # 記錄USD/NTD，作為與台幣匯率換算的基礎
                for key in rate.keys():
                    if key == 'Date':
                        date = datetime.strptime(rate[key], "%Y%m%d")
                    else:
                        rawRate = key.split('/')
                        value = float(rate[key])

                        if rawRate[1] == 'NTD':
                            if rawRate[0] == 'USD':
                                usd = value

                            datas.append(
                                {'import_date': date, 'code': rawRate[0], 'buy_rate': value})
                        elif rawRate[1] != 'RMB':  # RMB 已有 NTD 匯兌，所以要過濾
                            if rawRate[0] == 'USD':
                                datas.append(
                                    {'import_date': date, 'code': rawRate[1], 'buy_rate': round(usd / value, 4)})
                            else:
                                datas.append(
                                    {'import_date': date, 'code': rawRate[0], 'buy_rate': round(usd * value, 4)})

            result = FXRate.bulkInsert(FXRate, datas)

            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, None, 'Success'))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to build fx rate history'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/global/checkInvoice', methods=['POST'])
    def checkInvoice():
        # print('456', app.app_context().push())
        t = Thread(target=importInvoice)  # , args=(data, ))
        t.start()

        return jsonify(ResponseFormat.true_return(ResponseFormat, None, 'invoice is importing...'))

    def importInvoice():
        global invoicePayload
        today = datetime.today().date()

        result = None

        try:
            invoicePayload['version'] = '0.5'
            invoicePayload['cardType'] = '3J0002'
            invoicePayload['action'] = 'carrierInvChk'
            invoicePayload['onlyWinningInv'] = 'N'
            invoicePayload['uuid'] = '123456'
            invoicePayload['expTimeStamp'] = invoicePayload['timeStamp'] = int(
                datetime.now().timestamp())+100
            invoicePayload['startDate'] = today.strftime("%Y/%m/01")
            invoicePayload['endDate'] = today.strftime("%Y/%m/%d")

            invoiceList = requests.post(
                'https://api.einvoice.nat.gov.tw/PB2CAPIVAN/invServ/InvServ', params=invoicePayload, timeout=(10, 30))

            if invoiceList.json()['code'] == 200:
                datas = []
                data = {
                    'vesting_month': today.strftime("%Y%m"),
                    'action_main': 'No',
                    'action_main_type': 'No',
                    'action_main_table': 'No',
                    'action_sub': 'No',
                    'action_sub_type': 'No',
                    'action_sub_table': 'No',
                    'note': ''
                }

                with app.app_context():  # 因為新開 thread 但共用 db 所以需要指定
                    for invoice in invoiceList.json()['details']:
                        hasRecorded = Journal.queryByVestingMonthAndInvoice(
                            Journal, data['vesting_month'], invoice['invNum'])

                        # 如果找不到相關資料才寫入
                        if hasRecorded is None:
                            data['spend_date'] = datetime.utcfromtimestamp(
                                int(invoice['invDate']['time']/1000))  # 轉 UTC+0 DATE，参数要的长度是10位
                            data['invoice_number'] = invoice['invNum']
                            data['spending'] = -int(invoice['amount'])

                            # 利用載具號碼找出相對應消費方式:
                            carrierNo = CreditCard.queryByCarrierNo(
                                CreditCard, invoice['cardNo'])
                            if carrierNo is None:
                                data['spend_way'] = 'No'
                                data['spend_way_type'] = 'No'
                                data['spend_way_table'] = 'No'
                            else:
                                data['spend_way'] = carrierNo.id
                                data['spend_way_type'] = carrierNo.type
                                data['spend_way_table'] = carrierNo.table_name

                            # 取得發票消費明細
                            invoicePayload['expTimeStamp'] = invoicePayload['timeStamp'] = int(
                                datetime.now().timestamp())+100
                            invoicePayload['action'] = 'carrierInvDetail'
                            invoicePayload['invNum'] = invoice['invNum']
                            invoicePayload['invDate'] = datetime.fromtimestamp(int(invoice['invDate']['time']/1000)).strftime(
                                "%Y/%m/%d")
                            invoicePayload['amount'] = invoice['amount']

                            invoiceDetail = requests.post(
                                'https://api.einvoice.nat.gov.tw/PB2CAPIVAN/invServ/InvServ', params=invoicePayload, timeout=(10, 30))

                            if invoiceDetail.json()['code'] == 200:
                                for detail in invoiceDetail.json()['details']:
                                    data['note'] = f"{data['note']}{detail['description']} {detail['amount']}, "

                                datas.append(Journal(data))
                                data['note'] = ''
                                time.sleep(1)

                    Journal.bulkInsert(Journal, datas)
        except Exception as error:
            # 如果出錯就重新執行，直到沒有錯誤為止
            print('456', error)
            importInvoice()
