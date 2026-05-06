from db.database import get_db


def user_attendance_report(
    user_name=None,
    start_date=None,
    end_date=None
):
    conn = get_db()
    cur = conn.cursor()

    query = """
        SELECT
            u.id,
            u.name,
            a.date,
            a.session,
            COALESCE(a.status, 'absent') AS attendance_status,
            COALESCE(l.status, '-') AS leave_status
        FROM users u
        LEFT JOIN attendance a
            ON u.id = a.user_id
        LEFT JOIN leaves l
            ON u.id = l.user_id
            AND l.date = a.date
    """

    conditions = []
    params = []

    if user_name:
        conditions.append("u.name LIKE ?")
        params.append(f"%{user_name}%")

    if start_date:
        conditions.append("a.date >= ?")
        params.append(start_date)

    if end_date:
        conditions.append("a.date <= ?")
        params.append(end_date)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY a.date DESC, u.name"

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows
