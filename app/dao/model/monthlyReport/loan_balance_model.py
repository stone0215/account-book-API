from sqlalchemy import asc

from ...dao_base import DaoBase

db = DaoBase().getDB()


class LoanBalance(db.Model):
    __tablename__ = 'Loan_Balance'
    vesting_month = db.Column(db.String(6), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, LoanBalance):
        self.vesting_month = LoanBalance.vesting_month
        self.id = LoanBalance.id
        self.name = LoanBalance.name
        self.balance = LoanBalance.balance
        self.cost = LoanBalance.cost

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByVestingMonth(self, vesting_month):
        return self.query.filter_by(vesting_month=vesting_month).all()

    def getDebtBalanceHistory(self, start, end, type):
        sql = []

        # 信用卡
        sql.append(
            f"SELECT vesting_month AS dateString, 'debt' AS type, balance, fx_rate FROM Credit_Card_Balance WHERE ")
        if type == 'month':
            sql.append(
                f" vesting_month >= '{start}' AND vesting_month <= '{end}' ")
        else:
            sql.append(
                f" vesting_month >= '{start}12' AND vesting_month <= '{end}12' AND substr(vesting_month, 4,2) = '12' ")

        sql.append(" UNION ALL ")
        # 貸款
        sql.append(
            f"SELECT vesting_month AS dateString, 'debt' AS type, balance, 1 AS fx_rate FROM Loan_Balance WHERE ")
        if type == 'month':
            sql.append(
                f" vesting_month >= '{start}' AND vesting_month <= '{end}' ")
        else:
            sql.append(
                f" vesting_month >= '{start}12' AND vesting_month <= '{end}12' AND substr(vesting_month, 4,2) = '12' ")

        sql.append(" ORDER BY type, dateString ASC ")

        return db.engine.execute(''.join(sql))

    def add(self, LoanBalance):
        db.session.add(LoanBalance)
        db.session.flush()

        # if DaoBase.session_commit(self) == '':
        #     return LoanBalance
        # else:
        #     return False

    def deleteByVestingMonth(self, vesting_month):
        self.query.filter(self.vesting_month >= vesting_month).delete()

        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def outputForBalanceSheet(self, loans):
        amount = 0
        for loan in loans:
            amount += loan.balance

        return {
            'name': '貸款',
            'amount': amount
        }
