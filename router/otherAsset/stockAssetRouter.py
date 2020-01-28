# -*- coding: UTF-8 -*-

from flask import jsonify, request

from api.response_format import ResponseFormat
from app.dao.model.otherAsset.stock_detail_model import StockDetail
from app.dao.model.otherAsset.stock_journal_model import StockJournal


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
                                       asset_id=inputData['asset_id'])
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
            stock = StockJournal.queryByKey(StockJournal, stock_id)
            if stock is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                stock.stock_name = inputData['stock_name']
                if StockJournal.update(StockJournal):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update stock data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/other-asset/stock/<int:stock_id>', methods=['DELETE'])
    def deleteStockAsset(stock_id):
        try:
            stock = StockJournal.queryByKey(StockJournal, stock_id)
            if stock is None:
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
