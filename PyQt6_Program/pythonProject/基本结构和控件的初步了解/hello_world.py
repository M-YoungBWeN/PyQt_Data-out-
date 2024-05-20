"""
    第一个PyQt程序
"""
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
import sys

# QApplication--管理功能，如组件的初始化和结束
# QWidget--控件， 所有GUI界面的基类
# sys--python自带的解释器交互接口，处理运行环境时的问题
# QLabel--QWidget的孙类

app = QApplication(sys.argv)
# print(sys.argv)
# print(app.arguments())
# 创建一个应用
# 参数sys.argv传入的是py文件的参数
# 形参可以让应用程序获取到
# 可以添加脚本形参 如['E:\\1_Code\\PyQt\\PyQt6_Program\\pythonProject\\基本结构和控件的初步了解\\hello_world.py', '11', '22', '33']
# 复杂项目时可以用app.arguments()获取脚本形参

window = QWidget()

window.setWindowTitle("坤坤")
# 更改窗口标题
window.resize(400, 300)
# 更改窗口大小
window.move(600, 200)
# 更改窗口弹出位置

window.show()
# 创建一个QWidget，并用show()显示出来
# 窗口一闪而过

label = QLabel()
label.setText("鸡")
label.setParent(window)
# 认定window为父
label.move(100, 50)
# 位置
label.resize(150, 50)
# 大小
label.setStyleSheet("background-color:yellow;padding:10px")
# 样式
label.show()

# app.exec()
# 开始执行程序，并且进入消息循环等待
sys.exit(app.exec())
# 退出时会返回报错码，建议这样写
