"""
QWidget:控件和窗口的父类 ，自由度高(什么都东西都没有)，没有划分菜单、工具栏、状态栏、主窗口等区域


"""


import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        label = QLabel("这是窗口")  # 创建了一个Label
        label.setStyleSheet("font-size:30px;color:blue")    # 设置label的样式
        label.setParent(self)   # 设置label的显示位置


"""
一个PyQt程序必须包含以下两个部分：
    1.创建一个对象    app = QApplication(sys.argv)  
    2.实现程序的循环等待 sys.exit(app.exec_())或app.exec_() 
    以上两个部分中间包含的部分就是创建的对象
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建一个对象;sys.argv是给程序传入的参数
    # ---------------------------------------------------
    w = MyWindow()
    w.setWindowTitle("QWidget")
    w.show()
    # ---------------------------------------------------
    sys.exit(app.exec_())  # 实现程序的循环等待;事件检测的循环
