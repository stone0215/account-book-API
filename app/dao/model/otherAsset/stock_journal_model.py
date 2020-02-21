from datetime import datetime
from sqlalchemy import asc
import requests
import json

from ...dao_base import DaoBase

db = DaoBase().getDB()


class StockJournal(db.Model):
    __tablename__ = 'Stock_Journal'
    stock_id = db.Column(db.Integer, primary_key=True)
    stock_code = db.Column(db.String(10), nullable=False)
    stock_name = db.Column(db.String(60), nullable=False)
    asset_id = db.Column(db.Integer, nullable=False)
    account_id = db.Column(db.Integer, nullable=False)
    account_name = db.Column(db.String(60), nullable=False)
    expected_spend = db.Column(db.Float)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, stock_name, stock_code, asset_id, account_id, account_name, expected_spend):
        self.stock_name = stock_name
        self.asset_id = asset_id
        self.stock_code = stock_code
        self.account_id = account_id
        self.account_name = account_name
        self.expected_spend = expected_spend if expected_spend else None

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, stock_id):
        return self.query.filter_by(stock_id=stock_id).first()

    def query4Summary(self, asset_id):
        sql = []
        sql.append("SELECT *, ROUND(100*gain_lose/total_cost,2) AS ROI, ")
        sql.append(
            "    ROUND(100*total_cash_dividend/hold_amount/buy_price,2) AS dividend_yield ")
        sql.append(
            "FROM (SELECT stock_main.*, price.close_price AS now_price, ")
        sql.append(
            "    (total_buy+IFNULL(total_stock_dividend,0)-total_sell) AS hold_amount, ")
        sql.append(
            "    total_sell AS sold_amount, ROUND(total_cost/total_buy,2) AS buy_price, ")
        sql.append(
            "    ROUND(IFNULL(total_gain,0)/total_sell,2) AS sold_price, buy_date, sold_date, ")
        sql.append(
            "    (IFNULL(total_gain,0)+IFNULL(total_stock_dividend*price.close_price,0)+IFNULL(total_cash_dividend,0)-total_cost) AS gain_lose, ")
        sql.append(
            "    total_cost, IFNULL(total_cash_dividend,0) AS total_cash_dividend ")
        sql.append("FROM Stock_Journal stock_main ")
        sql.append("LEFT JOIN (")
        sql.append("    SELECT stock_id, SUM(excute_amount) AS total_buy, ")
        sql.append(
            "        SUM(excute_price) AS total_cost, MIN(excute_date) AS buy_date ")
        sql.append(
            "    FROM Stock_Detail WHERE excute_type='buy' GROUP BY stock_id) buy_detail ")
        sql.append("ON stock_main.stock_id=buy_detail.stock_id ")
        sql.append("LEFT JOIN (")
        sql.append("    SELECT stock_id, SUM(excute_amount) AS total_sell, ")
        sql.append(
            "        SUM(excute_price) AS total_gain, MAX(excute_date) AS sold_date ")
        sql.append(
            "    FROM Stock_Detail WHERE excute_type='sell' GROUP BY stock_id) sell_detail ")
        sql.append("ON stock_main.stock_id=sell_detail.stock_id ")
        sql.append("LEFT JOIN (")
        sql.append(
            "    SELECT stock_id, SUM(excute_amount) AS total_stock_dividend ")
        sql.append("    FROM Stock_Detail WHERE excute_type='stock' ")
        sql.append("    GROUP BY stock_id) stock_dividend ")
        sql.append("ON stock_main.stock_id=stock_dividend.stock_id ")
        sql.append("LEFT JOIN (")
        sql.append(
            "    SELECT stock_id, SUM(excute_price) AS total_cash_dividend ")
        sql.append(
            "    FROM Stock_Detail WHERE excute_type='cash' GROUP BY stock_id) cash_dividend ")
        sql.append("ON stock_main.stock_id=cash_dividend.stock_id ")
        sql.append("LEFT JOIN (")
        sql.append(
            "    SELECT stock_code, MAX(fetch_date) AS max_date FROM Stock_Price_History ")
        sql.append(
            "    GROUP BY stock_code ) max_date ON stock_main.stock_code=max_date.stock_code ")
        sql.append("LEFT JOIN Stock_Price_History price ")
        sql.append(
            "ON stock_main.stock_code=price.stock_code AND fetch_date=max_date ")
        sql.append("WHERE asset_id=" + str(asset_id))
        sql.append(" ORDER BY stock_main.stock_id ASC)")

        return db.engine.execute(''.join(sql))  # sql 陣列轉字串

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
        payload = {'action': 'single_stock_close', 'code': stock.stock_code,
                   'date': datetime.now().strftime("%Y/%m/%d")}
        response = requests.get('??', params=payload)
        data = response.json()['data']

        return {
            'stock_id': stock.stock_id,
            'stock_code': stock.stock_code,
            'stock_name': stock.stock_name,
            'asset_id': stock.asset_id,
            'account_id': stock.account_id,
            'account_name': stock.account_name,
            'expected_spend': stock.expected_spend,
            'now_price': data['price'],
            'hold_amount': stock.hold_amount,
            'sold_amount': stock.sold_amount,
            'buy_price': stock.buy_price,
            'sold_price': stock.sold_price,
            'buy_date': datetime.strptime(stock.buy_date, '%Y-%m-%d %H:%M:%S.%f') if stock.buy_date else '',
            'sold_date': datetime.strptime(stock.sold_date, '%Y-%m-%d %H:%M:%S.%f') if stock.sold_date else '',
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
