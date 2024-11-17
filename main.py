from categories import Categories
from menu import Menu
from customer import Customer
from order import Order
from stock import Stock
from bill import Bill
from database import DBhelper
from order import Order

food_menu = {
    "Fast Food": {"zinger_burger": 300, "chicken_burger": 350, "beef_burger": 700},
    "Desi Food": {"chicken_karahi": 1500, "beef_karahi": 1700, "mutton_karahi": 2000}
}

def initialize_tables(db):
    try:
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

        print("Tables initialized successfully.")
    except Exception as e:
        print(f"Error initializing tables: {e}")

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
        item_choice = input("\nEnter the number of the item you want to order (or 'done' to finish): ").strip()

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
            else:
                try:
                    required_quantity = float(input(f"Enter quantity in kg for {item_name}: ").strip())
                except ValueError:
                    print("Invalid quantity. Please enter a valid number.")
                    continue

            result = stock.handle_order_stock(item_name, category_name, required_quantity)
            if result:
                order_items.append((item_name, required_quantity))
        else:
            print("Invalid selection. Please try again.")

    return order_items

def take_order(db, customer_id):
    all_order_items = []
    categories = Categories(db)
    
    while True:
        try:
            category_id = categories.display_categories_and_get_choice()
            if category_id:
                category_name = [cat[1] for cat in categories.get_categories() if cat[0] == category_id][0]
                show_items_by_category(db, category_id)

                order_items = get_order_items(db, category_name)
                all_order_items.extend(order_items)

                continue_order = input("Would you like to order more items? (yes/no): ").strip().lower()
                if continue_order != 'yes':
                    break
            else:
                print("Invalid category selected. Try again.")

        except Exception as e:
            print(f"Error taking order: {e}")
            break
    order = Order(db)
    order.insert_order(customer_id, all_order_items)

    return all_order_items


