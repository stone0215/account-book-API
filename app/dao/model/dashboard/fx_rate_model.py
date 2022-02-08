from ...dao_base import DaoBase

db = DaoBase().getDB()


class FXRate(db.Model):
    __tablename__ = "FX_Rate"
    import_date = db.Column(db.DateTime, primary_key=True)
    code = db.Column(db.String(3), primary_key=True)
    buy_rate = db.Column(db.Float, nullable=False)  # 銀行向你買回的價格

    # 物件建立之後所要建立的初始化動作
    def __init__(self, FXRate):
        self.import_date = FXRate.import_date
        self.code = FXRate.code
        self.buy_rate = FXRate.buy_rate

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, import_date, code):
        sql = f"SELECT COUNT(*) as recordNum FROM FX_Rate WHERE import_date='{import_date}' AND code='{code}'"

        try:
            return db.engine.execute(sql).fetchone()
        except Exception as error:
            return None

    def bulkInsert(self, datas):
        sql = "INSERT INTO FX_Rate(import_date, code, buy_rate) VALUES(:1, :2, :3)"

        params = []
        try:
            for item in datas:
                params.append(
                    (item["import_date"], item["code"], item["buy_rate"]))

            db.engine.execute(sql, params)
            # with db.engine.connect() as conn:
            #     result = conn.execute(sql, params)
            #     print('123', result)
            return True
        except Exception as error:
            return False
