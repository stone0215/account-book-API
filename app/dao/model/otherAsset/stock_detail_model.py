from sqlalchemy import asc

from ...dao_base import DaoBase

db = DaoBase().getDB()


class StockDetail(db.Model):
    __tablename__ = 'Stock_Detail'
    distinct_number = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, nullable=False, index=True)
    excute_type = db.Column(db.String(10), nullable=False)
    excute_amount = db.Column(db.SmallInteger)
    excute_price = db.Column(db.Float)
    excute_date = db.Column(db.DateTime, nullable=False, index=True)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, stock_id, excute_type, excute_amount, excute_price, excute_date):
        self.stock_id = stock_id
        self.excute_type = excute_type
        self.excute_amount = excute_amount if excute_amount else None
        self.excute_price = excute_price if excute_price else None
        self.excute_date = excute_date

    # 定義物件的字串描述，執行 print(x) 就會跑這段

    def __str__(self):
        return self

    def getAll(self):
        return self.query.order_by(asc(self.excute_date)).all()

    def queryByKey(self, distinct_number):
        return self.query.filter_by(distinct_number=distinct_number).first()

    def queryByStockId(self, stock_id):
        return self.query.filter_by(stock_id=stock_id)

    def add(self, other_asset):
        db.session.add(other_asset)
        db.session.flush()

        return other_asset

    def update(self):
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def delete(self, distinct_number):
        self.query.filter_by(distinct_number=distinct_number).delete()
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def output(self, asset):
        return {
            'distinct_number': asset.distinct_number,
            'stock_id': asset.stock_id,
            'excute_type': asset.excute_type,
            'excute_amount': asset.excute_amount,
            'excute_price': asset.excute_price,
            'excute_date': asset.excute_date
        }
