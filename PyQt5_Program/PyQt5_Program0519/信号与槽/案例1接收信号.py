import sys

# from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QPushButton, QApplication, QWidget


# 继承于QWidget
class MyWindow(QWidget):
    def __init__(self):
        # 调用QWidget的初始化
        super().__init__()
        # 调用自己的初始化
        self.init_ui()

    def init_ui(self):
        # 设置窗口的大小
        self.resize(500, 300)
        # 使用了一个按钮
        btn = QPushButton('点我', self)
        # 设置按钮的位置大小
        btn.setGeometry(200, 200, 100, 30)
        # 将按钮点击的信号于与方法（函数）
        btn.clicked.connect(self.click_my_btn)

    # 定义了一个槽函数click_my_btn
    def click_my_btn(self, arg):
        print('点按钮了', arg)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MyWindow()
    w.show()

    sys.exit(app.exec_())
