# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
# from services.settings_service import update_meal_price, get_meal_price

# class UpdateMealPrice(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Update Meal Price")
#         self.setFixedSize(300, 150)

#         layout = QVBoxLayout()

#         layout.addWidget(QLabel(f"Current Price: ₹{get_meal_price()}"))

#         layout.addWidget(QLabel("New Meal Price:"))
#         self.price_input = QLineEdit()
#         layout.addWidget(self.price_input)

#         btn_update = QPushButton("Update Price")
#         btn_update.clicked.connect(self.update_price)
#         layout.addWidget(btn_update)

#         self.setLayout(layout)

#     def update_price(self):
#         try:
#             new_price = float(self.price_input.text())
#         except ValueError:
#             QMessageBox.warning(self, "Error", "Invalid price")
#             return

#         update_meal_price(new_price)
#         QMessageBox.information(self, "Success", f"Meal price updated to ₹{new_price}")
#         self.close()


from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from services.settings_service import update_meal_price, get_meal_price


class UpdateMealPrice(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Update Meal Price")
        self.setFixedSize(420, 280)   # Increased window size

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(14)

        # Fonts
        title_font = QFont("Arial", 14, QFont.Bold)
        label_font = QFont("Arial", 11)
        input_font = QFont("Arial", 11)
        button_font = QFont("Arial", 12, QFont.Bold)

        # Title
        title = QLabel("Update Meal Price")
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(10)

        # Current price
        self.current_price_label = QLabel(f"Current Price: ₹{get_meal_price()}")
        self.current_price_label.setFont(label_font)
        self.current_price_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.current_price_label)

        layout.addSpacing(10)

        # New price label
        lbl_price = QLabel("New Meal Price")
        lbl_price.setFont(label_font)
        layout.addWidget(lbl_price)

        # Price input
        self.price_input = QLineEdit()
        self.price_input.setFont(input_font)
        self.price_input.setMinimumHeight(36)
        self.price_input.setPlaceholderText("Enter new price")
        layout.addWidget(self.price_input)

        layout.addSpacing(15)

        # Update button
        btn_update = QPushButton("Update Price")
        btn_update.setFont(button_font)
        btn_update.setMinimumHeight(42)
        btn_update.clicked.connect(self.update_price)
        layout.addWidget(btn_update)

        self.setLayout(layout)

    def update_price(self):
        try:
            new_price = float(self.price_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid price")
            return

        update_meal_price(new_price)
        QMessageBox.information(
            self,
            "Success",
            f"Meal price updated to ₹{new_price}"
        )
        self.close()
