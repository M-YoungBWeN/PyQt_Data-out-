import sys
from typing import Optional

from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QDesktopWidget


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        label = QLabel("调整窗口大小和位置")
        label.setStyleSheet("font-size:20px;")
        label.setParent(self)


"""
QWidget的内置函数：
    resize可以调整窗口大小
    move可以调整窗口的位置，根据窗口的左上角定位
如何获取屏幕中心点：
    QWidgets有QDesktopWidget，可以获取屏幕信息
如何查找没见过的函数:
    现在pyqt文档查，查不到再去qt文档
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWindow()
    w.setWindowTitle("QWidget")

    w.resize(400, 100)  # 调整窗口的大小
    w.move(10, 90)

    center_pointer = QDesktopWidget().availableGeometry().center()  # 获取屏幕中央位置,返回的是PyQt5.QtCore.QPoint(959, 514)
    x = center_pointer.x()
    y = center_pointer.y()
    # w.move(x, y)
    print(w.frameGeometry())  # frameGeometry 获取窗口的位置和大小，返回的是PyQt5.QtCore.QRect(0, 0, 1000, 600)
    print(w.frameGeometry().getRect(),
          type(w.frameGeometry().getRect()))  # 直接获取窗口的位置和大小，返回的是元组(Tuple),(10, 90, 1000, 600)
    old_x, old_y, width, height = w.frameGeometry().getRect()  # 返回的是一个元组，要用四个变量接住元组的数据
    print(old_x, old_y)
    w.move(x - int(width / 2), y - int(height / 2))

    # w.move(0, 0)  # 调整窗口位置
    w.show()
    sys.exit(app.exec_())
