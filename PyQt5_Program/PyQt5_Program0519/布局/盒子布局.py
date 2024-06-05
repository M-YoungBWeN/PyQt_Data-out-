"""
QBoxLayout:包括水平QHBoxLayout和竖直QVBoxLayout

弹簧：addStretch()

布局器可以嵌套
"""
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton


class MyWindow(QWidget):
    # 一定要调用父类的__init__方法，因为它里面有很多对ui空间的初始化操作
    def __init__(self):
        super().__init__()

        self.resize(300, 300)
        self.setWindowTitle('垂直布局')

        # 创建一个布局器
        layout = QVBoxLayout()
        # 让当前窗口使用这个布局器
        self.setLayout(layout)

        btn1 = QPushButton('按钮1')
        btn2 = QPushButton('按钮2')
        btn3 = QPushButton('按钮3')
        btn4 = QPushButton('按钮4')
        btn5 = QPushButton('按钮5')
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        # 添加一个伸缩器（弹簧）
        layout.addStretch(3)
        layout.addWidget(btn3)
        layout.addStretch(1)
        layout.addWidget(btn4)
        layout.addStretch(2)
        layout.addWidget(btn5)


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建一个对象;sys.argv是给程序传入的参数
    # ---------------------------------------------------
    w = MyWindow()
    w.show()
    # ---------------------------------------------------
    sys.exit(app.exec_())  # 实现程序的循环等待;事件检测的循环
