from categories import Categories
from menu import Menu
from customer import Customer
from order import Order  
from database import DBhelper


food_menu = {
    "Fast Food": {"zinger_burger": 300, "chicken_burger": 350, "beef_burger": 700},
    "Desi Food": {"chicken_karahi": 1500, "beef_karahi": 1700, "mutton_karahi": 2000}
}

def reset_tables():
    """Reset all tables by dropping them."""
    db = DBhelper()
    tables = ['orders', 'menu', 'customer', 'categories'] 
    for table in tables:
        query = f"DROP TABLE IF EXISTS {table}"
        db.execute_query(query)
        print(f"Table {table} has been dropped.")

def initialize_tables():
    
    reset_tables()

    
    categories = Categories()
    categories.create_table()
    categories.insert_categories()  # Insert default categories

    
    menu = Menu()
    menu.create_table()
    menu.add_menu_items_from_dict(food_menu)  
 
    customer = Customer()
    customer.create_table()  

    
    order = Order()
    order.create_table()  

def display_categories_and_get_choice():
    categories = Categories()
    category_list = categories.get_categories()

    if not category_list:
        print("No categories available.")
        return None

    print("Available categories:")
    for category in category_list:
        print(f"{category[0]}. {category[1]}")

    
    category_id = input("Please enter the number of the category you'd like to view: ").strip()
    
    
    if category_id.isdigit() and int(category_id) in [cat[0] for cat in category_list]:
        return int(category_id)
    else:
        print("Invalid selection. Please try again.")
        return None

def show_items_by_category(category_id):
    categories = Categories()
    category_name = [cat[1] for cat in categories.get_categories() if cat[0] == category_id][0]
    menu = Menu()
    menu.get_items_by_category(category_name)  

def get_customer_details():
    
    name = input("Please enter your name: ").strip()
    info = input("Please enter your contact number: ").strip()

    
    if not name or not info:
        print("Name and contact information are required!")
        return None

    
    customer = Customer()
    customer.insert_customer(name, info)  

    
    customer_id = customer.get_customer_id(name)
    return customer_id, name, info  

def get_order_items(category_name):
    
    menu = Menu()
    menu_items = menu.get_items_by_category(category_name)

    if not menu_items:
        print("No items available in this category.")
        return []

    print("\nAvailable menu items:")
    for idx, (item, price) in enumerate(menu_items.items(), start=1):
        print(f"{idx}. {item} - Rs. {price}")

    
    order_items = []
    while True:
        item_choice = input("\nEnter the number of the item you'd like to order (or 'done' to finish): ").strip()

        if item_choice.lower() == 'done':
            if not order_items:
                print("Please select at least one item before finishing.")
                continue
            break

        if item_choice.isdigit() and 1 <= int(item_choice) <= len(menu_items):
            item_name = list(menu_items.keys())[int(item_choice) - 1]
            order_items.append(item_name)
        else:
            print("Invalid selection. Please try again.")

    return order_items

if __name__ == "__main__":
    initialize_tables()

    
    category_id = display_categories_and_get_choice()
    if category_id:
        categories = Categories()
        category_name = [cat[1] for cat in categories.get_categories() if cat[0] == category_id][0]
        
        
        show_items_by_category(category_id)

        
        customer_details = get_customer_details()
        if customer_details:
            customer_id, name, info = customer_details
            print(f"Thank you for your order, {name}!")

            
            order_items = get_order_items(category_name)

            
            order = Order()
            order.insert_order(customer_id, order_items)
        else:
            print("Failed to add customer. Please try again.")
    else:
        print("No valid category selected.")
