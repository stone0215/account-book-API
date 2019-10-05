from sqlalchemy import desc, asc

from ..dao_base import DaoBase

db = DaoBase().getDB()


class Account(db.Model):
    __tablename__ = 'Account'
    account_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, index=True)
    account_type = db.Column(db.String(1), nullable=False, index=True)
    fx_code = db.Column(db.String(3), nullable=False)
    is_calculate = db.Column(db.String(1), nullable=False)
    in_use = db.Column(db.String(1), nullable=False, index=True)
    discount = db.Column(db.Float)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, name, account_type, fx_code, is_calculate, in_use, discount):
        self.name = name
        self.account_type = account_type  # N：一般帳戶/ F：財務規劃帳戶
        self.fx_code = fx_code
        self.is_calculate = is_calculate
        self.in_use = in_use  # Y/M
        self.discount = discount

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, account_id):
        return self.query.filter_by(account_id=account_id).first()

    def queryByConditions(self, conditions):
        sql = []
        sql.append("SELECT * FROM Account WHERE 1=1")

        if conditions.get('name') != '':
            sql.append(f" AND name LIKE '%{conditions.get('name')}%'")

        if conditions.get('account_type') != '':
            sql.append(
                f" AND account_type = '{conditions.get('account_type')}'")

        if conditions.get('in_use') != '':
            sql.append(f" AND in_use = '{conditions.get('in_use')}'")

        return db.engine.execute(''.join(sql))

    def add(self, account):
        db.session.add(account)
        db.session.flush()

        # print(DaoBase.session_commit(self)) # print sql string
        if DaoBase.session_commit(self) == '':
            return account
        else:
            return False

    def update(self):
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def delete(self, account_id):
        self.query.filter_by(account_id=account_id).delete()
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def output(self, Account):
        return {
            'account_id': Account.account_id,
            'name': Account.name,
            'account_type': Account.account_type,
            'fx_code': Account.fx_code,
            'is_calculate': Account.is_calculate,
            'in_use': Account.in_use,
            'discount': Account.discount
        }
