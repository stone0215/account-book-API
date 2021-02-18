####
# 分類預算檔
####
from datetime import datetime
from sqlalchemy.sql import func

from ...dao_base import DaoBase

db = DaoBase().getDB()


class Budget(db.Model):
    __tablename__ = 'Budget'
    budget_year = db.Column(db.String(6), primary_key=True)
    category_code = db.Column(db.String(10), primary_key=True)
    category_name = db.Column(db.String(60), nullable=False)
    code_type = db.Column(db.String(10), nullable=False, index=True)
    expected1 = db.Column(db.Float, nullable=False)
    expected2 = db.Column(db.Float, nullable=False)
    expected3 = db.Column(db.Float, nullable=False)
    expected4 = db.Column(db.Float, nullable=False)
    expected5 = db.Column(db.Float, nullable=False)
    expected6 = db.Column(db.Float, nullable=False)
    expected7 = db.Column(db.Float, nullable=False)
    expected8 = db.Column(db.Float, nullable=False)
    expected9 = db.Column(db.Float, nullable=False)
    expected10 = db.Column(db.Float, nullable=False)
    expected11 = db.Column(db.Float, nullable=False)
    expected12 = db.Column(db.Float, nullable=False)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, category_code, category_name, code_type, budget_year=datetime.now().year, expected1=0, expected2=0, expected3=0, expected4=0, expected5=0, expected6=0, expected7=0, expected8=0, expected9=0, expected10=0, expected11=0, expected12=0):
        self.budget_year = budget_year  # yyyy/mm
        self.category_code = category_code  # Code_Data.code_id
        self.category_name = category_name  # Code_Data.name
        self.code_type = code_type  # Code_Data.code_type
        self.expected1 = expected1
        self.expected2 = expected2
        self.expected3 = expected3
        self.expected4 = expected4
        self.expected5 = expected5
        self.expected6 = expected6
        self.expected7 = expected7
        self.expected8 = expected8
        self.expected9 = expected9
        self.expected10 = expected10
        self.expected11 = expected11
        self.expected12 = expected12

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, data):
        return self.query.filter_by(budget_year=data['budget_year'],
                                    category_code=data['category_code']).first()

    def queryByYear(self, budget_year):
        return self.query.filter_by(budget_year=budget_year)

    def getBudgetRange(self):
        return db.session.query(func.max(self.budget_year).label("max"), func.min(self.budget_year).label("min")).one()

    def add(self, budget):
        db.session.add(budget)
        db.session.flush()

        if DaoBase.session_commit(self) == '':
            return budget
        else:
            return False

    def bulkInsert(self, datas):
        sql = 'INSERT INTO Budget(budget_year, category_code, category_name, code_type, expected1, expected2, expected3, expected4, expected5, expected6, expected7, expected8, expected9, expected10, expected11, expected12) VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16)'

        params = []
        try:
            for item in datas:
                # todo: search for better way to select before update
                params.append((item.budget_year, item.category_code, item.category_name, item.code_type, item.expected1, item.expected2, item.expected3, item.expected4,
                               item.expected5, item.expected6, item.expected7, item.expected8, item.expected9, item.expected10, item.expected11, item.expected12))

            db.engine.execute(sql, params)
            return True
        except Exception as error:
            return False

    def update(self, datas):
        sql = 'UPDATE Budget SET expected1=:1, expected2=:2, expected3=:3, expected4=:4, expected5=:5, expected6=:6, expected7=:7, expected8=:8, expected9=:9, expected10=:10, expected11=:11, expected12=:12 WHERE budget_year=:13 AND category_code=:14'

        params = []
        try:
            for item in datas:
                # todo: search for better way to select before update
                params.append((item['expected1'], item['expected2'], item['expected3'], item['expected4'], item['expected5'], item['expected6'], item['expected7'], item['expected8'], item['expected9'], item['expected10'], item['expected11'], item['expected12'],
                               item['budget_year'], item['category_code']))

            db.engine.execute(sql, params)
            return True
        except Exception as error:
            return False

    def outputByYear(self, budget):
        return {
            'budget_year': budget.budget_year,
            'category_code': budget.category_code,
            'category_name': budget.category_name,
            'code_type': budget.code_type,
            'expected1': budget.expected1,
            'expected2': budget.expected2,
            'expected3': budget.expected3,
            'expected4': budget.expected4,
            'expected5': budget.expected5,
            'expected6': budget.expected6,
            'expected7': budget.expected7,
            'expected8': budget.expected8,
            'expected9': budget.expected9,
            'expected10': budget.expected10,
            'expected11': budget.expected11,
            'expected12': budget.expected12
        }

    def outputRange(self, budget):
        thisYear = datetime.now().year
        return {
            'min': thisYear if budget.min is None else int(budget.min),
            'max': thisYear if budget.min is None else int(budget.max)
        }
