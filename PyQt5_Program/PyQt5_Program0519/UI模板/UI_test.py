import sys
from PyQt5.QtWidgets import QApplication, QWidget
# QApplication--管理功能，如组件的初始化和结束
# QWidget--控件， 所有GUI界面的基类
# sys--python自带的解释器交互接口，处理运行环境时的问题

if __name__ == '__main__':
    app = QApplication(sys.argv)

    print(sys.argv)

    w = QWidget()

    w.setWindowTitle("UI_test")

    w.show()

    # 开始执行程序，并且进入消息循环等待
    # app.exec()
    # 退出时会返回报错码，建议这样写
    sys.exit(app.exec_())
