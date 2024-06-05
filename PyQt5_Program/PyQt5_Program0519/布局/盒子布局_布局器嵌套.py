"""
布局器可以嵌套
"""
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGroupBox, QRadioButton, QHBoxLayout


class MyWindow(QWidget):
    # 一定要调用父类的__init__方法，因为它里面有很多对ui空间的初始化操作
    def __init__(self):
        super().__init__()
        # 创建一个自己的初始化方法，让父类方法不臃肿
        self.init_ui()

    def init_ui(self):
        self.resize(300, 300)
        self.setWindowTitle('嵌套布局')

        # 创建一个垂直布局器
        container = QVBoxLayout()

        # 为了实现布局器嵌套，创建了两个组QGroupBox
        # =========创建第1个组=========
        hobby_box = QGroupBox('爱好')
        # 创建布局器
        v_layout = QVBoxLayout()
        btn1 = QRadioButton('足球')
        btn2 = QRadioButton('乒乓球')
        btn3 = QRadioButton('游戏')
        v_layout.addWidget(btn1)
        v_layout.addWidget(btn2)
        v_layout.addWidget(btn3)
        # 使用布局器
        hobby_box.setLayout(v_layout)

        # =========创建第2个组=========
        gender_box = QGroupBox('性别')
        # 创建布局器
        h_layout = QHBoxLayout()
        btn4 = QRadioButton('男')
        btn5 = QRadioButton('女')
        h_layout.addWidget(btn4)
        h_layout.addWidget(btn5)
        # 使用布局器
        gender_box.setLayout(h_layout)

        # 把两个组添加到整体的布局器中
        container.addWidget(hobby_box)
        container.addWidget(gender_box)
        # 让当前窗口使用这个布局器
        self.setLayout(container)


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建一个对象;sys.argv是给程序传入的参数
    # ---------------------------------------------------
    w = MyWindow()
    w.show()
    # ---------------------------------------------------
    sys.exit(app.exec_())  # 实现程序的循环等待;事件检测的循环
