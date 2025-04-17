# db/database.py
import hashlib
import mysql.connector
from PyQt6.QtWidgets import QMessageBox

class Database:
    def __init__(self):
        # Подключение к базе данных
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            database="new"  # Укажите вашу БД
        )
        self.cursor = self.conn.cursor(dictionary=True)

<<<<<<< HEAD
    def fetchone(self, query, params=()):
        """Выполнить SELECT запрос и вернуть одну запись"""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetchall(self, query, params=()):
        """Выполнить SELECT запрос и вернуть все записи"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def execute(self, query, params=()):
        """Выполнить запрос (INSERT, UPDATE, DELETE)"""
        self.cursor.execute(query, params)
        self.conn.commit()

    def hash_password(self, password):
        """Хэширование пароля"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def check_user_exists(self, email):
        """Проверка, зарегистрирован ли пользователь"""
        query = "SELECT * FROM users WHERE email = %s"
        return self.fetchone(query, (email,)) is not None

    def add_user(self, email, password):
        """Добавление нового пользователя"""
        hashed_password = self.hash_password(password)
        query = "INSERT INTO users (email, password) VALUES (%s, %s)"
        self.execute(query, (email, hashed_password))

    def add_order(self, user_id, total_price, status="Новый"):
        """Добавление нового заказа"""
        query = """
            INSERT INTO orders (user_id, total_price, status, created_at) 
            VALUES (%s, %s, %s, NOW())
        """
        self.execute(query, (user_id, total_price, status))

    def update_order_status(self, order_id, status):
        """Обновление статуса заказа"""
        query = "UPDATE orders SET status = %s WHERE id = %s"
        self.execute(query, (status, order_id))

    def get_user_orders(self, user_id):
        """Получить заказы пользователя"""
        query = "SELECT * FROM orders WHERE user_id = %s"
        return self.fetchall(query, (user_id,))

    def get_discount(self, user_id):
        """Рассчитать скидку для пользователя"""
        orders = self.get_user_orders(user_id)
        total_spent = sum(order['total_price'] for order in orders)

        if total_spent > 500000:
            return 0.15
        elif total_spent > 300000:
            return 0.10
        elif total_spent > 100000:
            return 0.05
        return 0
=======
    def fetchall(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()
>>>>>>> da5dab4 (final)
