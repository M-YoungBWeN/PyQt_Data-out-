"""
        加载ui文件
"""
from PyQt6.QtGui import QValidator, QIntValidator
from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QTextEdit
from PyQt6 import uic, QtGui
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = uic.loadUi("./0404test_坤坤窗口.ui")

    mytextEdit: QTextEdit = ui.textEdit
    mytextEdit_2: QTextEdit = ui.textEdit_2
    mytextEdit.setTextColor(QtGui.QColor(255, 0, 0))
    # 设置第一个textEdit的字体颜色
    mytextEdit.setTextBackgroundColor(QtGui.QColor(255, 255, 0))
    # 设置第一个textEdit的字体背景颜色
    mytextEdit.setPlainText("IKUN")
    # 设置纯文本
    mytextEdit_2.setHtml("<a href='www.baidu.com'>baidu</a>")
    # 设置HTML
    print(mytextEdit.toPlainText())
    # 获取纯文本
    print(mytextEdit_2.toHtml())
    # 获取HTML
    # mytextEdit.clear()
    # 清空内容

    # mylineEdit: QLineEdit = ui.lineEdit
    # mylineEdit_2: QLineEdit = ui.lineEdit_2
    # print(QValidator.__subclasses__())
    # 查看QValidator的子类
    # [<cla   ss 'PyQt6.QtGui.QDoubleValidator'>,
    # <class 'PyQt6.QtGui.QIntValidator'>,
    # <class 'PyQt6.QtGui.QRegularExpressionValidator'>]
    # mylineEdit.setValidator(QIntValidator())
    # 只允许输入int类型

    # mylineEdit_2.setFocus()

    # print(mylineEdit_2.text())
    # mylineEdit_2.clear()

    ui.show()
    sys.exit(app.exec())
