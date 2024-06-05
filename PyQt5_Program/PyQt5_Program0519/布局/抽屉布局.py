"""
QStackedLayout
抽屉布局：提供了多页面切换的布局，一次只能看到一个界面

QWidget包括了一个抽屉布局器，抽屉布局器包括了两个QWidget（win1、win2）
"""
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedLayout, QLabel


class MyWindow(QWidget):
    # 一定要调用父类的__init__方法，因为它里面有很多对ui空间的初始化操作
    def __init__(self):
        super().__init__()
        self.create_stacked_layout()
        self.init_ui()

    def create_stacked_layout(self):
        # 创建一个抽屉布局器
        # 加self是为了让stacked_layout可以在整个类里用，而不是create_stacked_layout的局部变量
        self.stacked_layout = QStackedLayout()
        win1 = MyWindow1()
        win2 = MyWindow2()
        # 把窗口加到布局器里
        self.stacked_layout.addWidget(win1)
        self.stacked_layout.addWidget(win2)

    def init_ui(self):
        self.resize(300, 300)
        self.setWindowTitle('抽屉布局')

        # 全局的布局器使用的是竖直盒子布局器
        container = QVBoxLayout()
        self.setLayout(container)

        # =======创建全局布局器里要添加的窗口或容器=========
        # 创建了一个要显示内容的widget
        widget = QWidget()
        # 采用抽屉布局
        # 这个抽屉布局里还有win1、win2，相当于widget的两个子窗口
        widget.setLayout(self.stacked_layout)
        # 设置widget样式
        widget.setStyleSheet('background-color:grey;')

        # 创建俩按钮
        btn1 = QPushButton('按钮1')
        btn2 = QPushButton('按钮2')
        # 绑定信号与槽函数
        btn1.clicked.connect(self.btn_press1_clicked)
        btn2.clicked.connect(self.btn_press2_clicked)

        # =======把创建的窗口或容器添加进全局布局器=========
        container.addWidget(widget)
        container.addWidget(btn1)
        container.addWidget(btn2)

    # 点击按钮后触发的槽函数
    def btn_press1_clicked(self):
        # 设置抽屉的当前索引值
        self.stacked_layout.setCurrentIndex(0)

    def btn_press2_clicked(self):
        self.stacked_layout.setCurrentIndex(1)


class MyWindow1(QWidget):
    def __init__(self):
        super().__init__()
        QLabel('111111111', self)
        self.setStyleSheet('background-color:blue')


class MyWindow2(QWidget):
    def __init__(self):
        super().__init__()
        QLabel('222222222', self)
        self.setStyleSheet('background-color:yellow')


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建一个对象;sys.argv是给程序传入的参数
    # ---------------------------------------------------
    w = MyWindow()
    w.show()
    # ---------------------------------------------------
    sys.exit(app.exec_())  # 实现程序的循环等待;事件检测的循环
