# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTextEdit, QLineEdit
# from db.database import get_db

# class PaymentHistory(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Payment History")
#         self.setFixedSize(400, 450)

#         layout = QVBoxLayout()

#         # Search box
#         self.search_box = QLineEdit()
#         self.search_box.setPlaceholderText("Search user by name...")
#         self.search_box.textChanged.connect(self.filter_users)
#         layout.addWidget(self.search_box)

#         # Dropdown to select user
#         self.user_dropdown = QComboBox()
#         self.user_dropdown.addItem("Select User", None)
#         self.user_dropdown.currentIndexChanged.connect(self.show_history)
#         layout.addWidget(self.user_dropdown)

#         # Text area to display payment history
#         self.history_display = QTextEdit()
#         self.history_display.setReadOnly(True)
#         layout.addWidget(self.history_display)

#         self.setLayout(layout)

#         # Load all users
#         self.all_users = []
#         self.load_users()

#     def load_users(self):
#         """Load all users from DB"""
#         conn = get_db()
#         cur = conn.cursor()
#         cur.execute("SELECT id, name FROM users ORDER BY name")
#         self.all_users = cur.fetchall()
#         conn.close()
#         self.populate_dropdown(self.all_users)

#     def populate_dropdown(self, users):
#         """Fill dropdown with a given list of users"""
#         self.user_dropdown.blockSignals(True)  # prevent triggering show_history while updating
#         self.user_dropdown.clear()
#         self.user_dropdown.addItem("Select User", None)
#         for user_id, name in users:
#             self.user_dropdown.addItem(name, user_id)
#         self.user_dropdown.blockSignals(False)

#     def filter_users(self):
#         """Filter dropdown based on search text"""
#         text = self.search_box.text().lower()
#         filtered = [(uid, name) for uid, name in self.all_users if text in name.lower()]
#         self.populate_dropdown(filtered)

#     def show_history(self):
#         user_id = self.user_dropdown.currentData()
#         if not user_id:
#             self.history_display.clear()
#             return

#         conn = get_db()
#         cur = conn.cursor()
#         cur.execute("""
#             SELECT amount, date, mode FROM payments
#             WHERE user_id = ?
#             ORDER BY date DESC
#         """, (user_id,))
#         rows = cur.fetchall()
#         conn.close()

#         if not rows:
#             self.history_display.setText("No payment history for this user.")
#             return

#         text = ""
#         for amount, date, mode in rows:
#             text += f"₹{amount} | {date} | {mode}\n"
#         self.history_display.setText(text)


from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QComboBox, QTextEdit, QLineEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from db.database import get_db


class PaymentHistory(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Payment History")
        self.setFixedSize(480, 550)   # ⬅ increased window size

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(12)

        # Fonts
        label_font = QFont("Arial", 11)
        input_font = QFont("Arial", 11)

        # Search box
        self.search_box = QLineEdit()
        self.search_box.setFont(input_font)
        self.search_box.setPlaceholderText("Search user by name...")
        self.search_box.setMinimumHeight(36)
        self.search_box.textChanged.connect(self.filter_users)
        layout.addWidget(self.search_box)

        # Dropdown to select user
        self.user_dropdown = QComboBox()
        self.user_dropdown.setFont(input_font)
        self.user_dropdown.setMinimumHeight(36)
        self.user_dropdown.addItem("Select User", None)
        self.user_dropdown.currentIndexChanged.connect(self.show_history)
        layout.addWidget(self.user_dropdown)

        # Text area to display payment history
        self.history_display = QTextEdit()
        self.history_display.setFont(QFont("Arial", 10))
        self.history_display.setReadOnly(True)
        self.history_display.setMinimumHeight(300)
        layout.addWidget(self.history_display)

        self.setLayout(layout)

        # Load all users
        self.all_users = []
        self.load_users()

    def load_users(self):
        """Load all users from DB"""
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM users ORDER BY name")
        self.all_users = cur.fetchall()
        conn.close()
        self.populate_dropdown(self.all_users)

    def populate_dropdown(self, users):
        """Fill dropdown with a given list of users"""
        self.user_dropdown.blockSignals(True)
        self.user_dropdown.clear()
        self.user_dropdown.addItem("Select User", None)
        for user_id, name in users:
            self.user_dropdown.addItem(name, user_id)
        self.user_dropdown.blockSignals(False)

    def filter_users(self):
        """Filter dropdown based on search text"""
        text = self.search_box.text().lower()
        filtered = [
            (uid, name)
            for uid, name in self.all_users
            if text in name.lower()
        ]
        self.populate_dropdown(filtered)

    def show_history(self):
        user_id = self.user_dropdown.currentData()
        if not user_id:
            self.history_display.clear()
            return

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT amount, date, mode FROM payments
            WHERE user_id = ?
            ORDER BY date DESC
        """, (user_id,))
        rows = cur.fetchall()
        conn.close()

        if not rows:
            self.history_display.setText("No payment history for this user.")
            return

        text = ""
        for amount, date, mode in rows:
            text += f"₹{amount} | {date} | {mode}\n"

        self.history_display.setText(text)
