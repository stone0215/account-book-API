from datetime import datetime
from sqlalchemy import asc

# import requests
import json

from ...dao_base import DaoBase

db = DaoBase().getDB()


class StockJournal(db.Model):
    __tablename__ = "Stock_Journal"
    stock_id = db.Column(db.Integer, primary_key=True)
    stock_code = db.Column(db.String(10), nullable=False)
    stock_name = db.Column(db.String(60), nullable=False)
    asset_id = db.Column(db.Integer, nullable=False)
    expected_spend = db.Column(db.Float)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, StockJournal):
        self.stock_name = StockJournal["stock_name"]
        self.asset_id = StockJournal["asset_id"]
        self.stock_code = StockJournal["stock_code"]
        self.expected_spend = (
            StockJournal["expected_spend"] if StockJournal["expected_spend"] else None
        )

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, stock_id):
        return self.query.filter_by(stock_id=stock_id).first()

    def query4Display(self, asset_id):
        sql = []
        sql.append("SELECT stock_main.*, price.close_price AS now_price, ")
        sql.append(
            "IFNULL(total_sell,0) AS sold_amount, IFNULL(total_stock_dividend,0) AS total_stock_dividend, ")
        sql.append("buy_date, sold_date, IFNULL(total_gain,0) AS total_gain, ")
        sql.append(
            "IFNULL(total_gain,0)+IFNULL(total_stock_dividend,0)*IFNULL(price.close_price,0)+IFNULL(total_cash_dividend,0)+IFNULL(total_cost,0) AS gain_lose, "
        )
        sql.append(
            "IFNULL(total_cost,0) AS total_cost, IFNULL(total_cash_dividend,0) AS total_cash_dividend, IFNULL(total_buy,0) AS total_buy "
        )
        sql.append("FROM Stock_Journal stock_main ")
        sql.append("LEFT JOIN ( ")
        sql.append("SELECT stock_id, SUM(excute_amount) AS total_buy, ")
        sql.append(
            "SUM(excute_price) AS total_cost, MIN(excute_date) AS buy_date FROM Stock_Detail ")
        sql.append(
            "WHERE excute_type='buy' OR excute_type='merge' OR excute_type='split' GROUP BY stock_id) buy_detail "
        )
        sql.append("ON stock_main.stock_id=buy_detail.stock_id ")
        sql.append("LEFT JOIN ( ")
        sql.append("SELECT stock_id, SUM(excute_amount) AS total_sell, ")
        sql.append(
            "SUM(excute_price) AS total_gain, MAX(excute_date) AS sold_date ")
        sql.append(
            "FROM Stock_Detail WHERE excute_type='sell' GROUP BY stock_id) sell_detail "
        )
        sql.append("ON stock_main.stock_id=sell_detail.stock_id ")
        sql.append("LEFT JOIN ( ")
        sql.append("SELECT stock_id, SUM(excute_amount) AS total_stock_dividend ")
        sql.append("FROM Stock_Detail WHERE excute_type='stock' ")
        sql.append("GROUP BY stock_id) stock_dividend ")
        sql.append("ON stock_main.stock_id=stock_dividend.stock_id ")
        sql.append("LEFT JOIN ( ")
        sql.append("SELECT stock_id, SUM(excute_price) AS total_cash_dividend ")
        sql.append(
            "FROM Stock_Detail WHERE excute_type='cash' GROUP BY stock_id) cash_dividend "
        )
        sql.append("ON stock_main.stock_id=cash_dividend.stock_id ")
        sql.append("LEFT JOIN ( ")
        sql.append(
            "SELECT stock_code, MAX(fetch_date) AS max_date FROM Stock_Price_History "
        )
        sql.append(
            "GROUP BY stock_code ) max_date ON stock_main.stock_code=max_date.stock_code "
        )
        sql.append("LEFT JOIN Stock_Price_History price ")
        sql.append(
            "ON stock_main.stock_code=price.stock_code AND fetch_date=max_date ")
        sql.append(f"WHERE asset_id={asset_id} ")
        sql.append(" ORDER BY stock_main.stock_code ASC")

        return db.engine.execute("".join(sql))  # sql 陣列轉字串

    def query4Summary(self, vestingMonth):
        sql = []
        sql.append(
            "SELECT '' AS vesting_month, Journal.stock_id AS id, Journal.stock_code, stock_name, Journal.asset_id, "
        )
        sql.append(
            " IFNULL(positive_amount,0) AS positive_amount, IFNULL(negative_amount,0) AS negative_amount, IFNULL(close_price,0) AS close_price, "
        )
        sql.append(
            " IFNULL(positive_cost,0) AS positive_cost, IFNULL(negative_cost,0) AS negative_cost, Main.asset_name AS asset_name, Account.fx_code AS fx_code, "
        )
        sql.append(
            " IFNULL(buy_rate,1) AS fx_rate, 0 AS amount, 0 AS cost, 0 AS price FROM Stock_Journal Journal ")
        sql.append(
            " LEFT JOIN Other_Asset Main ON Main.asset_id=Journal.asset_id ")
        sql.append(
            " LEFT JOIN (SELECT stock_id, MAX(account_id) AS account_id, SUM(excute_amount) AS positive_amount, SUM(excute_price) AS positive_cost FROM Stock_Detail "
        )
        sql.append(
            f" WHERE excute_amount>0 AND STRFTIME('%Y%m', excute_date) <= '{vestingMonth}' GROUP BY stock_id) POSITIVE_Detail ON POSITIVE_Detail.stock_id = Journal.stock_id "
        )
        sql.append(
            " LEFT JOIN (SELECT stock_id, MAX(account_id) AS account_id, SUM(excute_amount) AS negative_amount, SUM(excute_price) AS negative_cost FROM Stock_Detail "
        )
        sql.append(
            f" WHERE excute_amount<0 AND STRFTIME('%Y%m', excute_date) <= '{vestingMonth}' GROUP BY stock_id) NEGATIVE_Detail ON NEGATIVE_Detail.stock_id = Journal.stock_id "
        )
        sql.append(
            " LEFT JOIN (SELECT id, fx_code FROM Account) Account ON Account.id=POSITIVE_Detail.account_id "
        )
        sql.append(
            " LEFT JOIN (SELECT code, buy_rate, MAX(import_date) FROM FX_Rate ")
        sql.append(
            f" WHERE STRFTIME('%Y%m', import_date) = '{vestingMonth}' GROUP BY code) Rate ON Rate.code = Account.fx_code "
        )
        sql.append(
            " LEFT JOIN (SELECT stock_code, close_price, MAX(fetch_date) FROM Stock_Price_History "
        )
        sql.append(
            f" WHERE STRFTIME('%Y%m', fetch_date) = '{vestingMonth}' GROUP BY stock_code) Price ON Price.stock_code = Journal.stock_code "
        )

        sql.append(" ORDER BY Journal.stock_id ASC")

        return db.engine.execute("".join(sql))

    def queryStockCodeList(self):
        sql = []
        sql.append("SELECT stock_code, vesting_nation FROM Stock_Journal Stock ")
        sql.append(
            "LEFT JOIN Other_Asset Asset ON Stock.asset_id=Asset.asset_id ")

        return db.engine.execute("".join(sql))

    def add(self, stock_journal):
        db.session.add(stock_journal)
        db.session.flush()

        if DaoBase.session_commit(self) == "":
            return stock_journal
        else:
            return False

    def update(self):
        if DaoBase.session_commit(self) == "":
            return True
        else:
            return False

    def delete(self, stock_id):
        self.query.filter_by(stock_id=stock_id).delete()
        if DaoBase.session_commit(self) == "":
            return True
        else:
            return False

    def output4View(self, stock):
        # print('123', stock.hold_amount)
        hold_amount = round(
            stock.total_buy, 6) + stock.total_stock_dividend + round(stock.sold_amount, 6)
        return {
            "stock_id": stock.stock_id,
            "stock_code": stock.stock_code,
            "stock_name": stock.stock_name,
            "asset_id": stock.asset_id,
            "expected_spend": stock.expected_spend,
            "now_price": stock.now_price,
            "hold_amount": hold_amount,
            "actual_buy_price": round(abs(stock.total_cost+stock.total_gain) / (stock.total_buy-stock.sold_amount), 2)
            if stock.total_buy-stock.sold_amount != 0
            else 0,
            "buy_price": round(abs(stock.total_cost+stock.total_cash_dividend+stock.total_gain) / hold_amount, 2)
            if hold_amount != 0
            else 0,
            "sold_price": abs(round(stock.total_gain / stock.sold_amount, 2))
            if stock.sold_amount != 0
            else 0,
            "buy_date": datetime.strptime(stock.buy_date, "%Y-%m-%d %H:%M:%S.%f")
            if stock.buy_date
            else "",
            "sold_date": datetime.strptime(stock.sold_date, "%Y-%m-%d %H:%M:%S.%f")
            if stock.sold_date
            else "",
            "gain_lose": round(stock.gain_lose, 2),
            "ROI": round(stock.gain_lose / abs(stock.total_cost), 2)
            if stock.total_cost != 0
            else 0,
            # "dividend_yield": stock.dividend_yield,
        }

    def output(self, stock):
        return {
            "stock_id": stock.stock_id,
            "stock_code": stock.stock_code,
            "stock_name": stock.stock_name,
            "asset_id": stock.asset_id,
        }
