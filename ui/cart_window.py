# ui/cart_window.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt

class CartWindow(QWidget):
    def __init__(self, cart, on_checkout):
        super().__init__()
        self.setWindowTitle("Корзина")
        self.cart = cart
        self.on_checkout = on_checkout
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Ковер", "Окантовка", "Ширина", "Длина", "Кол-во", "Стоимость"])
        self.table.setRowCount(len(self.cart))

        total_sum = 0
        for row, item in enumerate(self.cart):
            self.table.setItem(row, 0, QTableWidgetItem(item["carpet_name"]))
            self.table.setItem(row, 1, QTableWidgetItem(item["edging_name"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(item["width"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(item["height"])))
            self.table.setItem(row, 4, QTableWidgetItem(str(item["quantity"])))
            self.table.setItem(row, 5, QTableWidgetItem(f"{item['price']} ₽"))
            total_sum += item["price"]

        layout.addWidget(self.table)

        # Итого
        self.total_label = QLabel(f"Общая сумма: {round(total_sum, 2)} ₽")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.total_label)

        # Кнопка "Оформить заказ"
        btn_layout = QHBoxLayout()
        checkout_btn = QPushButton("Оформить заказ")
        checkout_btn.clicked.connect(self.checkout)

        btn_layout.addStretch()
        btn_layout.addWidget(checkout_btn)
        layout.addLayout(btn_layout)

    def checkout(self):
        if len(self.cart) == 0:
            QMessageBox.warning(self, "Внимание", "Корзина пуста")
            return
        self.on_checkout(self.cart)
        self.close()
