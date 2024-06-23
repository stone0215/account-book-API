from sqlalchemy import asc

from ...dao_base import DaoBase

db = DaoBase().getDB()


class OtherAsset(db.Model):
    __tablename__ = "Other_Asset"
    asset_id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(60), nullable=False)
    asset_type = db.Column(db.String(10), nullable=False)
    vesting_nation = db.Column(db.String(10))
    in_use = db.Column(db.String(1), nullable=False)
    asset_index = db.Column(db.SmallInteger, index=True)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, OtherAsset):
        self.asset_name = OtherAsset["asset_name"]
        self.asset_type = OtherAsset["asset_type"]
        self.vesting_nation = OtherAsset["vesting_nation"]
        self.in_use = OtherAsset["in_use"]  # Y/M
        self.asset_index = OtherAsset["asset_index"] or ""

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def getAll(self):
        return self.query.order_by(asc(self.asset_index)).all()

    def queryByKey(self, asset_id):
        return self.query.filter_by(asset_id=asset_id).first()

    def getDistinctItems(self):
        return (
            self.query.with_entities(self.asset_id, self.asset_name, self.asset_type)
            .filter_by(in_use="Y")
            .distinct()
            .all()
        )

    def getAssetBalanceHistory(self, start, end, type):
        sql = []

        # 帳戶
        sql.append(
            f"SELECT vesting_month AS dateString, balance, fx_rate, 'account' AS type FROM Account_Balance WHERE is_calculate='Y' AND "
        )
        if type == "month":
            sql.append(f" vesting_month >= '{start}' AND vesting_month <= '{end}' ")
        else:
            sql.append(
                f" vesting_month >= '{start}12' AND vesting_month <= '{end}12' AND substr(vesting_month, 5,2) = '12' "
            )

        sql.append(" UNION ALL ")
        # 不動產
        sql.append(
            f"SELECT vesting_month AS dateString, market_value AS balance, 1 AS fx_rate, 'estate' AS type FROM Estate_Net_Value_History WHERE "
        )
        if type == "month":
            sql.append(f" vesting_month >= '{start}' AND vesting_month <= '{end}' ")
        else:
            sql.append(
                f" vesting_month >= '{start}12' AND vesting_month <= '{end}12' AND substr(vesting_month, 5,2) = '12' "
            )
        sql.append(" UNION ALL ")
        # 保險
        sql.append(
            f"SELECT vesting_month AS dateString, surrender_value AS balance, fx_rate, 'insurance' AS type FROM Insurance_Net_Value_History WHERE "
        )
        if type == "month":
            sql.append(f" vesting_month >= '{start}' AND vesting_month <= '{end}' ")
        else:
            sql.append(
                f" vesting_month >= '{start}12' AND vesting_month <= '{end}12' AND substr(vesting_month, 5,2) = '12' "
            )
        sql.append(" UNION ALL ")
        # 股票
        sql.append(
            f"SELECT vesting_month AS dateString, price AS balance, fx_rate, 'stock' AS type FROM Stock_Net_Value_History WHERE "
        )
        if type == "month":
            sql.append(f" vesting_month >= '{start}' AND vesting_month <= '{end}' ")
        else:
            sql.append(
                f" vesting_month >= '{start}12' AND vesting_month <= '{end}12' AND substr(vesting_month, 5,2) = '12' "
            )
        sql.append(" ORDER BY dateString ASC ")

        return db.engine.execute("".join(sql))

    def add(self, other_asset):
        db.session.add(other_asset)
        db.session.flush()

        # return other_asset // 如後續要寫入 Code table 打開這段，並註解以下

        if DaoBase.session_commit(self) == "":
            return other_asset
        else:
            return False

    def update(self):
        if DaoBase.session_commit(self) == "":
            return True
        else:
            return False

    def delete(self, asset_id):
        self.query.filter_by(asset_id=asset_id).delete()
        if DaoBase.session_commit(self) == "":
            return True
        else:
            return False

    def output(self, asset):
        return {
            "asset_id": asset.asset_id,
            "asset_name": asset.asset_name,
            "asset_type": asset.asset_type,
            "vesting_nation": asset.vesting_nation,
            "in_use": asset.in_use,
            "asset_index": asset.asset_index,
        }

    def output4Item(self, asset):
        return {
            "asset_id": asset.asset_id,
            "asset_name": asset.asset_name,
            "asset_type": asset.asset_type,
        }
