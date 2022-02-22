from datetime import datetime, timedelta
from flask import jsonify, request
from threading import Thread
import time
import requests
import yfinance

from api.response_format import ResponseFormat

from app.dao.model.dashboard.fx_rate_model import FXRate
from app.dao.model.monthlyReport.journal_model import Journal
from app.dao.model.setting.credit_card_model import CreditCard
from app.dao.model.otherAsset.stock_journal_model import StockJournal
from app.dao.model.dashboard.stock_price_history_model import StockPriceHistory


def init_global_api(app):
    invoicePayload = {
        "appID": app.config['INVOICE_APP_ID'],
        "cardEncrypt": app.config['INVOICE_PASSWORD'],
        "cardNo": app.config['INVOICE_CARD_NO'],
    }

    @app.route("/global/server-alive")
    def serverAlive():
        return jsonify(ResponseFormat.true_return(ResponseFormat, True))

    @app.route("/global/check/<string:dataType>", methods=["POST"])
    def checkImportData(dataType):
        inputData = request.get_json(force=True)

        try:
            if dataType == "invoice":
                invoiceThread = Thread(
                    target=importInvoice, args=(inputData['period'], ))
                invoiceThread.start()
            elif dataType == 'stock':
                # , args=(data, ))
                stockThread = Thread(
                    target=importStockPrice, args=(inputData['period'], ))
                stockThread.start()
            else:
                fxThread = Thread(target=importFxRate)
                fxThread.start()

            return jsonify(
                ResponseFormat.true_return(
                    ResponseFormat, None, f"{dataType} is importing..."
                )
            )

        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    def importFxRate():
        with app.app_context():  # 因為新開 thread 但共用 db 所以需要指定
            datas = []

            # 寫法一
            # response = requests.get(
            #     'https://openapi.taifex.com.tw/v1/DailyForeignExchangeRates')

            # fxRateList = response.json()
            # for rate in fxRateList:
            #     date = None
            #     usd = None  # 記錄USD/NTD，作為與台幣匯率換算的基礎
            #     for key in rate.keys():
            #         if key == 'Date':
            #             date = datetime.strptime(rate[key], "%Y%m%d")
            #         else:
            #             rawRate = key.split('/')
            #             value = float(rate[key])

            #             if rawRate[1] == 'NTD':
            #                 if rawRate[0] == 'USD':
            #                     usd = value

            #                 datas.append(
            #                     {'import_date': date, 'code': rawRate[0], 'buy_rate': value})
            #             elif rawRate[1] != 'RMB':  # RMB 已有 NTD 匯兌，所以要過濾
            #                 if rawRate[0] == 'USD':
            #                     datas.append(
            #                         {'import_date': date, 'code': rawRate[1], 'buy_rate': round(usd / value, 4)})
            #                 else:
            #                     datas.append(
            #                         {'import_date': date, 'code': rawRate[0], 'buy_rate': round(usd * value, 4)})

            response = requests.get(
                "https://mma.sinopac.com/ws/share/rate/ws_exchange.ashx?exchangeType=REMIT"
            )

            data = response.json()
            date = datetime.utcfromtimestamp(
                datetime.strptime(
                    data[0]["TitleInfo"].split("：", 1)[1].split("<br>", 1)[0],
                    "%Y-%m-%d %H:%M:%S",
                ).timestamp()
            )

            for rate in data[0]["SubInfo"]:
                hasRecorded = FXRate.queryByKey(
                    FXRate, date, rate["DataValue4"])

                if hasRecorded["recordNum"] == 0:
                    datas.append(
                        {
                            "import_date": date,
                            "code": rate["DataValue4"],
                            "buy_rate": rate["DataValue2"],
                        }
                    )

            if len(datas):
                FXRate.bulkInsert(FXRate, datas)

    def importInvoice(period):
        invoicePayload
        today = datetime.today().date() if period == '' else datetime.strptime(
            period, '%Y%m').replace(day=28) + timedelta(days=4)

        today = today - timedelta(days=today.day)

        result = None

        try:
            invoicePayload["version"] = "0.5"
            invoicePayload["cardType"] = "3J0002"
            invoicePayload["action"] = "carrierInvChk"
            invoicePayload["onlyWinningInv"] = "N"
            invoicePayload["uuid"] = "123456"
            invoicePayload["expTimeStamp"] = invoicePayload["timeStamp"] = (
                int(datetime.now().timestamp()) + 100
            )
            invoicePayload["startDate"] = today.strftime("%Y/%m/01")
            invoicePayload["endDate"] = today.strftime("%Y/%m/%d")

            invoiceList = requests.post(
                "https://api.einvoice.nat.gov.tw/PB2CAPIVAN/invServ/InvServ",
                params=invoicePayload,
                timeout=(10, 30),
            )

            if invoiceList.json()["code"] == 200:
                datas = []
                data = {
                    "vesting_month": today.strftime("%Y%m"),
                    "action_main": "No",
                    "action_main_type": "No",
                    "action_main_table": "No",
                    "action_sub": "No",
                    "action_sub_type": "No",
                    "action_sub_table": "No",
                    "note": "",
                }

                with app.app_context():  # 因為新開 thread 但共用 db 所以需要指定
                    for invoice in invoiceList.json()["details"]:
                        hasRecorded = Journal.queryByVestingMonthAndInvoice(
                            Journal, data["vesting_month"], invoice["invNum"]
                        )

                        # 如果找不到相關資料才寫入
                        if hasRecorded is None:
                            data["spend_date"] = datetime.utcfromtimestamp(
                                int(invoice["invDate"]["time"] / 1000)
                            )  # 轉 UTC+0 DATE，参数要的长度是10位
                            data["invoice_number"] = invoice["invNum"]
                            data["spending"] = -int(invoice["amount"])

                            # 利用載具號碼找出相對應消費方式:
                            carrierNo = CreditCard.queryByCarrierNo(
                                CreditCard, invoice["cardNo"]
                            )
                            if carrierNo is None:
                                data["spend_way"] = "No"
                                data["spend_way_type"] = "No"
                                data["spend_way_table"] = "No"
                            else:
                                data["spend_way"] = carrierNo.id
                                data["spend_way_type"] = carrierNo.type
                                data["spend_way_table"] = carrierNo.table_name

                            # 取得發票消費明細
                            invoicePayload["expTimeStamp"] = invoicePayload[
                                "timeStamp"
                            ] = (int(datetime.now().timestamp()) + 100)
                            invoicePayload["action"] = "carrierInvDetail"
                            invoicePayload["invNum"] = invoice["invNum"]
                            invoicePayload["invDate"] = datetime.fromtimestamp(
                                int(invoice["invDate"]["time"] / 1000)
                            ).strftime("%Y/%m/%d")
                            invoicePayload["amount"] = invoice["amount"]

                            invoiceDetail = requests.post(
                                "https://api.einvoice.nat.gov.tw/PB2CAPIVAN/invServ/InvServ",
                                params=invoicePayload,
                                timeout=(10, 30),
                            )

                            if invoiceDetail.json()["code"] == 200:
                                for detail in invoiceDetail.json()["details"]:
                                    data[
                                        "note"
                                    ] = f"{data['note']}{detail['description']} {detail['amount']}, "

                                datas.append(Journal(data))
                                data["note"] = ""
                                time.sleep(1)

                    if len(datas):
                        Journal.bulkInsert(Journal, datas)
        except Exception as error:
            # 如果出錯就重新執行，直到沒有錯誤為止
            importInvoice()

    def importStockPrice(period):
        with app.app_context():  # 因為新開 thread 但共用 db 所以需要指定
            datas = []

            stockList = StockJournal.queryStockCodeList(StockJournal)
            for stock in stockList:
                stockData = yfinance.Ticker(
                    stock.stock_code + ".TW"
                    if stock.vesting_nation == "TW"
                    else stock.stock_code
                )
                stockPrice = stockData.history(period="1d")
                fetch_date = datetime.utcfromtimestamp(
                    int(list(stockPrice["Close"].items())[0][0].timestamp())
                )

                hasRecorded = StockPriceHistory.queryByKey(
                    StockPriceHistory, fetch_date, stock.stock_code
                )

                # 如果找不到相關資料才寫入
                if hasRecorded["recordNum"] == 0:
                    datas.append(
                        {
                            "stock_code": stock.stock_code,
                            "fetch_date": fetch_date,
                            "open_price": list(stockPrice["Open"].items())[0][1],
                            "highest_price": list(stockPrice["High"].items())[0][1],
                            "lowest_price": list(stockPrice["Low"].items())[0][1],
                            "close_price": list(stockPrice["Close"].items())[0][1],
                        }
                    )

            if len(datas):
                StockPriceHistory.bulkInsert(StockPriceHistory, datas)
