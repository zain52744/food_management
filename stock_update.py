def update_stock(cursor, item_name):
    query = "UPDATE stock SET quantity = quantity - 1 WHERE item_name = %s"
    cursor.execute(query, (item_name,))
