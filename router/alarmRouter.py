# -*- coding: UTF-8 -*-

from flask import jsonify, request

from api.response_format import ResponseFormat
from app.dao.model.alarm_model import Alarm


def init_alarm_api(app):
    @app.route('/alarm', methods=['GET'])
    def getAlarms():
        output = []

        try:
            alarms = Alarm.getAll(Alarm)
            for alarm in alarms:
                output.append(Alarm.output(Alarm, alarm))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/alarm/get-by-day', methods=['GET'])
    def getAlarmsByDay():
        output = []

        try:
            alarms = Alarm.getByMonth(Alarm, request.json['condition'])
            print(alarms)
            for alarm in alarms:
                output.append(Alarm.output4View(Alarm, alarm))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/alarm', methods=['POST'])
    def addAlarms():
        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)
            alarm = Alarm(alarm_type=inputData['alarm_type'], alarm_date=inputData['alarm_date'],
                          content=inputData['content'])

            result = Alarm.add(Alarm, alarm)
            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, Alarm.output(Alarm, result)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add alarm data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/alarm/<int:alarmId>', methods=['PUT'])
    def updateAlarms(alarmId):
        try:
            alarm = Alarm.getByKey(Alarm, alarmId)
            if alarm is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                alarm.alarm_type = inputData['alarm_type']
                alarm.alarm_date = inputData['alarm_date']
                alarm.content = inputData['content']
                if Alarm.update(Alarm):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update alarm data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/alarm/<int:alarmId>', methods=['DELETE'])
    def deleteAlarms(alarmId):
        try:
            alarm = Alarm.getByKey(Users, alarmId)
            if alarm is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                alarm.alarm_type = inputData['alarm_type']
                alarm.alarm_date = inputData['alarm_date']
                alarm.content = inputData['content']
                if Alarm.delete(Alarm, alarmId):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete alarm data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
