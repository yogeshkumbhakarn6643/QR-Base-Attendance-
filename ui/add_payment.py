from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from db.database import get_db
from services.wallet_service import add_payment, get_wallet_balance


class AddPayment(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Payment")
        self.setFixedSize(420, 360)   # Better window size

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(14)

        # Fonts
        title_font = QFont("Arial", 14, QFont.Bold)
        label_font = QFont("Arial", 11)
        input_font = QFont("Arial", 11)
        button_font = QFont("Arial", 12, QFont.Bold)

        # Title
        title = QLabel("Add Wallet Payment")
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        main_layout.addSpacing(10)

        # Search User
        lbl_search = QLabel("Search User")
        lbl_search.setFont(label_font)
        main_layout.addWidget(lbl_search)

        self.search_box = QLineEdit()
        self.search_box.setFont(input_font)
        self.search_box.setMinimumHeight(36)
        self.search_box.setPlaceholderText("Type user name...")
        self.search_box.textChanged.connect(self.filter_users)
        main_layout.addWidget(self.search_box)

        # User Dropdown
        lbl_user = QLabel("Select User")
        lbl_user.setFont(label_font)
        main_layout.addWidget(lbl_user)

        self.user_dropdown = QComboBox()
        self.user_dropdown.setFont(input_font)
        self.user_dropdown.setMinimumHeight(36)
        main_layout.addWidget(self.user_dropdown)

        # Amount
        lbl_amount = QLabel("Amount (₹)")
        lbl_amount.setFont(label_font)
        main_layout.addWidget(lbl_amount)

        self.amount_input = QLineEdit()
        self.amount_input.setFont(input_font)
        self.amount_input.setMinimumHeight(36)
        self.amount_input.setPlaceholderText("Enter amount")
        main_layout.addWidget(self.amount_input)

        main_layout.addSpacing(15)

        # Button
        btn_add = QPushButton("Add Payment")
        btn_add.setFont(button_font)
        btn_add.setMinimumHeight(42)
        btn_add.clicked.connect(self.add_payment_clicked)
        main_layout.addWidget(btn_add)

        self.setLayout(main_layout)

        # Load users
        self.all_users = []
        self.load_users()

    def load_users(self):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM users ORDER BY name")
        self.all_users = cur.fetchall()
        conn.close()
        self.populate_dropdown(self.all_users)

    def populate_dropdown(self, users):
        self.user_dropdown.blockSignals(True)
        self.user_dropdown.clear()
        self.user_dropdown.addItem("Select User", None)
        for user_id, name in users:
            self.user_dropdown.addItem(name, user_id)
        self.user_dropdown.blockSignals(False)

    def filter_users(self):
        text = self.search_box.text().lower()
        filtered = [(uid, name) for uid, name in self.all_users if text in name.lower()]
        self.populate_dropdown(filtered)

    def add_payment_clicked(self):
        user_id = self.user_dropdown.currentData()
        if not user_id:
            QMessageBox.warning(self, "Error", "Please select a user")
            return

        try:
            amount = float(self.amount_input.text())
            if amount <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Enter a valid positive amount")
            return

        add_payment(user_id, amount)
        balance = get_wallet_balance(user_id)

        QMessageBox.information(
            self,
            "Success",
            f"Added ₹{amount} to {self.user_dropdown.currentText()}\nNew Balance: ₹{balance}"
        )

        self.amount_input.clear()
        self.search_box.clear()
