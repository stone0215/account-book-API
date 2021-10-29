from sqlalchemy import asc

from ...dao_base import DaoBase

db = DaoBase().getDB()


class TargetSetting(db.Model):
    __tablename__ = 'Target_Setting'
    distinct_number = db.Column(db.Integer, primary_key=True)
    target_year = db.Column(db.String(4), nullable=False)
    setting_value = db.Column(db.String(45), nullable=False)
    is_done = db.Column(db.String(1), nullable=False)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, TargetSetting):
        self.target_year = TargetSetting['target_year']
        self.setting_value = TargetSetting['setting_value']
        self.is_done = TargetSetting['is_done']

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, distinct_number):
        return self.query.filter_by(distinct_number=distinct_number).first()

    def get_all(self):
        return self.query.all()

    def add(self, target):
        db.session.add(target)
        db.session.flush()

        if DaoBase.session_commit(self) == '':
            return target
        else:
            return False

    def update(self):
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def delete(self, distinct_number):
        self.query.filter_by(distinct_number=distinct_number).delete()

        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def output(self, target):
        return {
            'distinct_number': target.distinct_number,
            'target_year': target.target_year,
            'setting_value': target.setting_value,
            'is_done': target.is_done
        }
