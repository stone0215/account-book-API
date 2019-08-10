
from ..dao_base import DaoBase

db = DaoBase.getDB('')


class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(60), nullable=False)
    user_password = db.Column(db.String(30), nullable=False)
    user_nickname = db.Column(db.String(50))
    user_email = db.Column(db.String(30), nullable=False)

    def __init__(self, user_name, user_password, user_nickname, user_email):
        self.user_name = user_name
        self.user_password = user_password
        self.user_nickname = user_nickname
        self.user_email = user_email

    def __str__(self):
        return "Users(user_id='%s')" % self.user_id

    def get_all(self):
        return self.query.all()

    def get(self, user_id):
        return self.query.filter_by(user_id=user_id).first()

    def add(self, user):
        db.session.add(user)
        return DaoBase.session_commit(self)

    def update(self):
        return DaoBase.session_commit(self)

    def delete(self, user_id):
        self.query.filter_by(user_id=user_id).delete()
        return DaoBase.session_commit(self)

    def output(self, user):
        return {
            'user_id': user.user_id,
            'user_name': user.user_name,
            'user_nickname': user.user_nickname,
            'user_email': user.user_email
        }
