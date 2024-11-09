from menu_fetch import fetch_menu
from stocks_check import check_stock
from stock_update import update_stock

# def process_desi_food_order(cursor, item, ordered_items):
#     if item == "chicken_karahi":
#         stock = check_stock(cursor, "chicken")
#         if stock > 0:
#             print("Wait sir, your order is in process.")
#             update_stock(cursor, "chicken")
#             ordered_items.append((item, fetch_menu(cursor, "desi_food")[item]))
#             print(f"Updated chicken stock: {check_stock(cursor, 'chicken')} kg")
#         else:
#             print("Sir, we are sorry, the chicken is out of stock.")

def process_desi_food_order(cursor, connection, item, ordered_items):
    if item == "chicken_karahi":
        stock = check_stock(cursor, "chicken")
        if stock > 0:
            print("Wait sir, your order is in process.")
            update_stock(cursor, connection, "chicken")  # Pass connection here
            ordered_items.append((item, fetch_menu(cursor, "desi_food")[item]))
            print(f"Updated chicken stock: {check_stock(cursor, 'chicken')} kg")
        else:
            print("Sir, we are sorry, the chicken is out of stock.")
    # Rest of the code...

    elif item == "beef_karahi":
        stock = check_stock(cursor, "beef")
        if stock > 0:
            print("Wait sir, your order is in process.")
            update_stock(cursor, "beef")
            ordered_items.append((item, fetch_menu(cursor, "desi_food")[item]))
            print(f"Updated beef stock: {check_stock(cursor, 'beef')} kg")
        else:
            print("Sir, we are sorry, the beef is out of stock.")
    elif item == "mutton_karahi":
        stock = check_stock(cursor, "mutton")
        if stock > 0:
            print("Wait sir, your order is in process.")
            update_stock(cursor, "mutton")
            ordered_items.append((item, fetch_menu(cursor, "desi_food")[item]))
            print(f"Updated mutton stock: {check_stock(cursor, 'mutton')} kg")
        else:
            print("Sir, we are sorry, the mutton is out of stock.")
    else:
        print("Sorry, this item is not available in the menu.")