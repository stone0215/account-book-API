from datetime import datetime
from flask import jsonify
import requests

from api.response_format import ResponseFormat
from app.dao.model.dashboard.fx_rate_model import FXRate


def init_dashboard_api(app):
    @app.route('/dashboard/checkFxRate', methods=['POST'])
    def importFxRate():
        datas = []

        try:
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
                        rawRate = rate[key].split('/')

                        if rawRate[1] == 'NTD':
                            if rawRate[0] == 'USD':
                                usd = rate[key]

                            datas.append(
                                {'import_date': date, 'code': rawRate[0], 'buy_rate': rate[key]})
                        elif rawRate[1] != 'RMB':  # RMB 已有 NTD 匯兌，所以要過濾
                            if rawRate[0] == 'USD':
                                datas.append(
                                    {'import_date': date, 'code': rawRate[1], 'buy_rate': round(usd / rate[key], 2)})
                            else:
                                datas.append(
                                    {'import_date': date, 'code': rawRate[0], 'buy_rate': round(usd * rate[key], 2)})

                result = FXRate.bulkInsert(FXRate, datas)

                if result:
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None, 'Success'))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to build fx rate history'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
