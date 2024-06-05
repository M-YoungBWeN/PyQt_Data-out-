import psycopg2


def execute_query(conn, query, keyword):
    with conn.cursor() as cur:
        cur.execute(query, (keyword, keyword))  # 传递两个相同的参数
        return cur.fetchall()


# 连接数据库
conn = psycopg2.connect(database='pyqt5_test_database', user='postgres', password='174496',
                        host='localhost',
                        port='5432')

# 用户输入的关键字
keyword = "战"
keyword_like = '%' + keyword + '%'

# 整合结果列表
all_results = []

# 查询所有武器对应的武器类型
query1 = """
SELECT w.weapon_id, w.weapon_name, wt.type_name
FROM weapons w
JOIN weapon_types wt ON w.weapon_type_id = wt.type_id
WHERE w.weapon_name LIKE %s OR wt.type_name LIKE %s;
"""
weapons_and_types = execute_query(conn, query1, keyword_like)
all_results.extend([("武器和武器类型", row) for row in weapons_and_types])

# 查询所有载具对应的载具类型
query2 = """
SELECT v.vehicle_id, v.vehicle_name, vt.type_name
FROM vehicles v
JOIN vehicle_types vt ON v.vehicle_type_id = vt.type_id
WHERE v.vehicle_name LIKE %s OR vt.type_name LIKE %s;
"""
vehicles_and_types = execute_query(conn, query2, keyword_like)
all_results.extend([("载具和载具类型", row) for row in vehicles_and_types])

# 查询所有武器对应的兵种
query3 = """
SELECT w.weapon_id, w.weapon_name, s.soldier_id, s.soldier_type
FROM weapons w
JOIN soldiers s ON w.weapon_id = s.primary_weapon_id
WHERE w.weapon_name LIKE %s OR s.soldier_type LIKE %s;
"""
weapons_and_soldiers = execute_query(conn, query3, keyword_like)
all_results.extend([("武器和兵种", row) for row in weapons_and_soldiers])

# 查询所有武器类型对应的兵种
query4 = """
SELECT wt.type_id, wt.type_name, s.soldier_id, s.soldier_type
FROM weapon_types wt
JOIN weapons w ON wt.type_id = w.weapon_type_id
JOIN soldiers s ON w.weapon_id = s.primary_weapon_id
WHERE wt.type_name LIKE %s OR s.soldier_type LIKE %s;
"""
weapon_types_and_soldiers = execute_query(conn, query4, keyword_like)
all_results.extend([("武器类型和兵种", row) for row in weapon_types_and_soldiers])

# 关闭连接
conn.close()

# 输出整合后的结果
for result in all_results:
    print(result[0], result[1])
