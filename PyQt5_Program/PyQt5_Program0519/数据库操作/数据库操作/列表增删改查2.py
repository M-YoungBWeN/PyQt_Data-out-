import sys
import psycopg2
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QTabWidget, QDialog, QLabel, QFormLayout,
    QDialogButtonBox, QHBoxLayout, QLineEdit
)


class DatabaseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.connectDB()
        self.loadWeaponsData()
        self.loadVehiclesData()

    def initUI(self):
        self.setWindowTitle('数据库查看器')
        self.setGeometry(100, 100, 1000, 600)

        self.layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.weaponTab = QWidget()
        self.vehicleTab = QWidget()

        self.tabs.addTab(self.weaponTab, "武器")
        self.tabs.addTab(self.vehicleTab, "载具")

        self.initWeaponTab()
        self.initVehicleTab()

        self.setLayout(self.layout)

    def initWeaponTab(self):
        self.weaponLayout = QVBoxLayout()

        self.weaponTable = QTableWidget()
        self.weaponLayout.addWidget(self.weaponTable)

        self.weaponAddButton = QPushButton('增加')
        self.weaponAddButton.clicked.connect(self.openAddWeaponDialog)
        self.weaponLayout.addWidget(self.weaponAddButton)

        self.weaponTab.setLayout(self.weaponLayout)

    def initVehicleTab(self):
        self.vehicleLayout = QVBoxLayout()

        self.vehicleTable = QTableWidget()
        self.vehicleLayout.addWidget(self.vehicleTable)

        self.vehicleAddButton = QPushButton('增加')
        self.vehicleAddButton.clicked.connect(self.openAddVehicleDialog)
        self.vehicleLayout.addWidget(self.vehicleAddButton)

        self.vehicleTab.setLayout(self.vehicleLayout)

    def connectDB(self):
        try:
            self.conn = psycopg2.connect(
                database='pyqt5_test_database', user='postgres', password='174496',
                host='localhost',
                port='5432'
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            QMessageBox.critical(self, '数据库连接错误', str(e))

    def loadWeaponsData(self):
        self.cursor.execute("SELECT * FROM weapons")
        records = self.cursor.fetchall()
        self.weaponTable.setRowCount(len(records))
        self.weaponTable.setColumnCount(5)
        self.weaponTable.setHorizontalHeaderLabels(['ID', '武器名称', '武器类型ID', '更新', '删除'])

        for i, row in enumerate(records):
            self.weaponTable.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.weaponTable.setItem(i, 1, QTableWidgetItem(row[1]))
            self.weaponTable.setItem(i, 2, QTableWidgetItem(str(row[2])))

            updateButton = QPushButton('更新')
            updateButton.clicked.connect(lambda _, row=row: self.openUpdateWeaponDialog(row[0], row[1], row[2]))
            self.weaponTable.setCellWidget(i, 3, updateButton)

            deleteButton = QPushButton('删除')
            deleteButton.clicked.connect(lambda _, row=row: self.openDeleteWeaponDialog(row[0]))
            self.weaponTable.setCellWidget(i, 4, deleteButton)

    def loadVehiclesData(self):
        self.cursor.execute("SELECT * FROM vehicles")
        records = self.cursor.fetchall()
        self.vehicleTable.setRowCount(len(records))
        self.vehicleTable.setColumnCount(5)
        self.vehicleTable.setHorizontalHeaderLabels(['ID', '载具名称', '载具类型ID', '更新', '删除'])

        for i, row in enumerate(records):
            self.vehicleTable.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.vehicleTable.setItem(i, 1, QTableWidgetItem(row[1]))
            self.vehicleTable.setItem(i, 2, QTableWidgetItem(str(row[2])))

            updateButton = QPushButton('更新')
            updateButton.clicked.connect(lambda _, row=row: self.openUpdateVehicleDialog(row[0], row[1], row[2]))
            self.vehicleTable.setCellWidget(i, 3, updateButton)

            deleteButton = QPushButton('删除')
            deleteButton.clicked.connect(lambda _, row=row: self.openDeleteVehicleDialog(row[0]))
            self.vehicleTable.setCellWidget(i, 4, deleteButton)

    def openAddWeaponDialog(self):
        dialog = AddWeaponDialog(self)
        dialog.exec_()
        self.loadWeaponsData()

    def openDeleteWeaponDialog(self, weapon_id):
        dialog = DeleteWeaponDialog(self, weapon_id)
        dialog.exec_()
        self.loadWeaponsData()

    def openUpdateWeaponDialog(self, weapon_id, weapon_name, weapon_type_id):
        dialog = UpdateWeaponDialog(self, weapon_id, weapon_name, weapon_type_id)
        dialog.exec_()
        self.loadWeaponsData()

    def openAddVehicleDialog(self):
        dialog = AddVehicleDialog(self)
        dialog.exec_()
        self.loadVehiclesData()

    def openDeleteVehicleDialog(self, vehicle_id):
        dialog = DeleteVehicleDialog(self, vehicle_id)
        dialog.exec_()
        self.loadVehiclesData()

    def openUpdateVehicleDialog(self, vehicle_id, vehicle_name, vehicle_type_id):
        dialog = UpdateVehicleDialog(self, vehicle_id, vehicle_name, vehicle_type_id)
        dialog.exec_()
        self.loadVehiclesData()


class AddWeaponDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('增加武器')
        self.layout = QFormLayout(self)

        self.nameInput = QLineEdit(self)
        self.layout.addRow('武器名称:', self.nameInput)

        self.typeInput = QLineEdit(self)
        self.layout.addRow('武器类型ID:', self.typeInput)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def accept(self):
        name = self.nameInput.text()
        type_id = self.typeInput.text()
        if name and type_id:
            self.parent().cursor.execute("INSERT INTO weapons (weapon_name, weapon_type_id) VALUES (%s, %s)",
                                         (name, type_id))
            self.parent().conn.commit()
            super().accept()
        else:
            QMessageBox.warning(self, '输入错误', '武器名称和武器类型ID不能为空')


class DeleteWeaponDialog(QDialog):
    def __init__(self, parent=None, weapon_id=None):
        super().__init__(parent)
        self.setWindowTitle('删除武器')
        self.weapon_id = weapon_id
        self.layout = QVBoxLayout(self)

        self.label = QLabel(f"确定要删除武器ID为 {weapon_id} 的武器吗？", self)
        self.layout.addWidget(self.label)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def accept(self):
        self.parent().cursor.execute("DELETE FROM weapons WHERE weapon_id = %s", (self.weapon_id,))
        self.parent().conn.commit()
        super().accept()


class UpdateWeaponDialog(QDialog):
    def __init__(self, parent=None, weapon_id=None, weapon_name=None, weapon_type_id=None):
        super().__init__(parent)
        self.setWindowTitle('更新武器')
        self.weapon_id = weapon_id
        self.layout = QFormLayout(self)

        self.nameInput = QLineEdit(self)
        self.nameInput.setText(weapon_name)
        self.layout.addRow('武器名称:', self.nameInput)

        self.typeInput = QLineEdit(self)
        self.typeInput.setText(str(weapon_type_id))
        self.layout.addRow('武器类型ID:', self.typeInput)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def accept(self):
        new_name = self.nameInput.text()
        new_type_id = self.typeInput.text()
        if new_name and new_type_id:
            self.parent().cursor.execute(
                "UPDATE weapons SET weapon_name = %s, weapon_type_id = %s WHERE weapon_id = %s",
                (new_name, new_type_id, self.weapon_id))
            self.parent().conn.commit()
            super().accept()
        else:
            QMessageBox.warning(self, '输入错误', '武器名称和武器类型ID不能为空')


class AddVehicleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('增加载具')
        self.layout = QFormLayout(self)

        self.nameInput = QLineEdit(self)
        self.layout.addRow('载具名称:', self.nameInput)

        self.typeInput = QLineEdit(self)
        self.layout.addRow('载具类型ID:', self.typeInput)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def accept(self):
        name =self.nameInput.text()
        type_id = self.typeInput.text()
        if name and type_id:
            self.parent().cursor.execute("INSERT INTO vehicles (vehicle_name, vehicle_type_id) VALUES (%s, %s)",
                                         (name, type_id))
            self.parent().conn.commit()
            super().accept()
        else:
            QMessageBox.warning(self, '输入错误', '载具名称和载具类型ID不能为空')


class DeleteVehicleDialog(QDialog):
    def __init__(self, parent=None, vehicle_id=None):
        super().__init__(parent)
        self.setWindowTitle('删除载具')
        self.vehicle_id = vehicle_id
        self.layout = QVBoxLayout(self)

        self.label = QLabel(f"确定要删除载具ID为 {vehicle_id} 的载具吗？", self)
        self.layout.addWidget(self.label)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def accept(self):
        self.parent().cursor.execute("DELETE FROM vehicles WHERE vehicle_id = %s", (self.vehicle_id,))
        self.parent().conn.commit()
        super().accept()


class UpdateVehicleDialog(QDialog):
    def __init__(self, parent=None, vehicle_id=None, vehicle_name=None, vehicle_type_id=None):
        super().__init__(parent)
        self.setWindowTitle('更新载具')
        self.vehicle_id = vehicle_id
        self.layout = QFormLayout(self)

        self.nameInput = QLineEdit(self)
        self.nameInput.setText(vehicle_name)
        self.layout.addRow('载具名称:', self.nameInput)

        self.typeInput = QLineEdit(self)
        self.typeInput.setText(str(vehicle_type_id))
        self.layout.addRow('载具类型ID:', self.typeInput)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def accept(self):
        new_name = self.nameInput.text()
        new_type_id = self.typeInput.text()
        if new_name and new_type_id:
            self.parent().cursor.execute(
                "UPDATE vehicles SET vehicle_name = %s, vehicle_type_id = %s WHERE vehicle_id = %s",
                (new_name, new_type_id, self.vehicle_id))
            self.parent().conn.commit()
            super().accept()
        else:
            QMessageBox.warning(self, '输入错误', '载具名称和载具类型ID不能为空')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DatabaseApp()
    ex.show()
    sys.exit(app.exec_())

