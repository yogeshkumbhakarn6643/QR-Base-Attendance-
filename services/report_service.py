from db.database import get_db


def all_users_report(user_type=None):
    conn = get_db()
    cur = conn.cursor()

    query = """
        SELECT 
            u.id,
            u.name,
            u.mobile,
            u.user_type,
            IFNULL(w.balance, 0)
        FROM users u
        LEFT JOIN wallet w ON w.user_id = u.id
    """
    params = []

    if user_type:
        query += " WHERE u.user_type=?"
        params.append(user_type)

    query += " ORDER BY u.name"

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows


def low_balance_users(limit=500, user_type=None):
    conn = get_db()
    cur = conn.cursor()

    query = """
        SELECT 
            u.id,
            u.name,
            u.mobile,
            u.user_type,
            w.balance
        FROM wallet w
        JOIN users u ON u.id = w.user_id
        WHERE w.balance < ?
    """
    params = [limit]

    if user_type:
        query += " AND u.user_type=?"
        params.append(user_type)

    query += " ORDER BY w.balance"

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_user(user_id):
    """
    Permanently delete a user and all related data:
    wallet, attendance, leaves, payments.
    """
    conn = get_db()
    cur = conn.cursor()

    # Delete related data first
    cur.execute("DELETE FROM wallet WHERE user_id=?", (user_id,))
    cur.execute("DELETE FROM attendance WHERE user_id=?", (user_id,))
    cur.execute("DELETE FROM leaves WHERE user_id=?", (user_id,))
    cur.execute("DELETE FROM payments WHERE user_id=?", (user_id,))

    # Delete user
    cur.execute("DELETE FROM users WHERE id=?", (user_id,))

    conn.commit()
    conn.close()

