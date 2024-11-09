def check_stock(cursor, item_name):
    query = "SELECT quantity FROM stock WHERE item_name = %s"
    cursor.execute(query, (item_name,))
    result = cursor.fetchone()
    cursor.fetchall()
    return result[0] if result else 0

