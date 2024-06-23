from ...dao_base import DaoBase

db = DaoBase().getDB()


class CreditCard(db.Model):
    __tablename__ = 'Credit_Card'
    credit_card_id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(60), nullable=False, index=True)
    card_no = db.Column(db.String(19), nullable=False)
    last_day = db.Column(db.String(2), nullable=False)
    charge_day = db.Column(db.String(2), nullable=False)
    limit_date = db.Column(db.String(7), nullable=False)
    feedback_way = db.Column(db.String(5), nullable=False)
    fx_code = db.Column(db.String(3), nullable=False)
    in_use = db.Column(db.String(1), nullable=False, index=True)
    credit_card_index = db.Column(db.SmallInteger)
    carrier_no = db.Column(db.String(60))
    note = db.Column(db.Text)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, CreditCard):
        self.card_name = CreditCard["card_name"]
        self.card_no = CreditCard["card_no"]
        self.last_day = CreditCard["last_day"]
        self.charge_day = CreditCard["charge_day"]
        self.limit_date = CreditCard["limit_date"]
        self.feedback_way = CreditCard["feedback_way"]  # C：現金/ P：紅利/ N：無
        self.fx_code = CreditCard["fx_code"]
        self.in_use = CreditCard["in_use"]  # Y/M
        self.credit_card_index = CreditCard["credit_card_index"] or ''
        self.carrier_no = CreditCard["carrier_no"] or None
        self.note = CreditCard["note"]

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    # def getAll(self):
    #     return self.query.order_by(asc(self.charge_day)).all()

    def queryByKey(self, credit_card_id):
        return self.query.filter_by(credit_card_id=credit_card_id).first()

    def queryByConditions(self, conditions):
        sql = []
        sql.append(
            "SELECT * FROM Credit_Card WHERE 1=1")

        if conditions.get('card_name') != '':
            sql.append(
                f" AND card_name LIKE '%{conditions.get('card_name')}%'")

        if conditions.get('in_use') != '':
            sql.append(f" AND in_use = '{conditions.get('in_use')}'")

        sql.append(" ORDER BY credit_card_index ASC")

        return db.engine.execute(''.join(sql))

    def query4Selection(self):
        return self.query.with_entities(self.credit_card_id, self.card_name, self.feedback_way, self.credit_card_index).filter_by(in_use='Y')

    def query4Summary(self, lastMonth, vestingMonth):
        sql = []
        sql.append(
            "SELECT '' AS vesting_month, credit_card_id AS id, card_name AS name, IFNULL(balance,0) AS balance, IFNULL(buy_rate,1) AS fx_rate FROM Credit_Card ")
        sql.append(
            f" LEFT JOIN Credit_Card_Balance Balance ON Balance.vesting_month =  ")
        if lastMonth != '':
            sql.append(f" '{lastMonth}' ")
        else:
            sql.append(" (SELECT MAX(vesting_month) FROM Credit_Card_Balance) ")
        sql.append(
            " AND Balance.id=Credit_Card.credit_card_id LEFT JOIN (SELECT code, buy_rate, MAX(import_date) FROM FX_Rate ")
        sql.append(
            f" WHERE STRFTIME('%Y%m', import_date) = '{vestingMonth}' GROUP BY code) Rate ON Rate.code = Credit_Card.fx_code ")

        sql.append(" ORDER BY credit_card_id ASC")

        return db.engine.execute(''.join(sql))

    def queryByCarrierNo(self, carrier_no):
        sql = []
        sql.append(
            f"SELECT 'Account' AS table_name, id, account_type AS type, carrier_no FROM Account WHERE carrier_no = '{carrier_no}' ")
        sql.append(
            "UNION ALL ")
        sql.append(
            f"SELECT 'Credit_Card' AS table_name, credit_card_id AS id, 'Credit_Card' AS type, carrier_no FROM Credit_Card WHERE carrier_no = '{carrier_no}' ")

        return db.engine.execute(''.join(sql)).fetchone()

    def add(self, credit_card):
        db.session.add(credit_card)
        db.session.flush()

        if DaoBase.session_commit(self) == '':
            return credit_card
        else:
            return False

    def update(self):
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def delete(self, credit_card_id):
        self.query.filter_by(credit_card_id=credit_card_id).delete()
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def output(self, credit_card):
        return {
            'credit_card_id': credit_card.credit_card_id,
            'card_name': credit_card.card_name,
            'card_no': credit_card.card_no,
            'last_day': credit_card.last_day,
            'charge_day': credit_card.charge_day,
            'limit_date': credit_card.limit_date,
            'feedback_way': credit_card.feedback_way,
            'fx_code': credit_card.fx_code,
            'in_use': credit_card.in_use,
            'credit_card_index': credit_card.credit_card_index,
            'note': credit_card.note
        }

    def output4Selection(self, CreditCard):
        return {
            'key': CreditCard.credit_card_id,
            'value': CreditCard.card_name,
            'index': CreditCard.credit_card_index,
            'table': 'Credit_Card',
            'type': CreditCard.feedback_way
        }
