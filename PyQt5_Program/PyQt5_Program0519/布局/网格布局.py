"""
QGridLayout


"""
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QGridLayout, QPushButton


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(400, 250)
        self.setWindowTitle('计算器-网格布局')

        # 创建一个整体的布局器
        layout = QVBoxLayout()
        # 让当前窗口使用这个布局器
        self.setLayout(layout)

        # 输入框
        edit = QLineEdit()
        edit.setPlaceholderText('请输入内容')
        layout.addWidget(edit)

        # 网格布局器
        grid = QGridLayout()
        # 字典 key:value
        data = {
            0: ['7', '8', '9', '+', '('],
            1: ['4', '5', '6', '-', ')'],
            2: ['1', '2', '3', '*', '<-'],
            3: ['0', '.', '=', '/', 'C']
        }
        # 字典会取出随机的key，key的值可以直接作为行号
        for line_number, line_data in data.items():
            # 字典的value值为列表可以使用enumerate函数遍历出下标作为列号，值作为行号
            for col_number, number in enumerate(line_data):
                btn = QPushButton(number)
                # 网格布局器会根据行列添加窗口（或布局器）
                grid.addWidget(btn, line_number, col_number)
        layout.addLayout(grid)


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建一个对象;sys.argv是给程序传入的参数
    # ---------------------------------------------------
    w = MyWindow()
    w.show()
    # ---------------------------------------------------
    sys.exit(app.exec_())  # 实现程序的循环等待;事件检测的循环
