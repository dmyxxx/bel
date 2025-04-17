# ui/order_dialog.py
from PyQt6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout,
    QSpinBox, QPushButton, QComboBox, QDialogButtonBox, QFormLayout
)
from PyQt6.QtGui import QPixmap
from db.database import Database
import os

class OrderDialog(QDialog):
    def __init__(self, carpet, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Оформление изделия")
        self.carpet = carpet
        self.db = Database()
        self.setMinimumWidth(400)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Фото ковра
        image = QLabel()
        if os.path.exists(self.carpet['image_path']):
            pixmap = QPixmap(self.carpet['image_path']).scaled(200, 150)
            image.setPixmap(pixmap)
        else:
            image.setText("Нет изображения")
        layout.addWidget(image)

        # Ввод данных
        form = QFormLayout()
        self.width_input = QSpinBox()
        self.width_input.setRange(10, 1000)
        self.width_input.setValue(100)

        self.height_input = QSpinBox()
        self.height_input.setRange(10, 1000)
        self.height_input.setValue(100)

        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(1, 100)
        self.quantity_input.setValue(1)

        self.edging_select = QComboBox()
        self.edging_map = {}
        edgings = self.db.fetchall("SELECT * FROM edging_types")
        for e in edgings:
            self.edging_select.addItem(e["name"])
            self.edging_map[e["name"]] = e["id"]

        form.addRow("Ширина (см):", self.width_input)
        form.addRow("Длина (см):", self.height_input)
        form.addRow("Количество:", self.quantity_input)
        form.addRow("Окантовка:", self.edging_select)

        layout.addLayout(form)

        # Кнопки
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def get_data(self):
        width = self.width_input.value()
        height = self.height_input.value()
        quantity = self.quantity_input.value()
        edging_id = self.edging_map[self.edging_select.currentText()]

        # Расчет стоимости
        area_cm2 = width * height
        price = area_cm2 * float(self.carpet["price_per_cm2"]) * quantity

        return {
            "carpet_id": self.carpet["id"],
            "width": width,
            "height": height,
            "quantity": quantity,
            "edging_id": edging_id,
            "price": round(price, 2),
            "carpet_name": self.carpet["name"],
            "edging_name": self.edging_select.currentText()
        }
