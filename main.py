import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="F4d220190@"
)

cursor = db.cursor()


cursor.execute("CREATE DATABASE IF NOT EXISTS food_management")
cursor.execute("USE food_management")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS menu (
        id INT AUTO_INCREMENT PRIMARY KEY,
        category VARCHAR(50),
        item_name VARCHAR(50),
        price INT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock (
        id INT AUTO_INCREMENT PRIMARY KEY,
        category VARCHAR(50),
        item_name VARCHAR(50),
        quantity INT
    )
""")


menu_items = {'fast_food': {'zinger_burger': 300,'chicken_burger': 350,'beef_burger': 700},
            'desi_food': {'chicken_karahi': 1500,'beef_karahi': 1700,'mutton_karahi': 2000}}

stock_items = {'fast_food': {'chicken': 5,'beef': 5,},'desi_food': {'chicken': 5,'beef': 5,'mutton': 5,}}

def insert_menu_items(menu):
    for category, items in menu.items():
        for item_name, price in items.items():
            cursor.execute("INSERT INTO menu (category, item_name, price) VALUES (%s, %s, %s)", (category, item_name, price))


def insert_stock_items(stock):
    for category, items in stock.items():
        for item_name, quantity in items.items():
            cursor.execute("INSERT INTO stock (category, item_name, quantity) VALUES (%s, %s, %s)", (category, item_name, quantity))


insert_menu_items(menu_items)
insert_stock_items(stock_items)

db.commit()

def fetch_menu(category):
    query = "SELECT item_name, price FROM menu WHERE category = %s"
    cursor.execute(query, (category,))
    results = cursor.fetchall()
    return dict(results)

def check_stock(item_name):
    query = "SELECT quantity FROM stock WHERE item_name = %s"
    cursor.execute(query, (item_name,))
    result = cursor.fetchone()
    cursor.fetchall()  
    return result[0] if result else 0

def update_stock(item_name):
    query = "UPDATE stock SET quantity = quantity - 1 WHERE item_name = %s"
    cursor.execute(query, (item_name,))
    db.commit()

def process_fast_food_order(item, ordered_items):
    if item in ["chicken_burger", "zinger_burger"]:
        stock = check_stock("chicken")
        if stock > 0:
            print("Wait sir, your order is in process.")
            update_stock("chicken")
            ordered_items.append((item, fetch_menu("fast_food")[item]))
            print(f"Updated chicken stock: {check_stock('chicken')} kg")
        else:
            print("Sir, we are sorry, the chicken is out of stock.")
    elif item == "beef_burger":
        stock = check_stock("beef")
        if stock > 0:
            print("Wait sir, your order is in process.")
            update_stock("beef")
            ordered_items.append((item, fetch_menu("fast_food")[item]))
            print(f"Updated beef stock: {check_stock('beef')} kg")
        else:
            print("Sir, we are sorry, the beef is out of stock.")
    else:
        print("Sorry, this item is not available in the menu.")

def process_desi_food_order(item, ordered_items):
    if item == "chicken_karahi":
        stock = check_stock("chicken")
        if stock > 0:
            print("Wait sir, your order is in process.")
            update_stock("chicken")
            ordered_items.append((item, fetch_menu("desi_food")[item]))
            print(f"Updated chicken stock: {check_stock('chicken')} kg")
        else:
            print("Sir, we are sorry, the chicken is out of stock.")
    elif item == "beef_karahi":
        stock = check_stock("beef")
        if stock > 0:
            print("Wait sir, your order is in process.")
            update_stock("beef")
            ordered_items.append((item, fetch_menu("desi_food")[item]))
            print(f"Updated beef stock: {check_stock('beef')} kg")
        else:
            print("Sir, we are sorry, the beef is out of stock.")
    elif item == "mutton_karahi":
        stock = check_stock("mutton")
        if stock > 0:
            print("Wait sir, your order is in process.")
            update_stock("mutton")
            ordered_items.append((item, fetch_menu("desi_food")[item]))
            print(f"Updated mutton stock: {check_stock('mutton')} kg")
        else:
            print("Sir, we are sorry, the mutton is out of stock.")
    else:
        print("Sorry, this item is not available in the menu.")

def calculate_bill(ordered_items):
    total = sum(price for item, price in ordered_items)
    print("\n----- Bill Summary -----")
    for item, price in ordered_items:
        print(f"{item.replace('_', ' ').title()}: {price} PKR")
    print(f"Total: {total} PKR")
    print("------------------------")

def main():
    while True:
        ordered_items = []
        user_choice = input("Please select a category (fast food / desi food / fast food stock / desi food stock / exit): ").lower()

        if user_choice == "fast food":
            menu = fetch_menu("fast_food")
            print("Fast Food Menu:", menu)
            order_item = input("Please select an item from the menu or type 'done' to finish: ").lower()
            while order_item != "done":
                if order_item in menu:
                    process_fast_food_order(order_item, ordered_items)
                else:
                    print("Invalid item selection. Please select from the menu.")
                order_item = input("Please select another item or type 'done' to finish: ").lower()
            if ordered_items:
                calculate_bill(ordered_items)

        elif user_choice == "desi food":
            menu = fetch_menu("desi_food")
            print("Desi Food Menu:", menu)
            order_item = input("Please select an item from the menu or type 'done' to finish: ").lower()
            while order_item != "done":
                if order_item in menu:
                    process_desi_food_order(order_item, ordered_items)
                else:
                    print("Invalid item selection. Please select from the menu.")
                order_item = input("Please select another item or type 'done' to finish: ").lower()
            if ordered_items:
                calculate_bill(ordered_items)

        elif user_choice == "fast food stock":
            query = "SELECT item_name, quantity FROM stock WHERE category = 'fast_food'"
            cursor.execute(query)
            print("Fast Food Stock:", dict(cursor.fetchall()))

        elif user_choice == "desi food stock":
            query = "SELECT item_name, quantity FROM stock WHERE category = 'desi_food'"
            cursor.execute(query)
            print("Desi Food Stock:", dict(cursor.fetchall()))

        elif user_choice == "exit":
            print("Thank you for using the food management system.")
            break
        else:
            print("Invalid choice. Please select either 'fast food', 'desi food', 'fast food stock', or 'desi food stock'.")

if __name__ == "__main__":
    main()
    db.close()
