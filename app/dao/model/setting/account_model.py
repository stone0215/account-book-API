from ...dao_base import DaoBase

db = DaoBase().getDB()


class Account(db.Model):
    __tablename__ = 'Account'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(20))
    name = db.Column(db.String(60), nullable=False, index=True)
    account_type = db.Column(db.String(10), nullable=False, index=True)
    fx_code = db.Column(db.String(3), nullable=False)
    is_calculate = db.Column(db.String(1), nullable=False)
    in_use = db.Column(db.String(1), nullable=False, index=True)
    discount = db.Column(db.Float)
    memo = db.Column(db.Text)
    owner = db.Column(db.String(60))
    account_index = db.Column(db.SmallInteger)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, Account):
        self.account_id = Account['account_id']
        self.name = Account['name']
        self.account_type = Account['account_type']
        self.fx_code = Account['fx_code']
        self.is_calculate = Account['is_calculate']
        self.in_use = Account['in_use']  # Y/M
        self.discount = Account['discount']
        self.memo = Account['memo']
        self.owner = Account['owner']
        self.account_index = Account['account_index'] or None

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, id):
        return self.query.filter_by(id=id).first()

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

        sql.append(" ORDER BY account_index ASC")

        return db.engine.execute(''.join(sql))

    def query4Selection(self):
        return self.query.with_entities(self.id, self.name, self.account_type, self.account_index).filter_by(in_use='Y')

    def query4Summary(self, lastMonth, vestingMonth):
        sql = []
        sql.append(
            "SELECT '' AS vesting_month, Account.id, Account.name, IFNULL(balance,0) AS balance, Account.fx_code, IFNULL(buy_rate,1) AS fx_rate, Account.is_calculate ")
        sql.append(
            f" FROM Account LEFT JOIN Account_Balance Balance ON Balance.vesting_month = '{lastMonth}' AND Balance.id=Account.id ")
        sql.append(
            " LEFT JOIN (SELECT code, buy_rate, MAX(import_date) FROM FX_Rate ")
        sql.append(
            f" WHERE STRFTIME('%Y%m', import_date) = '{vestingMonth}' GROUP BY code) Rate ON Rate.code = Account.fx_code ")

        sql.append(" ORDER BY Account.id ASC")

        return db.engine.execute(''.join(sql))

    def add(self, account):
        db.session.add(account)
        db.session.flush()

        if DaoBase.session_commit(self) == '':
            return account
        else:
            return False

    def update(self):
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def delete(self, id):
        self.query.filter_by(id=id).delete()
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def output(self, Account):
        return {
            'id': Account.id,
            'account_id': Account.account_id,
            'name': Account.name,
            'account_type': Account.account_type,
            'fx_code': Account.fx_code,
            'is_calculate': Account.is_calculate,
            'in_use': Account.in_use,
            'discount': Account.discount,
            'memo': Account.memo,
            'owner': Account.owner,
            'account_index': Account.account_index
        }

    def output4Selection(self, Account):
        return {
            'key': Account.id,
            'value': Account.name,
            'index': Account.account_index,
            'type': Account.account_type,
            'table': 'Account'  # 為了區分每個 id 隸屬於哪個 table，因為下拉選單id可能重複
        }
