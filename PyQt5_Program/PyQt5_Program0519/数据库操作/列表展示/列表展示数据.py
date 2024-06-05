import sys

from PyQt5.QtWidgets import QMainWindow

from SQLTable import Ui_SQLTable
from PyQt5.Qt import QWidget, QApplication, QTableWidgetItem
import psycopg2


def set_database(self):
    return psycopg2.connect(database='pyqt5_test_database', user='postgres', password='174496',
                            host='localhost',
                            port='5432')


class SQLTable(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SQLTable()
        self.ui.setupUi(self)
        self.ui.pushButton_clear.clicked.connect(self.clear)
        self.ui.pushButton_load.clicked.connect(self.load)
        self.show()

    def clear(self):
        pass

    def load(self):
        conn = set_database(self)
        cur = conn.cursor()
        cur.execute('select * from weapons')
        rows = cur.fetchall()
        row = cur.rowcount  # 取得记录个数，用于设置表格的行数
        vol = len(rows[0])  # 取得字段数，用于设置表格的列数
        cur.close()
        conn.close()

        self.ui.tableWidget.setRowCount(row)
        self.ui.tableWidget.setColumnCount(vol)

        for i in range(row):
            for j in range(vol):
                temp_data = rows[i][j]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                self.ui.tableWidget.setItem(i, j, data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SQLTable()
    sys.exit(app.exec_())
