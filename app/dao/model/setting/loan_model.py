from sqlalchemy import asc

from ...dao_base import DaoBase

db = DaoBase().getDB()


class Loan(db.Model):
    __tablename__ = 'Loan'
    loan_id = db.Column(db.Integer, primary_key=True)
    loan_name = db.Column(db.String(60), nullable=False)
    account_id = db.Column(db.Integer, nullable=False)
    account_name = db.Column(db.String(60), nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    apply_date = db.Column(db.DateTime, nullable=False)
    pay_day = db.Column(db.String(2), nullable=False)
    loan_index = db.Column(db.SmallInteger, index=True)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, loan_name, account_id, account_name, interest_rate, apply_date, pay_day, loan_index):
        self.loan_name = loan_name
        self.account_id = account_id
        self.account_name = account_name
        self.interest_rate = interest_rate
        self.apply_date = apply_date
        self.pay_day = pay_day
        self.loan_index = loan_index

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def getAll(self):
        return self.query.order_by(asc(self.loan_index)).all()

    def queryByKey(self, loan_id):
        return self.query.filter_by(loan_id=loan_id).first()

    def add(self, loan):
        db.session.add(loan)

        if DaoBase.session_commit(self) == '':
            return loan
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

    def output(self, loan):
        return {
            'loan_id': loan.loan_id,
            'loan_name': loan.loan_name,
            'account_id': loan.account_id,
            'account_name': loan.account_name,
            'interest_rate': loan.interest_rate,
            'apply_date': loan.apply_date,
            'pay_day': loan.pay_day,
            'loan_index': loan.loan_index
        }
