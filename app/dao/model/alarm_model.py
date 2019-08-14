
from ..dao_base import DaoBase

db = DaoBase.getDB()


class Alarm(db.Model):
    __tablename__ = 'Alarm'
    alarm_id ＝ db.Column(db.Integer, primary_key=True)
    alarm_type = db.Column(db.Integer, index=True)
    alarm_date = db.Column(db.String(60), nullable=False)
    content = db.Column(db.String(30), nullable=False)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, alarm_id, alarm_type, alarm_date, content):
        self.alarm_id = alarm_id
        self.alarm_type = alarm_type  # Y/M
        self.alarm_date = alarm_date
        self.content = content

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def get_all(self):
        return self.query.all()

    def get(self, day):
        # alarm_date 可能是每個月 26 或 8/26
        return self.query.filter(self.alarm_date.in_(day))

    def add(self, Alarm):
        db.session.add(Alarm)
        return DaoBase.session_commit(self)

    def update(self):
        return DaoBase.session_commit(self)

    def delete(self, alarm_id):
        self.query.filter_by(alarm_id=alarm_id).delete()
        return DaoBase.session_commit(self)

    def output(self, Alarm):
        return {
            'alarm_id': Alarm.alarm_id,
            'alarm_type': Alarm.alarm_type,
            'alarm_date': Alarm.alarm_date,
            'content': Alarm.content
        }
