# -*- coding: UTF-8 -*-

from flask import jsonify, request

from api.response_format import ResponseFormat
from app.dao.model.setting.budget_model import Budget
from app.dao.model.setting.code_model import Code


def init_budget_api(app):
    @app.route('/budget/<string:this_year>', methods=['GET'])
    def getBudgetsByYear(this_year):
        output = []

        try:
            budgets = Budget.queryByYear(Budget, this_year)
            for budget in budgets:
                output.append(Budget.outputByYear(Budget, budget))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/budget/year-range', methods=['GET'])
    def getBudgetRange():
        output = []

        try:
            budgetRange = Budget.getBudgetRange(Budget)
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, Budget.outputRange(Budget, budgetRange)))

    @app.route('/budget', methods=['PUT'])
    def updateBudget():
        try:
            inputData = request.get_json(force=True)
            if Budget.update(Budget, inputData):
                return jsonify(ResponseFormat.true_return(ResponseFormat, None))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update budget data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/budget/<string:next_year>', methods=['POST'])
    def bulkInsertBudget(next_year):
        prepared_data = []
        try:
            codes = Code.query4BudgetSelection(Code)

            for code in codes:
                prepared_data.append(
                    Budget(budget_year=next_year, category_code=code.code_id, category_name=code.name, code_type=code.code_type))

            if Budget.bulkInsert(Budget, prepared_data):
                return jsonify(ResponseFormat.true_return(ResponseFormat, None))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to bulk insert budget data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
