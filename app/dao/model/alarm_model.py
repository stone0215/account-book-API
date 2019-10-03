
from ..dao_base import DaoBase

db = DaoBase().getDB()


class Alarm(db.Model):
    __tablename__ = 'Alarm'
    alarm_id = db.Column(db.Integer, primary_key=True)
    alarm_type = db.Column(db.String(1), nullable=False)
    alarm_date = db.Column(db.String(5), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, alarm_type, alarm_date, content):
        self.alarm_type = alarm_type  # Y/M
        self.alarm_date = alarm_date
        self.content = content

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def getAll(self):
        return self.query.all()

    def queryByKey(self, alarm_id):
        return self.query.filter_by(alarm_id=alarm_id).first()

    def queryByConditions(self, date):
        # alarm_date 可能是每個月 26 或 8/26
        return db.engine.execute(f"SELECT * FROM Alarm WHERE alarm_date = '{date}' OR alarm_date LIKE '%{date}'")

    def add(self, alarm):
        db.session.add(alarm)
        db.session.flush()

        if DaoBase.session_commit(self) == '':
            return alarm
        else:
            return False

    def update(self):
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def delete(self, alarm_id):
        self.query.filter_by(alarm_id=alarm_id).delete()
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def output(self, Alarm):
        return {
            'alarm_id': Alarm.alarm_id,
            'alarm_type': Alarm.alarm_type,
            'alarm_date': Alarm.alarm_date,
            'content': Alarm.content
        }

    def output4View(self, Alarm):
        return {
            'alarm_date': Alarm.alarm_date,
            'content': Alarm.content
        }
