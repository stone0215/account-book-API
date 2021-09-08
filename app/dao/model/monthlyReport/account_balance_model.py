from sqlalchemy import asc

from ...dao_base import DaoBase

db = DaoBase().getDB()


class AccountBalance(db.Model):
    __tablename__ = 'Account_Balance'
    vesting_month = db.Column(db.String(6), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    fx_rate = db.Column(db.Float, nullable=False)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, AccountBalance):
        self.vesting_month = AccountBalance.vesting_month
        self.id = AccountBalance.id
        self.name = AccountBalance.name
        self.balance = AccountBalance.balance
        self.fx_rate = AccountBalance.fx_rate

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByVestingMonth(self, vesting_month):
        return self.query.filter_by(vesting_month=vesting_month).all()

    def bulkInsert(self, datas):
        sql = 'INSERT INTO Account_Balance(vesting_month, id, name, balance, fx_rate) VALUES(:1, :2, :3, :4, :5)'

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

    def output(self, asset):
        return {
            'asset_id': asset.asset_id,
            'vesting_month': asset.vesting_month,
            'id': asset.id,
            'name': asset.name,
            'asset_id': asset.asset_id
        }
