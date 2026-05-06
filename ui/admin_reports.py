from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QComboBox, QPushButton, QMessageBox
)
from services.report_service import all_users_report, low_balance_users, delete_user


class AdminReports(QWidget):
    def __init__(self, mode="all"):
        super().__init__()
        self.mode = mode

        self.setWindowTitle("Admin Reports")
        self.resize(1000, 450)  # increased width for button column

        layout = QVBoxLayout()

        title = QLabel(
            "Low Balance Users" if mode == "low" else "All Users Report"
        )
        title.setStyleSheet("font-size:16px; font-weight:bold;")
        layout.addWidget(title)

        # 🔹 USER TYPE FILTER
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("All Users", None)
        self.filter_combo.addItem("Tiffin", "Tiffin")
        self.filter_combo.addItem("Direct Meal", "Direct Meal")
        self.filter_combo.currentIndexChanged.connect(self.reload_data)
        layout.addWidget(self.filter_combo)

        # 🔹 TABLE
        self.table = QTableWidget()
        self.table.setColumnCount(6)  # added delete button column
        self.table.setHorizontalHeaderLabels([
            "User ID", "Name", "Mobile", "User Type", "Balance", "Action"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.table)
        self.setLayout(layout)

        self.reload_data()

    def reload_data(self):
        user_type = self.filter_combo.currentData()

        if self.mode == "low":
            data = low_balance_users(user_type=user_type)
        else:
            data = all_users_report(user_type=user_type)

        self.load_data(data)

    def load_data(self, rows):
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))

            # 🔹 Add Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("background-color:#ff4d4d; color:white;")
            delete_btn.clicked.connect(lambda _, user_id=row[0]: self.confirm_delete(user_id))
            self.table.setCellWidget(r, 5, delete_btn)

    def confirm_delete(self, user_id):
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to permanently delete this user and all related data?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            delete_user(user_id)
            QMessageBox.information(self, "Deleted", f"User ID {user_id} deleted successfully!")
            self.reload_data()
