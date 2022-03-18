from sqlalchemy import desc, asc, or_

from ...dao_base import DaoBase

db = DaoBase().getDB()


class Code(db.Model):
    __tablename__ = 'Code_Data'
    code_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, index=True)
    code_type = db.Column(db.String(10), nullable=False, index=True)
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
        self.code_index = code_index or ''

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, code_id):
        return self.query.filter_by(code_id=code_id).first()

    def querySubCodeList(self, parent_id):
        return self.query.filter_by(code_group=parent_id).order_by(asc(self.code_index)).all()

    def queryByConditions(self, conditions):
        sql = []
        sql.append(
            "SELECT code_id, name, code_type, in_use, code_index FROM Code_Data WHERE code_group IS NULL")

        if conditions.get('name') != '':
            sql.append(f" AND name LIKE '%{conditions.get('name')}%'")

        if conditions.get('code_type') != '':
            sql.append(
                f" AND code_type = '{conditions.get('code_type')}'")

        sql.append(" ORDER BY code_index ASC, code_type")

        return db.engine.execute(''.join(sql))

    def query4BudgetSelection(self):
        return self.query.with_entities(self.code_id, self.name, self.code_type).filter_by(in_use='Y', code_group=None).filter(or_(Code.code_type == 'Fixed', Code.code_type == 'Floating')).all()

    def query4Selection(self):
        return self.query.with_entities(self.code_id, self.name, self.code_type, self.code_index).filter_by(in_use='Y', code_group=None)

    def query4SubSelection(self, parent_id):
        return self.query.with_entities(self.code_id, self.name, self.code_type, self.code_group, self.code_index).filter_by(code_group=parent_id, in_use='Y').order_by(asc(self.code_index)).all()

    def queryAllSubCodeList(self):
        sql = []
        sql.append(
            "SELECT code_id, name, code_type, code_group, code_index FROM Code_Data WHERE code_group IS NOT NULL")

        sql.append(" ORDER BY code_index ASC")

        return db.engine.execute(''.join(sql))

    def add(self, code):
        db.session.add(code)
        db.session.flush()

        # print(DaoBase.session_commit(self))  # print sql string
        if DaoBase.session_commit(self) == '':
            return code
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

    def outputMainCode(self, Code):
        return {
            'code_id': Code.code_id,
            'name': Code.name,
            'code_type': Code.code_type,
            'in_use': Code.in_use,
            'code_index': Code.code_index
        }

    def outputSubCode(self, Code):
        return {
            'code_id': Code.code_id,
            'name': Code.name,
            'in_use': Code.in_use,
            'code_index': Code.code_index
        }

    def output4Selection(self, Code):
        return {
            'key': Code.code_id,
            'value': Code.name,
            'index': Code.code_index,
            'type': Code.code_type,
            'table': 'Code'  # 為了區分每個 id 隸屬於哪個 table，因為下拉選單id可能重複
        }

    def output4SubSelection(self, Code):
        return {
            'key': Code.code_id,
            'value': Code.name,
            'index': Code.code_index,
            'type': Code.code_type,
            "code_group": Code.code_group,
            'table': 'Code'  # 為了區分每個 id 隸屬於哪個 table，因為下拉選單id可能重複
        }
