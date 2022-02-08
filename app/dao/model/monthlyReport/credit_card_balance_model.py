from sqlalchemy import asc

from ...dao_base import DaoBase

db = DaoBase().getDB()


class CreditCardBalance(db.Model):
    __tablename__ = 'Credit_Card_Balance'
    vesting_month = db.Column(db.String(6), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    fx_rate = db.Column(db.Float, nullable=False)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, CreditCardBalance):
        self.vesting_month = CreditCardBalance.vesting_month
        self.id = CreditCardBalance.id
        self.name = CreditCardBalance.name
        self.balance = CreditCardBalance.balance
        self.fx_rate = CreditCardBalance.fx_rate

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByVestingMonth(self, vesting_month):
        return self.query.filter_by(vesting_month=vesting_month).all()

    def queryForLiabilities(self, vestingMonth):
        lastMonth = int(vestingMonth) - \
            1 if (int(vestingMonth) -
                  1) % 100 != 0 else (int(vestingMonth[:4])-1)*100+12

        sql = []
        sql.append(
            "SELECT '信用卡' AS type, card_name AS name, spending, payment AS payment, (IFNULL(balance,0)-IFNULL(spending,0)+IFNULL(payment,0)) AS balance FROM Credit_Card ")
        sql.append(
            f"LEFT JOIN (SELECT id, balance FROM Credit_Card_Balance WHERE vesting_month='{lastMonth}') AS Balance ON Balance.id=credit_card_id ")
        sql.append(
            "LEFT JOIN (SELECT spend_way, spend_way_table, SUM(spending) AS spending FROM Journal ")
        sql.append(
            f"WHERE vesting_month = '{vestingMonth}' AND spend_way_table='Credit_Card' GROUP BY spend_way, spend_way_table) AS Journal_Spending ON credit_card_id=Journal_Spending.spend_way ")
        sql.append(
            "LEFT JOIN (SELECT action_sub, action_sub_table, SUM(spending) AS payment FROM Journal ")
        sql.append(
            f"WHERE vesting_month = '{vestingMonth}' AND action_sub_table='Credit_Card' GROUP BY action_sub, action_sub_table) AS Journal_Payment ON credit_card_id=Journal_Payment.action_sub ")
        sql.append(
            "WHERE in_use='Y' AND (IFNULL(balance,0) != 0 OR IFNULL(spending,0) != 0 OR IFNULL(payment,0) != 0) ")
        sql.append(
            "UNION ALL SELECT '貸款' AS type, loan_name AS name, spending, payment, IFNULL(balance, amount)+IFNULL(spending,0)+IFNULL(payment,0) AS balance FROM Loan ")
        sql.append(
            f"LEFT JOIN (SELECT id, balance FROM Loan_Balance WHERE vesting_month='{lastMonth}') AS Balance ON Balance.id=Loan.loan_id ")
        sql.append(
            "LEFT JOIN (SELECT loan_id, SUM(excute_price) AS spending FROM Loan_Journal ")
        sql.append(
            f"WHERE STRFTIME('%Y%m', excute_date) <= '{vestingMonth}' AND loan_excute_type='increment' GROUP BY loan_id) AS Journal_Spending ON Loan.loan_id=Journal_Spending.loan_id ")
        sql.append(
            "LEFT JOIN (SELECT loan_id, SUM(excute_price) AS payment FROM Loan_Journal ")
        sql.append(
            f"WHERE STRFTIME('%Y%m', excute_date) <= '{vestingMonth}' AND loan_excute_type='principal' GROUP BY loan_id) AS Journal_Payment ON Loan.loan_id=Journal_Payment.loan_id ")
        sql.append(
            "WHERE repayed='N' ")
        sql.append(" ORDER BY type ASC ")

        return db.engine.execute(''.join(sql))

    def bulkInsert(self, datas):
        sql = 'INSERT INTO Credit_Card_Balance(vesting_month, id, name, balance, fx_rate) VALUES(:1, :2, :3, :4, :5)'

        params = []
        try:
            for item in datas:
                params.append((item.vesting_month, item.id,
                               item.name, item.balance, item.fx_rate))

            db.engine.execute(sql, params)
            return True
        except Exception as error:
            return False

    def delete(self, vesting_month):
        self.query.filter(self.vesting_month >= vesting_month).delete()

        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def culculateBalance(self, vestingMonth, journals, cards):
        cardArray = []
        for card in cards:
            obj = self(card)
            obj.vesting_month = vestingMonth
            for journal in journals:
                # 處理扣項金額
                if journal['spend_way_table'] == 'Credit_Card' and obj.id == int(journal['spend_way']):
                    obj.balance -= journal['spending']
                # 處理加項金額
                elif journal['action_sub_table'] == 'Credit_Card' and obj.id == int(journal['action_sub']):
                    obj.balance += journal['spending']

            cardArray.append(obj)

        return cardArray

    def outputForLiability(self, liability):
        return {
            'type': liability.type,
            'name': liability.name,
            'spending':  liability.spending*-1 if liability.spending else None,
            'payment':  abs(liability.payment) if liability.payment else None,
            'balance':  liability.balance
        }

    def outputForBalanceSheet(self, cards):
        amount = 0
        for card in cards:
            amount += round(card.balance * card.fx_rate, 2)

        return {
            'name': '信用卡',
            'amount': abs(amount)
        }
