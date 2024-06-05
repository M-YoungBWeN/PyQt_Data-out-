"""
创建pyqtSignal(信号类型)、绑定connect、触发emit
"""

import time

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
import sys


class MyWindow(QWidget):
    # 声明一个自定义信号 只能放在类属性定义，不能放函数（方法）里
    my_signal = pyqtSignal(str)  # str 表示发送一个str类型的信号

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(500, 400)
        btn = QPushButton('开始检测', self)
        btn.setGeometry(200, 150, 100, 30)
        # connect用于绑定信号
        btn.clicked.connect(self.check)

        # 自定义信号my_signal绑定槽函数my_slot
        self.my_signal.connect(self.my_slot)

    def check(self):
        for i, ip in enumerate('192.168.1.%d' % x for x in range(1, 255)):  # %d python字符串格式化输出
            msg = '正在检查 %s 上的漏洞...' % ip
            # print('正在检查 %s 上的漏洞...'%ip )
            # print(msg)
            if i % 50 == 0:
                # 发射信号 对象.信号.发射(参数)
                self.my_signal.emit(msg + '【发现漏洞】')  # emit用发射信号，emit用在自定义信号中

            # 延时
            time.sleep(0.01)

    def my_slot(self, msg):
        print(msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MyWindow()
    w.show()

    sys.exit(app.exec_())
