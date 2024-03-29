# -*- coding: UTF-8 -*-

from flask import jsonify, request

from api.response_format import ResponseFormat
from app.dao.model.setting.code_model import Code
from app.dao.model.otherAsset.other_asset_model import OtherAsset


def init_other_asset_api(app):
    @app.route('/other-asset/query', methods=['GET'])
    def getOtherAssets():
        output = []

        try:
            other_assets = OtherAsset.getAll(OtherAsset)
            for other_asset in other_assets:
                output.append(OtherAsset.output(OtherAsset, other_asset))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/other-asset/items', methods=['GET'])
    def getOtherAssetItems():
        output = []

        try:
            other_asset_items = OtherAsset.getDistinctItems(OtherAsset)
            for item in other_asset_items:
                output.append(OtherAsset.output4Item(OtherAsset, item))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/other-asset', methods=['POST'])
    def addOtherAsset():
        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)

            # 新增其他資產
            other_asset = OtherAsset(inputData)
            outputData = OtherAsset.add(OtherAsset, other_asset)
            # 新增代碼主選單
            # code = Code(code_type='Asset', name=inputData['asset_name'],
            #             in_use=inputData['in_use'], code_index='')
            # result = Code.add(Code, code)

            if outputData:
                return jsonify(ResponseFormat.true_return(ResponseFormat, OtherAsset.output(OtherAsset, outputData)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add asset data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/other-asset/<int:asset_id>', methods=['PUT'])
    def updateOtherAsset(asset_id):
        try:
            other_asset = OtherAsset.queryByKey(OtherAsset, asset_id)
            if other_asset is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                other_asset.asset_type = inputData['asset_type']
                other_asset.vesting_nation = inputData['vesting_nation']
                other_asset.in_use = inputData['in_use']
                other_asset.asset_index = inputData['asset_index']
                if OtherAsset.update(OtherAsset):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update asset data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/other-asset/<int:asset_id>', methods=['DELETE'])
    def deleteOtherAsset(asset_id):
        try:
            other_asset = OtherAsset.queryByKey(OtherAsset, asset_id)
            if other_asset is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if OtherAsset.delete(OtherAsset, asset_id):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete asset data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
