from datetime import datetime
from sqlalchemy import asc
import json

from ...dao_base import DaoBase

db = DaoBase().getDB()


class Insurance(db.Model):
    __tablename__ = 'Insurance'
    insurance_id = db.Column(db.Integer, primary_key=True)
    insurance_name = db.Column(db.String(60), nullable=False)
    asset_id = db.Column(db.Integer, nullable=False)
    in_account_id = db.Column(db.Integer, nullable=False)
    in_account_name = db.Column(db.String(60), nullable=False)
    out_account_id = db.Column(db.Integer, nullable=False)
    out_account_name = db.Column(db.String(60), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, index=True)
    expected_end_date = db.Column(db.DateTime, nullable=False)
    pay_type = db.Column(db.String(10), nullable=False)
    pay_day = db.Column(db.String(23), nullable=False)
    expected_spend = db.Column(db.Float, nullable=False)
    has_closed = db.Column(db.String(1), nullable=False)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, insurance_name, asset_id, in_account_id, in_account_name, out_account_id, out_account_name, start_date, expected_end_date, pay_type, pay_day, expected_spend, has_closed):
        self.insurance_name = insurance_name
        self.asset_id = asset_id
        self.in_account_id = in_account_id
        self.in_account_name = in_account_name
        self.out_account_id = out_account_id
        self.out_account_name = out_account_name
        self.start_date = start_date
        self.expected_end_date = expected_end_date
        self.pay_type = pay_type
        self.pay_day = pay_day
        self.expected_spend = expected_spend if expected_spend else None
        self.has_closed = has_closed

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, insurance_id):
        return self.query.filter_by(insurance_id=insurance_id).first()

    def query4Display(self, asset_id):
        sql = []
        sql.append(
            "SELECT insurance_main.insurance_id, insurance_name, asset_id, in_account_id, in_account_name, out_account_id, out_account_name, ")
        sql.append(
            "pay_type, pay_day, start_date, expected_end_date, has_closed, expected_spend, Insurance_Amount.actual_spend, ")
        sql.append(
            "Insurance_Profit.gain_lose, ROUND(100*Insurance_Profit.gain_lose/Insurance_Amount.actual_spend,2) AS ROI ")
        sql.append("FROM Insurance insurance_main ")
        sql.append(
            "LEFT JOIN (SELECT insurance_id, insurance_excute_type, SUM(IFNULL(excute_price,0)) AS gain_lose ")
        sql.append("    FROM Insurance_Journal) Insurance_Profit ")
        sql.append(
            "    ON Insurance_Profit.insurance_id=insurance_main.insurance_id ")
        sql.append(
            "        AND (Insurance_Profit.insurance_excute_type = 'cash' OR Insurance_Profit.insurance_excute_type = 'return')")
        sql.append(
            "LEFT JOIN (SELECT insurance_id, insurance_excute_type, SUM(IFNULL(excute_price,0)) AS actual_spend ")
        sql.append("    FROM Insurance_Journal) Insurance_Amount ")
        sql.append(
            "    ON Insurance_Amount.insurance_id=insurance_main.insurance_id")
        sql.append("        AND Insurance_Amount.insurance_excute_type = 'pay'")
        sql.append("WHERE asset_id=" + str(asset_id))
        sql.append(" ORDER BY insurance_main.insurance_id ASC")

        return db.engine.execute(''.join(sql))  # sql 陣列轉字串

    def query4Selection(self):
        return self.query.with_entities(self.insurance_id, self.insurance_name)

    def query4Summary(self, vestingMonth):
        sql = []
        sql.append(
            "SELECT '' AS vesting_month, Insurance.insurance_id AS id, insurance_name AS name, Insurance.asset_id, IFNULL(surrender_value,0) AS surrender_value, IFNULL(cost,0) AS cost, Account.fx_code AS fx_code, IFNULL(buy_rate,1) AS fx_rate FROM Insurance ")
        sql.append(
            " LEFT JOIN (SELECT id, fx_code FROM Account) Account ON Account.id=in_account_id ")
        sql.append(
            " LEFT JOIN (SELECT insurance_id, SUM(excute_price) AS cost FROM Insurance_Journal ")
        sql.append(
            f" WHERE STRFTIME('%Y%m', excute_date) <= '{vestingMonth}' AND (insurance_excute_type='pay' OR insurance_excute_type='cash') ")
        sql.append(
            " GROUP BY insurance_id) Journal_Cost ON Journal_Cost.insurance_id = Insurance.insurance_id ")
        sql.append(
            " LEFT JOIN (SELECT insurance_id, excute_price AS surrender_value FROM Insurance_Journal ")
        sql.append(
            f" WHERE STRFTIME('%Y%m', excute_date) <= '{vestingMonth}' AND (insurance_excute_type='expect' OR insurance_excute_type='return')) ")
        sql.append(
            " Journal_surrender ON Journal_surrender.insurance_id = Insurance.insurance_id ")
        sql.append(
            " LEFT JOIN (SELECT code, buy_rate, MAX(import_date) FROM FX_Rate ")
        sql.append(
            f" WHERE STRFTIME('%Y%m', import_date) = '{vestingMonth}' GROUP BY code) Rate ON Rate.code = Account.fx_code ")

        sql.append(" WHERE has_closed='N' ORDER BY Insurance.insurance_id ASC")

        return db.engine.execute(''.join(sql))

    def add(self, insurance):
        db.session.add(insurance)
        db.session.flush()

        if DaoBase.session_commit(self) == '':
            return insurance
        else:
            return False

    def update(self):
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def delete(self, insurance_id):
        self.query.filter_by(insurance_id=insurance_id).delete()
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def output4View(self, insurance):
        return {
            'insurance_id': insurance.insurance_id,
            'insurance_name': insurance.insurance_name,
            'asset_id': insurance.asset_id,
            'in_account_id': insurance.in_account_id,
            'in_account_name': insurance.in_account_name,
            'out_account_id': insurance.out_account_id,
            'out_account_name': insurance.out_account_name,
            'pay_type': insurance.pay_type,
            'pay_day': insurance.pay_day,
            'expected_spend': insurance.expected_spend,
            'start_date': datetime.strptime(insurance.start_date, '%Y-%m-%d %H:%M:%S.%f') if insurance.start_date else '',
            'expected_end_date': datetime.strptime(insurance.expected_end_date, '%Y-%m-%d %H:%M:%S.%f') if insurance.expected_end_date else '',
            'has_closed': insurance.has_closed,
            'actual_spend': insurance.actual_spend,
            'gain_lose': insurance.gain_lose,
            'ROI': insurance.ROI
            # 'IRR': insurance.IRR
        }

    def output(self, insurance):
        return {
            'insurance_id': insurance.insurance_id,
            'insurance_name': insurance.insurance_name,
            'asset_id': insurance.asset_id
        }

    def output4Selection(self, Insurance):
        return {
            'key': Insurance.insurance_id,
            'value': Insurance.insurance_name,
            'table': 'Insurance'  # 為了區分每個 id 隸屬於哪個 table，因為下拉選單id可能重複
        }
