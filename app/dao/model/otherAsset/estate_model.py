from datetime import datetime, timedelta
from sqlalchemy import asc
import requests
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
    down_payment = db.Column(db.Float, nullable=False)
    loan_id = db.Column(db.Integer)
    estate_status = db.Column(db.String(10), nullable=False)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, estate_name, estate_type, estate_address, asset_id, obtain_date, down_payment, loan_id, estate_status):
        self.estate_name = estate_name
        self.estate_type = estate_type
        self.estate_address = estate_address
        self.asset_id = asset_id
        self.obtain_date = obtain_date
        self.down_payment = down_payment
        self.loan_id = loan_id if loan_id else None
        self.estate_status = estate_status

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, estate_id):
        return self.query.filter_by(estate_id=estate_id).first()

    def query4Summary(self, asset_id):
        sql = []
        sql.append(
            "SELECT estate_main.estate_id, estate_name, estate_type, estate_address, asset_id, obtain_date, down_payment, loan_id, loan_name, ")
        sql.append(
            "estate_status, Estate_Amount.cost, Estate_Profit.profit ")
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
            "LEFT JOIN (SELECT loan_id, loan_name) AS Loan ")
        sql.append(
            "    ON Loan.loan_id=estate_main.loan_id")
        sql.append("WHERE asset_id=" + str(asset_id))
        sql.append(" ORDER BY estate_main.estate_id ASC")

        return db.engine.execute(''.join(sql))  # sql 陣列轉字串

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
            'down_payment': estate.down_payment,
            'loan_id': estate.loan_id,
            'loan_name': estate.loan_name,
            'cost': estate.cost,
            'profit': estate.profit,
            'estate_status': estate.estate_status
            # 'gain_lose': estate.gain_lose,
            # 'ROI': estate.ROI
        }

    def output(self, estate):
        return {
            'estate_id': estate.estate_id,
            'estate_name': estate.estate_name,
            'asset_id': estate.asset_id
        }
