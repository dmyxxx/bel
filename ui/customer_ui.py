# ui/customer_ui.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractItemView

# Импортируем класс Database
from db.database import Database

class CustomerUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database()  # Создаем объект базы данных
        self.setWindowTitle("Интерфейс заказчика")
        self.setMinimumWidth(800)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.table_widget = QTableWidget(self)
        self.table_widget.setRowCount(5)  # примерное количество строк
        self.table_widget.setColumnCount(3)  # количество столбцов

        # Устанавливаем заголовки
        self.table_widget.setHorizontalHeaderLabels(["Модель", "Цена за м²", "Страна"])

        # Добавляем данные (пример)
        for row in range(5):
            self.table_widget.setItem(row, 0, QTableWidgetItem(f"Ковер {row + 1}"))
            self.table_widget.setItem(row, 1, QTableWidgetItem(f"1000"))
            self.table_widget.setItem(row, 2, QTableWidgetItem(f"Россия"))

        # Отключаем редактирование ячеек
        self.table_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        layout.addWidget(self.table_widget)

        self.add_to_cart_button = QPushButton("Добавить в корзину", self)
        layout.addWidget(self.add_to_cart_button)

        self.show()
