# from db.database import get_db, get_meal_price
# from services.billing_service import deduct_amount
# from services.wallet_service import get_wallet_balance


# def mark_tiffin_attendance(user_ids, attend_date, session):
#     conn = get_db()
#     cur = conn.cursor()
#     meal_price = get_meal_price()

#     success = []
#     failed = []

#     for user_id in user_ids:

#         # 1️⃣ Already marked?
#         cur.execute("""
#             SELECT id FROM attendance
#             WHERE user_id=? AND date=? AND session=?
#         """, (user_id, attend_date, session))
#         if cur.fetchone():
#             failed.append(user_id)
#             continue

#         # 2️⃣ Approved leave check (SAME as direct meal)
#         amount = meal_price
#         cur.execute("""
#             SELECT session FROM leaves
#             WHERE user_id=? AND date=? AND status='approved'
#         """, (user_id, attend_date))
#         row = cur.fetchone()
#         if row:
#             leave_session = row[0]
#             if leave_session in ("both", session):
#                 amount = 0

#         # 3️⃣ Wallet check
#         if amount > 0:
#             balance = get_wallet_balance(user_id)
#             if balance < amount:
#                 failed.append(user_id)
#                 continue

#             if not deduct_amount(cur, user_id, amount):
#                 failed.append(user_id)
#                 continue

#         # 4️⃣ Save attendance
#         cur.execute("""
#             INSERT INTO attendance (user_id, date, session, amount, status)
#             VALUES (?, ?, ?, ?, 'present')
#         """, (user_id, attend_date, session, amount))

#         success.append(user_id)

#     conn.commit()
#     conn.close()

#     return success, failed


from datetime import date
from db.database import get_db, get_meal_price
from services.billing_service import deduct_amount
from services.wallet_service import get_wallet_balance


def mark_tiffin_attendance(user_id, selected_date, session):
    """
    Manually mark attendance for TIFFIN users only
    """

    conn = get_db()
    cur = conn.cursor()

    # 🔹 Verify user type
    cur.execute("SELECT user_type FROM users WHERE id=?", (user_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False, "Invalid user"

    if row[0] != "Tiffin":
        conn.close()
        return False, "Only tiffin users allowed here"

    # 🔹 Check already marked
    cur.execute("""
        SELECT id FROM attendance
        WHERE user_id=? AND date=? AND session=?
    """, (user_id, selected_date, session))
    if cur.fetchone():
        conn.close()
        return False, "Attendance already marked"

    meal_price = get_meal_price()
    amount = meal_price

    # 🔹 Leave check
    cur.execute("""
        SELECT session FROM leaves
        WHERE user_id=? AND date=? AND status='approved'
    """, (user_id, selected_date))
    row = cur.fetchone()
    if row and row[0] in ("both", session):
        amount = 0

    # 🔹 Wallet deduction
    if amount > 0:
        balance = get_wallet_balance(user_id)
        if balance < amount:
            conn.close()
            return False, "Insufficient balance"

        if not deduct_amount(cur, user_id, amount):
            conn.close()
            return False, "Wallet deduction failed"

    # 🔹 Insert attendance
    cur.execute("""
        INSERT INTO attendance (user_id, date, session, amount, status)
        VALUES (?, ?, ?, ?, 'present')
    """, (user_id, selected_date, session, amount))

    conn.commit()
    conn.close()

    return True, "Attendance marked successfully"
