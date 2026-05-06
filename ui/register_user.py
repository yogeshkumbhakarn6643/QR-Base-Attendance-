# from PyQt5.QtWidgets import (
#     QWidget, QLabel, QLineEdit, QPushButton,
#     QVBoxLayout, QHBoxLayout, QMessageBox
# )
# from PyQt5.QtCore import Qt
# from db.database import get_db


# class RegisterUser(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Register User")
#         self.setFixedSize(420, 320)   # ✅ Proper window size

#         self.init_ui()

#     def init_ui(self):
#         # Title
#         title = QLabel("User Registration")
#         title.setAlignment(Qt.AlignCenter)
#         title.setStyleSheet("""
#             font-size: 20px;
#             font-weight: bold;
#             margin-bottom: 20px;
#         """)

#         # Name
#         name_label = QLabel("Full Name")
#         self.name_input = QLineEdit()
#         self.name_input.setPlaceholderText("Enter user name")

#         # Mobile
#         mobile_label = QLabel("Mobile Number")
#         self.mobile_input = QLineEdit()
#         self.mobile_input.setPlaceholderText("Enter mobile number")

#         # Button
#         save_btn = QPushButton("Register User")
#         save_btn.setFixedHeight(40)
#         save_btn.clicked.connect(self.save_user)

#         # Layout
#         layout = QVBoxLayout()
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(12)

#         layout.addWidget(title)
#         layout.addWidget(name_label)
#         layout.addWidget(self.name_input)
#         layout.addWidget(mobile_label)
#         layout.addWidget(self.mobile_input)
#         layout.addSpacing(10)
#         layout.addWidget(save_btn)

#         self.setLayout(layout)

#         # Global styling
#         self.setStyleSheet("""
#             QLabel {
#                 font-size: 14px;
#             }
#             QLineEdit {
#                 height: 42px;
#                 font-size: 14px;
#                 padding: 8px 10px;
#                 line-height: 20px;
#             }
#             QPushButton {
#                 font-size: 15px;
#                 background-color: #2E86C1;
#                 color: white;
#                 border-radius: 6px;
#                 height: 40px;
#             }
#             QPushButton:hover {
#                 background-color: #1F618D;
#             }
#         """)

#     def save_user(self):
#         name = self.name_input.text().strip()
#         mobile = self.mobile_input.text().strip()

#         if not name:
#             QMessageBox.warning(self, "Error", "Name is required")
#             return

#         conn = get_db()
#         cur = conn.cursor()
#         cur.execute(
#             "INSERT INTO users (name, mobile) VALUES (?, ?)",
#             (name, mobile)
#         )
#         conn.commit()
#         conn.close()

#         QMessageBox.information(self, "Success", "User registered successfully")
#         self.close()
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt
from db.database import get_db


class RegisterUser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register User")
        self.setFixedSize(420, 400)   # ✅ SAME size as before

        self.init_ui()

    def init_ui(self):
        # Title
        title = QLabel("User Registration")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 20px;
        """)

        # Name
        name_label = QLabel("Full Name")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter user name")

        # Mobile
        mobile_label = QLabel("Mobile Number")
        self.mobile_input = QLineEdit()
        self.mobile_input.setPlaceholderText("Enter mobile number")
        self.mobile_input.setMaxLength(10)

        # User Type
        type_label = QLabel("User Type")
        self.type_combo = QComboBox()
        self.type_combo.addItem("Direct Meal", "direct")
        self.type_combo.addItem("Tiffin", "tiffin")

        # Button
        save_btn = QPushButton("Register User")
        save_btn.setFixedHeight(40)
        save_btn.clicked.connect(self.save_user)

        # Layout (UNCHANGED)
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        layout.addWidget(title)
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(mobile_label)
        layout.addWidget(self.mobile_input)
        layout.addWidget(type_label)
        layout.addWidget(self.type_combo)
        layout.addSpacing(10)
        layout.addWidget(save_btn)

        self.setLayout(layout)

        # SAME STYLES
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QComboBox {
                height: 42px;
                font-size: 14px;
                padding: 8px 10px;
                line-height: 20px;
            }
            QPushButton {
                font-size: 15px;
                background-color: #2E86C1;
                color: white;
                border-radius: 6px;
                height: 40px;
            }
            QPushButton:hover {
                background-color: #1F618D;
            }
        """)

    def save_user(self):
        name = self.name_input.text().strip()
        mobile = self.mobile_input.text().strip()
        user_type = self.type_combo.currentText()

        # 🔒 VALIDATIONS
        if not name:
            QMessageBox.warning(self, "Error", "Name is required")
            return

        if not mobile.isdigit():
            QMessageBox.warning(self, "Error", "Mobile number must contain only digits")
            return

        if len(mobile) != 10:
            QMessageBox.warning(self, "Error", "Mobile number must be exactly 10 digits")
            return

        conn = get_db()
        cur = conn.cursor()

        # Unique mobile check
        cur.execute("SELECT id FROM users WHERE mobile=?", (mobile,))
        if cur.fetchone():
            conn.close()
            QMessageBox.warning(self, "Error", "Mobile number already registered")
            return

        # Insert
        cur.execute(
            "INSERT INTO users (name, mobile, user_type) VALUES (?, ?, ?)",
            (name, mobile, user_type)
        )
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "User registered successfully")
        self.close()
