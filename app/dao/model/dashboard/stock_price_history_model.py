from sqlalchemy import asc, Date, cast, and_

from ...dao_base import DaoBase

db = DaoBase().getDB()


class StockPriceHistory(db.Model):
    __tablename__ = "Stock_Price_History"
    stock_code = db.Column(db.String(10), primary_key=True)
    fetch_date = db.Column(db.DateTime, primary_key=True)
    open_price = db.Column(db.Float, nullable=False)
    highest_price = db.Column(db.Float, nullable=False)
    lowest_price = db.Column(db.Float, nullable=False)
    close_price = db.Column(db.Float, nullable=False)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, StockPriceHistory):
        self.stock_code = StockPriceHistory.stock_code
        self.fetch_date = StockPriceHistory.fetch_date
        self.open_price = StockPriceHistory.open_price
        self.highest_price = StockPriceHistory.highest_price
        self.lowest_price = StockPriceHistory.lowest_price
        self.close_price = StockPriceHistory.close_price

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, fetch_date, stock_code):
        # return self.query.filter(
        #     and_(
        #         cast(self.fetch_date, Date) == cast(fetch_date, Date),
        #         stock_code == stock_code,
        #     )
        # ).first()
        sql = f"SELECT COUNT(*) as recordNum FROM Stock_Price_History WHERE stock_code='{stock_code}' AND fetch_date='{fetch_date}'"

        try:
            return db.engine.execute(sql).fetchone()
        except Exception as error:
            return None

    def bulkInsert(self, datas):
        sql = "INSERT INTO Stock_Price_History(stock_code, fetch_date, open_price, highest_price, lowest_price, close_price) VALUES(:1, :2, :3, :4, :5, :6)"

        params = []
        try:
            for item in datas:
                params.append(
                    (
                        item["stock_code"],
                        item["fetch_date"],
                        round(item["open_price"], 2),
                        round(item["highest_price"], 2),
                        round(item["lowest_price"], 2),
                        round(item["close_price"], 2),
                    )
                )

            db.engine.execute(sql, params)
            return True
        except Exception as error:
            return False
