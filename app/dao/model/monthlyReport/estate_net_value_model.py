from sqlalchemy import asc

from ...dao_base import DaoBase

db = DaoBase().getDB()


class EstateNetValueHistory(db.Model):
    __tablename__ = 'Estate_Net_Value_History'
    vesting_month = db.Column(db.String(6), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    asset_id = db.Column(db.Integer, primary_key=True)
    market_value = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    estate_status = db.Column(db.String(10), nullable=False)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, EstateNetValueHistory):
        self.vesting_month = EstateNetValueHistory.vesting_month
        self.id = EstateNetValueHistory.id
        self.name = EstateNetValueHistory.name
        self.asset_id = EstateNetValueHistory.asset_id
        self.market_value = EstateNetValueHistory.market_value
        self.cost = EstateNetValueHistory.cost
        self.estate_status = EstateNetValueHistory.estate_status

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByVestingMonth(self, vesting_month):
        return self.query.filter_by(vesting_month=vesting_month).all()

    def add(self, obj):
        db.session.add(obj)
        db.session.flush()

        # if DaoBase.session_commit(self) == '':
        #     return obj
        # else:
        #     return False

    def delete(self, asset_id):
        self.query.filter_by(asset_id=asset_id).delete()
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def outputForBalanceSheet(self, estates):
        amount = 0
        for estate in estates:
            amount += estate.market_value

        return {
            'type': '固定資產',
            'name': '不動產',
            'amount': amount
        }

    def outputForReport(self, estate):
        return {
            'assetType': '不動產',
            'detailType': estate.estate_status,
            'name': estate.name,
            'amount': estate.market_value
        }
