from db import create_db_connection
from db_tables import create_tables
from insert_menu import insert_menu_items,insert_stock_items
from payment import calculate_bill
from menu_fetch import fetch_menu
from stocks_check import check_stock
from stock_update import update_stock
from fast_food_order import process_fast_food_order
from desi_food_order import process_desi_food_order

db = create_db_connection()
cursor = db.cursor()

create_tables(cursor)

insert_menu_items(cursor)
insert_stock_items(cursor)

db.commit()

def main():
    while True:
        ordered_items = []
        user_choice = input("Please select a category (fast food / desi food / fast food stock / desi food stock / exit): ").lower()

        if user_choice == "fast food":
            menu = fetch_menu(cursor, "fast_food")
            print("Fast Food Menu:", menu)
            order_item = input("Please select an item from the menu or type 'done' to finish: ").lower()
            while order_item != "done":
                if order_item in menu:
                    process_fast_food_order(cursor, order_item, ordered_items)
                else:
                    print("Invalid item selection. Please select from the menu.")
                order_item = input("Please select another item or type 'done' to finish: ").lower()
            if ordered_items:
                calculate_bill(ordered_items)

        elif user_choice == "desi food":
            menu = fetch_menu(cursor, "desi_food")
            print("Desi Food Menu:", menu)
            order_item = input("Please select an item from the menu or type 'done' to finish: ").lower()
            while order_item != "done":
                if order_item in menu:
                    process_desi_food_order(cursor, order_item, ordered_items)
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
