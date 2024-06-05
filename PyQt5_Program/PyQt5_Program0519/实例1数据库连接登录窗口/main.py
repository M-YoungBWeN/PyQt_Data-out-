import time

import psycopg2
from PyQt5.QtGui import QCursor

from loginUI import *
from InterfaceUI import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect
import sys
from PyQt5.QtCore import Qt  # 隐藏标题栏要用到的库
import webbrowser
import psycopg2

# 记录当前登录的用户
user_now = ''


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
    return psycopg2.connect(database='pyqt5_test_database', user='postgres', password='174496',
                            host='localhost',
                            port='5432')


# ----------------结束------------------

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
        conn = psycopg2.connect(database='pyqt5_test_database', user='postgres', password='174496', host='localhost',
                                port='5432')
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
        self.ui.pushButton_change_password.clicked.connect(self.change_password)

    def log_out(self):
        global user_now
        self.close()
        LoginWindow()
        # self.login = LoginWindow()
        user_now = ''

    def change_password(self):
        newpassword = self.ui.lineEdit.text()
        re_newpassword = self.ui.lineEdit_2.text()
        if len(newpassword) == 0 or re_newpassword == 0:
            self.ui.stackedWidget_show_reset_error.setCurrentIndex(2)
        elif newpassword == re_newpassword:
            conn = set_database(self)
            cur = conn.cursor()
            cur.execute(f"update users set passwords='{newpassword}' where accounts ='{user_now}' ")
            conn.commit()
            conn.close()
            self.ui.stackedWidget_show_reset_error.setCurrentIndex(3)
        else:
            self.ui.stackedWidget_show_reset_error.setCurrentIndex(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LoginWindow()  # 创建一个QMainWindow，用来装载需要的各种组件、控件
    main_window = InterFaceWindow()
    sys.exit(app.exec_())
