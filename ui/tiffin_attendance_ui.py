# from PyQt5.QtWidgets import (
#     QWidget, QLabel, QPushButton, QVBoxLayout,
#     QListWidget, QListWidgetItem, QComboBox,
#     QMessageBox, QDateEdit
# )
# from PyQt5.QtCore import Qt, QDate

# from db.database import get_db
# from services.tiffin_attendance_service import mark_tiffin_attendance


# class TiffinAttendanceUI(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Tiffin Attendance")
#         self.setFixedSize(500, 520)
#         self.init_ui()
#         self.load_users()

#     def init_ui(self):
#         title = QLabel("Manual Tiffin Attendance")
#         title.setAlignment(Qt.AlignCenter)
#         title.setStyleSheet("font-size:18px;font-weight:bold;")

#         self.date_edit = QDateEdit()
#         self.date_edit.setCalendarPopup(True)
#         self.date_edit.setDate(QDate.currentDate())

#         self.session_combo = QComboBox()
#         self.session_combo.addItems(["morning", "night"])

#         self.user_list = QListWidget()
#         self.user_list.setSelectionMode(QListWidget.MultiSelection)

#         mark_btn = QPushButton("Mark Attendance")
#         mark_btn.clicked.connect(self.mark_attendance)

#         layout = QVBoxLayout()
#         layout.setContentsMargins(25, 25, 25, 25)
#         layout.setSpacing(12)

#         layout.addWidget(title)
#         layout.addWidget(QLabel("Select Date"))
#         layout.addWidget(self.date_edit)
#         layout.addWidget(QLabel("Session"))
#         layout.addWidget(self.session_combo)
#         layout.addWidget(QLabel("Select Tiffin Users"))
#         layout.addWidget(self.user_list)
#         layout.addWidget(mark_btn)

#         self.setLayout(layout)

#     def load_users(self):
#         conn = get_db()
#         cur = conn.cursor()
#         cur.execute("SELECT id, name FROM users WHERE user_type='Tiffin'")
#         users = cur.fetchall()
#         conn.close()

#         for user_id, name in users:
#             item = QListWidgetItem(name)
#             item.setData(Qt.UserRole, user_id)
#             self.user_list.addItem(item)

#     def mark_attendance(self):
#         selected_items = self.user_list.selectedItems()
#         if not selected_items:
#             QMessageBox.warning(self, "Error", "Select at least one user")
#             return

#         selected_date = self.date_edit.date().toString("yyyy-MM-dd")
#         session = self.session_combo.currentText()

#         success = 0
#         failed = []

#         for item in selected_items:
#             user_id = item.data(Qt.UserRole)
#             ok, msg = mark_tiffin_attendance(user_id, selected_date, session)
#             if ok:
#                 success += 1
#             else:
#                 failed.append(f"{item.text()} → {msg}")

#         message = f"Success: {success}"
#         if failed:
#             message += "\n\nFailed:\n" + "\n".join(failed)

#         QMessageBox.information(self, "Result", message)


from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QListWidget, QListWidgetItem, QComboBox,
    QMessageBox, QDateEdit, QCheckBox
)
from PyQt5.QtCore import Qt, QDate

from db.database import get_db
from services.tiffin_attendance_service import mark_tiffin_attendance


class TiffinAttendanceUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tiffin Attendance")
        self.setFixedSize(540, 600)  # 🔼 slightly bigger
        self.init_ui()
        self.load_users()

    def init_ui(self):
        # -------- TITLE --------
        title = QLabel("Manual Tiffin Attendance")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        # -------- DATE --------
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setStyleSheet("font-size:15px; padding:6px;")

        # -------- SESSION --------
        self.session_combo = QComboBox()
        self.session_combo.addItems(["morning", "night"])
        self.session_combo.setStyleSheet("font-size:15px; padding:6px;")

        # -------- SELECT ALL --------
        self.select_all_chk = QCheckBox("Select All Users")
        self.select_all_chk.setStyleSheet("font-size:15px;")
        self.select_all_chk.stateChanged.connect(self.toggle_all_users)

        # -------- USER LIST --------
        self.user_list = QListWidget()
        self.user_list.setStyleSheet("""
            QListWidget {
                font-size: 15px;
            }
            QListWidget::item {
                height: 32px;
            }
        """)

        # -------- BUTTON --------
        mark_btn = QPushButton("Mark Attendance")
        mark_btn.setFixedHeight(42)
        mark_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                background-color: #2E86C1;
                color: white;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #1F618D;
            }
        """)
        mark_btn.clicked.connect(self.mark_attendance)

        # -------- LAYOUT --------
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        layout.addWidget(title)
        layout.addWidget(QLabel("Select Date"))
        layout.addWidget(self.date_edit)
        layout.addWidget(QLabel("Session"))
        layout.addWidget(self.session_combo)
        layout.addWidget(self.select_all_chk)
        layout.addWidget(QLabel("Select Tiffin Users"))
        layout.addWidget(self.user_list)
        layout.addWidget(mark_btn)

        self.setLayout(layout)

        # Label font
        self.setStyleSheet("""
            QLabel {
                font-size: 15px;
            }
        """)

    # -------- LOAD USERS --------
    def load_users(self):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM users WHERE user_type='Tiffin'")
        users = cur.fetchall()
        conn.close()

        self.user_list.clear()

        for user_id, name in users:
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, user_id)
            item.setCheckState(Qt.Unchecked)  # ✅ checkbox
            self.user_list.addItem(item)

    # -------- SELECT ALL HANDLER --------
    def toggle_all_users(self, state):
        check_state = Qt.Checked if state == Qt.Checked else Qt.Unchecked
        for i in range(self.user_list.count()):
            self.user_list.item(i).setCheckState(check_state)

    # -------- MARK ATTENDANCE --------
    def mark_attendance(self):
        selected_date = self.date_edit.date().toString("yyyy-MM-dd")
        session = self.session_combo.currentText()

        checked_items = [
            self.user_list.item(i)
            for i in range(self.user_list.count())
            if self.user_list.item(i).checkState() == Qt.Checked
        ]

        if not checked_items:
            QMessageBox.warning(self, "Error", "Select at least one user")
            return

        success = 0
        failed = []

        for item in checked_items:
            user_id = item.data(Qt.UserRole)
            ok, msg = mark_tiffin_attendance(user_id, selected_date, session)
            if ok:
                success += 1
            else:
                failed.append(f"{item.text()} → {msg}")

        message = f"Success: {success}"
        if failed:
            message += "\n\nFailed:\n" + "\n".join(failed)

        QMessageBox.information(self, "Result", message)
