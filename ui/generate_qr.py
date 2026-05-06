# from PyQt5.QtWidgets import (
#     QWidget, QLabel, QComboBox, QPushButton,
#     QVBoxLayout, QHBoxLayout, QFileDialog,
#     QMessageBox, QLineEdit
# )
# from PyQt5.QtGui import QFont, QPainter
# from PyQt5.QtCore import Qt
# from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
# from datetime import datetime
# from services.qr_service import generate_monthly_qr
# from db.database import get_db


# class GenerateQR(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Generate Monthly QR")
#         self.resize(500, 600)

#         self.current_qr_pixmap = None

#         # Fonts
#         self.label_font = QFont("Arial", 12, QFont.Bold)
#         self.input_font = QFont("Arial", 11)

#         # Search
#         self.search_input = QLineEdit()
#         self.search_input.setPlaceholderText("Search user by name...")
#         self.search_input.setMinimumHeight(36)
#         self.search_input.textChanged.connect(self.filter_users)

#         # Combos
#         self.user_combo = QComboBox()
#         self.user_combo.setMinimumHeight(36)

#         self.month_combo = QComboBox()
#         self.month_combo.setMinimumHeight(36)

#         self.year_combo = QComboBox()
#         self.year_combo.setMinimumHeight(36)

#         self.load_users()

#         months = [
#             "January", "February", "March", "April", "May", "June",
#             "July", "August", "September", "October", "November", "December"
#         ]
#         for m in months:
#             self.month_combo.addItem(m)

#         for y in range(2024, 2031):
#             self.year_combo.addItem(str(y))

#         # QR display
#         self.qr_label = QLabel("QR will appear here")
#         self.qr_label.setFixedSize(300, 300)
#         self.qr_label.setAlignment(Qt.AlignCenter)
#         self.qr_label.setStyleSheet("border:1px solid black;")
#         self.qr_label.setScaledContents(True)

#         # Buttons
#         self.gen_btn = QPushButton("Generate QR")
#         self.gen_btn.clicked.connect(self.generate)

#         self.download_btn = QPushButton("Download QR")
#         self.download_btn.setEnabled(False)
#         self.download_btn.clicked.connect(self.download_qr)

#         self.print_btn = QPushButton("Print QR")
#         self.print_btn.setEnabled(False)
#         self.print_btn.clicked.connect(self.print_qr)

#         # Layout
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(25, 20, 25, 20)
#         layout.setSpacing(12)

#         layout.addWidget(self.search_input)

#         lbl = QLabel("Select User")
#         lbl.setFont(self.label_font)
#         layout.addWidget(lbl)
#         layout.addWidget(self.user_combo)

#         lbl = QLabel("Select Month")
#         lbl.setFont(self.label_font)
#         layout.addWidget(lbl)
#         layout.addWidget(self.month_combo)

#         lbl = QLabel("Select Year")
#         lbl.setFont(self.label_font)
#         layout.addWidget(lbl)
#         layout.addWidget(self.year_combo)

#         layout.addWidget(self.gen_btn)
#         layout.addWidget(self.qr_label)

#         btns = QHBoxLayout()
#         btns.addWidget(self.download_btn)
#         btns.addWidget(self.print_btn)
#         layout.addLayout(btns)

#     # ---------- DB ----------
#     def load_users(self):
#         self.users = []
#         conn = get_db()
#         cur = conn.cursor()
#         cur.execute("SELECT id, name FROM users ORDER BY name")
#         self.users = cur.fetchall()
#         conn.close()
#         self.refresh_user_combo()

#     def refresh_user_combo(self):
#         self.user_combo.clear()
#         for uid, name in self.users:
#             self.user_combo.addItem(name, uid)

#     def filter_users(self, text):
#         self.user_combo.clear()
#         for uid, name in self.users:
#             if text.lower() in name.lower():
#                 self.user_combo.addItem(name, uid)

#     # ---------- ACTIONS ----------
#     def generate(self):
#         if self.user_combo.count() == 0:
#             QMessageBox.warning(self, "Error", "No user selected")
#             return

#         user_id = self.user_combo.currentData()
#         user_name = self.user_combo.currentText()
#         month = self.month_combo.currentIndex() + 1
#         year = int(self.year_combo.currentText())

