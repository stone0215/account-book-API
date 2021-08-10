from sqlalchemy import asc

from ...dao_base import DaoBase

db = DaoBase().getDB()


class Journal(db.Model):
    __tablename__ = 'Journal'
    distinct_number = db.Column(db.Integer, primary_key=True)
    vesting_month = db.Column(db.String(6), nullable=False, index=True)
    spend_date = db.Column(db.DateTime, nullable=False, index=True)
    spend_way = db.Column(db.String(10), nullable=False)
    spend_way_type = db.Column(db.String(20), nullable=False)
    spend_way_table = db.Column(db.String(15), nullable=False)
    action_main = db.Column(db.String(10), nullable=False)
    action_main_type = db.Column(db.String(20), nullable=False)
    action_main_table = db.Column(db.String(15), nullable=False)
    action_sub = db.Column(db.String(10), nullable=False)
    action_sub_table = db.Column(db.String(10), nullable=False)
    spending = db.Column(db.Float, nullable=False)
    note = db.Column(db.Text)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, Journal):
        self.vesting_month = Journal['vesting_month']
        self.spend_date = Journal['spend_date']
        self.spend_way = Journal['spend_way']
        self.spend_way_type = Journal['spend_way_type']
        self.spend_way_table = Journal['spend_way_table']
        self.action_main = Journal['action_main']
        self.action_main_type = Journal['action_main_type']
        self.action_main_table = Journal['action_main_table']
        self.action_sub = Journal['action_sub']
        self.action_sub_table = Journal['action_sub_table']
        self.spending = Journal['spending']
        self.note = Journal['note'] if Journal['note'] else None

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, distinct_number):
        return self.query.filter_by(distinct_number=distinct_number).first()

    def queryByVestingMonth(self, vesting_month):
        return self.query.filter_by(vesting_month=vesting_month).order_by(asc(self.spend_date)).all()

    def queryForExpenditureRatio(self, vestingMonth, sortColumn):
        sql = []
        sql.append("SELECT *, name AS action_main_name FROM Journal ")
        sql.append(" LEFT JOIN Code_Data ON code_id=action_main ")
        sql.append(
            f" WHERE vesting_month = '{vestingMonth}' AND action_main_table='Code' ")
        sql.append(f" ORDER BY {sortColumn} ASC ")

        return db.engine.execute(''.join(sql))

    def queryEstateOrLiabilityRecord(self, vestingMonth):
        sql = []
        sql.append(
            f"SELECT 'Estate' AS name, IFNULL(MAX(id),0) AS has_record FROM Estate_Net_Value_History WHERE vesting_month = '{vestingMonth}' ")
        sql.append(
            f" UNION ALL SELECT 'Insurance' AS name, IFNULL(MAX(id),0) AS has_record FROM Insurance_Net_Value_History WHERE vesting_month = '{vestingMonth}' ")
        sql.append(
            f" UNION ALL SELECT 'Loan' AS name, IFNULL(MAX(id),0) AS has_record FROM Loan_Balance WHERE vesting_month = '{vestingMonth}' ")
        sql.append(
            f" UNION ALL SELECT 'Stock' AS name, IFNULL(MAX(id),0) AS has_record FROM Stock_Net_Value_History WHERE vesting_month = '{vestingMonth}' ")

        return db.engine.execute(''.join(sql))

    def add(self, journal):
        db.session.add(journal)
        db.session.flush()

        if DaoBase.session_commit(self) == '':
            return journal
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

    def output(self, Journal):
        return {
            'distinct_number': Journal.distinct_number,
            'vesting_month': Journal.vesting_month,
            'spend_date': Journal.spend_date,
            'spend_way': Journal.spend_way,
            'spend_way_type': Journal.spend_way_type,
            'spend_way_table': Journal.spend_way_table,
            'action_main': Journal.action_main,
            'action_main_type': Journal.action_main_type,
            'action_main_table': Journal.action_main_table,
            'action_sub': Journal.action_sub,
            'action_sub_table': Journal.action_sub_table,
            'spending': Journal.spending,
            'note': Journal.note,
            'isEditMode': False
            # 'actionSubSelectionGroup': None  # 前端顯示所需，需先將欄位寫入
        }
