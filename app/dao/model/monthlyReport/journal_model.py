from datetime import datetime, timedelta
from sqlalchemy import asc

from ...dao_base import DaoBase

db = DaoBase().getDB()


class Journal(db.Model):
    __tablename__ = 'Journal'
    distinct_number = db.Column(db.Integer, primary_key=True)
    vesting_month = db.Column(db.String(6), nullable=False, index=True)
    spend_date = db.Column(db.DateTime, nullable=False, index=True)
    spend_way = db.Column(db.String(10), nullable=False)
    spend_way_type = db.Column(db.String(20), nullable=False)
    spend_way_table = db.Column(db.String(15), nullable=False)
    action_main = db.Column(db.String(10), nullable=False)
    action_main_type = db.Column(db.String(20), nullable=False)
    action_main_table = db.Column(db.String(15), nullable=False)
    action_sub = db.Column(db.String(10), nullable=False)
    action_sub_type = db.Column(db.String(20), nullable=False)
    action_sub_table = db.Column(db.String(10), nullable=False)
    spending = db.Column(db.Float, nullable=False)
    invoice_number = db.Column(db.String(10))
    note = db.Column(db.Text)

    # 物件建立之後所要建立的初始化動作
    def __init__(self, Journal):
        self.vesting_month = Journal['vesting_month']
        self.spend_date = Journal['spend_date']
        self.spend_way = Journal['spend_way']
        self.spend_way_type = Journal['spend_way_type']
        self.spend_way_table = Journal['spend_way_table']
        self.action_main = Journal['action_main']
        self.action_main_type = Journal['action_main_type']
        self.action_main_table = Journal['action_main_table']
        self.action_sub = Journal['action_sub']
        self.action_sub_type = Journal['action_sub_type']
        self.action_sub_table = Journal['action_sub_table']
        self.spending = Journal['spending']
        self.invoice_number = Journal['invoice_number'] if Journal['invoice_number'] else None
        self.note = Journal['note'] if Journal['note'] else None

    # 定義物件的字串描述，執行 print(x) 就會跑這段
    def __str__(self):
        return self

    def queryByKey(self, distinct_number):
        return self.query.filter_by(distinct_number=distinct_number).first()

    def queryByVestingMonth(self, vesting_month):
        sql = []
        sql.append(
            "SELECT Journal.*, fx_code, IFNULL(buy_rate,1) AS fx_rate FROM Journal ")
        sql.append("LEFT JOIN Account ON id=spend_way ")
        sql.append("LEFT JOIN FX_Rate ON code=fx_code AND ")
        sql.append(
            f"import_date=(SELECT MAX(import_date) FROM FX_Rate WHERE STRFTIME('%Y%m', import_date) = '{vesting_month}' )")
        sql.append(
            f"WHERE vesting_month = '{vesting_month}' ORDER BY spend_date")

        return db.engine.execute(''.join(sql))

    def queryByVestingMonthAndInvoice(self, vesting_month, invoice_number):
        return self.query.filter_by(vesting_month=vesting_month, invoice_number=invoice_number).first()

    def queryEstateOrLiabilityRecord(self, vestingMonth):
        sql = []
        sql.append(
            f"SELECT 'Estate' AS name, IFNULL(MAX(id),0) AS has_record FROM Estate_Net_Value_History WHERE vesting_month = '{vestingMonth}' ")
        sql.append(
            f" UNION ALL SELECT 'Insurance' AS name, IFNULL(MAX(id),0) AS has_record FROM Insurance_Net_Value_History WHERE vesting_month = '{vestingMonth}' ")
        sql.append(
            f" UNION ALL SELECT 'Loan' AS name, IFNULL(MAX(id),0) AS has_record FROM Loan_Balance WHERE vesting_month = '{vestingMonth}' ")
        sql.append(
            f" UNION ALL SELECT 'Stock' AS name, IFNULL(MAX(id),0) AS has_record FROM Stock_Net_Value_History WHERE vesting_month = '{vestingMonth}' ")

        return db.engine.execute(''.join(sql))

    def queryForExpenditureRatio(self, vestingMonth, sortColumn):
        inputDate = datetime.strptime(vestingMonth, '%Y%m')
        inputDateTime = datetime(
            inputDate.year, inputDate.month+1, 1, 23, 59, 59)-timedelta(days=1)
        sql = []
        sql.append(
            "SELECT *, name AS action_main_name, spending*IFNULL(fx_rate,1) AS spending FROM Journal ")
        sql.append(" LEFT JOIN Code_Data ON code_id=action_main ")
        sql.append(
            " LEFT JOIN (SELECT id, fx_code FROM Account) Account ON Account.id=Journal.spend_way AND spend_way_table='Account' ")
        sql.append(
            " LEFT JOIN (SELECT code, buy_rate AS fx_rate, MAX(import_date) FROM FX_Rate ")
        sql.append(
            f" WHERE import_date <= '{inputDateTime}' GROUP BY code) Rate ON Rate.code = Account.fx_code ")
        sql.append(
            f" WHERE vesting_month = '{vestingMonth}' AND action_main_table='Code' ")
        sql.append(f" ORDER BY {sortColumn} ASC ")

        return db.engine.execute(''.join(sql))

    def queryForInvestRatio(self, vestingMonth):
        sql = []
        # 賣出外幣
        sql.append(
            "SELECT '賣出' AS action, '換匯' AS target,  (CASE WHEN spend_way_type='finance' THEN spending*note ELSE spending END)*-1 AS spending FROM Journal ")
        sql.append(
            f"WHERE vesting_month = '{vestingMonth}' AND ((spend_way_type='finance' AND action_sub_type='normal' AND spending < 0 ) ")
        sql.append(
            "OR (spend_way_type='normal' AND action_sub_type='finance' AND spending > 0 )) ")
        # 賣出股票
        sql.append(
            " UNION ALL SELECT '賣出' AS action, '股票' AS target, excute_price*IFNULL(fx_rate,1)*-1 AS spending ")
        sql.append(
            " FROM Stock_Detail AS Stock LEFT JOIN (SELECT id, fx_code FROM Account) Account ON Account.id=Stock.account_id ")
        sql.append(
            " LEFT JOIN (SELECT code, buy_rate AS fx_rate, MAX(import_date) FROM FX_Rate ")
        sql.append(
            f" WHERE STRFTIME('%Y%m', import_date) = '{vestingMonth}' GROUP BY code) Rate ON Rate.code = Account.fx_code ")
        sql.append(
            f"WHERE STRFTIME('%Y%m', excute_date) = '{vestingMonth}' AND excute_type='sell' ")
        # 贖回保險
        sql.append(
            " UNION ALL SELECT '賣出' AS action, '保險' AS target, excute_price*IFNULL(fx_rate,1)*-1 AS spending ")
        sql.append(
            " FROM Insurance_Journal AS Insurance LEFT JOIN Insurance AS Insurance_Main ON Insurance_Main.insurance_id = Insurance.insurance_id ")
        sql.append(
            " LEFT JOIN (SELECT id, fx_code FROM Account) Account ON Account.id=Insurance_Main.out_account_id ")
        sql.append(
            " LEFT JOIN (SELECT code, buy_rate AS fx_rate, MAX(import_date) FROM FX_Rate ")
        sql.append(
            f" WHERE STRFTIME('%Y%m', import_date) = '{vestingMonth}' GROUP BY code) Rate ON Rate.code = Account.fx_code ")
        sql.append(
            f"WHERE STRFTIME('%Y%m', excute_date) = '{vestingMonth}' AND insurance_excute_type='return' ")
        # 賣出不動產
        sql.append(
            " UNION ALL SELECT '賣出' AS action, '不動產' AS target, excute_price*-1 AS spending FROM Estate_Journal AS Estate ")
        sql.append(
            f"WHERE STRFTIME('%Y%m', excute_date) = '{vestingMonth}' AND estate_excute_type='sold' ")
        # 買入外幣
        sql.append(
            " UNION ALL SELECT '買入' AS action, '換匯' AS target, ABS(CASE WHEN spend_way_type='finance' THEN spending*note ELSE spending END) AS spending FROM Journal ")
        sql.append(
            f"WHERE vesting_month = '{vestingMonth}' AND ((spend_way_type='finance' AND action_sub_type='normal' AND spending > 0 ) ")
        sql.append(
            "OR (spend_way_type='normal' AND action_sub_type='finance' AND spending < 0 )) ")
        # 買入股票
        sql.append(
            " UNION ALL SELECT '買入' AS action, '股票' AS target, ABS(excute_price*IFNULL(fx_rate,1)) AS spending ")
        sql.append(
            " FROM Stock_Detail AS Stock LEFT JOIN (SELECT id, fx_code FROM Account) Account ON Account.id=Stock.account_id ")
        sql.append(
            " LEFT JOIN (SELECT code, buy_rate AS fx_rate, MAX(import_date) FROM FX_Rate ")
        sql.append(
            f" WHERE STRFTIME('%Y%m', import_date) = '{vestingMonth}' GROUP BY code) Rate ON Rate.code = Account.fx_code ")
        sql.append(
            f"WHERE STRFTIME('%Y%m', excute_date) = '{vestingMonth}' AND excute_type='buy' ")
        # 買入保險
        sql.append(
            " UNION ALL SELECT '買入' AS action, '保險' AS target, ABS(excute_price*IFNULL(fx_rate,1)) AS spending FROM Insurance_Journal AS Insurance ")
        sql.append(
            " LEFT JOIN Insurance AS Insurance_Main ON Insurance_Main.insurance_id = Insurance.insurance_id ")
        sql.append(
            " LEFT JOIN (SELECT id, fx_code FROM Account) Account ON Account.id=Insurance_Main.in_account_id ")
        sql.append(
            " LEFT JOIN (SELECT code, buy_rate AS fx_rate, MAX(import_date) FROM FX_Rate ")
        sql.append(
            f" WHERE STRFTIME('%Y%m', import_date) = '{vestingMonth}' GROUP BY code) Rate ON Rate.code = Account.fx_code ")
        sql.append(
            f"WHERE STRFTIME('%Y%m', excute_date) = '{vestingMonth}' AND insurance_excute_type='pay' ")
        # 買入不動產
        sql.append(
            " UNION ALL SELECT '買入' AS action, '不動產' AS target, excute_price AS spending FROM Estate_Journal AS Estate ")
        sql.append(
            f"WHERE STRFTIME('%Y%m', excute_date) = '{vestingMonth}' AND estate_excute_type='downPayment' ")
        sql.append(
            " UNION ALL SELECT '買入' AS action, '不動產' AS target, excute_price AS spending FROM Estate ")
        sql.append(
            " LEFT JOIN Loan_Journal AS Loan ON Loan.loan_id = Estate.loan_id ")
        sql.append(
            f"WHERE STRFTIME('%Y%m', excute_date) = '{vestingMonth}' AND loan_excute_type='principal' ")
        sql.append(f" ORDER BY target ASC, action ASC ")

        return db.engine.execute(''.join(sql))

    def queryForSpendingReport(self, start, end, format):
        sql = []
        sql.append(
            f"SELECT STRFTIME('{format}', spend_date) AS dateString, spend_way_type, action_main_type, spending*IFNULL(fx_rate,1) AS spending, name FROM Journal ")
        sql.append(" LEFT JOIN Code_Data ON code_id=action_main ")
        sql.append(
            " LEFT JOIN (SELECT id, fx_code FROM Account) Account ON Account.id=Journal.spend_way AND spend_way_table='Account' ")
        sql.append(
            " LEFT JOIN (SELECT code, buy_rate AS fx_rate, MAX(import_date) FROM FX_Rate ")
        sql.append(
            f" WHERE STRFTIME('{format}', import_date) >= '{start}' AND STRFTIME('{format}', import_date) <= '{end}' GROUP BY code) Rate ON Rate.code = Account.fx_code ")
        sql.append(
            f" WHERE action_main_table='Code' AND STRFTIME('{format}', spend_date) >= '{start}' AND STRFTIME('{format}', spend_date) <= '{end}' ")
        sql.append(" ORDER BY dateString, action_main_type ASC ")

        return db.engine.execute(''.join(sql))

    def getGiftedList(self, year):
        sql = []
        sql.append(
            "SELECT Account_From.owner, SUM(spending*IFNULL(buy_rate,1)) AS amount FROM Journal ")
        sql.append(
            "LEFT JOIN Account AS Account_From ON Account_From.id=spend_way ")
        sql.append(
            "LEFT JOIN Account AS Account_To ON Account_To.id=action_sub ")
        sql.append(
            "LEFT JOIN FX_Rate ON Account_From.fx_code=code AND spend_date=import_date ")
        sql.append(
            "WHERE spend_way_table='Account' AND action_sub_table='Account' AND action_main='Transfer' AND Account_From.owner IS NOT NULL ")
        sql.append(
            f"AND STRFTIME('%Y', spend_date)='{year}' AND Account_From.owner != Account_To.owner ")
        sql.append(
            "GROUP BY Account_From.owner ")

        return db.engine.execute(''.join(sql))

    def add(self, journal):
        db.session.add(journal)
        db.session.flush()

        if DaoBase.session_commit(self) == '':
            return journal
        else:
            return False

    def bulkInsert(self, datas):
        sql = 'INSERT INTO Journal(vesting_month, spend_date, spend_way, spend_way_type, spend_way_table, action_main, action_main_type, action_main_table, action_sub, action_sub_type, action_sub_table, spending, invoice_number, note) VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14)'

        params = []
        try:
            for item in datas:
                params.append((item.vesting_month,
                               item.spend_date, item.spend_way, item.spend_way_type, item.spend_way_table,
                               item.action_main, item.action_main_type, item.action_main_table,
                               item.action_sub, item.action_sub_type, item.action_sub_table, item.spending,
                               item.invoice_number, item.note))

            db.engine.execute(sql, params)
            return True
        except Exception as error:
            return False

    def update(self):
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def delete(self, distinct_number):
        self.query.filter_by(distinct_number=distinct_number).delete()
        if DaoBase.session_commit(self) == '':
            return True
        else:
            return False

    def output(self, Journal):
        return {
            'distinct_number': Journal.distinct_number,
            'vesting_month': Journal.vesting_month,
            'spend_date': Journal.spend_date,
            'spend_way': Journal.spend_way,
            'spend_way_type': Journal.spend_way_type,
            'spend_way_table': Journal.spend_way_table,
            'action_main': Journal.action_main,
            'action_main_type': Journal.action_main_type,
            'action_main_table': Journal.action_main_table,
            'action_sub': Journal.action_sub,
            'action_sub_type': Journal.action_sub_type,
            'action_sub_table': Journal.action_sub_table,
            'spending': Journal.spending,
            'note': Journal.note,
            'isEditMode': False
            # 'actionSubSelectionGroup': None  # 前端顯示所需，需先將欄位寫入
        }

    def outputForReport(self, data):
        return {
            'dateString': data.dateString,
            'type': data.action_main_type,
            'name': data.name,
            'amount': round(data.spending, 2) if data.spend_way_type == 'finance' else data.spending
        }

    def outputForGifted(self, data):
        return {
            'owner': data.owner,
            'rate': abs(round(data.amount*100/2200000, 2)),
            'amount': abs(data.amount)
        }
