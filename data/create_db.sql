-- 帳戶設定檔
CREATE TABLE IF NOT EXISTS Account (
	id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	account_id NVARCHAR(20),
	name NVARCHAR(60) NOT NULL,
	account_type VARCHAR(10) NOT NULL,
	fx_code CHARACTER(3) NOT NULL, -- 對應 FX_Rate.code
    is_calculate CHARACTER(1) NOT NULL,
	in_use CHARACTER(1) NOT NULL,
	discount DECIMAL(4,3), -- 最多總共四位，小數點三位
	memo NVARCHAR(300), -- 活存利率等
	owner NVARCHAR(60),
	carrier_no NVARCHAR(60),
	account_index TINYINT
);

-- 餘額檔，關帳後寫入
CREATE TABLE IF NOT EXISTS Account_Balance (
	vesting_month CHARACTER(6) NOT NULL,
	id NVARCHAR(20),
	name NVARCHAR(60) NOT NULL,
	-- vesting_table VARCHAR(15) NOT NULL,
    balance DECIMAL(9,2) NOT NULL,
	fx_code CHARACTER(3) NOT NULL,
	fx_rate DECIMAL(5,2) NOT NULL,
	is_calculate CHARACTER(1) NOT NULL,
	PRIMARY KEY (vesting_month, id)
);

-- 定期支出提醒設定檔
CREATE TABLE IF NOT EXISTS Alarm (
    alarm_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	alarm_type VARCHAR(10) NOT NULL,
	alarm_date VARCHAR(5) NOT NULL,
    content NVARCHAR(60) NOT NULL,
	due_date DATE
);

-- 預算設定檔
CREATE TABLE IF NOT EXISTS Budget (
	budget_year CHARACTER(4), 
	category_code VARCHAR(10), --對應 Code_Data.code_id
	category_name NVARCHAR(60) NOT NULL, -- 對應 Code_Data.name
	code_type VARCHAR(10) NOT NULL, -- 對應 Code_Data.code_type
    expected01 DECIMAL(9,2) NOT NULL,
	expected02 DECIMAL(9,2) NOT NULL,
	expected03 DECIMAL(9,2) NOT NULL,
	expected04 DECIMAL(9,2) NOT NULL,
	expected05 DECIMAL(9,2) NOT NULL,
	expected06 DECIMAL(9,2) NOT NULL,
	expected07 DECIMAL(9,2) NOT NULL,
	expected08 DECIMAL(9,2) NOT NULL,
	expected09 DECIMAL(9,2) NOT NULL,
	expected10 DECIMAL(9,2) NOT NULL,
	expected11 DECIMAL(9,2) NOT NULL,
	expected12 DECIMAL(9,2) NOT NULL,
	PRIMARY KEY (budget_year, category_code)
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
	card_no NVARCHAR(19) NOT NULL,
	last_day CHARACTER(2) NOT NULL,
    charge_day CHARACTER(2) NOT NULL,
	limit_date NVARCHAR(7) NOT NULL,
    feedback_way NVARCHAR(5) NOT NULL, --Cash：現金/ Point：紅利/ None：無
	fx_code CHARACTER(3) NOT NULL, -- 對應 FX_Rate.code
	in_use CHARACTER(1) NOT NULL,
	credit_card_index TINYINT,
	carrier_no NVARCHAR(60),
    note TEXT -- 記錄額度，優惠到期日，回饋上限金額之類的
);

-- 可計算當月解約金的保險每月價值檔，關帳後寫入
CREATE TABLE IF NOT EXISTS Credit_Card_Balance (
	vesting_month CHARACTER(6) NOT NULL,
	id INTEGER,
	name NVARCHAR(60) NOT NULL,
	-- vesting_table VARCHAR(15) NOT NULL,
    balance DECIMAL(9,2) NOT NULL,
	fx_rate DECIMAL(5,2) NOT NULL,
	PRIMARY KEY (vesting_month, id)
);

