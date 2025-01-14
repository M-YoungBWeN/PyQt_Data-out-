#导入包
import sys
import pymysql
from functools import partial
from PyQt5.Qt import QWidget
from PyQt5 import QtGui,QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import (QFrame,QApplication,QDialog, QDialogButtonBox,
        QMessageBox,QVBoxLayout, QLineEdit,QTableWidgetItem,QTableWidget,QHBoxLayout)
#建立界面类
PASSWORD='数据库登录密码'
DATABASE='数据库名称'
TABLE_NOW='数据库表名称'
class creat_view(QDialog):
    def __init__(self,parent = None):
        super(creat_view,self).__init__(parent)
        #设置界面大小、名称、背景
        self.resize(600,900)
        self.setWindowTitle('零件详细信息')#窗口名称
        self.setStyleSheet("background-image:url(FC8616E8B9FBCC39ECBE29A921928C74.jpg)")#背景图片路径（可以是绝对路径，也可以是相对路径）
        #窗体属性
        self.setWindowFlags(Qt.Widget)
        #连接数据库
        db = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password=PASSWORD,
            database=DATABASE,
            charset='utf8'
        )
        #获取游标、数据
        cur = db.cursor()
        cur.execute("SELECT * FROM (%s)"%TABLE_NOW)
        data = cur.fetchall()
        #数据列名
        col_lst = [tup[0] for tup in cur.description]
        #数据的大小
        row = len(data)
        vol = len(data[0])
        #插入表格
        self.MyTable = QTableWidget(row,vol)
        font = QtGui.QFont('微软雅黑',20)
        #self.setForeground(QBrush(QColor(190, 88, 0))
        #设置字体、表头
        self.MyTable.horizontalHeader().setFont(font)
        self.MyTable.setHorizontalHeaderLabels(col_lst)
        #设置竖直方向表头不可见
        self.MyTable.verticalHeader().setVisible(False)
        self.MyTable.setFrameShape(QFrame.NoFrame)
        #设置表格颜色
        self.MyTable.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        #构建表格插入数据
        for i in range(row):
            for j in range(vol):
                temp_data = data[i][j]  # 临时记录，不能直接插入表格
                data1 = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                self.MyTable.setItem(i, j, data1)
        #编辑按钮
        self.qle = QLineEdit()
        buttonBox = QDialogButtonBox()
        #增删查四个按钮
        addButton = buttonBox.addButton("&ADD",QDialogButtonBox.ActionRole)
        okButton = buttonBox.addButton("&OK",QDialogButtonBox.ActionRole)
        deleteButton = buttonBox.addButton("&DELETE",QDialogButtonBox.ActionRole)
        inquireButton = buttonBox.addButton("&QUERY",QDialogButtonBox.ActionRole)

        #设置按钮内字体样式
        addButton.setFont(font)
        okButton.setFont(font)
        deleteButton.setFont(font)
        inquireButton.setFont(font)
        #垂直布局
        layout = QVBoxLayout()
        layout.addWidget(self.qle)
        layout.addWidget(buttonBox)
        layout.addWidget(self.MyTable)
        self.setLayout(layout)

        addButton.clicked.connect(partial(self.add_data,cur,db))#插入实现
        okButton.clicked.connect(partial(self.up_data, cur, db,col_lst))#插入实现
        deleteButton.clicked.connect(partial(self.del_data,cur,db))#删除实现
        inquireButton.clicked.connect(partial(self.inq_data,cur,db,col_lst))#查询实现

    #添加空表格
    def add_data(self,cur,db):
        #获取行数
        row = self.MyTable.rowCount()
        #在末尾插入一空行
        self.MyTable.insertRow(row)
    #插入数据
    def up_data(self,cur,db,col_lst):
        row_1 = self.MyTable.rowCount()
        value_lst = []
        for i in range(len(col_lst)):
            if(len(self.MyTable.item(row_1-1,i).text())==0):
                value_lst.append(None)
            else:
                value_lst.append(self.MyTable.item(row_1-1,i).text())

        tup_va_lst = []
        for cl,va in zip(col_lst,value_lst):
            tup_va_lst.append((cl,va))
            #print(cl,va)
        #插入语句
        sql='INSERT INTO '+TABLE_NOW+'('+','.join(col_lst)+')'+' value'+'('+','.join('"'+item+'"' for item in value_lst)+');'
        #sql是将插入命令利用python字符串进行格式化处理，可适用于任意一个表的数据插入
        cur.execute(sql)
        db.commit()#确认操作，在python与mysql数据库交互的过程中，修改数据或者添加数据都必须进行操作确认
    #删除
    def del_data(self,cur,db):
        #是否删除的对话框
        reply = QMessageBox.question(self, 'Message', 'Are you sure to delete it ?', QMessageBox.Yes | QMessageBox.No,
                             QMessageBox.No)
        if reply ==  QMessageBox.Yes:
            #当前行
            row_2 = self.MyTable.currentRow()
            del_d = self.MyTable.item(row_2, 0).text()
            #在数据库删除数据
            sql='DELETE FROM '+TABLE_NOW+' WHERE SNO = '+'"'+del_d+'"'
            cur.execute(sql)
            db.commit()#确认操作
            #删除表格
            self.MyTable.removeRow(row_2)
    #查询
    def inq_data(self,cur,db,col_lst):
        txt = self.qle.text()
        #查询
        if len(txt) != 0:
            sql='SELECT * FROM '+TABLE_NOW+ ' where '+' or '.join(item+' LIKE '+'"'+txt+'"' for item in col_lst)
            #同样格式化查询命令，进行模糊查询
            cur.execute(sql)
            data_x = cur.fetchall()
            self.MyTable.clearContents()
            row_4 = len(data_x)
            vol_1 = len(cur.description)
            print(row_4,vol_1)
            #查询到的更新带表格当中
            for i_x in range(row_4):
                for j_y in range(vol_1):
                    temp_data_1 = data_x[i_x][j_y]  # 临时记录，不能直接插入表格
                    data_1 = QTableWidgetItem(str(temp_data_1))  # 转换后可插入表格
                    self.MyTable.setItem(i_x, j_y, data_1)
        else: #空输入返回原先数据表格
            self.MyTable.clearContents()
            sql = 'SELECT * FROM ' + TABLE_NOW+';'
            cur.execute(sql)
            data_y = cur.fetchall()
            row_5 = len(data_y)
            vol_1 = len(cur.description)
            for i_x_1 in range(row_5):
                for j_y_1 in range(vol_1):
                    temp_data_2 = data_y[i_x_1][j_y_1]  # 临时记录，不能直接插入表格
                    data_2 = QTableWidgetItem(str(temp_data_2))  # 转换后可插入表格
                    self.MyTable.setItem(i_x_1, j_y_1, data_2)


if __name__ == "__main__":
    #显示
    app = QApplication(sys.argv)

    c = creat_view()
    c.show()

    sys.exit(app.exec_())

