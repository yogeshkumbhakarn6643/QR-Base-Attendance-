# import csv
# from PyQt5.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QLabel,
#     QLineEdit, QPushButton, QTableWidget,
#     QTableWidgetItem, QDateEdit, QFileDialog,
#     QMessageBox
# )
# from PyQt5.QtCore import QDate

# from services.attendance_report_service import user_attendance_report


# class UserAttendanceReport(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("User Attendance Report")
#         self.resize(900, 500)
#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout()

#         # -------- FILTER BAR --------
#         filter_layout = QHBoxLayout()

#         self.name_input = QLineEdit()
#         self.name_input.setPlaceholderText("Search user name")

#         self.start_date = QDateEdit()
#         self.start_date.setCalendarPopup(True)
#         self.start_date.setDate(QDate.currentDate().addDays(-7))

#         self.end_date = QDateEdit()
#         self.end_date.setCalendarPopup(True)
#         self.end_date.setDate(QDate.currentDate())

#         search_btn = QPushButton("Search")
#         search_btn.clicked.connect(self.load_data)

#         download_btn = QPushButton("Download CSV")
#         download_btn.clicked.connect(self.download_csv)

#         filter_layout.addWidget(QLabel("User"))
#         filter_layout.addWidget(self.name_input)
#         filter_layout.addWidget(QLabel("From"))
#         filter_layout.addWidget(self.start_date)
#         filter_layout.addWidget(QLabel("To"))
#         filter_layout.addWidget(self.end_date)
#         filter_layout.addWidget(search_btn)
#         filter_layout.addWidget(download_btn)

#         # -------- TABLE --------
#         self.table = QTableWidget()
#         self.table.setColumnCount(6)
#         self.table.setHorizontalHeaderLabels([
#             "User ID", "Name", "Date",
#             "Session", "Attendance", "Leave Status"
#         ])
#         self.table.horizontalHeader().setStretchLastSection(True)

#         layout.addLayout(filter_layout)
#         layout.addWidget(self.table)
#         self.setLayout(layout)

#     # -------- LOAD DATA --------
#     def load_data(self):
#         name = self.name_input.text().strip()
#         start = self.start_date.date().toString("yyyy-MM-dd")
#         end = self.end_date.date().toString("yyyy-MM-dd")

#         rows = user_attendance_report(
#             user_name=name,
#             start_date=start,
#             end_date=end
#         )

#         self.table.setRowCount(len(rows))
#         for r, row in enumerate(rows):
#             for c, val in enumerate(row):
#                 self.table.setItem(r, c, QTableWidgetItem(str(val)))

#         self.current_rows = rows  # store for download

#     # -------- DOWNLOAD CSV --------
#     def download_csv(self):
#         if not hasattr(self, "current_rows") or not self.current_rows:
#             QMessageBox.warning(self, "Error", "No data to download")
#             return

#         path, _ = QFileDialog.getSaveFileName(
#             self, "Save File", "attendance_report.csv", "CSV Files (*.csv)"
#         )
#         if not path:
#             return

#         with open(path, "w", newline="", encoding="utf-8") as f:
#             writer = csv.writer(f)
#             writer.writerow([
#                 "User ID", "Name", "Date",
#                 "Session", "Attendance", "Leave Status"
#             ])
#             writer.writerows(self.current_rows)

#         QMessageBox.information(self, "Success", "File downloaded successfully")


# from PyQt5.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout,
#     QLabel, QLineEdit, QPushButton,
#     QDateEdit, QTableWidget, QTableWidgetItem,
#     QFileDialog, QMessageBox
# )
# from PyQt5.QtCore import QDate, Qt
# import csv

# from db.database import get_db


# class UserAttendanceReport(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("User Attendance Report")
#         self.resize(1000, 550)

#         self.init_ui()

#     def init_ui(self):
#         main_layout = QVBoxLayout()
#         main_layout.setContentsMargins(20, 20, 20, 20)
#         main_layout.setSpacing(12)

#         # ---------- TITLE ----------
#         title = QLabel("Attendance Report")
#         title.setAlignment(Qt.AlignCenter)
#         title.setStyleSheet("font-size:18px; font-weight:bold;")
#         main_layout.addWidget(title)

#         # ---------- FILTERS ----------
#         filter_layout = QHBoxLayout()
#         filter_layout.setSpacing(10)

#         self.user_search = QLineEdit()
#         self.user_search.setPlaceholderText("User name starts with")

#         self.from_date = QDateEdit()
#         self.from_date.setCalendarPopup(True)
#         self.from_date.setDate(QDate.currentDate().addDays(-7))

#         self.to_date = QDateEdit()
#         self.to_date.setCalendarPopup(True)
#         self.to_date.setDate(QDate.currentDate())

#         search_btn = QPushButton("Search")
#         search_btn.clicked.connect(self.load_data)

#         download_btn = QPushButton("Download CSV")
#         download_btn.clicked.connect(self.download_csv)

