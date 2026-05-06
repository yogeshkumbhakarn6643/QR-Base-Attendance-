from datetime import date
from db.database import get_db, get_meal_price
from services.billing_service import deduct_amount

def run_daily_deduction():
    today = date.today().isoformat()
    conn = get_db()
    cur = conn.cursor()

    # 1️⃣ Check if already run today
    cur.execute("SELECT log_date FROM system_log WHERE log_date=?", (today,))
    if cur.fetchone():
        print("⚠ Deduction already processed today")
        conn.close()
        return

    # 2️⃣ Get meal price
    price = get_meal_price()

    # 3️⃣ Fetch all users
    cur.execute("SELECT id FROM users")
    users = cur.fetchall()

    # 4️⃣ Deduct for each user
    for (user_id,) in users:
        # Check if leave approved today
        cur.execute("""
            SELECT session FROM leaves
            WHERE user_id=? AND date=? AND status='approved'
        """, (user_id, today))
        leave = cur.fetchone()
        if leave:
            leave_session = leave[0]
            # If leave covers full day or both sessions, skip
            if leave_session in ["morning", "night", "both"]:
                continue

        # Deduct full meal amount
        deduct_amount(user_id, price)

    # 5️⃣ Log today
    cur.execute("INSERT INTO system_log (log_date) VALUES (?)", (today,))
    conn.commit()
    conn.close()

    print("✅ Daily deduction completed")
