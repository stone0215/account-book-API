from datetime import datetime, timedelta
from sqlalchemy import asc
import requests
import json

from ...dao_base import DaoBase

db = DaoBase().getDB()


class Loan(db.Model):
    __tablename__ = 'Loan'
    loan_id = db.Column(db.Integer, primary_key=True)
    loan_name = db.Column(db.String(60), nullable=False)
    loan_type = db.Column(db.String(10), nullable=False)
    account_id = db.Column(db.Integer, nullable=False)
    account_name = db.Column(db.String(60), nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    perid = db.Column(db.Integer, nullable=False)
    apply_date = db.Column(db.DateTime, nullable=False, index=True)
    pay_day = db.Column(db.String(2), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    repayed = db.Column(db.String(1), nullable=False, index=True)
    loan_index = db.Column(db.SmallInteger)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, loan_name, loan_type, account_id, account_name, interest_rate, perid, apply_date, pay_day, amount, repayed, loan_index):
        self.loan_name = loan_name
        self.loan_type = loan_type
        self.account_id = account_id
        self.account_name = account_name
        self.interest_rate = interest_rate
        self.perid = perid
        self.apply_date = apply_date
        self.pay_day = pay_day
        self.amount = amount
        self.repayed = repayed
        self.loan_index = loan_index or ''

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, loan_id):
        return self.query.filter_by(loan_id=loan_id).first()

    def query4Summary(self):
        sql = []
        sql.append(
            "SELECT loan_main.loan_id, loan_name, loan_type, apply_date, amount, ")
        sql.append("amount-principal_payed AS remaining, ")
        sql.append("principal_payed+interest_payed AS total_payed, repayed ")
        sql.append("FROM Loan Loan_Main ")
        sql.append(
            "LEFT JOIN (SELECT loan_id, SUM(IFNULL(excute_price,0)) AS principal_payed ")
        sql.append(
            "    FROM Loan_Journal WHERE loan_excute_type = 'principal') Loan_Payed ")
        sql.append(
            "    ON Loan_Payed.loan_id=Loan_Main.loan_id ")
        sql.append(
            "LEFT JOIN (SELECT loan_id, SUM(IFNULL(excute_price,0)) AS interest_payed ")
        sql.append(
            "    FROM Loan_Journal WHERE loan_excute_type = 'interest') Loan_Interest ")
        sql.append(
            "    ON Loan_Interest.loan_id=Loan_Main.loan_id ")
        sql.append(" ORDER BY Loan_Main.loan_id ASC")

        return db.engine.execute(''.join(sql))  # sql 陣列轉字串

    def query4Selection(self):
        return self.query.with_entities(self.loan_id, self.loan_name, self.loan_index).filter_by(repayed='N')

    def add(self, Loan):
        db.session.add(Loan)
        db.session.flush()

        if DaoBase.session_commit(self) == '':
            return Loan
        else:
            return False

    def update(self):
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def delete(self, loan_id):
        self.query.filter_by(loan_id=loan_id).delete()
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def output4View(self, Loan):
        return {
            'loan_id': Loan.loan_id,
            'loan_name': Loan.loan_name,
            'loan_type': Loan.loan_type,
            'apply_date': datetime.strptime(Loan.apply_date, '%Y-%m-%d %H:%M:%S.%f'),
            'amount': Loan.amount,
            'remaining': Loan.remaining,
            'total_payed': Loan.total_payed,
            'repayed': Loan.repayed,
        }

    def output(self, Loan):
        return {
            'loan_id': Loan.loan_id,
            'loan_name': Loan.loan_name
        }

    def output4Selection(self, Loan):
        return {
            'key': Loan.loan_id,
            'value': Loan.loan_name,
            'loan_index': Loan.loan_index
        }
