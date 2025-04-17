# main.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton, QMessageBox
from ui.customer_ui import CustomerUI
from ui.manager_ui import ManagerUI
from db.database import Database


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Магазин ковров 'Шелкопряд'")
        self.setGeometry(100, 100, 1000, 600)

        self.db = Database()
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.init_ui()

    def init_ui(self):
        print("Initializing UI...")
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)

        self.customer_button = QPushButton("Интерфейс заказчика", self)
        self.manager_button = QPushButton("Интерфейс менеджера", self)

        self.customer_button.clicked.connect(self.show_customer_ui)
        self.manager_button.clicked.connect(self.show_manager_ui)

        main_layout.addWidget(self.customer_button)
        main_layout.addWidget(self.manager_button)

        self.stacked_widget.addWidget(main_widget)

    def show_customer_ui(self):
        print("Loading customer UI...")
        try:
            customer_ui = CustomerUI(self)
            self.stacked_widget.addWidget(customer_ui)
            self.stacked_widget.setCurrentWidget(customer_ui)
        except Exception as e:
            print(f"Error loading customer UI: {e}")

    def show_manager_ui(self):
        print("Loading manager UI...")
        try:
            manager_ui = ManagerUI(self)
            self.stacked_widget.addWidget(manager_ui)
            self.stacked_widget.setCurrentWidget(manager_ui)
        except Exception as e:
            print(f"Error loading manager UI: {e}")


def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()
