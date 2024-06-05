import psycopg2

# 连接到数据库
conn = psycopg2.connect(
    database='pyqt5_test_database', user='postgres', password='174496',
    host='localhost',
    port='5432'
)

# 创建游标对象
cur = conn.cursor()

# 定义要查询的武器类型列表
weapon_types = ['中型机枪', '冲锋枪', '半自动步枪', '半自动装填步枪']

# 查询每种武器类型对应的武器
weapons_by_type = {}
for weapon_type in weapon_types:
    cur.execute("""
        SELECT weapon_name FROM weapons
        JOIN weapon_types ON weapons.weapon_type_id = weapon_types.type_id
        WHERE weapon_types.type_name = %s
    """, (weapon_type,))
    weapons = cur.fetchall()
    weapons_by_type[weapon_type] = [weapon[0] for weapon in weapons]

# 打印每种武器类型对应的武器
for weapon_type, weapons in weapons_by_type.items():
    print(f"{weapon_type} 对应的武器:")
    print(weapons)

# 关闭游标和连接
cur.close()
conn.close()
