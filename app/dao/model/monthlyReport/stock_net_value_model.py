from sqlalchemy import asc

from ...dao_base import DaoBase

db = DaoBase().getDB()


class StockNetValueHistory(db.Model):
    __tablestock_name__ = 'Stock_Net_Value_History'
    vesting_month = db.Column(db.String(6), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    stock_code = db.Column(db.String(10), nullable=False)
    stock_name = db.Column(db.String(60), nullable=False)
    asset_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.SmallInteger, nullable=False)
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    fx_rate = db.Column(db.Float, nullable=False)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, StockNetValueHistory):
        self.vesting_month = StockNetValueHistory.vesting_month
        self.id = StockNetValueHistory.id
        self.stock_code = StockNetValueHistory.stock_code
        self.stock_name = StockNetValueHistory.stock_name
        self.asset_id = StockNetValueHistory.asset_id
        self.amount = StockNetValueHistory.amount
        self.price = StockNetValueHistory.price
        self.cost = StockNetValueHistory.cost
        self.fx_rate = StockNetValueHistory.fx_rate

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByVestingMonth(self, vesting_month):
        return self.query.filter_by(vesting_month=vesting_month).all()

    def add(self, StockNetValueHistory):
        db.session.add(StockNetValueHistory)
        db.session.flush()

        # if DaoBase.session_commit(self) == '':
        #     return StockNetValueHistory
        # else:
        #     return False

    def delete(self, asset_id):
        self.query.filter_by(asset_id=asset_id).delete()
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def output(self, asset):
        return {
            'asset_id': asset.asset_id,
            'vesting_month': asset.vesting_month,
            'id': asset.id,
            'stock_name': asset.stock_name,
            'asset_id': asset.asset_id
        }
