# ui/checkout_dialog.py
from PyQt6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QLineEdit, QFormLayout,
    QDialogButtonBox, QSpinBox, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import hashlib
import random
import os
import pandas as pd
from db.database import Database
from openpyxl import Workbook

class CheckoutDialog(QDialog):
    def __init__(self, cart_items, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Оформление заказа")
        self.cart_items = cart_items
        self.db = Database()
        self.setMinimumWidth(400)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Почта и пароль
        form = QFormLayout()

        self.email_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_confirm_input = QLineEdit(self)
        self.password_confirm_input.setEchoMode(QLineEdit.EchoMode.Password)

        form.addRow("Почта:", self.email_input)
        form.addRow("Пароль:", self.password_input)
        form.addRow("Подтвердите пароль:", self.password_confirm_input)

        layout.addLayout(form)

        # Кнопки
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.checkout)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def checkout(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        password_confirm = self.password_confirm_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        if password != password_confirm:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают.")
            return

        # Проверка пользователя в БД
        user = self.db.fetchone("SELECT * FROM users WHERE email = %s", (email,))
        if user:
            if not self.check_password(password, user["password"]):
                QMessageBox.warning(self, "Ошибка", "Неверный пароль.")
                return
            user_id = user["id"]
        else:
            # Новый пользователь
            hashed_password = self.hash_password(password)
            user_id = self.register_user(email, hashed_password)

        # Сохраняем заказ
        order_id = self.save_order(user_id)

        # Применение скидки
        total_price = self.calculate_discount(user_id)

        # Генерация Excel-чека
        self.generate_receipt(order_id, total_price)

        QMessageBox.information(self, "Успех", f"Ваш заказ оформлен. Чек отправлен на почту.\nСумма со скидкой: {total_price} ₽")
        self.accept()

    def check_password(self, input_password, stored_password):
        return self.hash_password(input_password) == stored_password

    def hash_password(self, password):
        salt = os.urandom(32)  # Генерируем случайную соль
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

    def register_user(self, email, hashed_password):
        salt = os.urandom(32)
        self.db.execute(
            "INSERT INTO users (email, password, salt) VALUES (%s, %s, %s)",
            (email, hashed_password, salt)
        )
        return self.db.last_insert_id()

    def save_order(self, user_id):
        total_price = sum(item["price"] for item in self.cart_items)
        order_id = self.db.execute(
            "INSERT INTO orders (user_id, total_price, status) VALUES (%s, %s, %s)",
            (user_id, total_price, "new")
        )

        for item in self.cart_items:
            self.db.execute(
                "INSERT INTO order_items (order_id, carpet_id, width, height, quantity, edging_id, price) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (order_id, item["carpet_id"], item["width"], item["height"], item["quantity"], item["edging_id"], item["price"])
            )

        return order_id

    def calculate_discount(self, user_id):
        # Получаем все заказы пользователя
        orders = self.db.fetchall("SELECT * FROM orders WHERE user_id = %s", (user_id,))
        total_spent = sum(order["total_price"] for order in orders)

        # Применение скидки
        discount = 0
        if total_spent > 500000:
            discount = 0.15
        elif total_spent > 300000:
            discount = 0.10
        elif total_spent > 100000:
            discount = 0.05

        total_price = sum(item["price"] for item in self.cart_items)
        discounted_price = total_price * (1 - discount)

        return discounted_price

    def generate_receipt(self, order_id, total_price):
        # Получаем заказ
        order = self.db.fetchone("SELECT * FROM orders WHERE id = %s", (order_id,))
        order_items = self.db.fetchall("SELECT * FROM order_items WHERE order_id = %s", (order_id,))

        # Создаем Excel файл
        wb = Workbook()
        ws = wb.active
        ws.title = "Чек"

        # Заполняем данные
        ws.append(["Номер заказа", "Дата", "Ковер", "Ширина", "Длина", "Количество", "Окантовка", "Стоимость"])

        for item in order_items:
            carpet = self.db.fetchone("SELECT * FROM carpets WHERE id = %s", (item["carpet_id"],))
            edging = self.db.fetchone("SELECT * FROM edging_types WHERE id = %s", (item["edging_id"],))
            ws.append([
                order["id"], order["created_at"], carpet["name"], item["width"], item["height"],
                item["quantity"], edging["name"], item["price"]
            ])

        # Записываем итоговую сумму с учетом скидки
        ws.append(["", "", "", "", "", "Итого со скидкой", total_price])

        # Сохраняем файл
        file_name = f"receipt_order_{order_id}.xlsx"
        wb.save(file_name)

        # Пример отправки файла по почте можно реализовать здесь
        print(f"Чек сохранен: {file_name}")
