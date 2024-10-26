food_menu = {
    "fast_food": {"zinger_burger": 300,"chicken_burger": 350,"beef_burger": 700},
    "desi_food": {"chicken_karahi": 1500,"beef_karahi": 1700,"mutton_karahi": 2000}
}

stock = {"fast_food_stock": {"chicken": 5,  "beef": 5 },"desi_food_stock": {"chicken": 5, "beef": 5,  "mutton": 5}}

def process_fast_food_order(item, ordered_items):
    if item == "chicken_burger" or item == "zinger_burger":
        if stock["fast_food_stock"]["chicken"] > 0:
            print("Wait sir, your order is in process.")
            stock["fast_food_stock"]["chicken"] -= 1
            ordered_items.append((item, food_menu["fast_food"][item]))
            print(f"Updated chicken stock: {stock['fast_food_stock']['chicken']}kg")
        else:
            print("Sir, we are sorry, the chicken is out of stock.")
    elif item == "beef_burger":
        if stock["fast_food_stock"]["beef"] > 0:
            print("Wait sir, your order is in process.")
            stock["fast_food_stock"]["beef"] -= 1
            ordered_items.append((item, food_menu["fast_food"][item]))
            print(f"Updated beef stock: {stock['fast_food_stock']['beef']}kg")
        else:
            print("Sir, we are sorry, the beef is out of stock.")
    else:
        print("Sorry, this item is not available in the menu.")

def process_desi_food_order(item, ordered_items):
    if item == "chicken_karahi":
        if stock["desi_food_stock"]["chicken"] > 0:
            print("Wait sir, your order is in process.")
            stock["desi_food_stock"]["chicken"] -= 1
            ordered_items.append((item, food_menu["desi_food"][item]))
            print(f"Updated chicken stock: {stock['desi_food_stock']['chicken']}kg")
        else:
            print("Sir, we are sorry, the chicken is out of stock.")
    elif item == "beef_karahi":
        if stock["desi_food_stock"]["beef"] > 0:
            print("Wait sir, your order is in process.")
            stock["desi_food_stock"]["beef"] -= 1
            ordered_items.append((item, food_menu["desi_food"][item]))
            print(f"Updated beef stock: {stock['desi_food_stock']['beef']}kg")
        else:
            print("Sir, we are sorry, the beef is out of stock.")
    elif item == "mutton_karahi":
        if stock["desi_food_stock"]["mutton"] > 0:
            print("Wait sir, your order is in process.")
            stock["desi_food_stock"]["mutton"] -= 1
            ordered_items.append((item, food_menu["desi_food"][item]))
            print(f"Updated mutton stock: {stock['desi_food_stock']['mutton']}kg")
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
            print("Fast Food Menu:", food_menu["fast_food"])
            order_item = input("Please select an item from the menu (zinger_burger / chicken_burger / beef_burger) or type 'done' to finish: ").lower()
            while order_item != "done":
                if order_item in food_menu["fast_food"]:
                    process_fast_food_order(order_item, ordered_items)
                else:
                    print("Invalid item selection. Please select from the menu.")
                order_item = input("Please select another item or type 'done' to finish: ").lower()
            if ordered_items:
                calculate_bill(ordered_items)

        elif user_choice == "desi food":
            print("Desi Food Menu:", food_menu["desi_food"])
            order_item = input("Please select an item from the menu (chicken_karahi / beef_karahi / mutton_karahi) or type 'done' to finish: ").lower()
            while order_item != "done":
                if order_item in food_menu["desi_food"]:
                    process_desi_food_order(order_item, ordered_items)
                else:
                    print("Invalid item selection. Please select from the menu.")
                order_item = input("Please select another item or type 'done' to finish: ").lower()
            if ordered_items:
                calculate_bill(ordered_items)

        elif user_choice == "fast food stock":
            print("Fast Food Stock:", stock["fast_food_stock"])

        elif user_choice == "desi food stock":
            print("Desi Food Stock:", stock["desi_food_stock"])

        elif user_choice == "exit":
            print("Thank you for using the food management system.")
            break
        else:
            print("Invalid choice. Please select either 'fast food', 'desi food', 'fast food stock', or 'desi food stock'.")


if __name__ == "__main__":
    main()