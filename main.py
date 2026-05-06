import sys
import cv2
import json
import os
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QApplication, QFrame
)
from datetime import datetime
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl
from services.attendance_service import mark_attendance
from ui.register_user import RegisterUser
from ui.generate_qr import GenerateQR
from ui.admin_reports import AdminReports
from ui.leave_management import LeaveManagement
from ui.add_payment import AddPayment
from ui.update_meal_price import UpdateMealPrice
from ui.payment_history import PaymentHistory
from db.database import create_tables
from ui.tiffin_attendance_ui import TiffinAttendanceUI
from ui.user_attendance_report import UserAttendanceReport
from services.attendance_service import auto_mark_yesterday_absent


if __name__ == "__main__":
    create_tables()
    auto_mark_yesterday_absent()   # 🔥 YESTERDAY AUTO ABSENT + DEDUCTION


def resource_path(relative_path):
    """
    Get absolute path to resource (works for dev & PyInstaller EXE)
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mess Attendance System")
        # 🚀 Full screen but taskbar visible
        # self.showMaximized()
        

        # ------------------ MAIN LAYOUT ------------------
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ------------------ LEFT SIDEBAR ------------------
        sidebar = QFrame()
        sidebar.setFixedWidth(320)
        sidebar.setStyleSheet("background:#2c3e50;")

        side_layout = QVBoxLayout(sidebar)
        side_layout.setAlignment(Qt.AlignTop)
        side_layout.setContentsMargins(15, 15, 15, 15)
        side_layout.setSpacing(12)

        # Buttons: text and method
        btn_info = [
            ("Register User", self.open_register),
            ("Add User Payment", self.open_add_payment),
            ("Generate Monthly QR", self.open_qr),
            ("Scan Morning", lambda: self.start_camera("morning")),
            ("Scan Night", lambda: self.start_camera("night")),
            ("Stop Camera", self.stop_camera),   # <-- NEW BUTTON
            ("Tiffin Attendance", self.open_tiffin_attendance),
            ("All Users Report", self.open_all_users),
            ("Low Balance Users", self.open_low_balance),
            ("Manage Leaves", self.open_leave_management),
            ("Update Meal Price", self.open_update_meal_price),
            ("Payment History", self.open_payment_history),
            ("User Attendance Report", self.open_attendance_report),
        ]

        for text, func in btn_info:
            btn = QPushButton(text)
            btn.setFixedHeight(45)
            btn.setStyleSheet("""
                QPushButton {
                    color: white;
                    background: #34495e;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: #1abc9c;
                }
            """)
            btn.clicked.connect(func)
            side_layout.addWidget(btn)
            
        # ---- PUSH CONTENT TO BOTTOM ----
        side_layout.addStretch()

        # ---- POWERED BY TEXT ----
        footer = QLabel("Powered by yogeshkumbhakarn6643@gmail.com")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("""
            QLabel {
                color: #bdc3c7;
                font-size: 10px;
            }
        """)
        side_layout.addWidget(footer)

        # ------------------ RIGHT CAMERA PANEL ------------------
        self.camera_panel = QLabel("Camera will open here")
        self.camera_panel.setAlignment(Qt.AlignCenter)
        self.camera_panel.setStyleSheet("""
            border: 2px solid gray;
            font-size: 16px;
            background-color: #f4f4f4;
        """)
        # self.camera_panel.setMinimumSize(640, 480)
        self.camera_panel.setMinimumSize(520, 380)

        # Add left & right panels
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.camera_panel, 1)

        # ------------------ CAMERA VARIABLES ------------------
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_frame)
        self.scan_type = None
        
        # ------------------ Success sound ------------------
        self.success_sound = QSoundEffect()

        sound_path = resource_path("sounds/success.wav")
        self.success_sound.setSource(QUrl.fromLocalFile(sound_path))
        self.success_sound.setVolume(0.8)
    
    def start_camera(self, scan_type):
        self.scan_type = scan_type
        if not self.cap:
            self.cap = cv2.VideoCapture(0)
        self.timer.start(30)  # scan every 30 ms

    def stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        self.camera_panel.setText("Camera stopped")
    
    def _pause_scan_1s(self):
        """Pause QR scanning for 1 second to avoid double scans."""
        self._pause_scan = True
        QTimer.singleShot(2000, lambda: setattr(self, "_pause_scan", False))

    def read_frame(self):
        # If camera not started or currently paused
        if not self.cap or getattr(self, "_pause_scan", False):
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.resize(frame, (self.camera_panel.width(), self.camera_panel.height()))

        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(frame)

        # Show live camera feed
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.camera_panel.setPixmap(QPixmap.fromImage(img))

        if not data:
            return

        try:
            qr = json.loads(data)
            start_date_str = qr.get("start_date")
            end_date_str = qr.get("end_date")

            if not start_date_str or not end_date_str:
                return  # Invalid QR, ignore

            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            today = datetime.now().date()

            if not (start_date <= today <= end_date):
                self.show_temp_message(f"QR expired: {start_date} to {end_date}")
                self._pause_scan_1s()
                return

            user_id = qr.get("user_id") or qr.get("use_id")
            user_name = qr.get("user_name")
            if not user_id or not user_name:
                self.show_temp_message("Invalid QR")
                self._pause_scan_1s()
                return
            
            # Mark attendance
            result = mark_attendance(user_id, user_name, self.scan_type)
            self.show_temp_message(result)

            # 🔊 Play success sound only for actual deduction
            if result.startswith("Attendance marked"):
                QTimer.singleShot(50, self.success_sound.play)

            # Pause 1 second after scan
            self._pause_scan_1s()

        except Exception as e:
            self.show_temp_message(f"Error: {str(e)}")
            self._pause_scan_1s()

    # ------------------ TEMP MESSAGE ------------------
    def show_temp_message(self, message, duration=2000):
        """Show message on camera panel for short time (ms)."""
        self.camera_panel.setText(message)
        QTimer.singleShot(duration, lambda: self.camera_panel.setText("Camera ready to scan"))

    # ------------------ BUTTON METHODS ------------------
    def open_register(self):
        self.reg = RegisterUser()
        self.reg.show()

    def open_qr(self):
        self.qr = GenerateQR()
        self.qr.show()

    def open_all_users(self):
        self.report_window = AdminReports()
        self.report_window.show()

    def open_low_balance(self):
        self.report_window = AdminReports(mode="low")
        self.report_window.show()

    def open_leave_management(self):
        self.leave_window = LeaveManagement()
        self.leave_window.show()

    def open_add_payment(self):
        self.add_payment_win = AddPayment()
        self.add_payment_win.show()

    def open_update_meal_price(self):
        self.update_price_win = UpdateMealPrice()
        self.update_price_win.show()

    def open_payment_history(self):
        self.payment_history_window = PaymentHistory()
        self.payment_history_window.show()

    def open_tiffin_attendance(self):
        self.tiffin_window = TiffinAttendanceUI()
        self.tiffin_window.show()

    def open_attendance_report(self):
        self.att_report = UserAttendanceReport()
        self.att_report.show()

    # ------------------ CLOSE EVENT ------------------
    def closeEvent(self, event):
        self.stop_camera()

        try:
            from db.database import backup_db
            backup_db()
        except Exception as e:
            print("DB backup failed:", e)

        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    # 🚫 Do NOT call window.show() again
    window.showMaximized()
    sys.exit(app.exec_())
