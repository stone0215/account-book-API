from sqlalchemy import asc

from ...dao_base import DaoBase

db = DaoBase().getDB()


class InsuranceNetValueHistory(db.Model):
    __tablename__ = 'Insurance_Net_Value_History'
    vesting_month = db.Column(db.String(6), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    asset_id = db.Column(db.Integer, primary_key=True)
    surrender_value = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    fx_rate = db.Column(db.Float, nullable=False)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, InsuranceNetValueHistory):
        self.vesting_month = InsuranceNetValueHistory.vesting_month
        self.id = InsuranceNetValueHistory.id
        self.name = InsuranceNetValueHistory.name
        self.asset_id = InsuranceNetValueHistory.asset_id
        self.surrender_value = InsuranceNetValueHistory.surrender_value
        self.cost = InsuranceNetValueHistory.cost
        self.fx_rate = InsuranceNetValueHistory.fx_rate

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByVestingMonth(self, vesting_month):
        return self.query.filter_by(vesting_month=vesting_month).all()

    def add(self, InsuranceNetValueHistory):
        db.session.add(InsuranceNetValueHistory)
        db.session.flush()

        # if DaoBase.session_commit(self) == '':
        #     return InsuranceNetValueHistory
        # else:
        #     return False

    def delete(self, asset_id):
        self.query.filter_by(asset_id=asset_id).delete()
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def output(self, asset):
        return {
            'asset_id': asset.asset_id,
            'vesting_month': asset.vesting_month,
            'id': asset.id,
            'name': asset.name,
            'asset_id': asset.asset_id
        }