#         filter_layout.addWidget(QLabel("User"))
#         filter_layout.addWidget(self.user_search)
#         filter_layout.addWidget(QLabel("From"))
#         filter_layout.addWidget(self.from_date)
#         filter_layout.addWidget(QLabel("To"))
#         filter_layout.addWidget(self.to_date)
#         filter_layout.addWidget(search_btn)
#         filter_layout.addWidget(download_btn)

#         main_layout.addLayout(filter_layout)

#         # ---------- TABLE ----------
#         self.table = QTableWidget()
#         self.table.setColumnCount(6)
#         self.table.setHorizontalHeaderLabels([
#             "User ID",
#             "Name",
#             "Date",
#             "Session",
#             "Attendance Status",
#             "Leave Status"
#         ])

#         self.table.horizontalHeader().setStretchLastSection(True)
#         self.table.setAlternatingRowColors(True)

#         main_layout.addWidget(self.table)
#         self.setLayout(main_layout)

#         # ---------- STYLES ----------
#         self.setStyleSheet("""
#             QLabel {
#                 font-size: 15px;
#                 font-weight: 600;
#             }
#             QLineEdit, QDateEdit {
#                 font-size: 14px;
#                 padding: 6px;
#                 height: 32px;
#             }
#             QPushButton {
#                 font-size: 14px;
#                 padding: 8px 12px;
#             }
#             QTableWidget {
#                 font-size: 13px;
#             }
#             QHeaderView::section {
#                 font-size: 14px;
#                 font-weight: bold;
#                 padding: 6px;
#             }
#         """)

#     # ---------- LOAD DATA ----------
#     def load_data(self):
#         name = self.user_search.text().strip()
#         from_date = self.from_date.date().toString("yyyy-MM-dd")
#         to_date = self.to_date.date().toString("yyyy-MM-dd")

#         conn = get_db()
#         cur = conn.cursor()

#         cur.execute("""
#             SELECT 
#                 u.id,
#                 u.name,
#                 a.date,
#                 a.session,
#                 IFNULL(a.status, 'absent') AS attendance_status,
#                 IFNULL(l.status, '-') AS leave_status
#             FROM users u
#             LEFT JOIN attendance a
#                 ON u.id = a.user_id
#                 AND a.date BETWEEN ? AND ?
#             LEFT JOIN leaves l
#                 ON l.user_id = u.id
#                 AND l.date = a.date
#                 AND l.session = a.session
#             WHERE u.name LIKE ?
#             ORDER BY u.name, a.date
#         """, (from_date, to_date, name + '%'))

#         rows = cur.fetchall()
#         conn.close()

#         self.table.setRowCount(len(rows))

#         for r, row in enumerate(rows):
#             for c, val in enumerate(row):
#                 self.table.setItem(
#                     r, c, QTableWidgetItem(str(val))
#                 )

#         if not rows:
#             QMessageBox.information(
#                 self, "No Data", "No attendance found for given filters"
#             )

#     # ---------- DOWNLOAD CSV ----------
#     def download_csv(self):
#         if self.table.rowCount() == 0:
#             QMessageBox.warning(self, "Error", "No data to download")
#             return

#         path, _ = QFileDialog.getSaveFileName(
#             self, "Save Attendance Report", "",
#             "CSV Files (*.csv)"
#         )

#         if not path:
#             return

#         with open(path, "w", newline="", encoding="utf-8") as f:
#             writer = csv.writer(f)
#             writer.writerow([
#                 "User ID",
#                 "Name",
#                 "Date",
#                 "Session",
#                 "Attendance Status",
#                 "Leave Status"
#             ])

#             for row in range(self.table.rowCount()):
#                 writer.writerow([
#                     self.table.item(row, col).text()
#                     for col in range(self.table.columnCount())
#                 ])

#         QMessageBox.information(
#             self, "Success", "Report downloaded successfully"
#         )


from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QDateEdit, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox, QListWidget
)
from PyQt5.QtCore import QDate, Qt
import csv

from db.database import get_db


