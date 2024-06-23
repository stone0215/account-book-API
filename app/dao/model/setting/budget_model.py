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
    def __init__(self, Budget):
        self.budget_year = Budget['budget_year']  # yyyy
        self.category_code = Budget['category_code']  # Code_Data.code_id
        self.category_name = Budget['category_name']  # Code_Data.name
        self.code_type = Budget['code_type']  # Code_Data.code_type
        self.expected01 = Budget['expected01'] if 'expected01' in Budget else 0
        self.expected02 = Budget['expected02'] if 'expected02' in Budget else 0
        self.expected03 = Budget['expected03'] if 'expected03' in Budget else 0
        self.expected04 = Budget['expected04'] if 'expected04' in Budget else 0
        self.expected05 = Budget['expected05'] if 'expected05' in Budget else 0
        self.expected06 = Budget['expected06'] if 'expected06' in Budget else 0
        self.expected07 = Budget['expected07'] if 'expected07' in Budget else 0
        self.expected08 = Budget['expected08'] if 'expected08' in Budget else 0
        self.expected09 = Budget['expected09'] if 'expected09' in Budget else 0
        self.expected10 = Budget['expected10'] if 'expected10' in Budget else 0
        self.expected11 = Budget['expected11'] if 'expected11' in Budget else 0
        self.expected12 = Budget['expected12'] if 'expected12' in Budget else 0

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
            f"SELECT code_type AS type, category_name AS name, IFNULL(spending,0) AS spending, {budgetColumn} AS budget, {budgetColumn}-IFNULL(spending,0) AS quota FROM Budget ")
        sql.append(
            "LEFT JOIN (SELECT action_main, action_main_type, SUM(spending*IFNULL(buy_rate,1)) AS spending FROM Journal ")
        sql.append(
            "LEFT JOIN Account ON spend_way_table='Account' AND spend_way=id ")
        sql.append(
            "LEFT JOIN Credit_Card ON spend_way_table='Credit_Card' AND spend_way=credit_card_id ")
        sql.append(
            "LEFT JOIN FX_Rate ON code = IFNULL(Account.fx_code, Credit_Card.fx_code) AND import_date=(SELECT MAX(import_date) AS import_date FROM FX_Rate WHERE STRFTIME('%Y%m', import_date)=vesting_month) ")
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
        sql = 'INSERT INTO Budget(budget_year, category_code, category_name, code_type, expected01, expected02, expected03, expected04, expected05, expected06, expected07, expected08, expected09, expected10, expected11, expected12) VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16)'

        params = []
        try:
            for item in datas:
                params.append((item.budget_year, item.category_code, item.category_name, item.code_type, item.expected01,
                               item.expected02, item.expected03, item.expected04, item.expected05, item.expected06,
                               item.expected07, item.expected08, item.expected09, item.expected10, item.expected11,
                               item.expected12))

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
                params.append((item['expected1'], item['expected2'], item['expected3'], item['expected4'], item['expected5'],
                               item['expected6'], item['expected7'], item['expected8'], item['expected9'], item['expected10'],
                               item['expected11'], item['expected12'], item['budget_year'], item['category_code']))

            db.engine.execute(sql, params)
            return True
        except Exception as error:
            return False

    def deleteByYear(self, year):
        self.query.filter(self.budget_year == year).delete()

        if DaoBase.session_commit(self) == '':
            return True
        else:
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
            'spending': round(Journal.spending, 2),
            'budget': Journal.budget,
            'quota': round(Journal.quota, 3)
        }
