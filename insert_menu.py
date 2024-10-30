
menu_items = {
    'fast_food': {'zinger_burger': 300, 'chicken_burger': 350, 'beef_burger': 700},
    'desi_food': {'chicken_karahi': 1500, 'beef_karahi': 1700, 'mutton_karahi': 2000}
}

stock_items = {
    'fast_food': {'chicken': 5, 'beef': 5},
    'desi_food': {'chicken': 5, 'beef': 5, 'mutton': 5}
}

def insert_menu_items(cursor):
    """Inserts menu items into the database."""
    for category, items in menu_items.items():
        for item_name, price in items.items():
            cursor.execute(
                "INSERT INTO menu (category, item_name, price) VALUES (%s, %s, %s)", 
                (category, item_name, price)
            )

def insert_stock_items(cursor):
    """Inserts stock items into the database."""
    for category, items in stock_items.items():
        for item_name, quantity in items.items():
            cursor.execute(
                "INSERT INTO stock (category, item_name, quantity) VALUES (%s, %s, %s)", 
                (category, item_name, quantity)
            )
