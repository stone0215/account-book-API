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
    amount = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    fx_code = db.Column(db.String(3), nullable=False)
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
        self.fx_code = StockNetValueHistory.fx_code
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

    def deleteByVestingMonth(self, vesting_month):
        self.query.filter(self.vesting_month >= vesting_month).delete()

        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def outputForBalanceSheet(self, stocks):
        amount = 0
        for stock in stocks:
            amount += stock.price * stock.fx_rate

        return {
            'type': '流動資產',
            'name': '股票',
            'amount': round(amount, 2)
        }

    def outputForReport(self, stock):
        return {
            'assetType': '股票',
            'detailType': stock.asset_name,
            'name': stock.stock_name,
            'amount': stock.price * stock.fx_rate
        }
