from db.database import get_db


def update_meal_price(new_price):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE settings SET meal_price = ? WHERE id = 1", (new_price,))
    conn.commit()
    conn.close()


def get_meal_price():
    from db.database import get_meal_price
    return get_meal_price()
