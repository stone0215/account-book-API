from sqlalchemy import asc

from ..dao_base import DaoBase

db = DaoBase().getDB()


class Loan(db.Model):
    __tablename__ = 'Loan'
    loan_id = db.Column(db.Integer, primary_key=True)
    loan_name = db.Column(db.String(60), nullable=False)
    account_id = db.Column(db.Integer, nullable=False)
    account_name = db.Column(db.String(60), nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    pay_day = db.Column(db.String(5), nullable=False, index=True)
    loan_index = db.Column(db.SmallInteger, index=True)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, loan_name, account_id, account_name, interest_rate, pay_day, loan_index):
        self.loan_name = loan_name
        self.account_id = account_id  # N：一般帳戶/ F：財務規劃帳戶
        self.account_name = account_name
        self.interest_rate = interest_rate
        self.pay_day = pay_day  # Y/M
        self.loan_index = loan_index

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def getAll(self):
        return self.query.order_by(asc(self.loan_index)).all()

    def queryByKey(self, loan_id):
        return self.query.filter_by(loan_id=loan_id).first()

    def add(self, other_asset):
        db.session.add(other_asset)
        db.session.flush()

        return other_asset

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

    def output(self, Account):
        return {
            'loan_id': Account.loan_id,
            'loan_name': Account.loan_name,
            'account_id': Account.account_id,
            'account_name': Account.account_name,
            'interest_rate': Account.interest_rate,
            'pay_day': Account.pay_day,
            'loan_index': Account.loan_index
        }
