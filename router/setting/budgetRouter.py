# -*- coding: UTF-8 -*-

from flask import jsonify, request

from api.response_format import ResponseFormat
from app.dao.model.setting.budget_model import Budget


def init_budget_api(app):
    @app.route('/budget', methods=['GET'])
    def getBudgets():
        output = []

        try:
            budgets = Budget.getAll(Budget)
            for budget in budgets:
                output.append(Budget.output(Budget, budget))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/budget/get-by-month/<string:year_month>', methods=['GET'])
    def getBudgetsByMonth():
        output = []

        try:
            budgets = Budget.queryByMonth(Budget, year_month)
            for budget in budgets:
                output.append(Budget.outputByMonth(Budget, budget))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/budget', methods=['POST'])
    def addBudget():
        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)
            budget = Budget(year_month=inputData['year_month'], category_code=inputData['category_code'],
                            category_name=inputData['category_name'], expected=inputData['expected'], actual=inputData['actual'])

            result = Budget.add(Budget, budget)
            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, Budget.output(Budget, result)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add budget data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/budget', methods=['PUT'])
    def updateBudget():
        try:
            inputData = request.get_json(force=True)
            budget = Budget.getByKey(Budget, inputData)
            if budget is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                budget.alarm_type = inputData['alarm_type']
                budget.alarm_date = inputData['alarm_date']
                budget.content = inputData['content']
                if Budget.update(Budget):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update budget data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/budget/<int:alarmId>', methods=['DELETE'])
    def deleteBudget(alarmId):
        try:
            budget = Budget.getByKey(Budget, alarmId)
            if budget is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if Budget.delete(Budget, alarmId):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete budget data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
