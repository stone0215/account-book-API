-- 初始金額設定檔
CREATE TABLE IF NOT EXISTS Initial_Setting (
	code_id INTEGER, -- 對應 Code_Data.code_id 或 Account.account_id 或 Credit_Card.credit_card_id
    code_name NVARCHAR(60) NOT NULL, -- 對應 Code_Data.name
	initial_type VARCHAR(10) NOT NULL, -- 對應 Code_Data.code_type
	setting_value VARCHAR(10) NOT NULL,
	setting_date DATE NOT NULL,
	PRIMARY KEY (code_id, initial_type)
);

-- 年度目標設定檔
CREATE TABLE IF NOT EXISTS Target_Setting (
	target_year SMALLINT PRIMARY KEY,
    name NVARCHAR(60) NOT NULL,
	setting_value NVARCHAR(45) NOT NULL -- 描述該年度目標
);

-- 帳戶設定檔
CREATE TABLE IF NOT EXISTS Account (
	account_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	name NVARCHAR(60) NOT NULL,
	account_type VARCHAR(10) NOT NULL,
	fx_code CHARACTER(3) NOT NULL, -- 對應 FX_Rate.code
    is_calculate CHARACTER(1) NOT NULL,
	in_use CHARACTER(1) NOT NULL,
	discount DECIMAL(4,3), -- 最多總共四位，小數點三位
	account_index TINYINT
);

-- 帳戶餘額檔，關帳後寫入
CREATE TABLE IF NOT EXISTS Account_Balance (
	account_id INTEGER, -- 對應 Account.account_id
	balance_month CHARACTER(6),
	name NVARCHAR(60) NOT NULL,
    balance DECIMAL(8,2) NOT NULL,
    buy_rate DECIMAL(5,2),
	PRIMARY KEY (account_id, balance_month)
);

-- 歷史匯率檔，當天有撈才會寫入
CREATE TABLE IF NOT EXISTS FX_Rate (
	import_date DATETIME,
	code CHARACTER(3),
	buy_rate DECIMAL(5,2) NOT NULL,
    sell_rate DECIMAL(5,2) NOT NULL,
	PRIMARY KEY (import_date, code)
);

-- 代碼檔
CREATE TABLE IF NOT EXISTS Code_Data (
	code_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	code_type VARCHAR(10) NOT NULL, --S：固定支出/ F：浮動支出/ I：收入/ A：資產
	name NVARCHAR(60) NOT NULL,
	code_group INTEGER, --如果是副選單，會寫入Code_Data.code_id
	code_group_name NVARCHAR(60), --如果是副選單，會寫入Code_Data.name
	in_use CHARACTER(1) NOT NULL,
    code_index TINYINT
);

-- 信用卡設定檔
CREATE TABLE IF NOT EXISTS Credit_Card (
	credit_card_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	card_name NVARCHAR(60) NOT NULL,
	last_day CHARACTER(2) NOT NULL,
    charge_day CHARACTER(2) NOT NULL,
	limit_date DATE NOT NULL,
    feedback_way CHARACTER(1) NOT NULL, --C：現金/ P：紅利/ N：無
	fx_code CHARACTER(3) NOT NULL, -- 對應 FX_Rate.code
	in_use CHARACTER(1) NOT NULL,
	credit_card_index TINYINT,
    note TEXT
);

-- 信用卡餘額檔，關帳後寫入
CREATE TABLE IF NOT EXISTS Credit_Card_Balance (
	credit_card_id INTEGER, -- 對應 Credit_Card.credit_card_id
	balance_month CHARACTER(6),
	name NVARCHAR(60) NOT NULL, -- 對應 Credit_Card.name
    balance DECIMAL(8,2) NOT NULL,
	PRIMARY KEY (credit_card_id, balance_month)
);

-- 貸款設定檔
CREATE TABLE IF NOT EXISTS Loan (
	loan_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	loan_name NVARCHAR(60) NOT NULL,
	account_id INTEGER NOT NULL, -- 對應 Account.account_id
    account_name NVARCHAR(60) NOT NULL, -- 對應 Account.name
	interest_rate DECIMAL(4,3) NOT NULL,
	apply_date DATE NOT NULL,
    pay_day VARCHAR(2) NOT NULL,
	loan_index TINYINT
);

-- 貸款餘額檔，關帳後寫入
CREATE TABLE IF NOT EXISTS Loan_Balance (
	loan_id INTEGER, -- 對應 Loan.loan_id
	balance_month CHARACTER(6),
	name NVARCHAR(60) NOT NULL, -- 對應 Loan.name
    balance DECIMAL(8,2) NOT NULL,
	PRIMARY KEY (loan_id, balance_month)
);

