from datetime import datetime, timedelta
from sqlalchemy import asc
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
    period = db.Column(db.Integer, nullable=False)
    apply_date = db.Column(db.DateTime, nullable=False, index=True)
    grace_expire_date = db.Column(db.DateTime)
    pay_day = db.Column(db.String(2), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    repayed = db.Column(db.String(1), nullable=False, index=True)
    loan_index = db.Column(db.SmallInteger)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, Loan):
        self.loan_name = Loan['loan_name']
        self.loan_type = Loan['loan_type']
        self.account_id = Loan['account_id']
        self.account_name = Loan['account_name']
        self.interest_rate = Loan['interest_rate']
        self.period = Loan['period']
        self.apply_date = Loan['apply_date']
        self.grace_expire_date = Loan['grace_expire_date']
        self.pay_day = Loan['pay_day']
        self.amount = Loan['amount']
        self.repayed = Loan['repayed']
        self.loan_index = Loan['loan_index'] if Loan['loan_index'] else None

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, loan_id):
        return self.query.filter_by(loan_id=loan_id).first()

    def query4Display(self):
        sql = []
        sql.append(
            "SELECT loan_main.loan_id, loan_name, loan_type, apply_date, grace_expire_date, amount, ")
        sql.append("amount-IFNULL(principal_payed,0) AS remaining, ")
        sql.append(
            "IFNULL(principal_payed+interest_payed,0) AS total_payed, repayed ")
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
        return self.query.with_entities(self.loan_id, self.loan_name, self.loan_index)

    def query4Summary(self, vestingMonth):
        sql = []
        sql.append(
            "SELECT '' AS vesting_month, Loan.loan_id AS id, loan_name AS name, amount+IFNULL(payed,0) AS balance, IFNULL(cost,0) AS cost FROM Loan ")
        sql.append(
            f" LEFT JOIN (SELECT loan_id, SUM(excute_price) AS payed FROM Loan_Journal WHERE STRFTIME('%Y%m', excute_date) <= '{vestingMonth}' ")
        sql.append(
            " AND (loan_excute_type='principal' OR loan_excute_type='increment') GROUP BY loan_id) Journal_Payed ")
        sql.append(" ON Journal_Payed.loan_id=Loan.loan_id ")
        sql.append(
            f" LEFT JOIN (SELECT loan_id, SUM(excute_price) AS cost FROM Loan_Journal WHERE STRFTIME('%Y%m', excute_date) <= '{vestingMonth}' ")
        sql.append(
            " AND (loan_excute_type='interest' OR loan_excute_type='fee') GROUP BY loan_id) Journal_Cost ")
        sql.append(" ON Journal_Cost.loan_id=Loan.loan_id ")
        sql.append(" WHERE repayed='N' ORDER BY Loan.loan_id ASC")

        return db.engine.execute(''.join(sql))

    def query4CashFlow(self, vestingMonth):
        lastMonth = int(vestingMonth) - \
            1 if int(vestingMonth) - \
            1 % 100 != 0 else (int(vestingMonth[:4])-1)*100+12

        sql = []
        sql.append(
            "SELECT '貸款' AS type, loan_name AS name, IFNULL(balance,amount) AS balance FROM Loan ")
        sql.append(
            f" LEFT JOIN Loan_Balance Balance ON Balance.vesting_month = '{lastMonth}' ")

        sql.append(" ORDER BY loan_id ASC")

        return db.engine.execute(''.join(sql))

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
            'grace_expire_date': datetime.strptime(Loan.grace_expire_date, '%Y-%m-%d %H:%M:%S.%f') if Loan.grace_expire_date else '',
            'amount': Loan.amount,
            'remaining': Loan.remaining,
            'total_payed': Loan.total_payed,
            'repayed': Loan.repayed,
        }

    def output(self, Loan):
        return {
            'loan_id': Loan.loan_id,
            'loan_name': Loan.loan_name,
            'loan_type': Loan.loan_type,
            'account_id': Loan.account_id,
            'account_name': Loan.account_name,
            'interest_rate': Loan.interest_rate,
            'period': Loan.period,
            'apply_date': Loan.apply_date,
            'grace_expire_date': Loan.grace_expire_date,
            'pay_day': Loan.pay_day,
            'amount': Loan.amount,
            'repayed': Loan.repayed,
            'loan_index': Loan.loan_index if Loan.loan_index else ''
        }

    def output4Selection(self, Loan):
        return {
            'key': Loan.loan_id,
            'value': Loan.loan_name,
            'index:': Loan.loan_index,
            'table': 'Loan'
        }