-- 不動產主檔
CREATE TABLE IF NOT EXISTS Estate (
	estate_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	estate_name NVARCHAR(60) NOT NULL,
	estate_type VARCHAR(10) NOT NULL, -- house:獨棟透天 / townhouse:連棟透天 / condo:公寓 / apartment:電梯大樓 / highrise:商辦 / land:土地
	estate_address NVARCHAR(300) NOT NULL,
	asset_id INTEGER NOT NULL,
	obtain_date DATE NOT NULL,
	-- down_payment DECIMAL(9,2) NOT NULL, -- 初始本金/頭期款
	loan_id INTEGER, -- 對應 Loan.loan_id
	-- loan_amount DECIMAL(9,2) NOT NULL,
	-- pay_day CHAR(5), -- mm/dd
	-- expected_end_date DATE,
	estate_status VARCHAR(10) NOT NULL, -- idle:閒置 / live:居住 / rent:出租 / sold:賣出
	memo NVARCHAR(300) -- 寫坪數/建造日/總樓高/有什麼車位/格局/有無管理
);
CREATE INDEX IF NOT EXISTS Estate_idx ON Estate (estate_id, asset_id);

-- 不動產流水帳檔
CREATE TABLE IF NOT EXISTS Estate_Journal (
	distinct_number INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	estate_id INTEGER NOT NULL,
	-- estate_excute_name NVARCHAR(60) NOT NULL,
	estate_excute_type VARCHAR(20) NOT NULL, -- tax:稅費 / fee:雜費 / insurance:保險 / fix:修繕 / rent:租金 / deposit:押金
	excute_price DECIMAL(9,2) NOT NULL,
	excute_date DATE NOT NULL,
	memo NVARCHAR(300)
);
CREATE INDEX IF NOT EXISTS Estate_Journal_idx ON Estate_Journal (estate_id, excute_date);
CREATE INDEX IF NOT EXISTS Estate_Income_idx ON Estate_Journal (estate_id, estate_excute_type);

-- 可計算當月解約金的保險每月價值檔，關帳後寫入
CREATE TABLE IF NOT EXISTS Estate_Net_Value_History (
	vesting_month CHARACTER(6) NOT NULL,
	id INTEGER, -- Estate.estate_id
	name NVARCHAR(60) NOT NULL,
	asset_id INTEGER NOT NULL, -- Estate.asset_id
	market_value DECIMAL(9,2) NOT NULL, -- 從估價網站輸入對等條件取值填入
	cost DECIMAL(9,2) NOT NULL, -- 會算入所有支出收入，為計算當下報酬率
	estate_status VARCHAR(10) NOT NULL,
	PRIMARY KEY (vesting_month, id, asset_id)
);

-- 歷史匯率檔，當天有撈才會寫入
CREATE TABLE IF NOT EXISTS FX_Rate (
	import_date DATETIME,
	code CHARACTER(3),
	buy_rate DECIMAL(5,2) NOT NULL,
	PRIMARY KEY (import_date, code)
);

-- 初始金額設定檔
-- CREATE TABLE IF NOT EXISTS Initial_Setting (
-- 	id INTEGER, -- 對應 Code_Data.code_id 或 Account.account_id 或 Credit_Card.credit_card_id
-- 	code_table VARCHAR(15) NOT NULL, -- id 對應的 table
--     code_name NVARCHAR(60) NOT NULL, -- 對應 Code_Data.name
-- 	initial_type VARCHAR(10) NOT NULL, -- id 對應的 table
-- 	setting_value VARCHAR(10) NOT NULL,
-- 	setting_date DATE NOT NULL,
-- 	PRIMARY KEY (code_id, initial_type)
-- );

-- 保險流水帳檔
CREATE TABLE IF NOT EXISTS Insurance (
	insurance_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	insurance_name NVARCHAR(60) NOT NULL,
	-- insurance_type VARCHAR(10) NOT NULL, -- save:儲蓄險/ live:壽險/ invest:投資型，直接用頁籤分類，所以先不用
	asset_id INTEGER NOT NULL,
	in_account_id INTEGER NOT NULL,
    in_account_name NVARCHAR(60) NOT NULL,
	out_account_id INTEGER NOT NULL,
    out_account_name NVARCHAR(60) NOT NULL,
	start_date DATE NOT NULL,
	expected_end_date DATE NOT NULL,
	pay_type VARCHAR(10) NOT NULL, -- 繳別，month:月/ season:季/ year:年/ once:躉繳
    pay_day VARCHAR(23), -- 依繳別，month:dd/ season:mm/dd,mm/dd.../ year:mm/dd
	expected_spend INTEGER NOT NULL,
	has_closed CHARACTER(1) NOT NULL
);

