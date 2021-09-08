# -*- coding: UTF-8 -*-

from datetime import datetime
from flask import jsonify, request

from api.response_format import ResponseFormat
from app.dao.model.otherAsset.estate_journal_model import EstateJournal
from app.dao.model.otherAsset.estate_model import Estate

date_format = '%Y-%m-%dT%H:%M:%S.%fZ'


def init_estate_asset_api(app):
    @app.route('/other-asset/estate/<int:asset_id>', methods=['GET'])
    def getEstateAssets(asset_id):
        output = []

        try:
            estate_assets = Estate.query4Display(
                Estate, asset_id)
            for estate_asset in estate_assets:
                output.append(Estate.output4View(
                    Estate, estate_asset))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/other-asset/estate', methods=['POST'])
    def addEstateAsset():
        global date_format

        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)

            inputData['obtain_date'] = datetime.strptime(
                inputData['obtain_date'], date_format)

            result = Estate.add(Estate, Estate(inputData))

            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, Estate.output(Estate, result)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add estate data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/other-asset/estate/<int:estate_id>', methods=['PUT'])
    def updateEstateAsset(estate_id):
        global date_format

        try:
            estate_asset = Estate.queryByKey(
                Estate, estate_id)
            if estate_asset is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                estate_asset.estate_name = inputData['estate_name']
                estate_asset.estate_type = inputData['estate_type']
                estate_asset.estate_address = inputData['estate_address']
                estate_asset.obtain_date = datetime.strptime(
                    inputData['obtain_date'], date_format)
                # estate_asset.down_payment = inputData['down_payment']
                estate_asset.loan_id = inputData['loan_id'] if inputData['loan_id'] else None
                estate_asset.estate_status = inputData['estate_status']
                estate_asset.memo = inputData['memo']
                if Estate.update(Estate):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update estate data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/other-asset/estate/<int:estate_id>', methods=['DELETE'])
    def deleteEstateAsset(estate_id):
        try:
            estate_asset = Estate.queryByKey(
                Estate, estate_id)
            if estate_asset is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if Estate.delete(Estate, estate_id):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete estate data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/other-asset/estate/detail/<int:estate_id>', methods=['GET'])
    def getEstateJournals(estate_id):
        output = []

        try:
            estate_journals = EstateJournal.queryByEstateId(
                EstateJournal, estate_id)
            for estate_journal in estate_journals:
                output.append(EstateJournal.output(
                    EstateJournal, estate_journal))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/other-asset/estate/detail', methods=['POST'])
    def addEstateJournal():
        global date_format

        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)

            estate_journal = EstateJournal(estate_id=inputData['estate_id'], estate_excute_type=inputData['estate_excute_type'],
                                           excute_price=inputData['excute_price'], excute_date=datetime.strptime(
                inputData['excute_date'], date_format),
                memo=inputData['memo'])
            result = EstateJournal.add(EstateJournal, estate_journal)

            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, EstateJournal.output(EstateJournal, result)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add estate detail data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/other-asset/estate/detail/<int:distinct_number>', methods=['PUT'])
    def updateEstateJournal(distinct_number):
        global date_format

        try:
            estate_journal = EstateJournal.queryByKey(
                EstateJournal, distinct_number)
            if estate_journal is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                estate_journal.estate_excute_type = inputData['estate_excute_type']
                estate_journal.excute_price = inputData['excute_price']
                estate_journal.excute_date = datetime.strptime(
                    inputData['excute_date'], date_format)
                estate_journal.memo = inputData['memo']

                if EstateJournal.update(EstateJournal):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update estate detail data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/other-asset/estate/detail/<int:distinct_number>', methods=['DELETE'])
    def deleteEstateJournal(distinct_number):
        try:
            estate_journal = EstateJournal.queryByKey(
                EstateJournal, distinct_number)
            if estate_journal is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if EstateJournal.delete(EstateJournal, distinct_number):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete estate detail data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
