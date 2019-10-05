from sqlalchemy import desc, asc

from ..dao_base import DaoBase

db = DaoBase().getDB()


class Code(db.Model):
    __tablename__ = 'Code_Data'
    code_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, index=True)
    code_type = db.Column(db.String(1), nullable=False, index=True)
    code_group = db.Column(db.Integer)
    code_group_name = db.Column(db.String(60))
    in_use = db.Column(db.String(1), nullable=False, index=True)
    code_index = db.Column(db.SmallInteger)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, name, code_type, in_use, code_index, code_group=None, code_group_name=None):
        self.name = name
        self.code_type = code_type  # S：固定支出 / F：浮動支出 / I：收入 / A：資產
        self.code_group = code_group
        self.code_group_name = code_group_name
        self.in_use = in_use  # Y/M
        self.code_index = code_index

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, code_id):
        return self.query.filter_by(code_id=code_id).first()

    def queryByConditions(self, conditions):
        sql = []
        sql.append("SELECT * FROM Code_Data WHERE 1=1")

        if conditions.get('name') != '':
            sql.append(f" AND name LIKE '%{conditions.get('name')}%'")

        if conditions.get('code_type') != '':
            sql.append(
                f" AND code_type = '{conditions.get('code_type')}'")

        sql.append(" ORDER BY code_index ASC, code_type")

        return db.engine.execute(''.join(sql))

    def add(self, account):
        db.session.add(account)
        # db.session.flush()

        print(DaoBase.session_commit(self))  # print sql string
        if DaoBase.session_commit(self) == '':
            return account
        else:
            return False

    def update(self):
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def delete(self, code_id):
        self.query.filter_by(code_id=code_id).delete()
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def output(self, CreditCard):
        return {
            'code_id': CreditCard.code_id,
            'name': CreditCard.name,
            'code_type': CreditCard.code_type,
            'code_group': CreditCard.code_group,
            'code_group_name': CreditCard.code_group_name,
            'in_use': CreditCard.in_use,
            'code_index': CreditCard.code_index
        }
