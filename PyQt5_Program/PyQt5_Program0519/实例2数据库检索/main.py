# from PyQt5.QtGui import QCursor
import time
from Db import *
from loginUI import *
from InterfaceUI import *
from Dialog_Select_Null_UI import *
from DatabaseApp import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect, QTableWidgetItem, QDialog
import sys
from PyQt5.QtCore import Qt, QCoreApplication, QPoint  # 隐藏标题栏要用到的库
import webbrowser
import psycopg2

# 记录当前登录的用户
user_now = ''

# 记录当前数据库信息
DB_DATABASE = 'pyqt5_test_database'
DB_USER = 'postgres'
DB_PASSWORD = '174496'
DB_HOST = 'localhost'
DB_PORT = '5432'


# -------------- 全局方法-----------------
# 去除窗口标题栏和空背景
def window_attribute_effect(self):
    self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏标题栏
    self.setAttribute(Qt.WA_TranslucentBackground)  # 隐藏空背景


# 增加窗口阴影
def window_shadow_effect(self):
    # 创建一个QGraphicsDropShadowEffect对象
    shadow_effect = QGraphicsDropShadowEffect(self)
    # 设置阴影的参数
    shadow_effect.setBlurRadius(20)  # 模糊半径
    shadow_effect.setColor(Qt.black)  # 阴影颜色
    shadow_effect.setOffset(3, 3)  # 偏移量
    # 将阴影应用到窗口
    self.setGraphicsEffect(shadow_effect)


# 面向对象-便于更改数据库配置
def set_database(self):
    global DB_DATABASE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
    return psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD,
                            host=DB_HOST,
                            port=DB_PORT)


# 模糊查询实现
def get_db_input_result(self):
    def execute_query(conn, query, keyword):
        with conn.cursor() as cur:
            cur.execute(query, (keyword, keyword))  # 传递两个相同的参数
            result = cur.fetchall()
            return result

    # 连接数据库
    try:
        conn = set_database(self)

        # 用户输入的关键字
        keyword = self.ui.lineEdit_input_types_2.text()
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
        all_results.extend([("武器和武器类型", *row) for row in weapons_and_types])

        # 查询所有载具对应的载具类型
        query2 = """
        SELECT v.vehicle_id, v.vehicle_name, vt.type_name
        FROM vehicles v
        JOIN vehicle_types vt ON v.vehicle_type_id = vt.type_id
        WHERE v.vehicle_name LIKE %s OR vt.type_name LIKE %s;
        """
        vehicles_and_types = execute_query(conn, query2, keyword_like)
        all_results.extend([("载具和载具类型", *row) for row in vehicles_and_types])

        # 查询所有武器对应的兵种
        query3 = """
        SELECT w.weapon_id, w.weapon_name, s.soldier_id, s.soldier_type
        FROM weapons w
        JOIN soldiers s ON w.weapon_id = s.primary_weapon_id
        WHERE w.weapon_name LIKE %s OR s.soldier_type LIKE %s;
        """
        weapons_and_soldiers = execute_query(conn, query3, keyword_like)
        all_results.extend([("武器和兵种", *row) for row in weapons_and_soldiers])

        # 查询所有武器类型对应的兵种
        query4 = """
        SELECT wt.type_id, wt.type_name, s.soldier_id, s.soldier_type
        FROM weapon_types wt
        JOIN weapons w ON wt.type_id = w.weapon_type_id
        JOIN soldiers s ON w.weapon_id = s.primary_weapon_id
        WHERE wt.type_name LIKE %s OR s.soldier_type LIKE %s;
        """
        weapon_types_and_soldiers = execute_query(conn, query4, keyword_like)
        all_results.extend([("武器类型和兵种", *row) for row in weapon_types_and_soldiers])

        # 关闭连接
        conn.close()
        if len(all_results) == 0:  # 如果查询结果为空
            dialog_null.show()
            raise ValueError("查询未返回结果")
        else:
            # 输出整合后的结果
            for result in all_results:
                description = result[0]
                data = result[1:]
                print(f"{description}: {data}")

            # 展示到table
            rows = all_results  # 获取数据
            # print(rows)
            row = len(rows)  # 获取行数
            vol = len(rows[0])  # 获取列数
            print(row, vol)

            self.ui.tableWidget_input_2_result.setRowCount(row)  # 设置table行列
            self.ui.tableWidget_input_2_result.setColumnCount(vol)
            for i in range(row):
                for j in range(vol):
                    temp_data = rows[i][j]  # 临时记录，不能直接插入表格
                    data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.ui.tableWidget_input_2_result.setItem(i, j, data)
            self.ui.tableWidget_input_2_result.resizeColumnsToContents()
            self.ui.stackedWidget_db_select.setCurrentIndex(5)

    except ValueError as e:
        print(f"错误: {e}")

    except psycopg2.Error as e:
        print(f"数据库错误: {e}")

    # finally:
    #     if conn:
    #         conn.close()


# ----------------结束------------------

