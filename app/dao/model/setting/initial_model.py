from datetime import datetime

from ...dao_base import DaoBase

db = DaoBase().getDB()


class InitialSetting(db.Model):
    __tablecode_name__ = 'Initial_Setting'
    code_id = db.Column(db.Integer, primary_key=True)
    code_name = db.Column(db.String(60), nullable=False)
    initial_type = db.Column(db.String(1), nullable=False, index=True)
    setting_value = db.Column(db.Float, nullable=False)
    setting_date = db.Column(db.DateTime, nullable=False)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, code_id, code_name, initial_type, setting_value, setting_date=datetime.now()):
        self.code_id = code_id
        self.code_name = code_name
        self.initial_type = initial_type
        self.setting_value = setting_value
        self.setting_date = setting_date

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByConditions(self, conditions):
        sql = []
        sql.append(
            "SELECT * FROM Initial_Setting WHERE 1=1")

        if conditions.get('initial_type') != '':
            sql.append(
                f" AND initial_type = '{conditions.get('initial_type')}'")

        sql.append(" ORDER BY initial_type ASC")

        return db.engine.execute(''.join(sql))

    def queryByKey(self, initial):
        print(initial)
        return self.query.filter_by(code_id=initial['code_id'], initial_type=initial['initial_type']).first()

    def add(self, initial):
        db.session.add(initial)

        # print(DaoBase.session_commit(self))  # print sql string
        if DaoBase.session_commit(self) == '':
            return initial
        else:
            return False

    def update(self):
        self.setting_date = datetime.now()

        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def delete(self, initial):
        self.query.filter_by(code_id=initial.code_id,
                             initial_type=initial.initial_type).delete()
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def output(self, Initial):
        return {
            'code_id': Initial.code_id,
            'code_name': Initial.code_name,
            'initial_type': Initial.initial_type,
            'setting_value': Initial.setting_value,
            'setting_date': Initial.setting_date
        }