-- 保險明細檔
CREATE TABLE IF NOT EXISTS Insurance_Journal (
	distinct_number INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	insurance_id INTEGER NOT NULL,
	insurance_excute_type VARCHAR(20) NOT NULL, -- pay:扣款/ cash:配息/ return:贖回/ expect:預期價值
	excute_price DECIMAL(7,3) NOT NULL,
	excute_date DATE NOT NULL,
	memo NVARCHAR(300)
);
CREATE INDEX IF NOT EXISTS Insurance_Journal_idx ON Insurance_Journal (insurance_id, excute_date);
CREATE INDEX IF NOT EXISTS Insurance_Income_idx ON Insurance_Journal (insurance_id, insurance_excute_type);

-- 可計算當月解約金的保險每月價值檔，關帳後寫入
CREATE TABLE IF NOT EXISTS Insurance_Net_Value_History (
	vesting_month CHARACTER(6) NOT NULL,
	id INTEGER, -- Insurance.insurance_id
	name NVARCHAR(60) NOT NULL,
	asset_id INTEGER NOT NULL, -- Insurance.asset_id
	surrender_value DECIMAL(9,2) NOT NULL, -- 當年度解約金或預期價值，一個月只能有一筆
	cost DECIMAL(9,2) NOT NULL, -- 會算入配息與所有支出，為計算當下報酬率
	fx_code CHARACTER(3) NOT NULL,
	fx_rate DECIMAL(5,2) NOT NULL,
	PRIMARY KEY (vesting_month, id, asset_id)
);

-- 流水帳檔
CREATE TABLE IF NOT EXISTS Journal (
	distinct_number INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	vesting_month CHARACTER(6) NOT NULL,
	spend_date DATE NOT NULL,
	spend_way VARCHAR(10) NOT NULL, -- account_id / credit_card_id
	spend_way_type VARCHAR(20) NOT NULL,
	spend_way_table VARCHAR(15) NOT NULL, -- id 對應的 table
	-- spend_way_name NVARCHAR(60) NOT NULL,
	action_main VARCHAR(10) NOT NULL,
	action_main_type VARCHAR(20) NOT NULL,
	action_main_table VARCHAR(15) NOT NULL,
	-- action_main_name NVARCHAR(60) NOT NULL,
    action_sub VARCHAR(10) NOT NULL,
	action_sub_type VARCHAR(20) NOT NULL,
	action_sub_table VARCHAR(15) NOT NULL, -- id 對應的 table
	-- action_sub_name NVARCHAR(60) NOT NULL,
    spending DECIMAL(9,2) NOT NULL, -- 收入為正，支出為負
	invoice_number CHAR(10), -- 有填發票號碼為匯入資料，用來判斷是否要寫入新的匯入資料
    note TEXT
);
CREATE INDEX IF NOT EXISTS Journal_spend_date_idx ON Journal (spend_date);

-- 貸款主檔
CREATE TABLE IF NOT EXISTS Loan (
	loan_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	loan_name NVARCHAR(60) NOT NULL,
	loan_type VARCHAR(10) NOT NULL, -- unsecured:信貸 / mortgage:房貸 / financial:理財型房貸 / secured:擔保貸款
	account_id INTEGER NOT NULL, -- 對應 Account.account_id
    account_name NVARCHAR(60) NOT NULL, -- 對應 Account.name
	interest_rate DECIMAL(4,3) NOT NULL,
	period INTEGER NOT NULL,
	apply_date DATE NOT NULL,
	grace_expire_date DATE,
	pay_day VARCHAR(2) NOT NULL,
	amount DECIMAL(9,2) NOT NULL,
	repayed CHARACTER(1) NOT NULL,
	loan_index TINYINT
);

