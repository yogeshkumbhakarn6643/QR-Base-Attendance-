from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QLabel
)
from db.database import get_db


class UserReport(QWidget):
    def __init__(self, query=None, title_text="User Attendance Report"):
        super().__init__()
        self.setWindowTitle(title_text)
        self.resize(700, 400)

        self.query = query

        layout = QVBoxLayout()

        title = QLabel(title_text)
        title.setStyleSheet("font-size:16px; font-weight:bold;")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "User Name", "Mobile", "Date", "Session", "Amount"
        ])

        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_data()

    def load_data(self):
        conn = get_db()
        cur = conn.cursor()

        # Default → ALL REPORTS
        if not self.query:
            self.query = """
                SELECT 
                    u.name,
                    u.mobile,
                    a.date,
                    a.session,
                    a.amount
                FROM attendance a
                JOIN users u ON u.id = a.user_id
                ORDER BY a.date DESC
            """

        cur.execute(self.query)
        rows = cur.fetchall()

        self.table.setRowCount(len(rows))

        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.table.setItem(
                    row_idx, col_idx,
                    QTableWidgetItem(str(value))
                )

        conn.close()
