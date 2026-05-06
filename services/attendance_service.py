from datetime import date, timedelta
from db.database import get_db, get_meal_price
from services.billing_service import deduct_amount
from services.wallet_service import get_wallet_balance


def mark_attendance(user_id, name, session):
    today = date.today().isoformat()
    conn = get_db()
    cur = conn.cursor()

    # 🔹 Get user type
    cur.execute(
        "SELECT user_type FROM users WHERE id=? AND name=?",
        (user_id, name)
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        return "Invalid user"

    user_type = row[0]

    # ❌ Prevent tiffin user from QR scan
    if user_type == "Tiffin":
        conn.close()
        return "Tiffin users must be marked manually"

    # ---------- EXISTING LOGIC BELOW (UNCHANGED) ----------

    cur.execute("""
        SELECT id FROM attendance
        WHERE user_id=? AND date=? AND session=?
    """, (user_id, today, session))
    if cur.fetchone():
        conn.close()
        return "Attendance already marked"

    meal_price = get_meal_price()
    amount = meal_price

    cur.execute("""
        SELECT session FROM leaves
        WHERE user_id=? AND date=? AND status='approved'
    """, (user_id, today))
    row = cur.fetchone()
    if row:
        if row[0] in ("both", session):
            amount = 0

    if amount > 0:
        balance = get_wallet_balance(user_id)
        if balance < amount:
            conn.close()
            return "Insufficient balance – please recharge"

        if not deduct_amount(cur, user_id, amount):
            conn.close()
            return "Wallet deduction failed"

    cur.execute("""
        INSERT INTO attendance (user_id, date, session, amount, status)
        VALUES (?, ?, ?, ?, 'present')
    """, (user_id, today, session, amount))

    conn.commit()
    conn.close()

    return "Leave approved no deduction" if amount == 0 else f"Attendance marked – ₹{amount} deducted"


def auto_mark_yesterday_absent():
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    conn = get_db()
    cur = conn.cursor()

    meal_price = get_meal_price()
    sessions = ["morning", "night"]

    # Run only once per day
    cur.execute("""
        CREATE TABLE IF NOT EXISTS auto_attendance_log (
            date TEXT PRIMARY KEY
        )
    """)

    cur.execute("""
        SELECT 1 FROM auto_attendance_log WHERE date=?
    """, (yesterday,))
    if cur.fetchone():
        conn.close()
        return  # Already processed

    # Get Direct Meal users
    cur.execute("""
        SELECT id FROM users WHERE user_type='Direct Meal'
    """)
    users = cur.fetchall()

    for (user_id,) in users:

        # 🔹 FETCH ALL APPROVED LEAVES FOR USER (FIXED LOGIC)
        cur.execute("""
            SELECT session FROM leaves
            WHERE user_id=? AND date=? AND status='approved'
        """, (user_id, yesterday))

        leave_sessions = [row[0] for row in cur.fetchall()]

        for session in sessions:

            # Check attendance
            cur.execute("""
                SELECT 1 FROM attendance
                WHERE user_id=? AND date=? AND session=?
            """, (user_id, yesterday, session))
            if cur.fetchone():
                continue

            # ✅ Skip full-day leave
            if "both" in leave_sessions:
                continue

            # ✅ Skip only approved session
            if session in leave_sessions:
                continue

            # Deduct amount
            amount = 0
            balance = get_wallet_balance(user_id)
            if balance >= meal_price:
                deduct_amount(cur, user_id, meal_price)
                amount = meal_price

            # Mark ABSENT
            cur.execute("""
                INSERT INTO attendance (user_id, date, session, amount, status)
                VALUES (?, ?, ?, ?, 'absent')
            """, (user_id, yesterday, session, amount))

    # Log execution
    cur.execute("""
        INSERT INTO auto_attendance_log VALUES (?)
    """, (yesterday,))

    conn.commit()
    conn.close()
