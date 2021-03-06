from sqlalchemy import asc

from ...dao_base import DaoBase

db = DaoBase().getDB()


class InsuranceJournal(db.Model):
    __tablename__ = 'Insurance_Journal'
    distinct_number = db.Column(db.Integer, primary_key=True)
    insurance_id = db.Column(db.Integer, nullable=False, index=True)
    insurance_excute_type = db.Column(db.String(10), nullable=False)
    excute_price = db.Column(db.Float)
    excute_date = db.Column(db.DateTime, nullable=False, index=True)
    memo = db.Column(db.Text)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, insurance_id, insurance_excute_type, excute_price, excute_date, memo):
        self.insurance_id = insurance_id
        self.insurance_excute_type = insurance_excute_type
        self.excute_price = excute_price
        self.excute_date = excute_date
        self.memo = memo if memo else None

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def getAll(self):
        return self.query.order_by(asc(self.excute_date)).all()

    def queryByKey(self, distinct_number):
        return self.query.filter_by(distinct_number=distinct_number).first()

    def queryByInsuranceId(self, insurance_id):
        return self.query.filter_by(insurance_id=insurance_id)

    def add(self, insurance_asset):
        db.session.add(insurance_asset)
        db.session.flush()

        if DaoBase.session_commit(self) == '':
            return insurance_asset
        else:
            return False

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
            'insurance_id': asset.insurance_id,
            'insurance_excute_type': asset.insurance_excute_type,
            'excute_price': asset.excute_price,
            'excute_date': asset.excute_date,
            'memo': asset.memo
        }
