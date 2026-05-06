from datetime import date
from db.database import get_db


def add_payment(user_id, amount, mode="cash"):
    conn = get_db()
    cur = conn.cursor()

    # Add payment record
    cur.execute("""
        INSERT INTO payments (user_id, amount, date, mode)
        VALUES (?, ?, ?, ?)
    """, (user_id, amount, date.today().isoformat(), mode))

    # Update wallet
    cur.execute("""
        INSERT INTO wallet (user_id, balance)
        VALUES (?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET balance = balance + excluded.balance
    """, (user_id, amount))

    conn.commit()
    conn.close()


def deduct_amount(cur, user_id, amount):
    """
    Deduct amount using EXISTING cursor
    """
    if amount <= 0:
        return True

    cur.execute("""
        SELECT balance FROM wallet WHERE user_id = ?
    """, (user_id,))
    row = cur.fetchone()

    if not row or row[0] < amount:
        return False

    cur.execute("""
        UPDATE wallet
        SET balance = balance - ?
        WHERE user_id = ?
    """, (amount, user_id))

    return True
