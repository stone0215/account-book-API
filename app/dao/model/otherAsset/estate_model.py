from datetime import datetime
from sqlalchemy import asc
import json

from ...dao_base import DaoBase

db = DaoBase().getDB()


class Estate(db.Model):
    __tablename__ = 'Estate'
    estate_id = db.Column(db.Integer, primary_key=True)
    estate_name = db.Column(db.String(60), nullable=False)
    estate_type = db.Column(db.String(10), nullable=False)
    estate_address = db.Column(db.Text, nullable=False)
    asset_id = db.Column(db.Integer, nullable=False)
    obtain_date = db.Column(db.DateTime, nullable=False, index=True)
    # down_payment = db.Column(db.Float, nullable=False)
    loan_id = db.Column(db.Integer)
    estate_status = db.Column(db.String(10), nullable=False)
    memo = db.Column(db.Text)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, Estate):
        self.estate_name = Estate['estate_name']
        self.estate_type = Estate['estate_type']
        self.estate_address = Estate['estate_address']
        self.asset_id = Estate['asset_id']
        self.obtain_date = Estate['obtain_date']
        # self.down_payment = Estate['down_payment']
        self.loan_id = Estate['loan_id'] if Estate['loan_id'] else None
        self.estate_status = Estate['estate_status']
        self.memo = Estate['memo'] if Estate['memo'] else None

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, estate_id):
        return self.query.filter_by(estate_id=estate_id).first()

    def query4Display(self, asset_id):
        sql = []
        sql.append(
            "SELECT estate_main.estate_id, estate_name, estate_type, estate_address, asset_id, obtain_date, estate_main.loan_id, loan_name, ")
        sql.append(
            "estate_status, memo, Estate_Amount.cost, Estate_Profit.profit ")
        sql.append("FROM Estate estate_main ")
        sql.append(
            "LEFT JOIN (SELECT estate_id, estate_excute_type, SUM(IFNULL(excute_price,0)) AS cost ")
        sql.append("    FROM Estate_Journal WHERE estate_excute_type = 'tax' OR estate_excute_type = 'fee' OR estate_excute_type = 'fix') Estate_Amount ")
        sql.append(
            "    ON Estate_Amount.estate_id=estate_main.estate_id ")
        sql.append(
            "LEFT JOIN (SELECT estate_id, estate_excute_type, SUM(IFNULL(excute_price,0)) AS profit ")
        sql.append(
            "    FROM Estate_Journal WHERE estate_excute_type = 'rent') Estate_Profit ")
        sql.append(
            "    ON Estate_Profit.estate_id=estate_main.estate_id ")
        sql.append(
            "LEFT JOIN (SELECT loan_id, loan_name FROM Loan) Loan ")
        sql.append(
            "    ON Loan.loan_id=estate_main.loan_id ")
        sql.append(" WHERE asset_id=" + str(asset_id))
        sql.append(" ORDER BY estate_main.estate_id ASC")

        return db.engine.execute(''.join(sql))  # sql 陣列轉字串

    def query4Summary(self, vestingMonth):
        sql = []
        sql.append(
            "SELECT '' AS vesting_month, Estate.estate_id AS id, estate_name AS name, Estate.asset_id, IFNULL(market_value,0) AS market_value, IFNULL(cost,0) AS cost, estate_status FROM Estate ")
        sql.append(
            " LEFT JOIN (SELECT estate_id, SUM(excute_price) AS cost FROM Estate_Journal ")
        sql.append(
            f" WHERE STRFTIME('%Y%m', excute_date) <= '{vestingMonth}' AND estate_excute_type != 'marketValue' GROUP BY estate_id) Journal ON Journal.estate_id = Estate.estate_id ")
        sql.append(
            " LEFT JOIN (SELECT estate_id, excute_price AS market_value FROM Estate_Journal ")
        sql.append(
            f" WHERE STRFTIME('%Y%m', excute_date) <= '{vestingMonth}' AND estate_excute_type = 'marketValue') Journal_Market ON Journal_Market.estate_id = Estate.estate_id ")

        sql.append(" WHERE estate_status != 'sold' ORDER BY Estate.estate_id ASC")

        return db.engine.execute(''.join(sql))

    def add(self, Estate):
        db.session.add(Estate)
        db.session.flush()

        if DaoBase.session_commit(self) == '':
            return Estate
        else:
            return False

    def update(self):
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def delete(self, estate_id):
        self.query.filter_by(estate_id=estate_id).delete()
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def output4View(self, estate):
        return {
            'estate_id': estate.estate_id,
            'estate_name': estate.estate_name,
            'estate_type': estate.estate_type,
            'estate_address': estate.estate_address,
            'asset_id': estate.asset_id,
            'obtain_date': datetime.strptime(estate.obtain_date, '%Y-%m-%d %H:%M:%S.%f'),
            # 'down_payment': estate.down_payment,
            'loan_id': estate.loan_id,
            'loan_name': estate.loan_name,
            'cost': estate.cost,
            'profit': estate.profit,
            'estate_status': estate.estate_status,
            'memo': estate.memo
            # 'gain_lose': estate.gain_lose,
            # 'ROI': estate.ROI
        }

    def output(self, estate):
        return {
            'estate_id': estate.estate_id,
            'estate_name': estate.estate_name,
            'asset_id': estate.asset_id
        }