-- 流水帳檔
CREATE TABLE IF NOT EXISTS Journal (
	spend_date DATE NOT NULL,
	spend_way VARCHAR(10) NOT NULL,
	action_main VARCHAR(10) NOT NULL,
    action_sub VARCHAR(10) NOT NULL,
    spending DECIMAL(8,2) NOT NULL,
    note TEXT
);
CREATE INDEX IF NOT EXISTS Journal_spend_date_idx ON Journal (spend_date);

-- 股票流水帳檔
CREATE TABLE IF NOT EXISTS Stock_Journal (
	stock_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	stock_code VARCHAR(10) NOT NULL,
	stock_name NVARCHAR(60) NOT NULL,
	asset_id INTEGER NOT NULL
);

-- 股票明細檔
CREATE TABLE IF NOT EXISTS Stock_Detail (
	distinct_number INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	stock_id INTEGER,
	excute_type VARCHAR(10) NOT NULL, -- buy:買入/ sell:賣出/ stock:配股/ cash:配息
	excute_amount INT, --以股為單位
	excute_price DECIMAL(7,3),
	excute_date DATE NOT NULL
);
CREATE INDEX IF NOT EXISTS Stock_Detail_idx ON Stock_Detail (stock_id, excute_date);

-- 股票歷史價格檔
CREATE TABLE IF NOT EXISTS Stock_Price_History (
	stock_code VARCHAR(10) NOT NULL,
	fetch_date DATE NOT NULL,
	open_price DECIMAL(7,3),
	highest_price DECIMAL(7,3),
	lowest_price DECIMAL(7,3),
	close_price DECIMAL(7,3) NOT NULL
);
CREATE INDEX IF NOT EXISTS Stock_Price_History_idx ON Stock_Price_History (stock_code, fetch_date);

-- 保險流水帳檔
CREATE TABLE IF NOT EXISTS Insurance (
	insurance_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	insurance_name NVARCHAR(60) NOT NULL,
	insurance_type VARCHAR(10) NOT NULL,
	create_date DATE NOT NULL,
	pay_type VARCHAR(10) NOT NULL,
    pay_day VARCHAR(23) NOT NULL,
	expected_pay INTEGER NOT NULL,
	insurance_index TINYINT
);

-- 保險餘額檔，關帳後如有異動才寫入，因為不一定是月繳
CREATE TABLE IF NOT EXISTS Insurance_Balance (
	insurance_id INTEGER, -- 對應 Insurance.insurance_id
	balance_month CHARACTER(6),
	name NVARCHAR(60) NOT NULL, -- 對應 Insurance.name
    balance DECIMAL(8,2) NOT NULL,
	PRIMARY KEY (insurance_id, balance_month)
);

-- 保險歷史價值檔，每年更新解約金額
CREATE TABLE IF NOT EXISTS Insurance_History (
	insurance_id INTEGER, -- 對應 Insurance.insurance_id
	year CHARACTER(4),
	value DECIMAL(10,3)  NOT NULL,
    balance DECIMAL(10,3) NOT NULL,
    fx_code CHARACTER(3) NOT NULL, -- 對應 Insurance.code
	PRIMARY KEY (insurance_id, year)
);

-- 預算設定檔
CREATE TABLE IF NOT EXISTS Budget (
	budget_year CHARACTER(4), 
	category_code VARCHAR(10), --對應 Code_Data.code_id
	category_name NVARCHAR(60) NOT NULL, -- 對應 Code_Data.name
	code_type VARCHAR(10) NOT NULL, -- 對應 Code_Data.code_type
    expected1 DECIMAL(8,2) NOT NULL,
	expected2 DECIMAL(8,2) NOT NULL,
	expected3 DECIMAL(8,2) NOT NULL,
	expected4 DECIMAL(8,2) NOT NULL,
	expected5 DECIMAL(8,2) NOT NULL,
	expected6 DECIMAL(8,2) NOT NULL,
	expected7 DECIMAL(8,2) NOT NULL,
	expected8 DECIMAL(8,2) NOT NULL,
	expected9 DECIMAL(8,2) NOT NULL,
	expected10 DECIMAL(8,2) NOT NULL,
	expected11 DECIMAL(8,2) NOT NULL,
	expected12 DECIMAL(8,2) NOT NULL,
	PRIMARY KEY (budget_year, category_code)
);

-- 定期支出提醒設定檔
CREATE TABLE IF NOT EXISTS Alarm (
    alarm_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	alarm_type VARCHAR(10) NOT NULL,
	alarm_date VARCHAR(5) NOT NULL,
    content NVARCHAR(60) NOT NULL
);

-- 其他資產設定檔
CREATE TABLE IF NOT EXISTS Other_Asset (
    asset_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	asset_name NVARCHAR(60) NOT NULL,
	asset_type VARCHAR(10) NOT NULL,
	account_id INTEGER NOT NULL,
    account_name NVARCHAR(60) NOT NULL,
	expected_spend INTEGER,
	in_use CHARACTER(1) NOT NULL,
	asset_index TINYINT
);