#         try:
#             pixmap = generate_monthly_qr(user_id, month, year, user_name)
#             self.current_qr_pixmap = pixmap
#             self.qr_label.setPixmap(pixmap)

#             self.download_btn.setEnabled(True)
#             self.print_btn.setEnabled(True)

#             QMessageBox.information(self, "Success", "QR Generated Successfully")
#         except Exception as e:
#             QMessageBox.critical(self, "Error", str(e))

#     def download_qr(self):
#         if not self.current_qr_pixmap:
#             return

#         user_name = self.user_combo.currentText().replace(" ", "_")
#         today = datetime.now().strftime("%Y-%m-%d")

#         default_name = f"{user_name}_{today}.png"

#         file_path, _ = QFileDialog.getSaveFileName(
#             self,
#             "Save QR",
#             default_name,
#             "PNG Files (*.png)"
#         )

#         if file_path:
#             self.current_qr_pixmap.save(file_path, "PNG")
#             QMessageBox.information(self, "Saved", "QR saved successfully")

#     def print_qr(self):
#         if not self.current_qr_pixmap:
#             return

#         printer = QPrinter()
#         dialog = QPrintDialog(printer, self)
#         if dialog.exec_() == QPrintDialog.Accepted:
#             painter = QPainter(printer)
#             rect = painter.viewport()
#             scaled = self.current_qr_pixmap.scaled(
#                 rect.size(), Qt.KeepAspectRatio
#             )
#             painter.drawPixmap(0, 0, scaled)
#             painter.end()



# from PyQt5.QtWidgets import (
#     QWidget, QLabel, QPushButton,
#     QVBoxLayout, QHBoxLayout, QFileDialog,
#     QMessageBox, QLineEdit, QDateEdit, QComboBox
# )
# from PyQt5.QtGui import QFont, QPainter
# from PyQt5.QtCore import Qt, QDate
# from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
# from datetime import datetime
# from services.qr_service import generate_monthly_qr
# from db.database import get_db


# class GenerateQR(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Generate QR (Date Range)")
#         self.resize(500, 620)

#         self.current_qr_pixmap = None

#         # Fonts
#         self.label_font = QFont("Arial", 12, QFont.Bold)

#         # Search
#         self.search_input = QLineEdit()
#         self.search_input.setPlaceholderText("Search user by name...")
#         self.search_input.setMinimumHeight(36)
#         self.search_input.textChanged.connect(self.filter_users)

#         # User combo
#         self.user_combo = QComboBox()
#         self.user_combo.setMinimumHeight(36)

#         self.load_users()

#         # Start Date
#         self.start_date = QDateEdit()
#         self.start_date.setCalendarPopup(True)
#         self.start_date.setDate(QDate.currentDate())
#         self.start_date.setMinimumHeight(36)

#         # End Date
#         self.end_date = QDateEdit()
#         self.end_date.setCalendarPopup(True)
#         self.end_date.setDate(QDate.currentDate())
#         self.end_date.setMinimumHeight(36)

#         # QR display
#         self.qr_label = QLabel("QR will appear here")
#         self.qr_label.setFixedSize(300, 300)
#         self.qr_label.setAlignment(Qt.AlignCenter)
#         self.qr_label.setStyleSheet("border:1px solid black;")
#         self.qr_label.setScaledContents(True)

#         # Buttons
#         self.gen_btn = QPushButton("Generate QR")
#         self.gen_btn.clicked.connect(self.generate)

#         self.download_btn = QPushButton("Download QR")
#         self.download_btn.setEnabled(False)
#         self.download_btn.clicked.connect(self.download_qr)

#         self.print_btn = QPushButton("Print QR")
#         self.print_btn.setEnabled(False)
#         self.print_btn.clicked.connect(self.print_qr)

#         # Layout
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(25, 20, 25, 20)
#         layout.setSpacing(12)

#         layout.addWidget(self.search_input)

#         lbl = QLabel("Select User")
#         lbl.setFont(self.label_font)
#         layout.addWidget(lbl)
#         layout.addWidget(self.user_combo)

