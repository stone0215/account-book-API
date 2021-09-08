-- 選單
INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Floating', '主食', NULL, NULL, 'Y', NULL UNION ALL
SELECT 'Floating', '副食', NULL, NULL, 'Y', NULL UNION ALL
SELECT 'Floating', '日用品', NULL, NULL, 'Y', NULL UNION ALL
SELECT 'Floating', '行車交通', NULL, NULL, 'Y', NULL UNION ALL
SELECT 'Floating', '學習', NULL, NULL, 'Y', NULL UNION ALL
SELECT 'Floating', '醫療費', NULL, NULL, 'Y', NULL UNION ALL
SELECT 'Floating', '毛小孩', NULL, NULL, 'Y', NULL UNION ALL
SELECT 'Floating', '尊親費用', NULL, NULL, 'Y', NULL UNION ALL
SELECT 'Floating', '休閒娛樂', NULL, NULL, 'Y', NULL UNION ALL
SELECT 'Floating', '人情往來', NULL, NULL, 'Y', NULL UNION ALL
SELECT 'Floating', '捐款', NULL, NULL, 'Y', NULL UNION ALL
SELECT 'Floating', '其他', NULL, NULL, 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_type='Floating' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Floating','食材', ( SELECT code_id FROM Code_Data WHERE name='主食' ), '主食', 'Y', NULL UNION ALL
SELECT 'Floating','水果', ( SELECT code_id FROM Code_Data WHERE name='主食' ), '主食', 'Y', NULL UNION ALL
SELECT 'Floating','早餐', ( SELECT code_id FROM Code_Data WHERE name='主食' ), '主食', 'Y', NULL UNION ALL
SELECT 'Floating','午餐', ( SELECT code_id FROM Code_Data WHERE name='主食' ), '主食', 'Y', NULL UNION ALL
SELECT 'Floating','晚餐', ( SELECT code_id FROM Code_Data WHERE name='主食' ), '主食', 'Y', NULL UNION ALL
SELECT 'Floating','調味料', ( SELECT code_id FROM Code_Data WHERE name='主食' ), '主食', 'Y', NULL UNION ALL
SELECT 'Floating','宵夜', ( SELECT code_id FROM Code_Data WHERE name='主食' ), '主食', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='主食' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Floating','食材', ( SELECT code_id FROM Code_Data WHERE name='副食' ), '副食', 'Y', NULL UNION ALL
SELECT 'Floating','宵夜', ( SELECT code_id FROM Code_Data WHERE name='副食' ), '副食', 'Y', NULL UNION ALL
SELECT 'Floating','飲料', ( SELECT code_id FROM Code_Data WHERE name='副食' ), '副食', 'Y', NULL UNION ALL
SELECT 'Floating','酒水', ( SELECT code_id FROM Code_Data WHERE name='副食' ), '副食', 'Y', NULL UNION ALL
SELECT 'Floating','零食', ( SELECT code_id FROM Code_Data WHERE name='副食' ), '副食', 'Y', NULL UNION ALL
SELECT 'Floating','甜點', ( SELECT code_id FROM Code_Data WHERE name='副食' ), '副食', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='副食' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Floating','衛生用品', ( SELECT code_id FROM Code_Data WHERE name='日用品' ), '日用品', 'Y', NULL UNION ALL
SELECT 'Floating','3C', ( SELECT code_id FROM Code_Data WHERE name='日用品' ), '日用品', 'Y', NULL UNION ALL
SELECT 'Floating','清潔用品', ( SELECT code_id FROM Code_Data WHERE name='日用品' ), '日用品', 'Y', NULL UNION ALL
SELECT 'Floating','衣裝', ( SELECT code_id FROM Code_Data WHERE name='日用品' ), '日用品', 'Y', NULL UNION ALL
SELECT 'Floating','餐具', ( SELECT code_id FROM Code_Data WHERE name='日用品' ), '日用品', 'Y', NULL UNION ALL
SELECT 'Floating','其他', ( SELECT code_id FROM Code_Data WHERE name='日用品' ), '日用品', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='日用品' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Floating','加油', ( SELECT code_id FROM Code_Data WHERE name='行車交通' ), '行車交通', 'Y', NULL UNION ALL
SELECT 'Floating','停車費', ( SELECT code_id FROM Code_Data WHERE name='行車交通' ), '行車交通', 'Y', NULL UNION ALL
SELECT 'Floating','修理費', ( SELECT code_id FROM Code_Data WHERE name='行車交通' ), '行車交通', 'Y', NULL UNION ALL
SELECT 'Floating','公車', ( SELECT code_id FROM Code_Data WHERE name='行車交通' ), '行車交通', 'Y', NULL UNION ALL
SELECT 'Floating','捷運', ( SELECT code_id FROM Code_Data WHERE name='行車交通' ), '行車交通', 'Y', NULL UNION ALL
SELECT 'Floating','計程車', ( SELECT code_id FROM Code_Data WHERE name='行車交通' ), '行車交通', 'Y', NULL UNION ALL
SELECT 'Floating','鐵路', ( SELECT code_id FROM Code_Data WHERE name='行車交通' ), '行車交通', 'Y', NULL UNION ALL
SELECT 'Floating','客運', ( SELECT code_id FROM Code_Data WHERE name='行車交通' ), '行車交通', 'Y', NULL UNION ALL
SELECT 'Floating','收費站', ( SELECT code_id FROM Code_Data WHERE name='行車交通' ), '行車交通', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='行車交通' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Floating','讀書會', ( SELECT code_id FROM Code_Data WHERE name='學習' ), '學習', 'Y', NULL UNION ALL
SELECT 'Floating','上課', ( SELECT code_id FROM Code_Data WHERE name='學習' ), '學習', 'Y', NULL UNION ALL
SELECT 'Floating','書', ( SELECT code_id FROM Code_Data WHERE name='學習' ), '學習', 'Y', NULL UNION ALL
SELECT 'Floating','其他', ( SELECT code_id FROM Code_Data WHERE name='學習' ), '學習', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='學習' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Floating','西醫', ( SELECT code_id FROM Code_Data WHERE name='醫療費' ), '醫療費', 'Y', NULL UNION ALL
SELECT 'Floating','中醫', ( SELECT code_id FROM Code_Data WHERE name='醫療費' ), '醫療費', 'Y', NULL UNION ALL
SELECT 'Floating','牙醫', ( SELECT code_id FROM Code_Data WHERE name='醫療費' ), '醫療費', 'Y', NULL UNION ALL
SELECT 'Floating','其他', ( SELECT code_id FROM Code_Data WHERE name='醫療費' ), '醫療費', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='醫療費' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Floating','食品', ( SELECT code_id FROM Code_Data WHERE name='毛小孩' ), '毛小孩', 'Y', NULL UNION ALL
SELECT 'Floating','用品', ( SELECT code_id FROM Code_Data WHERE name='毛小孩' ), '毛小孩', 'Y', NULL UNION ALL
SELECT 'Floating','玩具', ( SELECT code_id FROM Code_Data WHERE name='毛小孩' ), '毛小孩', 'Y', NULL UNION ALL
SELECT 'Floating','醫療', ( SELECT code_id FROM Code_Data WHERE name='毛小孩' ), '毛小孩', 'Y', NULL UNION ALL
SELECT 'Floating','其他', ( SELECT code_id FROM Code_Data WHERE name='毛小孩' ), '毛小孩', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='毛小孩' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Floating','食品', ( SELECT code_id FROM Code_Data WHERE name='尊親費用' ), '尊親費用', 'Y', NULL UNION ALL
SELECT 'Floating','用品', ( SELECT code_id FROM Code_Data WHERE name='尊親費用' ), '尊親費用', 'Y', NULL UNION ALL
SELECT 'Floating','3C', ( SELECT code_id FROM Code_Data WHERE name='尊親費用' ), '尊親費用', 'Y', NULL UNION ALL
SELECT 'Floating','其他', ( SELECT code_id FROM Code_Data WHERE name='尊親費用' ), '尊親費用', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='尊親費用' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Floating','聚餐', ( SELECT code_id FROM Code_Data WHERE name='休閒娛樂' ), '休閒娛樂', 'Y', NULL UNION ALL
SELECT 'Floating','展覽', ( SELECT code_id FROM Code_Data WHERE name='休閒娛樂' ), '休閒娛樂', 'Y', NULL UNION ALL
SELECT 'Floating','玩具', ( SELECT code_id FROM Code_Data WHERE name='休閒娛樂' ), '休閒娛樂', 'Y', NULL UNION ALL
SELECT 'Floating','國內旅遊', ( SELECT code_id FROM Code_Data WHERE name='休閒娛樂' ), '休閒娛樂', 'Y', NULL UNION ALL
SELECT 'Floating','出國', ( SELECT code_id FROM Code_Data WHERE name='休閒娛樂' ), '休閒娛樂', 'Y', NULL UNION ALL
SELECT 'Floating','電影', ( SELECT code_id FROM Code_Data WHERE name='休閒娛樂' ), '休閒娛樂', 'Y', NULL UNION ALL
SELECT 'Floating','紀念品', ( SELECT code_id FROM Code_Data WHERE name='休閒娛樂' ), '休閒娛樂', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='休閒娛樂' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Floating','代買', ( SELECT code_id FROM Code_Data WHERE name='人情往來' ), '人情往來', 'Y', NULL UNION ALL
SELECT 'Floating','送禮', ( SELECT code_id FROM Code_Data WHERE name='人情往來' ), '人情往來', 'Y', NULL UNION ALL
SELECT 'Floating','婚宴', ( SELECT code_id FROM Code_Data WHERE name='人情往來' ), '人情往來', 'Y', NULL UNION ALL
SELECT 'Floating','過年', ( SELECT code_id FROM Code_Data WHERE name='人情往來' ), '人情往來', 'Y', NULL UNION ALL
SELECT 'Floating','其他禮金', ( SELECT code_id FROM Code_Data WHERE name='人情往來' ), '人情往來', 'Y', NULL UNION ALL
SELECT 'Floating','請客', ( SELECT code_id FROM Code_Data WHERE name='人情往來' ), '人情往來', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='人情往來' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Floating','可報稅機構', ( SELECT code_id FROM Code_Data WHERE name='捐款' ), '捐款', 'Y', NULL UNION ALL
SELECT 'Floating','一般捐款', ( SELECT code_id FROM Code_Data WHERE name='捐款' ), '捐款', 'Y', NULL UNION ALL
SELECT 'Floating','寺廟納金', ( SELECT code_id FROM Code_Data WHERE name='捐款' ), '捐款', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='捐款' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Floating','遺失', ( SELECT code_id FROM Code_Data WHERE name='其他' ), '其他', 'Y', NULL UNION ALL
SELECT 'Floating','短期保險', ( SELECT code_id FROM Code_Data WHERE name='其他' ), '其他', 'Y', NULL UNION ALL
SELECT 'Floating','借出', ( SELECT code_id FROM Code_Data WHERE name='其他' ), '其他', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='其他' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Income', '薪資', NULL, NULL, 'Y', NULL UNION ALL
SELECT 'Income', '獎金', NULL, NULL, 'Y', NULL UNION ALL
SELECT 'Income', '投資', NULL, NULL, 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_type='Income' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Income','工作', ( SELECT code_id FROM Code_Data WHERE name='薪資' ), '薪資', 'Y', NULL UNION ALL
SELECT 'Income','外包', ( SELECT code_id FROM Code_Data WHERE name='薪資' ), '薪資', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='薪資' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Income','一般獎金', ( SELECT code_id FROM Code_Data WHERE name='獎金' ), '獎金', 'Y', NULL UNION ALL
SELECT 'Income','年終獎金', ( SELECT code_id FROM Code_Data WHERE name='獎金' ), '獎金', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='獎金' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Income','資本利得', ( SELECT code_id FROM Code_Data WHERE name='投資' ), '投資', 'Y', NULL UNION ALL
SELECT 'Income','抽籤', ( SELECT code_id FROM Code_Data WHERE name='投資' ), '投資', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='投資' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Fixed', '生活基本', NULL, NULL, 'Y', NULL UNION ALL
SELECT 'Fixed', '尊親費用', NULL, NULL, 'Y', NULL UNION ALL
SELECT 'Fixed', '居家物業', NULL, NULL, 'Y', NULL UNION ALL
SELECT 'Fixed', '稅費', NULL, NULL, 'Y', NULL UNION ALL
SELECT 'Fixed', '保險費', NULL, NULL, 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_type='Fixed' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Fixed','水費', ( SELECT code_id FROM Code_Data WHERE name='生活基本' ), '生活基本', 'Y', NULL UNION ALL
SELECT 'Fixed','電費', ( SELECT code_id FROM Code_Data WHERE name='生活基本' ), '生活基本', 'Y', NULL UNION ALL
SELECT 'Fixed','瓦斯費', ( SELECT code_id FROM Code_Data WHERE name='生活基本' ), '生活基本', 'Y', NULL UNION ALL
SELECT 'Fixed','電話網路', ( SELECT code_id FROM Code_Data WHERE name='生活基本' ), '生活基本', 'Y', NULL UNION ALL
SELECT 'Fixed','消耗品', ( SELECT code_id FROM Code_Data WHERE name='生活基本' ), '生活基本', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='生活基本' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Fixed','生活費', ( SELECT code_id FROM Code_Data WHERE name='尊親費用' AND code_type='Fixed' ), '尊親費用', 'Y', NULL UNION ALL
SELECT 'Fixed','保險費', ( SELECT code_id FROM Code_Data WHERE name='尊親費用' AND code_type='Fixed' ), '尊親費用', 'Y', NULL UNION ALL
SELECT 'Fixed','基本支出', ( SELECT code_id FROM Code_Data WHERE name='尊親費用' AND code_type='Fixed' ), '尊親費用', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='尊親費用' AND code_type='Fixed' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Fixed','房租', ( SELECT code_id FROM Code_Data WHERE name='居家物業' ), '居家物業', 'Y', NULL UNION ALL
SELECT 'Fixed','房貸', ( SELECT code_id FROM Code_Data WHERE name='居家物業' ), '居家物業', 'Y', NULL UNION ALL
SELECT 'Fixed','汽機車保養', ( SELECT code_id FROM Code_Data WHERE name='居家物業' ), '居家物業', 'Y', NULL UNION ALL
SELECT 'Fixed','物業管理費', ( SELECT code_id FROM Code_Data WHERE name='居家物業' ), '居家物業', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='居家物業' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Fixed','所得稅', ( SELECT code_id FROM Code_Data WHERE name='稅費' ), '稅費', 'Y', NULL UNION ALL
SELECT 'Fixed','燃料稅', ( SELECT code_id FROM Code_Data WHERE name='稅費' ), '稅費', 'Y', NULL UNION ALL
SELECT 'Fixed','房屋稅', ( SELECT code_id FROM Code_Data WHERE name='稅費' ), '稅費', 'Y', NULL UNION ALL
SELECT 'Fixed','二代健保', ( SELECT code_id FROM Code_Data WHERE name='稅費' ), '稅費', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='稅費' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Fixed','醫療險', ( SELECT code_id FROM Code_Data WHERE name='保險費' ), '保險費', 'Y', NULL UNION ALL
SELECT 'Fixed','壽險', ( SELECT code_id FROM Code_Data WHERE name='保險費' ), '保險費', 'Y', NULL UNION ALL
SELECT 'Fixed','意外險', ( SELECT code_id FROM Code_Data WHERE name='保險費' ), '保險費', 'Y', NULL UNION ALL
SELECT 'Fixed','儲蓄險', ( SELECT code_id FROM Code_Data WHERE name='保險費' ), '保險費', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='保險費' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Passive', '孳息收入', NULL, NULL, 'Y', NULL UNION ALL
SELECT 'Passive', '借貸收入', NULL, NULL, 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_type='Passive' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Passive','銀行利息', ( SELECT code_id FROM Code_Data WHERE name='孳息收入' ), '孳息收入', 'Y', NULL UNION ALL
SELECT 'Passive','股息', ( SELECT code_id FROM Code_Data WHERE name='孳息收入' ), '孳息收入', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='孳息收入' );

