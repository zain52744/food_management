from menu_fetch import fetch_menu
from stocks_check import check_stock
from stock_update import update_stock

def process_fast_food_order(cursor,item, ordered_items):
    if item in ["chicken_burger", "zinger_burger"]:
        stock = check_stock(cursor,"chicken")
        if stock > 0:
            print("Wait sir, your order is in process.")
            update_stock(cursor,"chicken")
           
            ordered_items.append((item, fetch_menu(cursor, "fast_food")[item]))  # Pass cursor here
            print(f"Updated chicken stock: {check_stock(cursor,'chicken')} kg")
        else:
            print("Sir, we are sorry, the chicken is out of stock.")
    elif item == "beef_burger":
        stock = check_stock(cursor,"beef")
        if stock > 0:
            print("Wait sir, your order is in process.")
            update_stock(cursor,"beef")

            ordered_items.append((item, fetch_menu(cursor, "fast_food")[item]))  
            print(f"Updated beef stock: {check_stock(cursor,'beef')} kg")
        else:
            print("Sir, we are sorry, the beef is out of stock.")
    else:
        print("Sorry, this item is not available in the menu.")