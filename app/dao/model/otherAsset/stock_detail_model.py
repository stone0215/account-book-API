from sqlalchemy import asc

from ...dao_base import DaoBase

db = DaoBase().getDB()


class StockDetail(db.Model):
    __tablename__ = "Stock_Detail"
    distinct_number = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, nullable=False, index=True)
    excute_type = db.Column(db.String(10), nullable=False)
    excute_amount = db.Column(db.Float)
    excute_price = db.Column(db.Float)
    excute_date = db.Column(db.DateTime, nullable=False, index=True)
    account_id = db.Column(db.Integer, nullable=False)
    account_name = db.Column(db.String(60), nullable=False)
    memo = db.Column(db.Text)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, StockDetail):
        self.stock_id = StockDetail["stock_id"]
        self.excute_type = StockDetail["excute_type"]
        self.excute_amount = (
            StockDetail["excute_amount"] if StockDetail["excute_amount"] else None
        )
        self.excute_price = (
            StockDetail["excute_price"] if StockDetail["excute_price"] else 0
        )
        self.excute_date = StockDetail["excute_date"]
        self.account_id = StockDetail["account_id"]
        self.account_name = StockDetail["account_name"]
        self.memo = StockDetail["memo"] if StockDetail["memo"] else None

    # 定義物件的字串描述，執行 print(x) 就會跑這段

    def __str__(self):
        return self

    def getAll(self):
        return self.query.order_by(asc(self.excute_date)).all()

    def queryByKey(self, distinct_number):
        return self.query.filter_by(distinct_number=distinct_number).first()

    def queryByStockId(self, stock_id):
        return self.query.filter_by(stock_id=stock_id)

    def add(self, stock_asset):
        db.session.add(stock_asset)
        db.session.flush()

        if DaoBase.session_commit(self) == "":
            return stock_asset
        else:
            return False

    def update(self):
        if DaoBase.session_commit(self) == "":
            return True
        else:
            return False

    def delete(self, distinct_number):
        self.query.filter_by(distinct_number=distinct_number).delete()
        if DaoBase.session_commit(self) == "":
            return True
        else:
            return False

    def output(self, asset):
        return {
            "distinct_number": asset.distinct_number,
            "stock_id": asset.stock_id,
            "excute_type": asset.excute_type,
            "excute_amount": asset.excute_amount,
            "excute_price": asset.excute_price,
            "excute_date": asset.excute_date,
            "account_id": asset.account_id,
            "account_name": asset.account_name,
            "memo": asset.memo,
        }