INSERT INTO Code_Data (code_type, name ,code_group, code_group_name, in_use, code_index)
SELECT * FROM (
SELECT 'Passive','房租收入', ( SELECT code_id FROM Code_Data WHERE name='借貸收入' ), '借貸收入', 'Y', NULL UNION ALL
SELECT 'Passive','借款收入', ( SELECT code_id FROM Code_Data WHERE name='借貸收入' ), '借貸收入', 'Y', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Code_Data WHERE code_group_name='借貸收入' );

-- 帳戶
INSERT INTO Account (account_id, name ,account_type, fx_code, is_calculate, in_use, discount, memo, account_index)
SELECT * FROM (
SELECT NULL, '自己手邊', 'cash', 'TWD', 'N', 'Y', NULL, NULL, NULL UNION ALL
SELECT '807-1234567890', '永豐大戶', 'normal', 'TWD', 'Y', 'Y', NULL, '活存50萬內1.1%及免費跨行轉提20次，至2021年12月31日', NULL )
WHERE NOT EXISTS ( SELECT NULL FROM Account );

INSERT INTO Account_Balance (vesting_month, id, name ,balance, fx_rate)
SELECT * FROM (
SELECT '202012', ( SELECT id FROM Account WHERE name='永豐大戶' ), '永豐大戶', 123456, 1 )
WHERE NOT EXISTS ( SELECT NULL FROM Account_Balance );

