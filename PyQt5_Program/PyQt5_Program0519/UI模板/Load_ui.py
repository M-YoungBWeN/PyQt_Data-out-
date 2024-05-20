from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
import sys

if __name__ == '__main__':
    # 参数sys.argv传入的是py文件的参数
    app = QApplication(sys.argv)
    ui = uic.loadUi("E:/1_Code/PyQt_Data/PyQt5_Program/PyQt5_Program0519/0519案例.ui")

    ui.show()
    sys.exit(app.exec_())
