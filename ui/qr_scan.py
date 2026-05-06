# import cv2
# import json
# from services.attendance_service import mark_attendance


# def scan_qr(session="morning"):
#     """
#     Open camera, scan QR code, mark attendance for the user,
#     and respect approved leaves (no deduction).
#     """
#     print("Opening camera...")
#     cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow on Windows

#     if not cap.isOpened():
#         print("❌ Camera not opened")
#         return

#     print("✅ Camera opened")
#     detector = cv2.QRCodeDetector()

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("❌ Frame not read")
#             break

#         # Detect QR code
#         data, _, _ = detector.detectAndDecode(frame)

#         if data:
#             print("QR Data:", data)
#             try:
#                 qr = json.loads(data)
#                 mark_attendance(qr["user_id"], session)
#                 print(f"✅ Attendance marked for user_id {qr['user_id']} ({session})") # noqa
#             except Exception as e:
#                 print("❌ Error marking attendance:", e)
#             break  # Stop scanning after successful read

#         # Show live camera feed
#         cv2.imshow("QR Scanner (Press q to exit)", frame)

#         # Press 'q' to quit manually
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             print("Exit pressed")
#             break

#     # Release camera & close window
#     cap.release()
#     cv2.destroyAllWindows()


# if __name__ == "__main__":
#     scan_qr()

import cv2
import json
from datetime import datetime
from services.attendance_service import mark_attendance


def scan_qr(session="morning"):
    """
    Scan QR code and validate month/year before marking attendance
    """

    print("Opening camera...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("❌ Camera not opened")
        return

    print("✅ Camera opened")
    detector = cv2.QRCodeDetector()

    current_month = datetime.now().strftime("%B")  # e.g. "January"
    current_year = datetime.now().year              # e.g. 2026

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Frame not read")
            break

        data, _, _ = detector.detectAndDecode(frame)

        if data:
            print("QR Data:", data)
            try:
                qr = json.loads(data)

                qr_month = qr.get("month")
                qr_year = qr.get("year")
                user_id = qr.get("user_id")

                if not (qr_month and qr_year and user_id):
                    print("❌ Invalid QR data")
                    break

                # 🔒 Month & Year Validation
                if (
                    qr_month.lower() != current_month.lower()
                    or int(qr_year) != current_year
                ):
                    print("❌ QR Code Expired")
                    print(f"QR: {qr_month} {qr_year}")
                    print(f"Current: {current_month} {current_year}")
                    break

                # ✅ Valid QR
                mark_attendance(user_id, session)
                print(f"✅ Attendance marked for user_id {user_id} ({session})")

            except Exception as e:
                print("❌ Error:", e)

            break  # stop scanning after one QR

        cv2.imshow("QR Scanner (Press q to exit)", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Exit pressed")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    scan_qr()
