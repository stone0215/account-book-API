####
# 分類預算檔
####
from datetime import datetime
from sqlalchemy.sql import func

from ...dao_base import DaoBase

db = DaoBase().getDB()


class Budget(db.Model):
    __tablename__ = 'Budget'
    budget_year = db.Column(db.String(4), primary_key=True)
    category_code = db.Column(db.String(10), primary_key=True)
    category_name = db.Column(db.String(60), nullable=False)
    code_type = db.Column(db.String(10), nullable=False, index=True)
    expected01 = db.Column(db.Float, nullable=False)
    expected02 = db.Column(db.Float, nullable=False)
    expected03 = db.Column(db.Float, nullable=False)
    expected04 = db.Column(db.Float, nullable=False)
    expected05 = db.Column(db.Float, nullable=False)
    expected06 = db.Column(db.Float, nullable=False)
    expected07 = db.Column(db.Float, nullable=False)
    expected08 = db.Column(db.Float, nullable=False)
    expected09 = db.Column(db.Float, nullable=False)
    expected10 = db.Column(db.Float, nullable=False)
    expected11 = db.Column(db.Float, nullable=False)
    expected12 = db.Column(db.Float, nullable=False)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, category_code, category_name, code_type, budget_year=datetime.now().year, expected1=0, expected2=0, expected3=0, expected4=0, expected5=0, expected6=0, expected7=0, expected8=0, expected9=0, expected10=0, expected11=0, expected12=0):
        self.budget_year = budget_year  # yyyy/mm
        self.category_code = category_code  # Code_Data.code_id
        self.category_name = category_name  # Code_Data.name
        self.code_type = code_type  # Code_Data.code_type
        self.expected01 = expected1
        self.expected02 = expected2
        self.expected03 = expected3
        self.expected04 = expected4
        self.expected05 = expected5
        self.expected06 = expected6
        self.expected07 = expected7
        self.expected08 = expected8
        self.expected09 = expected9
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

    def queryForExpenditureBudget(self, vestingMonth):
        budgetColumn = 'expected'+vestingMonth[4:]
        sql = []

        sql.append(
            f"SELECT code_type AS type, category_name AS name, spending, {budgetColumn} AS budget, {budgetColumn}-IFNULL(spending,0) AS quota FROM Budget ")
        sql.append(
            "LEFT JOIN (SELECT action_main, action_main_type, SUM(spending) AS spending FROM Journal ")
        sql.append(
            f"WHERE vesting_month = '{vestingMonth}' AND (action_main_type='Floating' OR action_main_type='Fixed') GROUP BY action_main, action_main_type) ")
        sql.append(
            "AS Journal ON category_code=action_main ")
        # sql.append(
        #     "LEFT JOIN Code_Data Code ON code_id=category_code AND Code.code_type=Budget.code_type ")
        sql.append(
            f"WHERE budget_year=substr({vestingMonth}, 0,5) ")
        sql.append(" ORDER BY type ASC ")

        return db.engine.execute(''.join(sql))

    def query4Summary(self, year):
        sql = []

        sql.append(
            "SELECT SUM(expected01) AS expected01, SUM(expected02) AS expected02, SUM(expected03) AS expected03, ")
        sql.append(
            "SUM(expected04) AS expected04, SUM(expected05) AS expected05, SUM(expected06) AS expected06, SUM(expected07) AS expected07, ")
        sql.append(
            "SUM(expected08) AS expected08, SUM(expected09) AS expected09, SUM(expected10) AS expected10, ")
        sql.append(
            "SUM(expected11) AS expected11, SUM(expected12) AS expected12 FROM Budget ")
        sql.append(
            f"WHERE budget_year = '{year}' GROUP BY budget_year")

        return db.engine.execute(''.join(sql))

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
        sql = 'UPDATE Budget SET expected01=:1, expected02=:2, expected03=:3, expected04=:4, expected05=:5, expected06=:6, expected07=:7, expected08=:8, expected09=:9, expected10=:10, expected11=:11, expected12=:12 WHERE budget_year=:13 AND category_code=:14'

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
            'expected1': budget.expected01,
            'expected2': budget.expected02,
            'expected3': budget.expected03,
            'expected4': budget.expected04,
            'expected5': budget.expected05,
            'expected6': budget.expected06,
            'expected7': budget.expected07,
            'expected8': budget.expected08,
            'expected9': budget.expected09,
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

    def outputForBudget(self, Journal):
        return {
            'type': Journal.type,
            'name': Journal.name,
            'spending': Journal.spending,
            'budget': Journal.budget,
            'quota': Journal.quota
        }
