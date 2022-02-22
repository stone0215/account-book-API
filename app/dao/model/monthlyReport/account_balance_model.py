from sqlalchemy import asc

from ...dao_base import DaoBase

db = DaoBase().getDB()


class AccountBalance(db.Model):
    __tablename__ = 'Account_Balance'
    vesting_month = db.Column(db.String(6), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    fx_code = db.Column(db.String(3), nullable=False)
    fx_rate = db.Column(db.Float, nullable=False)
    is_calculate = db.Column(db.String(1), nullable=False)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, AccountBalance):
        self.vesting_month = AccountBalance.vesting_month
        self.id = AccountBalance.id
        self.name = AccountBalance.name
        self.balance = AccountBalance.balance
        self.fx_code = AccountBalance.fx_code
        self.fx_rate = AccountBalance.fx_rate
        self.is_calculate = AccountBalance.is_calculate

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByVestingMonth(self, vesting_month):
        return self.query.filter_by(vesting_month=vesting_month).all()

    def bulkInsert(self, datas):
        sql = 'INSERT INTO Account_Balance(vesting_month, id, name, balance, fx_code, fx_rate, is_calculate) VALUES(:1, :2, :3, :4, :5, :6, :7)'

        params = []
        try:
            for item in datas:
                params.append((item.vesting_month, item.id,
                               item.name, item.balance, item.fx_code, item.fx_rate, item.is_calculate))

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

    def culculateBalance(self, vestingMonth, journals, accounts):
        accountArray = []
        for account in accounts:
            obj = AccountBalance(account)
            obj.vesting_month = vestingMonth
            for journal in journals:
                # 處理扣項金額
                if journal['spend_way_table'] == 'Account' and obj.id == int(journal['spend_way']):
                    print(
                        journal['spending'], obj.balance) if journal['spend_way'] == '20' else None
                    obj.balance += journal['spending']

                # 處理加項金額
                if journal['action_sub_table'] == 'Account' and obj.id == int(journal['action_sub']):
                    if journal['spend_way_type'] == 'normal' and journal['action_sub_type'] == 'finance':
                        obj.balance -= round(journal['spending'] /
                                             float(journal['note']), 2)
                    elif journal['spend_way_type'] == 'finance' and journal['action_sub_type'] == 'normal':
                        obj.balance -= journal['spending'] * \
                            float(journal['note'])
                    else:
                        obj.balance -= journal['spending']

            accountArray.append(obj)

        return accountArray

    def outputForBalanceSheet(self, accounts):
        amount = 0
        for account in accounts:
            if (account.is_calculate == 'Y'):
                amount += account.balance * account.fx_rate

        return {
            'type': '流動資產',
            'name': '現金',
            'amount': round(amount, 2)
        }

    def outputForReport(self, account):
        return {
            'assetType': '現金',
            'detailType': account.fx_code,
            'name': account.name,
            'amount': account.balance * account.fx_rate
        }
