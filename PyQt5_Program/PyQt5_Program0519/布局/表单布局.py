"""
QFormLayout

"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QFormLayout


class DemoFormLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗口标题
        self.setWindowTitle('实战PyQt5: QFormLayout Demo!')
        # 设置窗口大小
        self.resize(400, 160)

        # 表单布局
        form_layout = QFormLayout(self)
        form_layout.setSpacing(10)

        le_ip_addr = QLineEdit(self)
        le_ip_addr.setInputMask('000.000.000.000;_')
        le_subnet_mask = QLineEdit(self)
        le_subnet_mask.setInputMask('000.000.000.000;_')
        le_gate = QLineEdit(self)
        le_gate.setInputMask('000.000.000.000;_')
        le_mac_addr = QLineEdit(self)
        le_mac_addr.setInputMask('HH:HH:HH:HH:HH:HH;_')

        form_layout.addRow(QLabel('IP 地址:', self), le_ip_addr)
        form_layout.addRow(QLabel('子网掩码:', self), le_subnet_mask)
        form_layout.addRow(QLabel('默认网关:', self), le_gate)
        form_layout.addRow(QLabel('MAC 地址:', self), le_mac_addr)

        self.setLayout(form_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DemoFormLayout()
    window.show()
    sys.exit(app.exec())
