from sqlalchemy import asc

from ...dao_base import DaoBase

db = DaoBase().getDB()


class StockJournal(db.Model):
    __tablename__ = 'Stock_Journal'
    stock_id = db.Column(db.Integer, primary_key=True)
    stock_code = db.Column(db.String(10), nullable=False)
    stock_name = db.Column(db.String(60), nullable=False)
    asset_id = db.Column(db.Integer, nullable=False)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, stock_name, stock_code, asset_id):
        self.stock_name = stock_name
        self.asset_id = asset_id
        self.stock_code = stock_code

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, stock_id):
        return self.query.filter_by(stock_id=stock_id).first()

    def query4Summary(self, asset_id):
        sql = []
        sql.append("SELECT *, ROUND(gain_lose/total_cost,2)*100+'%' AS ROI, ")
        sql.append("    ROUND(total_cash_dividend/buy_price,2)*100+'%' AS dividend_yield ")
        sql.append("FROM (SELECT stock_main.*, price.close_price AS now_price, ")
        sql.append("    (total_buy+total_stock_dividend-total_sell) AS hold_amount, ")
        sql.append("    total_sell AS sold_amount, ROUND(total_cost/total_buy,2) AS buy_price, ")
        sql.append("    ROUND(total_gain/total_sell,2) AS sold_price, buy_date, sold_date, ")
        sql.append("    (total_gain+total_stock_dividend*price.close_price+total_cash_dividend-total_cost) AS gain_lose, ")
        sql.append("    total_cost, total_cash_dividend ")
        sql.append("FROM Stock_Journal stock_main ")
        sql.append("LEFT JOIN (")
        sql.append("    SELECT stock_id, SUM(excute_amount) AS total_buy, ")
        sql.append("        SUM(excute_price) AS total_cost, MIN(excute_date) AS buy_date ")
        sql.append("    FROM Stock_Detail WHERE excute_type='buy' GROUP BY stock_id) buy_detail ")
        sql.append("ON stock_main.stock_id=buy_detail.stock_id ")
        sql.append("LEFT JOIN (")
        sql.append("    SELECT stock_id, SUM(excute_amount) AS total_sell, ")
        sql.append("        SUM(excute_price) AS total_gain, MAX(excute_date) AS sold_date ")
        sql.append("    FROM Stock_Detail WHERE excute_type='sell' GROUP BY stock_id) sell_detail ")
        sql.append("ON stock_main.stock_id=sell_detail.stock_id ")
        sql.append("LEFT JOIN (")
        sql.append("    SELECT stock_id, SUM(excute_amount) AS total_stock_dividend ")
        sql.append("    FROM Stock_Detail WHERE excute_type='stock' ")
        sql.append("    GROUP BY stock_id) stock_dividend ")
        sql.append("ON stock_main.stock_id=stock_dividend.stock_id ")
        sql.append("LEFT JOIN (")
        sql.append("    SELECT stock_id, SUM(excute_price) AS total_cash_dividend ")
        sql.append("    FROM Stock_Detail WHERE excute_type='cash' GROUP BY stock_id) cash_dividend ")
        sql.append("ON stock_main.stock_id=cash_dividend.stock_id ")
        sql.append("LEFT JOIN (")
        sql.append("    SELECT stock_code, MAX(fetch_date) AS max_date FROM Stock_Price_History ")
        sql.append("    GROUP BY stock_code ) max_date ON stock_main.stock_code=max_date.stock_code ")
        sql.append("LEFT JOIN Stock_Price_History price ")
        sql.append("ON stock_main.stock_code=price.stock_code AND fetch_date=max_date ")
        sql.append("WHERE asset_id=" + str(asset_id))
        sql.append(" ORDER BY stock_main.stock_id ASC)")
        
        return db.engine.execute(''.join(sql)) # sql 陣列轉字串

    def add(self, stock_journal):
        db.session.add(stock_journal)
        db.session.flush()

        if DaoBase.session_commit(self) == '':
            return stock_journal
        else:
            return False

    def update(self):
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def delete(self, stock_id):
        self.query.filter_by(stock_id=stock_id).delete()
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def output4View(self, stock):
        return {
            'stock_id': stock.stock_id,
            'stock_code': stock.stock_code,
            'stock_name': stock.stock_name,
            'asset_id': stock.asset_id,
            'now_price': stock.now_price,
            'hold_amount': stock.hold_amount,
            'sold_amount': stock.sold_amount,
            'buy_price': stock.buy_price,
            'sold_price': stock.sold_price,
            'buy_date': stock.buy_date,
            'sold_date': stock.sold_date,
            'gain_lose': stock.gain_lose,
            'ROI': stock.ROI,
            'dividend_yield': stock.dividend_yield
        }

    def output(self, stock):
        return {
            'stock_id': stock.stock_id,
            'stock_code': stock.stock_code,
            'stock_name': stock.stock_name,
            'asset_id': stock.asset_id
        }