#         lbl = QLabel("Start Date")
#         lbl.setFont(self.label_font)
#         layout.addWidget(lbl)
#         layout.addWidget(self.start_date)

#         lbl = QLabel("End Date")
#         lbl.setFont(self.label_font)
#         layout.addWidget(lbl)
#         layout.addWidget(self.end_date)

#         layout.addWidget(self.gen_btn)
#         layout.addWidget(self.qr_label)

#         btns = QHBoxLayout()
#         btns.addWidget(self.download_btn)
#         btns.addWidget(self.print_btn)
#         layout.addLayout(btns)

#     # ---------- DB ----------
#     def load_users(self):
#         conn = get_db()
#         cur = conn.cursor()
#         cur.execute("SELECT id, name FROM users ORDER BY name")
#         self.users = cur.fetchall()
#         conn.close()
#         self.refresh_user_combo()

#     def refresh_user_combo(self):
#         self.user_combo.clear()
#         for uid, name in self.users:
#             self.user_combo.addItem(name, uid)

#     def filter_users(self, text):
#         self.user_combo.clear()
#         for uid, name in self.users:
#             if text.lower() in name.lower():
#                 self.user_combo.addItem(name, uid)

#     # ---------- ACTIONS ----------
#     def generate(self):
#         if self.user_combo.count() == 0:
#             QMessageBox.warning(self, "Error", "No user selected")
#             return

#         if self.start_date.date() > self.end_date.date():
#             QMessageBox.warning(self, "Error", "Start date cannot be after End date")
#             return

#         user_id = self.user_combo.currentData()
#         user_name = self.user_combo.currentText()

#         start_date = self.start_date.date().toString("yyyy-MM-dd")
#         end_date = self.end_date.date().toString("yyyy-MM-dd")

#         try:
#             pixmap = generate_monthly_qr(
#                 user_id=user_id,
#                 month=None,
#                 year=None,
#                 user_name=user_name,
#                 start_date=start_date,
#                 end_date=end_date
#             )

#             self.current_qr_pixmap = pixmap
#             self.qr_label.setPixmap(pixmap)

#             self.download_btn.setEnabled(True)
#             self.print_btn.setEnabled(True)

#             QMessageBox.information(self, "Success", "Date Range QR Generated")
#         except Exception as e:
#             QMessageBox.critical(self, "Error", str(e))

#     def download_qr(self):
#         if not self.current_qr_pixmap:
#             return

#         user_name = self.user_combo.currentText().replace(" ", "_")
#         today = datetime.now().strftime("%Y-%m-%d")
#         default_name = f"{user_name}_{today}.png"

#         file_path, _ = QFileDialog.getSaveFileName(
#             self, "Save QR", default_name, "PNG Files (*.png)"
#         )

#         if file_path:
#             self.current_qr_pixmap.save(file_path, "PNG")
#             QMessageBox.information(self, "Saved", "QR saved successfully")

#     def print_qr(self):
#         if not self.current_qr_pixmap:
#             return

#         printer = QPrinter()
#         dialog = QPrintDialog(printer, self)
#         if dialog.exec_() == QPrintDialog.Accepted:
#             painter = QPainter(printer)
#             rect = painter.viewport()
#             scaled = self.current_qr_pixmap.scaled(
#                 rect.size(), Qt.KeepAspectRatio
#             )
#             painter.drawPixmap(0, 0, scaled)
#             painter.end()


from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog,
    QMessageBox, QLineEdit, QDateEdit, QComboBox
)
from PyQt5.QtGui import QFont, QPainter
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from datetime import datetime
from services.qr_service import generate_monthly_qr
from db.database import get_db


