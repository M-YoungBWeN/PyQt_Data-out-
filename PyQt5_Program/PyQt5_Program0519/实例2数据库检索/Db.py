from main import *
from Dialog_Select_Null_UI import *


# 数据库信息更新
# def db_message(self):
#     DB_DATABASE = self.ui.lineEdit_db_name.text()
#     DB_USER = self.ui.lineEdit_db_user.text()
#     DB_PASSWORD = self.ui.lineEdit_db_password.text()
#     DB_HOST = self.ui.lineEdit_db_host.text()
#     DB_PORT = self.ui.lineEdit_db_port.text()
#     t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
#     self.ui.textBrowser.append('-------------------')
#     self.ui.textBrowser.append(f'{t}')
#     self.ui.textBrowser.append('数据库信息更新成功！')
#     self.ui.textBrowser.append('当前的信息为：')
#     self.ui.textBrowser.append(f'database:{DB_DATABASE}')
#     self.ui.textBrowser.append(f'user:{DB_USER}')
#     self.ui.textBrowser.append(f'host:{DB_HOST}')
#     self.ui.textBrowser.append(f'port:{DB_PORT}')
#     self.ui.textBrowser.ensureCursorVisible()
#     return DB_DATABASE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


# -----------广泛下拉查询-----------
def set_table_weapons_and_type(self):
    conn = set_database(self)
    cur = conn.cursor()
    cur.execute(
        'SELECT w.weapon_id, w.weapon_name, wt.type_name FROM weapons w JOIN weapon_types wt ON w.weapon_type_id = wt.type_id;')
    rows = cur.fetchall()  # 获取数据
    # print(rows)
    row = cur.rowcount  # 获取行数
    vol = len(rows[0]) - 1  # 获取列数
    # print(row,col)
    cur.close()
    conn.close()
    self.ui.tableWidget_all_weapons.setRowCount(row)  # 设置table行列
    self.ui.tableWidget_all_weapons.setColumnCount(vol)

    for i in range(row):
        for j in range(vol):
            temp_data = rows[i][j + 1]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.ui.tableWidget_all_weapons.setItem(i, j, data)
    self.ui.tableWidget_all_weapons.resizeColumnsToContents()
    self.ui.stackedWidget_db_select.setCurrentIndex(2)


def set_table_vehicles_and_types(self):
    conn = set_database(self)
    cur = conn.cursor()
    cur.execute(
        'SELECT v.vehicle_id, v.vehicle_name, vt.type_name FROM vehicles v JOIN vehicle_types vt ON v.vehicle_type_id = vt.type_id;')
    rows = cur.fetchall()  # 获取数据
    # print(rows)
    row = cur.rowcount  # 获取行数
    vol = len(rows[0]) - 1  # 获取列数
    # print(row,col)
    cur.close()
    conn.close()
    self.ui.tableWidget_all_vehicles.setRowCount(row)  # 设置table行列
    self.ui.tableWidget_all_vehicles.setColumnCount(vol)

    for i in range(row):
        for j in range(vol):
            temp_data = rows[i][j + 1]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.ui.tableWidget_all_vehicles.setItem(i, j, data)
    self.ui.tableWidget_all_vehicles.resizeColumnsToContents()  # 自适应行宽
    self.ui.stackedWidget_db_select.setCurrentIndex(3)


def set_table_soldiertypes_and_weaponstypes(self):
    conn = set_database(self)
    cur = conn.cursor()
    cur.execute(
        'SELECT s.soldier_type, wt.type_name FROM soldiers s JOIN weapon_types wt ON s.primary_weapon_id = wt.type_id;')
    rows = cur.fetchall()  # 获取数据
    # print(rows)
    row = cur.rowcount  # 获取行数
    vol = len(rows[0])  # 获取列数
    # print(row,col)
    cur.close()
    conn.close()
    self.ui.tableWidget_all_soldiertypes.setRowCount(row)  # 设置table行列
    self.ui.tableWidget_all_soldiertypes.setColumnCount(vol)

    for i in range(row):
        for j in range(vol):
            temp_data = rows[i][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.ui.tableWidget_all_soldiertypes.setItem(i, j, data)
    self.ui.tableWidget_all_soldiertypes.resizeColumnsToContents()
    self.ui.stackedWidget_db_select.setCurrentIndex(4)


# ---------------结束---------------

# 细分下拉查询
# 获取数据库中所有的细分类别
def get_db_select_types_combobox(self):
    try:
        conn = set_database(self)
        cursor = conn.cursor()

        cursor.execute("SELECT type_name FROM weapon_types UNION SELECT type_name FROM vehicle_types")
        all_weapon_types = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()
        print(all_weapon_types)

        self.ui.comboBox_db_select_types.addItems(all_weapon_types)
        self.QVBoxLayout.addWidget(self.ui.comboBox_db_select_types)


    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


# 展示细分查询结果
def get_db_select_types_result(self):
    db_select_types = self.ui.comboBox_db_select_types.currentText()

    # 创建游标对象
    try:
        conn = set_database(self)
        cur = conn.cursor()

        # 查询类型对应的载具或武器
        cur.execute("""
            SELECT vehicle_name FROM vehicles
            JOIN vehicle_types ON vehicles.vehicle_type_id = vehicle_types.type_id
            WHERE vehicle_types.type_name = %s
        """, (db_select_types,))
        weapons_vehicles = cur.fetchall()

        # 如果没有找到载具，再查找武器
        if len(weapons_vehicles) == 0:
            cur.execute("""
                SELECT weapon_name FROM weapons
                JOIN weapon_types ON weapons.weapon_type_id = weapon_types.type_id
                WHERE weapon_types.type_name = %s
            """, (db_select_types,))
            weapons_vehicles = cur.fetchall()

        # 关闭游标和连接
        cur.close()
        conn.close()

        if len(weapons_vehicles) == 0:  # 如果查询结果为空
            # dialog_null.show()
            # self.ui.stackedWidget_db_select.setCurrentIndex(1)
            raise ValueError("查询未返回结果")
        else:
            # 展示到table
            rows = weapons_vehicles  # 获取数据
            # print(rows)
            row = len(rows)  # 获取行数
            vol = len(rows[0])  # 获取列数
            print(row, vol)

            self.ui.tableWidget_select_types_result.setRowCount(row)  # 设置table行列
            self.ui.tableWidget_select_types_result.setColumnCount(vol)
            for i in range(row):
                for j in range(vol):
                    temp_data = rows[i][j]  # 临时记录，不能直接插入表格
                    data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.ui.tableWidget_select_types_result.setItem(i, j, data)
            self.ui.tableWidget_select_types_result.resizeColumnsToContents()
            self.ui.stackedWidget_db_select.setCurrentIndex(0)

    except ValueError as e:
        print(f"错误: {e}")

    except psycopg2.Error as e:
        print(f"数据库错误: {e}")

    finally:
        if conn:
            conn.close()
