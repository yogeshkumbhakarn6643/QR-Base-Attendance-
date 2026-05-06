from db.database import get_db
from datetime import date


def user_wallet_report():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT u.id, u.name, u.mobile, IFNULL(w.balance, 0)
        FROM users u
        LEFT JOIN wallet w ON u.id = w.user_id
        ORDER BY u.name
    """)

    data = cur.fetchall()
    conn.close()
    return data


def daily_collection(report_date=None):
    if not report_date:
        report_date = date.today().isoformat()

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*), IFNULL(SUM(amount), 0)
        FROM attendance
        WHERE date = ?
    """, (report_date,))

    result = cur.fetchone()
    conn.close()
    return result


def monthly_collection(year, month):
    month = f"{month:02d}"
    pattern = f"{year}-{month}%"

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*), IFNULL(SUM(amount), 0)
        FROM attendance
        WHERE date LIKE ?
    """, (pattern,))

    result = cur.fetchone()
    conn.close()
    return result


def attendance_report(report_date):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT u.name, a.session, a.amount, a.status
        FROM attendance a
        JOIN users u ON u.id = a.user_id
        WHERE a.date = ?
    """, (report_date,))

    data = cur.fetchall()
    conn.close()
    return data


def low_balance_users(threshold=100):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT u.name, u.mobile, w.balance
        FROM wallet w
        JOIN users u ON u.id = w.user_id
        WHERE w.balance < ?
    """, (threshold,))

    data = cur.fetchall()
    conn.close()
    return data
