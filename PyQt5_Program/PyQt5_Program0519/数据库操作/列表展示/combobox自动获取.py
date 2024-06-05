import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox
import psycopg2

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weapon and Vehicle Types")

        # Create the main layout
        layout = QVBoxLayout()

        # Create a QWidget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect to the PostgreSQL database
        try:
            conn = psycopg2.connect(
                database='pyqt5_test_database', user='postgres', password='174496',
                host='localhost',
                port='5432'
            )
            cursor = conn.cursor()

            # Retrieve weapon and vehicle types from the database
            cursor.execute("SELECT type_name FROM weapon_types UNION SELECT type_name FROM vehicle_types")
            types = [row[0] for row in cursor.fetchall()]

            # Close the cursor and connection
            cursor.close()
            conn.close()
            print(types)
            # Add types to the QComboBox
            type_combobox = QComboBox()
            type_combobox.addItems(types)
            layout.addWidget(type_combobox)

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 400, 200)
    window.show()
    sys.exit(app.exec_())
