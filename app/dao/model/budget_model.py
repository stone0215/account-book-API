####
# 分類預算檔
####
from ..dao_base import DaoBase

db = DaoBase().getDB()


class Budget(db.Model):
    __tablename__ = 'Budget'
    year_month = db.Column(db.String(6), primary_key=True)
    category_code = db.Column(db.String(10), primary_key=True)
    category_name = db.Column(db.String(60), primary_key=True)
    expected = db.Column(db.Float, nullable=False)
    actual = db.Column(db.Float)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, year_month, category_code, category_name, expected, actual):
        self.year_month = year_month  # yyyy/mm
        self.category_code = category_code  # Code_Data.code
        self.category_name = category_name  # Code_Data.name
        self.expected = expected
        self.actual = actual

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def getAll(self):
        return self.query.all()

    def queryByKey(self, data):
        return self.query.filter_by(year_month=data['year_month'],
                                    category_code=data['category_code']).first()

    def queryByMonth(self, year_month):
        return self.query.filter_by(year_month=year_month)

    def add(self, budget):
        db.session.add(budget)
        db.session.flush()

        if DaoBase.session_commit(self) == '':
            return budget
        else:
            return False

    def update(self):
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def delete(self, data):
        self.query.filter_by(year_month=data['year_month'],
                             category_code=data['category_code']).delete()
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def output(self, Budget):
        return {
            'year_month': Budget.year_month,
            'category_code': Budget.category_code,
            'category_name': Budget.category_name,
            'expected': Budget.expected,
            'actual': Budget.actual
        }

    def outputByMonth(self, Budget):
        return {
            'category_name': Budget.category_name,
            'expected': Budget.expected
        }
