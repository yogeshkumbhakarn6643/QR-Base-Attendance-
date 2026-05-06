# import qrcode
# import json
# from io import BytesIO
# from PyQt5.QtGui import QPixmap
# from db.database import get_db


# def generate_monthly_qr(user_id, month, year, user_name=None):
#     """
#     Generate monthly QR in MEMORY (no file saving)
#     Returns: QPixmap
#     """

#     month_names = [
#         "January", "February", "March", "April", "May", "June",
#         "July", "August", "September", "October", "November", "December"
#     ]

#     month_name = month_names[month - 1] if isinstance(month, int) else month

#     # Fetch username if not provided
#     if not user_name:
#         conn = get_db()
#         cur = conn.cursor()
#         cur.execute("SELECT name FROM users WHERE id=?", (user_id,))
#         row = cur.fetchone()
#         conn.close()
#         user_name = row[0] if row else f"user{user_id}"

#     qr_payload = {
#         "user_id": user_id,
#         "user_name": user_name,
#         "month": month_name,
#         "year": year,
#         "type": "monthly"
#     }

#     qr = qrcode.make(json.dumps(qr_payload))

#     # Save QR to memory
#     buffer = BytesIO()
#     qr.save(buffer, format="PNG")
#     buffer.seek(0)

#     pixmap = QPixmap()
#     pixmap.loadFromData(buffer.getvalue(), "PNG")

#     return pixmap

import qrcode
import json
from io import BytesIO
from PyQt5.QtGui import QPixmap
from db.database import get_db


def generate_monthly_qr(user_id, month=None, year=None, user_name=None, start_date=None, end_date=None):
    """
    Generate Date Range QR
    Returns: QPixmap
    """

    if not user_name:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT name FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()
        conn.close()
        user_name = row[0] if row else f"user{user_id}"

    qr_payload = {
        "user_id": user_id,
        "user_name": user_name,
        "start_date": start_date,
        "end_date": end_date,
        "type": "date_range"
    }

    qr = qrcode.make(json.dumps(qr_payload))

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    pixmap = QPixmap()
    pixmap.loadFromData(buffer.getvalue(), "PNG")

    return pixmap
