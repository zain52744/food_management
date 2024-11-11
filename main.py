from categories import Categories
from menu import Menu
from customer import Customer
from order import Order
from stock import Stock
from bill import Bill  
from database import DBhelper


food_menu = {
    "Fast Food": {"zinger_burger": 300, "chicken_burger": 350, "beef_burger": 700},
    "Desi Food": {"chicken_karahi": 1500, "beef_karahi": 1700, "mutton_karahi": 2000}
}

def initialize_tables(db):
    
    categories = Categories(db)
    categories.create_table()
    categories.insert_categories()

    menu = Menu(db)
    menu.create_table()
    menu.add_menu_items_from_dict(food_menu)

    customer = Customer(db)
    customer.create_table()

    order = Order(db)
    order.create_table()

    stock = Stock(db)
    stock.create_table()
    stock.insert_initial_stock()

    bill = Bill(db)
    bill.create_table()

def display_categories_and_get_choice(db):
    categories = Categories(db)
    category_list = categories.get_categories()

    if not category_list:
        print("No categories available.")
        return None

    print("Available categories:")
    for category in category_list:
        print(f"{category[0]}. {category[1]}")

    category_id = input("Please enter the number of the category you like to view: ").strip()

    if category_id.isdigit() and int(category_id) in [cat[0] for cat in category_list]:
        return int(category_id)
    else:
        print("Invalid selection. Please try again.")
        return None

def show_items_by_category(db, category_id):
    categories = Categories(db)
    category_name = [cat[1] for cat in categories.get_categories() if cat[0] == category_id][0]
    menu = Menu(db)
    menu.get_items_by_category(category_name)

def get_customer_details(db):
    name = input("Please enter your name: ").strip()
    info = input("Please enter your contact number: ").strip()

    if not name or not info:
        print("Name and contact information are required!")
        return None

    customer = Customer(db)
    customer.insert_customer(name, info)
    customer_id = customer.get_customer_id(name)
    return customer_id, name, info

def get_order_items(db, category_name):
    menu = Menu(db)
    menu_items = menu.get_items_by_category(category_name)
    stock = Stock(db)

    if not menu_items:
        print("No items available in this category.")
        return []

    print("\nAvailable menu items:")
    for idx, (item, price) in enumerate(menu_items.items(), start=1):
        print(f"{idx}. {item} - Rs. {price}")

    order_items = []
    while True:
        item_choice = input("\nEnter the number of the item you like to order (or 'done' to finish): ").strip()

        if item_choice.lower() == 'done':
            if order_items:
                break
            else:
                print("No items were selected.")
                break

        if item_choice.isdigit() and 1 <= int(item_choice) <= len(menu_items):
            item_name = list(menu_items.keys())[int(item_choice) - 1]

            if category_name == "Fast Food":
                required_quantity = 1  
                stock_deduction = 0.5  
            else:
                try:
                    required_quantity = float(input(f"Enter quantity in kg for {item_name}: ").strip())
                    stock_deduction = required_quantity
                except ValueError:
                    print("Invalid quantity. Please enter a valid number.")
                    continue

            if stock.check_stock(item_name, stock_deduction):
                order_items.append((item_name, required_quantity))
                stock.update_stock(item_name, stock_deduction)
            else:
                print(f"Insufficient stock for {item_name}.")
        else:
            print("Invalid selection. Please try again.")

    return order_items

def take_order(db, customer_id):
    all_order_items = []
    
    while True:
        category_id = display_categories_and_get_choice(db)
        if category_id:
            categories = Categories(db)
            category_name = [cat[1] for cat in categories.get_categories() if cat[0] == category_id][0]
            show_items_by_category(db, category_id)

            order_items = get_order_items(db, category_name)
            all_order_items.extend(order_items)

            continue_order = input("Would you like to order more items? (yes/no): ").strip().lower()
            if continue_order != 'yes':
                break
        else:
            print("Invalid category selected.")
            break

    return all_order_items

def main():
    db = DBhelper()  
    initialize_tables(db)  

    while True:
        customer_details = get_customer_details(db)
        if customer_details:
            customer_id, name, info = customer_details
            print(f"Thank you for your order, {name}!")

            
            all_order_items = take_order(db, customer_id)
            
            if all_order_items:
                order = Order(db)
                for item_name, quantity in all_order_items:
                    order.insert_order(customer_id, [item_name])
                
                
                bill = Bill(db)
                total_amount = bill.generate_bill(customer_id, all_order_items)
                print(f"Total Amount to Pay: Rs. {total_amount}")
        else:
            print("Failed to add customer. Please try again.")

        continue_session = input("Do you want to start a new session for another customer? (yes/no): ").strip().lower()
        if continue_session != 'yes':
            print("Thank you for using the system!")
            break

    db.close_connection()

if __name__ == "__main__":
    main()
