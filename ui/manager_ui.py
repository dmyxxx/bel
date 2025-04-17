# ui/manager_ui.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QComboBox, QMessageBox
from db.database import Database


class ManagerUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Менеджер")
        self.db = Database()
        self.setMinimumWidth(800)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Таблица с заказами
        self.orders_table = QTableWidget(self)
        self.orders_table.setColumnCount(5)
        self.orders_table.setHorizontalHeaderLabels(["ID", "Пользователь", "Сумма", "Статус", "Дата"])

        self.update_orders_table()

        # Выпадающий список для изменения статуса
        self.status_combo = QComboBox(self)
        self.status_combo.addItems(["Новый", "В обработке", "Готов", "Получен"])
        layout.addWidget(self.status_combo)

        # Кнопка для обновления статуса
        self.change_status_button = QPushButton("Изменить статус", self)
        self.change_status_button.clicked.connect(self.change_order_status)
        layout.addWidget(self.change_status_button)

        layout.addWidget(self.orders_table)

    def update_orders_table(self):
        """Обновление таблицы заказов"""
        orders = self.db.fetchall("SELECT * FROM orders")

        self.orders_table.setRowCount(len(orders))
        for row, order in enumerate(orders):
            self.orders_table.setItem(row, 0, QTableWidgetItem(str(order["id"])))
            self.orders_table.setItem(row, 1, QTableWidgetItem(order["user_id"]))
            self.orders_table.setItem(row, 2, QTableWidgetItem(str(order["total_price"])))
            self.orders_table.setItem(row, 3, QTableWidgetItem(order["status"]))
            self.orders_table.setItem(row, 4, QTableWidgetItem(str(order["created_at"])))

    def change_order_status(self):
        """Изменение статуса заказа"""
        selected_row = self.orders_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ для изменения статуса.")
            return


