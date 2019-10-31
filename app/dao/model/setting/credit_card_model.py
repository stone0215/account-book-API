from ...dao_base import DaoBase

db = DaoBase().getDB()


class CreditCard(db.Model):
    __tablename__ = 'Credit_Card'
    credit_card_id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(60), nullable=False, index=True)
    last_day = db.Column(db.String(2), nullable=False)
    charge_day = db.Column(db.String(2), nullable=False)
    feedback_way = db.Column(db.String(1), nullable=False)
    fx_code = db.Column(db.String(3), nullable=False)
    in_use = db.Column(db.String(1), nullable=False, index=True)
    credit_card_index = db.Column(db.SmallInteger)
    note = db.Column(db.Text)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, card_name, last_day, charge_day, feedback_way, fx_code, in_use, note, credit_card_index=None):
        self.card_name = card_name
        self.last_day = last_day
        self.charge_day = charge_day
        self.feedback_way = feedback_way  # C：現金/ P：紅利/ N：無
        self.fx_code = fx_code
        self.in_use = in_use  # Y/M
        self.credit_card_index = credit_card_index
        self.note = note

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
        return self.query.with_entities(self.credit_card_id, self.card_name).filter_by(in_use='Y')

    def add(self, credit_card):
        db.session.add(credit_card)
        db.session.flush()

        return credit_card

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
            'last_day': credit_card.last_day,
            'charge_day': credit_card.charge_day,
            'feedback_way': credit_card.feedback_way,
            'fx_code': credit_card.fx_code,
            'in_use': credit_card.in_use,
            'credit_card_index': credit_card.credit_card_index,
            'note': credit_card.note
        }

    def output4Selection(self, credit_card):
        return {
            'key': credit_card.credit_card_id,
            'value': credit_card.card_name
        }