-- 貸款流水帳檔
CREATE TABLE IF NOT EXISTS Loan_Journal (
	distinct_number INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	loan_id INTEGER NOT NULL,
	loan_excute_type VARCHAR(20) NOT NULL, -- principal:償還本金 / interest:支付利息 / increment:增貸 / fee:雜費
	excute_price DECIMAL(9,2) NOT NULL,
	excute_date DATE NOT NULL,
	memo NVARCHAR(300)
);
CREATE INDEX IF NOT EXISTS Loan_Journal_idx ON Loan_Journal (loan_id, excute_date);
CREATE INDEX IF NOT EXISTS Loan_Income_idx ON Loan_Journal (loan_id, Loan_excute_type);

-- 貸款餘額檔，關帳後寫入
CREATE TABLE IF NOT EXISTS Loan_Balance (
	vesting_month CHARACTER(6) NOT NULL,
	id INTEGER,
	name NVARCHAR(60) NOT NULL,
    balance DECIMAL(9,2) NOT NULL,
	cost DECIMAL(9,2) NOT NULL, -- 會算入繳息與所有支出，為計算當下總成本
	PRIMARY KEY (vesting_month, id)
);

-- 其他資產設定檔
CREATE TABLE IF NOT EXISTS Other_Asset (
    asset_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	asset_name NVARCHAR(60) NOT NULL,
	asset_type VARCHAR(10) NOT NULL,
	in_use CHARACTER(1) NOT NULL,
	asset_index TINYINT
);

-- 歷史每月淨值檔，關帳後寫入
-- CREATE TABLE IF NOT EXISTS Other_Asset_Net_Value_History (
-- 	vesting_month CHARACTER(6) NOT NULL,
-- 	id INTEGER,
-- 	name NVARCHAR(60) NOT NULL,
-- 	asset_type VARCHAR(10) NOT NULL,
--     -- net_value DECIMAL(9,2) NOT NULL, 由各資產歷史淨值檔計算
-- 	PRIMARY KEY (vesting_month, id, asset_type)
-- );

-- 股票流水帳檔
CREATE TABLE IF NOT EXISTS Stock_Journal (
	stock_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	stock_code VARCHAR(10) NOT NULL,
	stock_name NVARCHAR(60) NOT NULL,
	asset_id INTEGER NOT NULL,
	expected_spend INTEGER
);

-- 股票明細檔
CREATE TABLE IF NOT EXISTS Stock_Detail (
	distinct_number INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	stock_id INTEGER NOT NULL,
	excute_type VARCHAR(20) NOT NULL, -- buy:買入/ sell:賣出/ stock:配股/ cash:配息
	excute_amount INT, --以股為單位
	excute_price DECIMAL(9,3),
	excute_date DATE NOT NULL,
	account_id INTEGER NOT NULL,
    account_name NVARCHAR(60) NOT NULL,
	memo NVARCHAR(300)
);
CREATE INDEX IF NOT EXISTS Stock_Detail_idx ON Stock_Detail (stock_id, excute_date);

-- 股票每月淨值檔，關帳後寫入
CREATE TABLE IF NOT EXISTS Stock_Net_Value_History (
	vesting_month CHARACTER(6) NOT NULL,
	id INTEGER, -- Stock_Journal.stock_id
	stock_code VARCHAR(10) NOT NULL,
	stock_name NVARCHAR(60) NOT NULL,
	asset_id INTEGER NOT NULL,
	amount INT NOT NULL,
	price DECIMAL(7,3) NOT NULL,
	cost DECIMAL(9,2) NOT NULL, -- 會算入配息，為計算當下報酬率
	fx_code CHARACTER(3) NOT NULL,
	fx_rate DECIMAL(5,2) NOT NULL,
	PRIMARY KEY (vesting_month, id, asset_id)
);

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

-- 年度目標設定檔
CREATE TABLE IF NOT EXISTS Target_Setting (
	distinct_number INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	target_year CHARACTER(4) NOT NULL,
	setting_value NVARCHAR(45) NOT NULL, -- 描述該年度目標
	is_done CHARACTER(1) NOT NULL
);
