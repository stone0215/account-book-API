from sqlalchemy import asc

from ...dao_base import DaoBase

db = DaoBase().getDB()


class OtherAsset(db.Model):
    __tablename__ = 'Other_Asset'
    asset_id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(60), nullable=False)
    asset_type = db.Column(db.String(1), nullable=False)
    account_id = db.Column(db.Integer, nullable=False)
    account_name = db.Column(db.String(60), nullable=False)
    expected_spend = db.Column(db.Float, nullable=False)
    in_use = db.Column(db.String(1), nullable=False)
    asset_index = db.Column(db.SmallInteger, index=True)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, asset_name, asset_type, account_id, account_name, expected_spend, in_use, asset_index):
        self.asset_name = asset_name
        self.account_id = account_id
        self.asset_type = asset_type
        self.account_name = account_name
        self.expected_spend = expected_spend
        self.in_use = in_use  # Y/M
        self.asset_index = asset_index

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def getAll(self):
        return self.query.order_by(asc(self.asset_index)).all()

    def queryByKey(self, asset_id):
        return self.query.filter_by(asset_id=asset_id).first()

    def add(self, other_asset):
        db.session.add(other_asset)
        db.session.flush()

        return other_asset

    def update(self):
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def delete(self, asset_id):
        self.query.filter_by(asset_id=asset_id).delete()
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def output(self, asset):
        return {
            'asset_id': asset.asset_id,
            'asset_name': asset.asset_name,
            'asset_type': asset.asset_type,
            'account_id': asset.account_id,
            'account_name': asset.account_name,
            'expected_spend': asset.expected_spend,
            'in_use': asset.in_use,
            'asset_index': asset.asset_index
        }
