from sqlalchemy import asc

from ...dao_base import DaoBase

db = DaoBase().getDB()


class OtherAsset(db.Model):
    __tablename__ = 'Other_Asset'
    asset_id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(60), nullable=False)
    asset_type = db.Column(db.String(10), nullable=False)
    in_use = db.Column(db.String(1), nullable=False)
    asset_index = db.Column(db.SmallInteger, index=True)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, asset_name, asset_type, in_use, asset_index):
        self.asset_name = asset_name
        self.asset_type = asset_type
        self.in_use = in_use  # Y/M
        self.asset_index = asset_index or ''

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def getAll(self):
        return self.query.order_by(asc(self.asset_index)).all()

    def queryByKey(self, asset_id):
        return self.query.filter_by(asset_id=asset_id).first()

    def getDistinctItems(self):
        return self.query.with_entities(self.asset_id, self.asset_name, self.asset_type).filter_by(in_use='Y').distinct().all()

    def queryForInvestRatio(self, vestingMonth):
        sql = []
        sql.append(
            "SELECT estate_id, estate_excute_type, excute_price, excute_date, Other_Asset.asset_id, asset_name FROM Estate_Journal ")
        sql.append(
            " LEFT JOIN Estate ON Estate_Journal.estate_id=Estate.estate_id ")
        sql.append(
            " LEFT JOIN Other_Asset ON Estate.asset_id=Other_Asset.asset_id ")
        sql.append(
            f" WHERE STRFTIME('%Y%m', excute_date) <= '{vestingMonth}' ")
        sql.append(
            " UNION ALL SELECT insurance_id, insurance_excute_type, excute_price, excute_date, Other_Asset.asset_id, asset_name FROM Insurance_Journal ")
        sql.append(
            " LEFT JOIN Insurance ON Insurance_Journal.insurance_id=Insurance.insurance_id ")
        sql.append(
            " LEFT JOIN Other_Asset ON Insurance.asset_id=Other_Asset.asset_id ")
        sql.append(
            f" WHERE STRFTIME('%Y%m', excute_date) <= '{vestingMonth}' ")
        sql.append(
            " UNION ALL SELECT stock_id, excute_type, excute_price, excute_date, Other_Asset.asset_id, asset_name FROM Stock_Detail ")
        sql.append(
            " LEFT JOIN Stock_Journal ON Stock_Detail.stock_id=Stock_Journal.stock_id ")
        sql.append(
            " LEFT JOIN Other_Asset ON Stock_Journal.asset_id=Other_Asset.asset_id ")
        sql.append(
            f" WHERE STRFTIME('%Y%m', excute_date) <= '{vestingMonth}' ")
        sql.append(f" ORDER BY asset_id ASC ")

        return db.engine.execute(''.join(sql))

    def add(self, other_asset):
        db.session.add(other_asset)
        db.session.flush()

        # return other_asset // 如後續要寫入 Code table 打開這段，並註解以下

        if DaoBase.session_commit(self) == '':
            return other_asset
        else:
            return False

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
            'in_use': asset.in_use,
            'asset_index': asset.asset_index
        }

    def output4Item(self, asset):
        return {
            'asset_id': asset.asset_id,
            'asset_name': asset.asset_name,
            'asset_type': asset.asset_type
        }
