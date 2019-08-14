# -*- coding: UTF-8 -*-

from flask import jsonify, request

from api.response_format import ResponseFormat
from app.dao.model.alarm_model import Alarm


def init_alarm_api(app):
    @app.route('/alarm', methods=['GET'])
    def getAlarms():
        output = []

        try:
            alarms = Alarm.get_all(Alarm)
            for alarm in alarms:
                output.append(Alarm.output(Alarm, alarm))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/alarm/<path:day>', methods=['GET'])
    def getAlarmsByDay(day):
        output = []

        try:
            alarms = Alarm.get(Alarm, day)
            for alarm in alarms:
                output.append(Alarm.output(Alarm, alarm))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/alarm', methods=['POST'])
    def addAlarms():
        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)
            alarm_type = inputData['alarm_type']
            alarm_date = inputData['alarm_date']
            content = inputData['content']
            alarm = Alarm(alarm_type=alarm_type, alarm_date=alarm_date,
                          content=content)
            result = Alarm.add(Alarm, alarm)
            if result:
                return getUser(alarm.user_id)
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, result))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/user/<int:userId>', methods=['PUT'])
    def updateAlarms(userId):
        user = Users.get(Users, userId)
        if user is None:
            return jsonify(ResponseFormat.false_return(ResponseFormat, None, '找不到要修改的数据'))
        else:
            user_name = request.form.get('user_name')
            user_password = request.form.get('user_password')
            user_nickname = request.form.get('user_nickname')
            user_email = request.form.get('user_email')

            user.user_name = user_name
            user.user_password = user_password
            user.user_nickname = user_nickname
            user.user_email = user_email

            Users.update(Users)
            return getUser(user.user_id)

    @app.route('/user/<int:userId>', methods=['DELETE'])
    def deleteAlarms(userId):
        user = Users.get(Users, userId)
        if user is None:
            return jsonify(ResponseFormat.false_return(ResponseFormat, None, '找不到要删除的数据'))
        else:
            Users.delete(Users, userId)
            user = Users.get(Users, userId)
            if user is None:
                return getUsers()
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, '删除失败'))