# 登录窗口
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # ----------直接把装配ui的过程放在了这里----------
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)  # 执行类中的setupUi方法,self是win
        # ------------------装配结束-------------------
        window_attribute_effect(self)  # 调用去除窗口标题栏和空背景方法
        window_shadow_effect(self)  # 调用窗口阴影方法
        self.pushbutton_connect()  # 点击事件
        self.show()

    # 登陆注册面板点击事件
    def pushbutton_connect(self):
        self.ui.pushButton_login.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.pushButton_register.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        # 确认登陆按钮绑定
        self.ui.pushButton_login_sure.clicked.connect(self.login_in)
        # 确认注册按钮绑定
        self.ui.pushButton_register_sure.clicked.connect(self.register_in)

    # 获取登录时用户的账号密码
    def login_in(self):
        account = self.ui.lineEdit_account.text()
        password = self.ui.lineEdit_password.text()

        # ======数据库操作=======
        account_list = []  # 存放从数据表读出的数据
        password_list = []
        conn = set_database(self)
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')  # 在此添加SQL语句
        rows = cur.fetchall()  # rows存储在数据表user读出的数据
        # print(rows)
        for row in rows:  # 把账号密码分别存入列表
            account_list.append(row[0])  # append() 函数可以向列表末尾添加元素
            password_list.append(row[1])
        # print(account_list, password_list)
        for i in range(len(account_list)):
            if len(account) == 0 or password == 0:
                self.ui.stackedWidget.setCurrentIndex(1)
            elif account == account_list[i] and password == password_list[i]:
                global user_now
                user_now = account
                # print(f'当前用户为：{account}')
                win.close()
                main_window.show()
            else:
                self.ui.stackedWidget.setCurrentIndex(2)
        conn.commit()  # 提交SQL语句
        conn.close()
        # =========结束==========

        # # -------测试入口--------
        # if account == '123' and password == '000':
        #     win.close()
        #     main_window.show()
        # else:
        #     print('WRONG')
        # # ---------结束---------

    # # 重写窗口移动方法
    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.drag = True
    #         self.offset = event.globalPos() - self.pos()
    #         print("Moving...")
    #         QApplication.setOverrideCursor(QCursor(Qt.OpenHandCursor))
    #
    # def mouseMoveEvent(self, event):
    #     if self.drag:
    #         new_pos = event.globalPos() - self.offset
    #         self.move(new_pos)
    #
    # def mouseReleaseEvent(self, event):
    #     if self.drag and event.button() == Qt.LeftButton:
    #         self.drag = False
    #         QApplication.restoreOverrideCursor()
    #         print("Moved")

    def register_in(self):
        register_account = self.ui.lineEdit_newaccount.text()
        register_password = self.ui.lineEdit_newpassword.text()
        register_re_password = self.ui.lineEdit_renewpassword.text()
        if len(register_password) == 0 or len(register_re_password) == 0:
            self.ui.stackedWidget.setCurrentIndex(4)
        elif register_password == register_re_password:
            conn = set_database(self)
            cur = conn.cursor()
            cur.execute(f" insert into users values('{register_account}','{register_password}')")
            conn.commit()
            conn.close()
            self.ui.stackedWidget.setCurrentIndex(5)
        else:
            self.ui.stackedWidget.setCurrentIndex(3)

    # ----------窗口移动------------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()
    # -------------结束-------------


