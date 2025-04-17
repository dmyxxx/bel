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

    def fetchall(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

