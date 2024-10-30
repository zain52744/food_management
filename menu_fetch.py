def fetch_menu(cursor,category):
    query = "SELECT item_name, price FROM menu WHERE category = %s"
    cursor.execute(query, (category,))
    results = cursor.fetchall()
    return dict(results)