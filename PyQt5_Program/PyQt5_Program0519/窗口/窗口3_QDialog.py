"""
对话框窗口
"""
import sys

from PyQt5.QtWidgets import QApplication, QDialog, QPushButton


class MyWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        ok_btn = QPushButton('确定',self)
        # 设置按钮位置
        ok_btn.setGeometry(50,50,100,30)


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建一个对象;sys.argv是给程序传入的参数
    # ---------------------------------------------------
    w = MyWindow()
    w.setWindowTitle("QDialog")
    w.show()
    # ---------------------------------------------------
    sys.exit(app.exec_())  # 实现程序的循环等待;事件检测的循环
