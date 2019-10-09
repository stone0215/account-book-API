# -*- coding: UTF-8 -*-

from flask import jsonify, request

from api.response_format import ResponseFormat
from app.dao.model.code_model import Code


def init_code_api(app):
    @app.route('/code/query', methods=['GET'])
    def getCodes():
        output = []

        try:
            codes = Code.queryByConditions(Code, request.args)
            for code in codes:
                output.append(Code.outputMainCode(Code, code))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/code', methods=['POST'])
    def addCode():
        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)
            code = Code(code_type=inputData['code_type'], name=inputData['name'],
                        in_use=inputData['in_use'], code_index=inputData['code_index'])

            result = Code.add(Code, code)
            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, Code.outputMainCode(Code, result)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add code data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/code/<int:code_id>', methods=['PUT'])
    def updateCode(code_id):
        try:
            code = Code.queryByKey(Code, code_id)
            if code is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)
                code.name = inputData['name']
                code.code_type = inputData['code_type']
                code.in_use = inputData['in_use']
                code.code_index = inputData['code_index']

                if Code.update(Code):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update code data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/code/<int:code_id>', methods=['DELETE'])
    def deleteCode(code_id):
        try:
            code = Code.queryByKey(Code, code_id)
            if code is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if Code.delete(Code, code_id):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete code data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/sub-code/query/<int:parent_id>', methods=['GET'])
    def getSubCodes(parent_id):
        output = []

        try:
            codes = Code.querySubCodeList(Code, parent_id)
            for code in codes:
                output.append(Code.outputSubCode(Code, code))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/sub-code', methods=['POST'])
    def addSubCode():
        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)
            code = Code(name=inputData['name'], code_type=inputData['code_type'],
                        code_group=inputData['code_group'], code_group_name=inputData['code_group_name'],
                        in_use=inputData['in_use'], code_index=inputData['code_index'])

            result = Code.add(Code, code)
            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, Code.outputSubCode(Code, result)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add sub code data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/sub-code/<int:code_id>', methods=['PUT'])
    def updateSubCode(code_id):
        try:
            code = Code.queryByKey(Code, code_id)
            if code is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)
                code.name = inputData['name']
                code.code_type = inputData['code_type']
                code.code_group = inputData['code_group']
                code.code_group_name = inputData['code_group_name']
                code.in_use = inputData['in_use']
                code.code_index = inputData['code_index']

                if Code.update(Code):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update sub code data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
