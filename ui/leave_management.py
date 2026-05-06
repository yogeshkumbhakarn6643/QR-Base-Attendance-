# from PyQt5.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QLabel,
#     QPushButton, QCheckBox, QScrollArea,
#     QDateEdit, QMessageBox, QGroupBox, QRadioButton
# )
# from PyQt5.QtCore import QDate
# from db.database import get_db


# class LeaveManagement(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Leave Management")
#         self.resize(500, 650)

#         main = QVBoxLayout()

#         title = QLabel("Approve Leave")
#         title.setStyleSheet("font-size:18px; font-weight:bold;")
#         main.addWidget(title)

#         # Date
#         date_layout = QHBoxLayout()
#         date_layout.addWidget(QLabel("Leave Date:"))
#         self.date_edit = QDateEdit()
#         self.date_edit.setDate(QDate.currentDate())
#         self.date_edit.setCalendarPopup(True)
#         date_layout.addWidget(self.date_edit)
#         main.addLayout(date_layout)

#         # Session selection
#         session_box = QGroupBox("Leave Session")
#         session_layout = QHBoxLayout()

#         self.rb_morning = QRadioButton("Morning")
#         self.rb_night = QRadioButton("Night")
#         self.rb_both = QRadioButton("Both")
#         self.rb_both.setChecked(True)

#         session_layout.addWidget(self.rb_morning)
#         session_layout.addWidget(self.rb_night)
#         session_layout.addWidget(self.rb_both)

#         session_box.setLayout(session_layout)
#         main.addWidget(session_box)

#         # Users list
#         users_box = QGroupBox("Select Users")
#         users_layout = QVBoxLayout()
#         self.user_checkboxes = []

#         conn = get_db()
#         cur = conn.cursor()
#         cur.execute("SELECT id, name FROM users ORDER BY name")
#         for uid, name in cur.fetchall():
#             cb = QCheckBox(f"{name} (ID {uid})")
#             cb.user_id = uid
#             self.user_checkboxes.append(cb)
#             users_layout.addWidget(cb)
#         conn.close()

#         users_box.setLayout(users_layout)

#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         scroll.setWidget(users_box)
#         main.addWidget(scroll)

#         # Save button
#         btn = QPushButton("Approve Leave")
#         btn.setStyleSheet("padding:8px; font-size:14px;")
#         btn.clicked.connect(self.save_leave)
#         main.addWidget(btn)

#         self.setLayout(main)

#     def save_leave(self):
#         users = [cb.user_id for cb in self.user_checkboxes if cb.isChecked()]
#         if not users:
#             QMessageBox.warning(self, "Error", "Select at least one user")
#             return

#         if self.rb_morning.isChecked():
#             session = "morning"
#         elif self.rb_night.isChecked():
#             session = "night"
#         else:
#             session = "both"

#         leave_date = self.date_edit.date().toString("yyyy-MM-dd")

#         try:
#             conn = get_db()
#             cur = conn.cursor()

#             for uid in users:
#                 # Check if leave already approved for this user/date/session
#                 cur.execute("""
#                     SELECT id FROM leaves
#                     WHERE user_id=? AND date=? AND (session=? OR session='both') AND status='approved'
#                 """, (uid, leave_date, session))
#                 if cur.fetchone():
#                     continue  # skip this user

#                 cur.execute("""
#                     INSERT INTO leaves (user_id, date, session, status)
#                     VALUES (?, ?, ?, 'approved')
#                 """, (uid, leave_date, session))

#             conn.commit()
#             conn.close()

#             QMessageBox.information(self, "Success", "Leave approved successfully")

#         except Exception as e:
#             QMessageBox.critical(self, "Error", str(e))


from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QCheckBox, QScrollArea,
    QDateEdit, QMessageBox, QGroupBox,
    QRadioButton, QLineEdit
)
from PyQt5.QtCore import QDate
from db.database import get_db


class LeaveManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Leave Management")
        self.resize(500, 650)

        main = QVBoxLayout()

        # ---------- Title ----------
        title = QLabel("Approve Leave")
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        main.addWidget(title)

        # ---------- Date ----------
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Leave Date:"))
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        date_layout.addWidget(self.date_edit)
        main.addLayout(date_layout)

        # ---------- Session ----------
        session_box = QGroupBox("Leave Session")
        session_layout = QHBoxLayout()

        self.rb_morning = QRadioButton("Morning")
        self.rb_night = QRadioButton("Night")
        self.rb_both = QRadioButton("Both")
        self.rb_both.setChecked(True)

        session_layout.addWidget(self.rb_morning)
        session_layout.addWidget(self.rb_night)
        session_layout.addWidget(self.rb_both)
        session_box.setLayout(session_layout)
        main.addWidget(session_box)

        # ---------- Search ----------
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search user by name...")
        self.search_box.textChanged.connect(self.filter_users)
        main.addWidget(self.search_box)

        # ---------- Users ----------
        self.users_box = QGroupBox("Select Users")
        self.users_layout = QVBoxLayout()
        self.users_box.setLayout(self.users_layout)

        self.user_checkboxes = []
        self.load_users()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.users_box)
        main.addWidget(scroll)

        # ---------- Button ----------
        btn = QPushButton("Approve Leave")
        btn.setStyleSheet("padding:8px; font-size:14px;")
        btn.clicked.connect(self.save_leave)
        main.addWidget(btn)

        self.setLayout(main)

    # =============================
    # Load Users
    # =============================
    def load_users(self):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM users ORDER BY name")
        users = cur.fetchall()
        conn.close()

        self.user_checkboxes.clear()

        for uid, name in users:
            cb = QCheckBox(f"{name} (ID {uid})")
            cb.user_id = uid
            cb.user_name = name.lower()
            self.user_checkboxes.append(cb)
            self.users_layout.addWidget(cb)

    # =============================
    # Search Filter
    # =============================
    def filter_users(self):
        text = self.search_box.text().lower()

        for cb in self.user_checkboxes:
            cb.setVisible(text in cb.user_name)

    # =============================
    # Save Leave
    # =============================
    def save_leave(self):
        users = [cb.user_id for cb in self.user_checkboxes if cb.isChecked()]
        if not users:
            QMessageBox.warning(self, "Error", "Select at least one user")
            return

        if self.rb_morning.isChecked():
            session = "morning"
        elif self.rb_night.isChecked():
            session = "night"
        else:
            session = "both"

        leave_date = self.date_edit.date().toString("yyyy-MM-dd")

        try:
            conn = get_db()
            cur = conn.cursor()

            for uid in users:
                cur.execute("""
                    SELECT id FROM leaves
                    WHERE user_id=? AND date=? AND status='approved'
                """, (uid, leave_date))

                if cur.fetchone():
                    continue

                cur.execute("""
                    INSERT INTO leaves (user_id, date, session, status)
                    VALUES (?, ?, ?, 'approved')
                """, (uid, leave_date, session))

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Leave approved successfully")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