class GenerateQR(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generate QR (Date Range)")
        self.resize(500, 620)

        self.current_qr_pixmap = None

        # Fonts
        self.label_font = QFont("Arial", 12, QFont.Bold)

        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search user by name...")
        self.search_input.setMinimumHeight(36)
        self.search_input.textChanged.connect(self.filter_users)

        # User combo
        self.user_combo = QComboBox()
        self.user_combo.setMinimumHeight(36)

        self.load_users()

        # Start Date
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        self.start_date.setMinimumHeight(36)

        # End Date
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setMinimumHeight(36)

        # QR display
        self.qr_label = QLabel("QR will appear here")
        self.qr_label.setFixedSize(300, 300)
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setStyleSheet("border:1px solid black;")
        self.qr_label.setScaledContents(True)

        # 🔹 QR info (Name + Date)
        self.qr_info_label = QLabel("")
        self.qr_info_label.setAlignment(Qt.AlignCenter)
        self.qr_info_label.setFont(QFont("Arial", 10, QFont.Bold))

        # Buttons
        self.gen_btn = QPushButton("Generate QR")
        self.gen_btn.clicked.connect(self.generate)

        self.download_btn = QPushButton("Download QR")
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.download_qr)

        self.print_btn = QPushButton("Print QR")
        self.print_btn.setEnabled(False)
        self.print_btn.clicked.connect(self.print_qr)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(12)

        layout.addWidget(self.search_input)

        lbl = QLabel("Select User")
        lbl.setFont(self.label_font)
        layout.addWidget(lbl)
        layout.addWidget(self.user_combo)

        lbl = QLabel("Start Date")
        lbl.setFont(self.label_font)
        layout.addWidget(lbl)
        layout.addWidget(self.start_date)

        lbl = QLabel("End Date")
        lbl.setFont(self.label_font)
        layout.addWidget(lbl)
        layout.addWidget(self.end_date)

        layout.addWidget(self.gen_btn)
        layout.addWidget(self.qr_label)
        layout.addWidget(self.qr_info_label)

        btns = QHBoxLayout()
        btns.addWidget(self.download_btn)
        btns.addWidget(self.print_btn)
        layout.addLayout(btns)

    # ---------- DB ----------
    def load_users(self):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM users ORDER BY name")
        self.users = cur.fetchall()
        conn.close()
        self.refresh_user_combo()

    def refresh_user_combo(self):
        self.user_combo.clear()
        for uid, name in self.users:
            self.user_combo.addItem(name, uid)

    def filter_users(self, text):
        self.user_combo.clear()
        for uid, name in self.users:
            if text.lower() in name.lower():
                self.user_combo.addItem(name, uid)

    # ---------- ACTIONS ----------
    def generate(self):
        if self.user_combo.count() == 0:
            QMessageBox.warning(self, "Error", "No user selected")
            return

        if self.start_date.date() > self.end_date.date():
            QMessageBox.warning(self, "Error", "Start date cannot be after End date")
            return

        user_id = self.user_combo.currentData()
        user_name = self.user_combo.currentText()

        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")

        try:
            pixmap = generate_monthly_qr(
                user_id=user_id,
                month=None,
                year=None,
                user_name=user_name,
                start_date=start_date,
                end_date=end_date
            )

            self.current_qr_pixmap = pixmap
            self.qr_label.setPixmap(pixmap)

            # 🔹 Show name + date below QR
            self.qr_info_label.setText(
                f"{user_name}\n{start_date} to {end_date}"
            )

            self.download_btn.setEnabled(True)
            self.print_btn.setEnabled(True)

            QMessageBox.information(self, "Success", "Date Range QR Generated")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def download_qr(self):
        if not self.current_qr_pixmap:
            return

        user_name = self.user_combo.currentText().replace(" ", "_")
        today = datetime.now().strftime("%Y-%m-%d")
        default_name = f"{user_name}_{today}.png"

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save QR", default_name, "PNG Files (*.png)"
        )

        if file_path:
            self.current_qr_pixmap.save(file_path, "PNG")
            QMessageBox.information(self, "Saved", "QR saved successfully")

    def print_qr(self):
        if not self.current_qr_pixmap:
            return

        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter(printer)
            rect = painter.viewport()

            # Space for text
            qr_height = rect.height() - 80

            # Draw QR
            scaled = self.current_qr_pixmap.scaled(
                rect.width(), qr_height, Qt.KeepAspectRatio
            )
            painter.drawPixmap(
                (rect.width() - scaled.width()) // 2,
                0,
                scaled
            )

            # Draw text below QR
            painter.setFont(QFont("Arial", 12, QFont.Bold))
            painter.drawText(
                rect,
                Qt.AlignHCenter | Qt.AlignBottom,
                self.qr_info_label.text()
            )

            painter.end()
