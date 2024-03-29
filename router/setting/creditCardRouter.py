# -*- coding: UTF-8 -*-

# from datetime import datetime
from flask import jsonify, request

from api.response_format import ResponseFormat
from app.dao.model.setting.credit_card_model import CreditCard
# from app.dao.model.setting.initial_model import InitialSetting


def init_credit_card_api(app):
    @app.route('/credit-card/query', methods=['GET'])
    def getCreditCards():
        output = []

        try:
            creditCards = CreditCard.queryByConditions(
                CreditCard, request.args)
            for credit_card in creditCards:
                output.append(CreditCard.output(CreditCard, credit_card))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/credit-card', methods=['POST'])
    def addCreditCard():

        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)
            credit_card = CreditCard(inputData)

            # 新增信用卡
            result = CreditCard.add(CreditCard, credit_card)

            # 新增初始值
            # initial = InitialSetting(code_id=credit_card.credit_card_id, code_name=credit_card.card_name,
            #                          initial_type='CreditCard', setting_value=0)
            # result = InitialSetting.add(InitialSetting, initial)

            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, CreditCard.output(CreditCard, result)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add credit card data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/credit-card/<int:credit_card_id>', methods=['PUT'])
    def updateCreditCard(credit_card_id):

        try:
            credit_card = CreditCard.queryByKey(CreditCard, credit_card_id)
            if credit_card is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                credit_card.card_name = inputData['card_name']
                credit_card.last_day = inputData['last_day']
                credit_card.charge_day = inputData['charge_day']
                credit_card.limit_date = inputData['limit_date']
                credit_card.feedback_way = inputData['feedback_way']
                credit_card.fx_code = inputData['fx_code']
                credit_card.in_use = inputData['in_use']
                credit_card.credit_card_index = inputData['credit_card_index']
                credit_card.note = inputData['note']
                credit_card.note = inputData['carrier_no']
                if CreditCard.update(CreditCard):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update credit card data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/credit-card/<int:credit_card_id>', methods=['DELETE'])
    def deleteCreditCard(credit_card_id):
        try:
            credit_card = CreditCard.queryByKey(CreditCard, credit_card_id)
            if credit_card is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if CreditCard.delete(CreditCard, credit_card_id):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete credit card data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