-- 其他資產
INSERT INTO Other_Asset (asset_name, asset_type, in_use ,asset_index)
SELECT * FROM (
SELECT '台股', 'Stock', 'Y', NULL UNION ALL 
SELECT '美股', 'Stock', 'Y', NULL UNION ALL 
SELECT '儲蓄險', 'Insurance', 'Y', NULL  UNION ALL 
SELECT '房地產', 'Estate', 'Y', NULL  )
WHERE NOT EXISTS ( SELECT NULL FROM Other_Asset );

-- 預算
INSERT INTO Budget (budget_year, category_code, category_name ,code_type, expected01, expected02, expected03, expected04, expected05, expected06, expected07, expected08, expected09, expected10, expected11, expected12)
SELECT * FROM (
SELECT '2021', ( SELECT code_id FROM Code_Data WHERE name='主食' ), '主食', 'Floating', -4377, -5092, -5097, -4224, -4688, -6399, -4071, -4996, -4606, -4752, -4826, -7677 UNION ALL 
SELECT '2021', ( SELECT code_id FROM Code_Data WHERE name='副食' ), '副食', 'Floating', -636, -669, -665, -826, -160, -219, -194, -1067, -586, -2310, -1625, -3341 UNION ALL 
SELECT '2021', ( SELECT code_id FROM Code_Data WHERE name='日用品' ), '日用品', 'Floating', -94, 0, -245, -265, -1599, -1369, -526, 0, -5950, -1883, -8500, -856 UNION ALL 
SELECT '2021', ( SELECT code_id FROM Code_Data WHERE name='行車交通' ), '行車交通', 'Floating', -670, -738, -933, -711, -1229, -881, -842, -1038, -1057, -1116, -952, -855 UNION ALL 
SELECT '2021', ( SELECT code_id FROM Code_Data WHERE name='學習' ), '學習', 'Floating', -1914, -319, -606, -199, -199, -199, 0, -750, -6413, 0, 0, -3500 UNION ALL 
SELECT '2021', ( SELECT code_id FROM Code_Data WHERE name='醫療費' ), '醫療費', 'Floating', -270, -240, -320, 0, -100, -2620, -3150, -6050, -7350, -370, 0, 0 UNION ALL 
SELECT '2021', ( SELECT code_id FROM Code_Data WHERE name='毛小孩' ), '毛小孩', 'Floating', -270, -240, -320, 0, -100, -2620, -3150, -6050, -7350, -370, 0, 0 UNION ALL 
SELECT '2021', ( SELECT code_id FROM Code_Data WHERE name='尊親費用' AND code_type='Floating' ), '尊親費用', 'Floating', -286, -17556, 0, -3104, -1645, -3660, -1598, -4266, -678, -5647, -704, -371 UNION ALL 
SELECT '2021', ( SELECT code_id FROM Code_Data WHERE name='休閒娛樂' ), '休閒娛樂', 'Floating', 0, 0, 0, 0, -4288, -1248, -5223, 0, 0, 0, -576, 0 UNION ALL 
SELECT '2021', ( SELECT code_id FROM Code_Data WHERE name='人情往來' ), '人情往來', 'Floating', 0, -24400, 0, 0, -4200, 0, 0, 0, 0, 0, -3400, -0 UNION ALL 
SELECT '2021', ( SELECT code_id FROM Code_Data WHERE name='捐款' ), '捐款', 'Floating', -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000 UNION ALL 
SELECT '2021', ( SELECT code_id FROM Code_Data WHERE name='其他' ), '其他', 'Floating', 0, -1228, -800, -0, -800, -800, -89, 0, -3766, -615, -4867, -1202 UNION ALL 
SELECT '2021', ( SELECT code_id FROM Code_Data WHERE name='生活基本' ), '生活基本', 'Fixed', -3000, -3000, -3000, -3000, -3000, -3000, -3000, -3000, -3000, -3000, -3000, -3000 UNION ALL 
SELECT '2021', ( SELECT code_id FROM Code_Data WHERE name='尊親費用' AND code_type='Fixed' ), '尊親費用', 'Fixed', -12000, -12000, -12000, -12000, -72197, -12000, -12000, -12000, -12000, -12000, -12000, -12000 UNION ALL 
SELECT '2021', ( SELECT code_id FROM Code_Data WHERE name='居家物業' ), '居家物業', 'Fixed', -15000, -15000, -15000, -15000, -15000, -15000, -15000, -15000, -15000, -15000, -15000, -15000 UNION ALL 
SELECT '2021', ( SELECT code_id FROM Code_Data WHERE name='稅費' ), '稅費', 'Fixed', 0, 0, 0, 0, -10000, -10000, -1000, 0, 0, 0, 0, 0 UNION ALL 
SELECT '2021', ( SELECT code_id FROM Code_Data WHERE name='保險費' ), '保險費', 'Fixed', -16081, -8375, 0, 0, 0, -20184, 0, -1200, 0, 0, 0, 0 )
WHERE NOT EXISTS ( SELECT NULL FROM Budget );