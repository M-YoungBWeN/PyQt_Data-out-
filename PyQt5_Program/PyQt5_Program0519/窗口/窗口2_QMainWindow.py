"""
QMainWindow 是 QWidget 的子类，包含菜单栏，工具栏,状态栏,标题栏等,中间部分则为主窗口区域

"""

import sys
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow


class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        label = QLabel("这是窗口")  # 创建了一个Label
        label.setStyleSheet("font-size:30px;color:blue")
        label.setParent(self)
        # QMainWidget有菜单栏状态栏，要把内容放到中间，所以可以用setCentralWidget
        self.setCentralWidget(label)

        # 父类中的menuBar,对菜单栏进行操作
        menu = self.menuBar()

        file_menu = menu.addMenu('文件')
        file_menu.addAction('打开')
        file_menu.addAction('新建')
        file_menu.addAction('保存')

        edit_menu = menu.addMenu('编辑')
        edit_menu.addAction('复制')
        edit_menu.addAction('粘贴')
        edit_menu.addAction('剪切')


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建一个对象;sys.argv是给程序传入的参数
    # ---------------------------------------------------
    w = MyWindow()
    w.setWindowTitle("QMainWidget")
    w.resize(400, 300)
    w.show()
    # ---------------------------------------------------
    sys.exit(app.exec_())  # 实现程序的循环等待;事件检测的循环