def manage_stock(db):
    stock = Stock(db)
    
    while True:
        print("\nStock Management:")
        print("1. Add Stock Item")
        print("2. Update Stock Item")
        print("3. Delete Stock Item")
        print("4. View All Stock Items")
        print("5. Go Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            item_name = input("Enter item name: ").strip()
            try:
                quantity = float(input("Enter quantity in kg: ").strip())
            except ValueError:
                print("Invalid quantity. Please enter a valid number.")
                continue
            stock.insert_stock_item(item_name, quantity)

        elif choice == "2":
            item_name = input("Enter item name to update: ").strip()
            try:
                new_quantity = float(input("Enter new quantity in kg: ").strip())
            except ValueError:
                print("Invalid quantity. Please enter a valid number.")
                continue
            stock.update_stock_item(item_name, new_quantity)

        elif choice == "3":
            item_name = input("Enter item name to delete: ").strip()
            stock.delete_stock_item(item_name)

        elif choice == "4":
            stock.retrieve_stock_items()

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please try again.")

def manage_categories(db):
    categories = Categories(db)
    while True:
        category_list = categories.get_categories()

        if category_list:
            print("\nAvailable categories:")
            for category in category_list:
                print(f"{category[0]}. {category[1]}")

        print("\n1. Update Category")
        print("2. Delete Category")
        print("3. Add Category")
        print("4. Go Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            categories.update_category_name()
        elif choice == "2":
            categories.delete_category_by_id()
        elif choice == "3":
            categories.add_category(prompt_for_menu=True)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

def manage_menu(db):
    menu = Menu(db)
    
    while True:
        print("\nMenu Management:")
        print("1. Add Menu Item")
        print("2. Update Menu Item")
        print("3. Delete Menu Item")
        print("4. View All Menu Items")
        print("5. Go Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter item name: ").strip()
            try:
                price = float(input("Enter item price: ").strip())
            except ValueError:
                print("Invalid price. Please enter a valid number.")
                continue
            category_name = input("Enter category name: ").strip()
            menu.add_menu_item(name, price, category_name)

        elif choice == "2":
            try:
                menu_id = int(input("Enter menu item ID to update: ").strip())
            except ValueError:
                print("Invalid ID. Please enter a valid number.")
                continue

            new_name = input("Enter new name (leave blank to keep current): ").strip() or None
            try:
                new_price = input("Enter new price (leave blank to keep current): ").strip()
                new_price = float(new_price) if new_price else None
            except ValueError:
                print("Invalid price. Please enter a valid number.")
                continue
            new_category_name = input("Enter new category name (leave blank to keep current): ").strip() or None

            menu.update_menu_item(menu_id, new_name, new_price, new_category_name)

        elif choice == "3":
            try:
                menu_id = int(input("Enter menu item ID to delete: ").strip())
            except ValueError:
                print("Invalid ID. Please enter a valid number.")
                continue
            menu.delete_menu_item(menu_id)

        elif choice == "4":
            menu.retrieve_menu_items()

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please try again.")

def manage_customers(db):
    customer = Customer(db)

    while True:
        print("\nCustomer Management:")
        print("1. Add Customer")
        print("2. View All Customers")
        print("3. Get Customer by ID")
        print("4. Update Customer Details")
        print("5. Delete Customer")
        print("6. Go Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter customer name: ").strip()
            info = input("Enter customer contact info: ").strip()
            if name and info:
                customer.insert_customer(name, info)
                print("Customer added successfully!")
            else:
                print("Name and contact info are required.")

        elif choice == "2":
            customers = customer.get_all_customers()
            if customers:
                print("\nCustomer List:")
                for c_id, name, info in customers:
                    print(f"ID: {c_id}, Name: {name}, Info: {info}")
            else:
                print("No customers found.")

        elif choice == "3":
            try:
                customer_id = int(input("Enter customer ID: ").strip())
                customer_data = customer.get_customer_by_id(customer_id)
                if customer_data:
                    print(f"ID: {customer_data[0]}, Name: {customer_data[1]}, Info: {customer_data[2]}")
                else:
                    print("Customer not found.")
            except ValueError:
                print("Invalid ID. Please enter a valid number.")

        elif choice == "4":
            try:
                customer_id = int(input("Enter customer ID: ").strip())
                new_name = input("Enter new name (leave blank to keep current): ").strip()
                new_info = input("Enter new contact info (leave blank to keep current): ").strip()
                customer.update_customer(customer_id, new_name or None, new_info or None)
                print("Customer details updated successfully!")
            except ValueError:
                print("Invalid ID. Please enter a valid number.")

        elif choice == "5":
            try:
                customer_id = int(input("Enter customer ID to delete: ").strip())
                customer.delete_customer(customer_id)
                print("Customer deleted successfully!")
            except ValueError:
                print("Invalid ID. Please enter a valid number.")

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")

def manage_orders(db):
    order = Order(db)

    while True:
        print("\nOrder Management:")
        print("1. Place Order")
        print("2. View Order by ID")
        print("3. Update Order")
        print("4. Delete Order")
        print("5. View All Orders")  
        print("6. Go Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            customer_id, _, _ = get_customer_details(db)
            if customer_id:
                order_items = take_order(db, customer_id)
                if order_items:
                    order.insert_order(customer_id, order_items)

        elif choice == "2":
            try:
                order_id = int(input("Enter Order ID: ").strip())
                order.retrieve_order(order_id)
            except ValueError:
                print("Invalid ID. Please enter a valid number.")

        elif choice == "3":
            try:
                order_id = int(input("Enter Order ID to update: ").strip())
                new_item_name = input("Enter new item name (leave blank to keep current): ").strip() or None
                try:
                    new_quantity = input("Enter new quantity (leave blank to keep current): ").strip()
                    new_quantity = float(new_quantity) if new_quantity else None
                except ValueError:
                    print("Invalid quantity.")
                    continue
                order.update_order(order_id, new_item_name, new_quantity)
            except ValueError:
                print("Invalid ID. Please enter a valid number.")

        elif choice == "4":
            try:
                order_id = int(input("Enter Order ID to delete: ").strip())
                order.delete_order(order_id)
            except ValueError:
                print("Invalid ID. Please enter a valid number.")

        elif choice == "5":
            order.view_all_orders()  

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")

def manage_bills(db):
    bill = Bill(db)
    
    while True:
        print("\nBill Management:")
        print("1. View All Bills")
        print("2. Get Bill by ID")
        print("3. Update Bill")
        print("4. Delete Bill")
        print("5. Go Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            bills = bill.get_all_bills()
            if bills:
                print("\nBills List:")
                for bill_data in bills:
                    print(f"Bill ID: {bill_data[0]}, Customer ID: {bill_data[1]}, Item: {bill_data[2]}, Quantity: {bill_data[3]}, Total: Rs. {bill_data[4]}")
            else:
                print("No bills found.")

        elif choice == "2":
            try:
                bill_id = int(input("Enter Bill ID: ").strip())
                bill_data = bill.get_bill_by_id(bill_id)
                if bill_data:
                    print(f"Bill ID: {bill_data[0]}, Customer ID: {bill_data[1]}, Item: {bill_data[2]}, Quantity: {bill_data[3]}, Total: Rs. {bill_data[4]}")
                else:
                    print("Bill not found.")
            except ValueError:
                print("Invalid ID. Please enter a valid number.")

        elif choice == "3":
            try:
                bill_id = int(input("Enter Bill ID to update: ").strip())
                item_name = input("Enter new item name (leave blank to keep current): ").strip() or None
                quantity = input("Enter new quantity (leave blank to keep current): ").strip()
                quantity = float(quantity) if quantity else None
                total_price = input("Enter new total price (leave blank to keep current): ").strip()
                total_price = float(total_price) if total_price else None
                bill.update_bill(bill_id, item_name, quantity, total_price)
                print("Bill updated successfully!")
            except ValueError:
                print("Invalid input. Please enter valid numbers.")

        elif choice == "4":
            try:
                bill_id = int(input("Enter Bill ID to delete: ").strip())
                bill.delete_bill(bill_id)
                print("Bill deleted successfully!")
            except ValueError:
                print("Invalid ID. Please enter a valid number.")

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please try again.")


def main():
    db = DBhelper()

    try:
        initialize_tables(db)

        while True:
            print("\nMain Menu:")
            print("1. Take Order")
            print("2. Manage Stock")
            print("3. Manage Categories")
            print("4. Manage Menu")
            print("5. Manage Customers")
            print("6. Manage Orders")
            print("7.Manage Bills")
            print("8. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                customer_id, name, info = get_customer_details(db)
                if customer_id:
                    order_items = take_order(db, customer_id)
                    if order_items:
                        print(f"\n{name}, your order summary:")
                        for item in order_items:
                            print(f"Item: {item[0]}, Quantity: {item[1]} kg")
                        
                        bill = Bill(db)
                        total_amount = bill.generate_bill(customer_id, order_items)
                        print(f"\nTotal Bill for {name}: Rs. {total_amount}")
                    else:
                        print("No order placed.")

            elif choice == "2":
                manage_stock(db)

            elif choice == "3":
                manage_categories(db)

            elif choice == "4":
                manage_menu(db)

            elif choice == "5":
                manage_customers(db)

            elif choice == "6":
                manage_orders(db)

            elif choice =="7":
                    manage_bills(db)

            elif choice == "8":
                print("Exiting program.")
                break

            else:
                print("Invalid choice. Please try again.")
    finally:
        db.close_connection()

if __name__ == "__main__":
    main()


