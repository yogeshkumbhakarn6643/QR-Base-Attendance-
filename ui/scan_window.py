import cv2
import json
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap

from services.attendance_service import mark_attendance


class ScanWindow(QWidget):
    def __init__(self, scan_type):
        super().__init__()
        self.scan_type = scan_type

        self.setWindowTitle(f"{scan_type.capitalize()} Scan")
        self.resize(700, 550)

        layout = QVBoxLayout(self)

        title = QLabel(f"{scan_type.upper()} SCAN")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:18px;font-weight:bold;")
        layout.addWidget(title)

        self.camera_label = QLabel()
        self.camera_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.camera_label)

        self.cap = cv2.VideoCapture(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_frame)
        self.timer.start(30)

    def read_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(frame)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.camera_label.setPixmap(QPixmap.fromImage(img))

        if data:
            try:
                qr_data = json.loads(data)

                # ✅ FIX HERE
                if "user_id" not in qr_data:
                    raise ValueError("Invalid QR Code")

                user_id = qr_data["user_id"]

                result = mark_attendance(user_id, self.scan_type)

                QMessageBox.information(
                    self,
                    "Result",
                    result
                )
                self.close()

            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
                self.close()

    def closeEvent(self, event):
        self.timer.stop()
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        event.accept()
