from datetime import datetime, timedelta
from sqlalchemy import asc
import requests
import json

from ...dao_base import DaoBase

db = DaoBase().getDB()


class InsuranceJournal(db.Model):
    __tablename__ = 'Insurance_Journal'
    insurance_id = db.Column(db.Integer, primary_key=True)
    insurance_name = db.Column(db.String(60), nullable=False)
    # insurance_type = db.Column(db.String(10), nullable=False)
    asset_id = db.Column(db.Integer, nullable=False)
    account_id = db.Column(db.Integer, nullable=False)
    account_name = db.Column(db.String(60), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, index=True)
    expected_end_date = db.Column(db.DateTime, nullable=False)
    pay_type = db.Column(db.String(10), nullable=False)
    pay_day = db.Column(db.String(23), nullable=False)
    expected_spend = db.Column(db.Float, nullable=False)
    has_closed = db.Column(db.String(1), nullable=False)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, insurance_name, stock_code, asset_id, account_id, account_name, start_date, expected_end_date, pay_type, pay_day, expected_spend, has_closed):
        self.insurance_name = insurance_name
        # self.insurance_type = insurance_type
        self.asset_id = asset_id
        self.stock_code = stock_code
        self.account_id = account_id
        self.account_name = account_name
        self.start_date = start_date
        self.expected_end_date = expected_end_date
        self.pay_type = pay_type
        self.pay_day = pay_day
        self.expected_spend = expected_spend if expected_spend else None
        self.has_closed = has_closed

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, insurance_id):
        return self.query.filter_by(insurance_id=insurance_id).first()

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
        sql.append("FROM Insurance_Journal stock_main ")
        sql.append("LEFT JOIN (")
        sql.append("    SELECT insurance_id, SUM(excute_amount) AS total_buy, ")
        sql.append(
            "        SUM(excute_price) AS total_cost, MIN(excute_date) AS buy_date ")
        sql.append(
            "    FROM Insurance_Detail WHERE excute_type='buy' GROUP BY insurance_id) buy_detail ")
        sql.append("ON stock_main.insurance_id=buy_detail.insurance_id ")
        sql.append("LEFT JOIN (")
        sql.append("    SELECT insurance_id, SUM(excute_amount) AS total_sell, ")
        sql.append(
            "        SUM(excute_price) AS total_gain, MAX(excute_date) AS sold_date ")
        sql.append(
            "    FROM Insurance_Detail WHERE excute_type='sell' GROUP BY insurance_id) sell_detail ")
        sql.append("ON stock_main.insurance_id=sell_detail.insurance_id ")
        sql.append("LEFT JOIN (")
        sql.append(
            "    SELECT insurance_id, SUM(excute_amount) AS total_stock_dividend ")
        sql.append("    FROM Insurance_Detail WHERE excute_type='stock' ")
        sql.append("    GROUP BY insurance_id) stock_dividend ")
        sql.append("ON stock_main.insurance_id=stock_dividend.insurance_id ")
        sql.append("LEFT JOIN (")
        sql.append(
            "    SELECT insurance_id, SUM(excute_price) AS total_cash_dividend ")
        sql.append(
            "    FROM Insurance_Detail WHERE excute_type='cash' GROUP BY insurance_id) cash_dividend ")
        sql.append("ON stock_main.insurance_id=cash_dividend.insurance_id ")
        sql.append("LEFT JOIN (")
        sql.append(
            "    SELECT stock_code, MAX(fetch_date) AS max_date FROM Insurance_Price_History ")
        sql.append(
            "    GROUP BY stock_code ) max_date ON stock_main.stock_code=max_date.stock_code ")
        sql.append("LEFT JOIN Insurance_Price_History price ")
        sql.append(
            "ON stock_main.stock_code=price.stock_code AND fetch_date=max_date ")
        sql.append("WHERE asset_id=" + str(asset_id))
        sql.append(" ORDER BY stock_main.insurance_id ASC)")

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

    def delete(self, insurance_id):
        self.query.filter_by(insurance_id=insurance_id).delete()
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def output4View(self, stock):
        queryDate = datetime.now()
        payload = {'action': 'single_stock_close', 'code': stock.stock_code,
                   'date': queryDate.strftime("%Y/%m/%d")}
        data = ''

        # search for previous day if queryDate's price not exist
        while data == '':
            response = requests.get(
                'http://139.162.105.61/stone/index.py', params=payload)
            data = response.json()['data']
            queryDate = queryDate - timedelta(days=1)
            payload['date'] = queryDate.strftime("%Y/%m/%d")

        return {
            'insurance_id': stock.insurance_id,
            'stock_code': stock.stock_code,
            'insurance_name': stock.insurance_name,
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
            'insurance_id': stock.insurance_id,
            'stock_code': stock.stock_code,
            'insurance_name': stock.insurance_name,
            'asset_id': stock.asset_id
        }