# 主窗口
class InterFaceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_InterFaceWindow()
        self.ui.setupUi(self)
        window_attribute_effect(self)  # 调用去除窗口标题栏和空背景方法
        # window_shadow_effect(self)  # 调用窗口阴影方法
        self.pushbutton_connect()  # 登陆注册面板点击事件

    def pushbutton_connect(self):
        # 左侧菜单栏跳转
        self.ui.pushButton_home.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_search.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_myaccount.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.pushButton_support.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.pushButton_help.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        # 帮助与支持菜单栏网页跳转
        self.ui.pushButton_support_web.clicked.connect(lambda: webbrowser.open('https://042333.xyz/'))
        # 退出登录
        self.ui.pushButton_logout.clicked.connect(self.log_out)
        # 更改密码确认按钮
        self.ui.pushButton_change_password_3.clicked.connect(self.change_password)
        # -----db-----
        # 下拉列表查询
        self.ui.comboBox_db_select.currentIndexChanged.connect(self.get_db_select_result)  # 关联信号与槽
        # 模糊查询
        self.ui.pushButton_select_types_2.clicked.connect(self.db_input_result)
        # 细分查询
        self.db_select_types_combobox()
        self.ui.comboBox_db_select_types.currentIndexChanged.connect(self.db_select_types_result)
        # ----end-----
        # 数据库管理界面
        self.ui.pushButton_db_mange.clicked.connect(self.to_db_mange)
        # 更新数据库信息
        self.ui.pushButton_db_change_sure.clicked.connect(self.get_db_message)

    # 广泛下拉查询
    def get_db_select_result(self):

        flag_select = self.ui.comboBox_db_select.currentIndex()
        # print(flag_select)
        if flag_select == 0:
            dialog_null.show()
            self.ui.stackedWidget_db_select.setCurrentIndex(1)

        elif flag_select == 1:
            set_table_weapons_and_type(self)

        elif flag_select == 2:
            set_table_vehicles_and_types(self)

        elif flag_select == 3:
            set_table_soldiertypes_and_weaponstypes(self)

    # 模糊查询
    def db_input_result(self):
        get_db_input_result(self)

    # 细分下拉查询
    # 获取数据库中所有的细分类别
    def db_select_types_combobox(self):
        get_db_select_types_combobox(self)

    # 展示细分查询结果
    def db_select_types_result(self):
        if self.ui.comboBox_db_select_types.currentIndex() == 0:
            dialog_null.show()
            self.ui.stackedWidget_db_select.setCurrentIndex(1)
        else:
            get_db_select_types_result(self)

    # 主界面退出方法
    def log_out(self):
        global user_now
        self.close()
        LoginWindow()
        # self.login = LoginWindow()
        user_now = ''

    # 更改个人密码方法
    def change_password(self):
        newpassword = self.ui.lineEdit_5.text()
        re_newpassword = self.ui.lineEdit_6.text()
        if len(newpassword) == 0 or re_newpassword == 0:
            self.ui.stackedWidget_show_reset_error_3.setCurrentIndex(2)
        elif newpassword == re_newpassword:
            conn = set_database(self)
            cur = conn.cursor()
            cur.execute(f"update users set passwords='{newpassword}' where accounts ='{user_now}' ")
            conn.commit()
            conn.close()
            self.ui.stackedWidget_show_reset_error_3.setCurrentIndex(3)
        else:
            self.ui.stackedWidget_show_reset_error_3.setCurrentIndex(1)

    # 打开数据库管理界面
    def to_db_mange(self):
        database_app.show()

    # 更新数据库
    def get_db_message(self):
        # db_message(self)
        global DB_DATABASE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
        DB_DATABASE = str(self.ui.lineEdit_db_name.text())
        DB_USER = self.ui.lineEdit_db_user.text()
        DB_PASSWORD = self.ui.lineEdit_db_password.text()
        DB_HOST = self.ui.lineEdit_db_host.text()
        DB_PORT = self.ui.lineEdit_db_port.text()
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.ui.textBrowser.append('-------------------')
        self.ui.textBrowser.append(f'{t}')
        self.ui.textBrowser.append('数据库信息更新成功！')
        self.ui.textBrowser.append('当前的信息为：')
        self.ui.textBrowser.append(f'database:{DB_DATABASE}')
        self.ui.textBrowser.append(f'user:{DB_USER}')
        self.ui.textBrowser.append(f'host:{DB_HOST}')
        self.ui.textBrowser.append(f'port:{DB_PORT}')
        self.ui.textBrowser.ensureCursorVisible()

    # # ----------窗口移动------------有bug
    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.old_pos = event.globalPos()
    #
    # def mouseMoveEvent(self, event):
    #     if event.buttons() == Qt.LeftButton:
    #         delta = QPoint(event.globalPos() - self.old_pos)
    #         self.move(self.x() + delta.x(), self.y() + delta.y())
    #         self.old_pos = event.globalPos()
    # # -------------结束-------------


# 警告窗口
class DialogSelectNull(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DialogSelectNull()
        self.ui.setupUi(self)

    # def initWeaponTab(self):
    #     # 创建武器选项卡的布局
    #     weaponLayout = self.ui.tabWidget()
    #
    #     # 创建武器表格
    #     weaponTable = self.ui.weaponTab
    #     weaponLayout.addWidget(weaponTable)
    #
    #     # 创建增加武器按钮，并连接槽函数
    #     weaponAddButton = QPushButton('增加')
    #     weaponAddButton.clicked.connect(self.openAddWeaponDialog)
    #     self.weaponLayout.addWidget(self.weaponAddButton)
    #
    #     # 将布局应用到武器选项卡
    #     self.weaponTab.setLayout(self.weaponLayout)

    # def initVehicleTab(self):
    #     # 创建载具选项卡的布局
    #     self.vehicleLayout = QVBoxLayout()
    #
    #     # 创建载具表格
    #     self.vehicleTable = QTableWidget()
    #     self.vehicleLayout.addWidget(self.vehicleTable)
    #
    #     # 创建增加载具按钮，并连接槽函数
    #     self.vehicleAddButton = QPushButton('增加')
    #     self.vehicleAddButton.clicked.connect(self.openAddVehicleDialog)
    #     self.vehicleLayout.addWidget(self.vehicleAddButton)
    #
    #     # 将布局应用到载具选项卡
    #     self.vehicleTab.setLayout(self.vehicleLayout)


# 数据库管理

if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    # 解决不同电脑不同缩放比例问题
    # QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    win = LoginWindow()  # 创建一个QMainWindow，用来装载需要的各种组件、控件
    main_window = InterFaceWindow()
    dialog_null = DialogSelectNull()
    database_app = DatabaseApp()
    sys.exit(app.exec_())
