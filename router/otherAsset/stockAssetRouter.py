# -*- coding: UTF-8 -*-

from datetime import datetime
from flask import jsonify, request

from api.response_format import ResponseFormat
from app.dao.model.otherAsset.stock_detail_model import StockDetail
from app.dao.model.otherAsset.stock_journal_model import StockJournal

date_format = '%Y-%m-%dT%H:%M:%S.%fZ'


def init_stock_asset_api(app):
    @app.route('/other-asset/stock/<int:asset_id>', methods=['GET'])
    def getStockAssets(asset_id):
        output = []

        try:
            stock_assets = StockJournal.query4Summary(StockJournal, asset_id)
            for stock_asset in stock_assets:
                output.append(StockJournal.output4View(
                    StockJournal, stock_asset))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/other-asset/stock', methods=['POST'])
    def addStockAsset():
        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)

            stock_asset = StockJournal(stock_code=inputData['stock_code'], stock_name=inputData['stock_name'],
                                       asset_id=inputData['asset_id'], account_id=inputData['account_id'],
                                       account_name=inputData['account_name'], expected_spend=inputData['expected_spend'])
            result = StockJournal.add(StockJournal, stock_asset)

            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, StockJournal.output(StockJournal, result)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add stock data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/other-asset/stock/<int:stock_id>', methods=['PUT'])
    def updateStockAsset(stock_id):
        try:
            stock_asset = StockJournal.queryByKey(StockJournal, stock_id)
            if stock_asset is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                stock_asset.stock_name = inputData['stock_name']
                other_asset.account_id = inputData['account_id']
                other_asset.account_name = inputData['account_name']
                other_asset.expected_spend = inputData['expected_spend'] if inputData['expected_spend'] else None
                if StockJournal.update(StockJournal):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update stock data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/other-asset/stock/<int:stock_id>', methods=['DELETE'])
    def deleteStockAsset(stock_id):
        try:
            stock_asset = StockJournal.queryByKey(StockJournal, stock_id)
            if stock_asset is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if StockJournal.delete(StockJournal, stock_id):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete stock data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/other-asset/stock/detail/<int:stock_id>', methods=['GET'])
    def getStockDetails(stock_id):
        output = []

        try:
            stock_details = StockDetail.queryByStockId(StockDetail, stock_id)
            for stock_detail in stock_details:
                output.append(StockDetail.output(StockDetail, stock_detail))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/other-asset/stock/detail', methods=['POST'])
    def addStockDetail():
        global date_format

        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)

            stock_detail = StockDetail(stock_id=inputData['stock_id'], excute_type=inputData['excute_type'],
                                       excute_amount=inputData['excute_amount'], excute_price=inputData['excute_price'],
                                       excute_date=datetime.strptime(inputData['excute_date'], date_format), memo=inputData['memo'])
            result = StockDetail.add(StockDetail, stock_detail)

            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, StockDetail.output(StockDetail, result)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add stock detail data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/other-asset/stock/detail/<int:distinct_number>', methods=['PUT'])
    def updateStockDetail(distinct_number):
        global date_format

        try:
            stock_detail = StockDetail.queryByKey(StockDetail, distinct_number)
            if stock_detail is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                stock_detail.excute_type = inputData['excute_type']
                stock_detail.excute_amount = inputData['excute_amount']
                stock_detail.excute_price = inputData['excute_price']
                stock_detail.excute_date = datetime.strptime(
                    inputData['excute_date'], date_format)
                stock_detail.memo = inputData['memo']

                if StockDetail.update(StockDetail):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update stock detail data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/other-asset/stock/detail/<int:distinct_number>', methods=['DELETE'])
    def deleteStockDetail(distinct_number):
        try:
            stock_detail = StockDetail.queryByKey(StockDetail, distinct_number)
            if stock_detail is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if StockDetail.delete(StockDetail, distinct_number):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete stock detail data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
