from db.database import get_db
from datetime import datetime


def get_wallet_balance(user_id=None):
    """
    If user_id is provided → return that user's balance
    If not provided → return 0 (safe default, avoids crash)
    """
    if user_id is None:
        return 0.0

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT balance FROM wallet WHERE user_id = ?",
        (user_id,)
    )
    row = cur.fetchone()
    conn.close()

    return row[0] if row else 0.0


def add_payment(user_id, amount, mode="cash"):
    conn = get_db()
    cur = conn.cursor()

    # Save payment history
    cur.execute("""
        INSERT INTO payments (user_id, amount, date, mode)
        VALUES (?, ?, ?, ?)
    """, (user_id, amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), mode))

    # Update wallet
    cur.execute("""
        INSERT INTO wallet (user_id, balance)
        VALUES (?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET balance = balance + ?
    """, (user_id, amount, amount))

    conn.commit()
    conn.close()


def get_payment_history(user_id=None):
    conn = get_db()
    cur = conn.cursor()
    if user_id:
        cur.execute("""
            SELECT id, user_id, amount, date, mode
            FROM payments
            WHERE user_id = ?
            ORDER BY date DESC
        """, (user_id,))
    else:
        cur.execute("""
            SELECT id, user_id, amount, date, mode
            FROM payments
            ORDER BY date DESC
        """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_total_wallet_balance():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT SUM(balance) FROM wallet")
    total = cur.fetchone()[0] or 0
    conn.close()
    return total