class UserAttendanceReport(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Attendance Report")
        self.resize(1000, 580)

        self.all_users = []
        self.selected_user_id = None

        self.init_ui()
        self.load_users()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(8)

        # ---------- TITLE ----------
        title = QLabel("Attendance Report")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        main_layout.addWidget(title)

        # ---------- USER SEARCH ----------
        main_layout.addWidget(QLabel("User"))

        self.user_search = QLineEdit()
        self.user_search.setPlaceholderText("Search user (starts with)")
        self.user_search.textChanged.connect(self.filter_users)
        main_layout.addWidget(self.user_search)

        self.user_list = QListWidget()
        self.user_list.setFixedHeight(90)   # ✅ smaller height
        self.user_list.itemClicked.connect(self.select_user)
        main_layout.addWidget(self.user_list)

        # ---------- DATE FILTER ----------
        filter_layout = QHBoxLayout()

        self.from_date = QDateEdit()
        self.from_date.setCalendarPopup(True)
        self.from_date.setDate(QDate.currentDate().addDays(-7))

        self.to_date = QDateEdit()
        self.to_date.setCalendarPopup(True)
        self.to_date.setDate(QDate.currentDate())

        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.load_data)

        download_btn = QPushButton("Download CSV")
        download_btn.clicked.connect(self.download_csv)

        filter_layout.addWidget(QLabel("From"))
        filter_layout.addWidget(self.from_date)
        filter_layout.addWidget(QLabel("To"))
        filter_layout.addWidget(self.to_date)
        filter_layout.addWidget(search_btn)
        filter_layout.addWidget(download_btn)

        main_layout.addLayout(filter_layout)

        # ---------- TABLE ----------
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "User ID",
            "Name",
            "Date",
            "Session",
            "Attendance Status",
            "Leave Status"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        main_layout.addWidget(self.table)

        # ---------- STYLES ----------
        self.setStyleSheet("""
            QLabel { font-size: 14px; font-weight: 600; }
            QLineEdit, QDateEdit {
                font-size: 14px;
                height: 32px;
                padding: 6px;
            }
            QListWidget {
                font-size: 14px;
            }
            QPushButton {
                font-size: 14px;
                padding: 8px 12px;
            }
            QTableWidget {
                font-size: 13px;
            }
        """)

    # ---------- LOAD USERS ----------
    def load_users(self):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM users ORDER BY name")
        self.all_users = cur.fetchall()
        conn.close()

    # ---------- FILTER USERS (STARTS WITH) ----------
    def filter_users(self):
        text = self.user_search.text().lower()
        self.user_list.clear()

        if not text:
            return

        for user_id, name in self.all_users:
            if name.lower().startswith(text):
                item = f"{name} (ID: {user_id})"
                lw_item = self.user_list.addItem(item)
                self.user_list.item(self.user_list.count() - 1).setData(
                    Qt.UserRole, user_id
                )

    # ---------- SELECT USER ----------
    def select_user(self, item):
        self.selected_user_id = item.data(Qt.UserRole)

        # 🔒 BLOCK SIGNAL to avoid re-filter
        self.user_search.blockSignals(True)
        self.user_search.setText(item.text().split(" (")[0])
        self.user_search.blockSignals(False)

        self.user_list.clear()

    # ---------- LOAD DATA ----------
    def load_data(self):
        if not self.selected_user_id:
            QMessageBox.warning(self, "Error", "Please select a user")
            return

        from_date = self.from_date.date().toString("yyyy-MM-dd")
        to_date = self.to_date.date().toString("yyyy-MM-dd")

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                u.id,
                u.name,
                a.date,
                a.session,
                IFNULL(a.status, 'absent'),
                IFNULL(l.status, '-')
            FROM users u
            LEFT JOIN attendance a
                ON u.id = a.user_id
                AND a.date BETWEEN ? AND ?
            LEFT JOIN leaves l
                ON l.user_id = u.id
                AND l.date = a.date
                AND l.session = a.session
            WHERE u.id = ?
            ORDER BY a.date
        """, (from_date, to_date, self.selected_user_id))

        rows = cur.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))

    # # ---------- DOWNLOAD CSV ----------
    # def download_csv(self):
    #     if self.table.rowCount() == 0:
    #         QMessageBox.warning(self, "Error", "No data to download")
    #         return

    #     path, _ = QFileDialog.getSaveFileName(
    #         self, "Save Attendance Report", "", "CSV Files (*.csv)"
    #     )
    #     if not path:
    #         return

    #     with open(path, "w", newline="", encoding="utf-8") as f:
    #         writer = csv.writer(f)
    #         writer.writerow([
    #             "User ID", "Name", "Date",
    #             "Session", "Attendance Status", "Leave Status"
    #         ])
    #         for r in range(self.table.rowCount()):
    #             writer.writerow([
    #                 self.table.item(r, c).text()
    #                 for c in range(self.table.columnCount())
    #             ])

    #     QMessageBox.information(self, "Success", "Report downloaded successfully")
    def download_csv(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Error", "No data to download")
            return

        # 🔹 Get username safely
        user_name = self.user_search.text().strip().replace(" ", "_")

        from_date = self.from_date.date().toString("yyyy-MM-dd")
        to_date = self.to_date.date().toString("yyyy-MM-dd")

        default_filename = f"{user_name}_Attendance_{from_date}_to_{to_date}.csv"

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Attendance Report",
            default_filename,          # ✅ DEFAULT NAME HERE
            "CSV Files (*.csv)"
        )

        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "User ID", "Name", "Date",
                "Session", "Attendance Status", "Leave Status"
            ])
            for r in range(self.table.rowCount()):
                writer.writerow([
                    self.table.item(r, c).text()
                    for c in range(self.table.columnCount())
                ])

        QMessageBox.information(self, "Success", "Report downloaded successfully")

