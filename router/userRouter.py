from flask import jsonify, request

from api.response_format import ResponseFormat
from app.dao.model.user_model import Users


def init_api(app):
    @app.route('/')
    def index():
        return jsonify(ResponseFormat.true_return(ResponseFormat, 'Hello Flask!'))

    @app.route('/user', methods=['GET'])
    def getUsers():
        users = Users.get_all(Users)
        output = []
        for user in users:
            output.append(Users.output(Users, user))
        return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/user/<int:userId>', methods=['GET'])
    def getUser(userId):
        user = Users.get(Users, userId)
        if user is None:
            return jsonify(ResponseFormat.false_return(ResponseFormat, None, '找不到数据'))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, Users.output(Users, user)))

    @app.route('/user', methods=['POST'])
    def addUser():
        inputData = request.get_json(force=True)
        # print(inputData['user_name'])
        user_name = inputData['user_name']
        user_password = inputData['user_password']
        user_nickname = inputData['user_nickname']
        user_email = inputData['user_email']
        user = Users(user_name=user_name, user_password=user_password,
                     user_nickname=user_nickname, user_email=user_email)
        result = Users.add(Users, user)
        if user.user_id:
            return getUser(user.user_id)
        else:
            return jsonify(ResponseFormat.false_return(ResponseFormat, None, result))

    @app.route('/user/<int:userId>', methods=['PUT'])
    def updateUser(userId):
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
    def deleteUser(userId):
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
