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

        order_id = self.orders_table.item(selected_row, 0).text()
        new_status = self.status_combo.currentText()

        # Проверка на валидность изменения статуса
        current_status = self.orders_table.item(selected_row, 3).text()
        if current_status == "Новый" and new_status == "Готов":
            QMessageBox.warning(self, "Ошибка", "Невозможно сразу выбрать статус 'Готов'. Выберите сначала 'В обработке'.")
            return

        if current_status == "В обработке" and new_status == "Получен":
            QMessageBox.warning(self, "Ошибка", "Невозможно сразу выбрать статус 'Получен'. Выберите сначала 'Готов'.")
            return

        # Обновление статуса
        self.db.update_order_status(order_id, new_status)
        self.update_orders_table()
        QMessageBox.information(self, "Успех", "Статус заказа изменен.")
