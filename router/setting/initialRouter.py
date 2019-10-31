from flask import jsonify, request

from api.response_format import ResponseFormat
from app.dao.model.setting.initial_model import InitialSetting


def init_initial_api(app):
    @app.route('/initial/query', methods=['GET'])
    def getInitialSettings():
        output = []

        try:
            initials = InitialSetting.queryByConditions(
                InitialSetting, request.args)
            for initial in initials:
                output.append(InitialSetting.output(
                    InitialSetting, initial))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/initial', methods=['POST'])
    def addInitial():
        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)
            initial = InitialSetting(
                inputData['code_id'], inputData['code_name'], inputData['initial_type'], inputData['setting_value'])

            result = InitialSetting.add(InitialSetting, initial)
            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, InitialSetting.output(InitialSetting, result)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add initial data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/initial', methods=['PUT'])
    def updateInitialSetting():
        try:
            inputData = request.get_json(force=True)

            initial = InitialSetting.queryByKey(InitialSetting, inputData)
            if initial is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                initial.setting_value = inputData['setting_value']

                if InitialSetting.update(InitialSetting):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update initial data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/initial', methods=['DELETE'])
    def deleteInitialSetting():
        try:
            inputData = request.get_json(force=True)

            initial = InitialSetting.queryByKey(InitialSetting, inputData)
            if initial is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if InitialSetting.delete(InitialSetting, initial):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete credit card data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
