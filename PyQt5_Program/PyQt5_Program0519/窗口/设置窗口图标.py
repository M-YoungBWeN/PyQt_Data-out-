import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QApplication


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        label = QLabel("设置窗口图标")
        label.setStyleSheet("font-size:20px;")
        label.setParent(self)


"""
在QtGui里有个QIcon可以解析图片路径。
更美观的标题栏需要把原本的标题栏隐藏，自己画一个标题栏。

"""
if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MyWindow()
    w.setWindowTitle("QWidget")
    w.setWindowIcon(QIcon("../icon/文件夹.png"))    # 使用了QIcon(fileName: str)的用法
    w.show()

    sys.exit(app.exec_())
