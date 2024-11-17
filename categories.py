from database import DBhelper
from menu import Menu

class Categories:
    def __init__(self, db):
        self.db = db

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS categories (
            ca_ID INT PRIMARY KEY AUTO_INCREMENT,
            category_name VARCHAR(50) NOT NULL
        )
        """
        self.db.execute_query(query)

    def insert_categories(self):
        query = "INSERT INTO categories (category_name) VALUES (%s)"
        values = [("Desi Food",), ("Fast Food",)]
        self.db.execute_many(query, values)

    def get_categories(self):
        query = "SELECT ca_ID, category_name FROM categories"
        return self.db.fetch_all(query)

    def update_category(self, category_id, new_name):
        query = "UPDATE categories SET category_name = %s WHERE ca_ID = %s"
        self.db.execute_query(query, (new_name, category_id))

    def delete_category(self, category_id):
        query = "DELETE FROM categories WHERE ca_ID = %s"
        self.db.execute_query(query, (category_id,))

    def display_categories_and_get_choice(self):
        categories = self.get_categories()
        if not categories:
            print("No categories available.")
            return None

        print("Available categories:")
        for category in categories:
            print(f"{category[0]}. {category[1]}")
        choice = input("Choose a category by entering its number: ").strip()
        try:
            category_id = int(choice)
            if category_id in [cat[0] for cat in categories]:
                return category_id
            else:
                print("Invalid category choice.")
                return None
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return None

    def add_category(self, prompt_for_menu=False):
        category_name = input("Enter the name of the new category: ").strip()
        if category_name:
            query = "INSERT INTO categories (category_name) VALUES (%s)"
            self.db.execute_query(query, (category_name,))
            print(f"Category '{category_name}' added successfully.")

            if prompt_for_menu:
                add_menu_choice = input(f"Do you want to add menu items to '{category_name}'? (yes/no): ").strip().lower()
                if add_menu_choice == 'yes':
                    menu = Menu(self.db)
                    while True:
                        name = input("Enter item name (or type 'done' to finish): ").strip()
                        if name.lower() == 'done':
                            break
                        try:
                            price = float(input("Enter item price: ").strip())
                        except ValueError:
                            print("Invalid price. Please enter a valid number.")
                            continue
                        menu.add_menu_item(name, price, category_name)
        else:
            print("Invalid category name. Please try again.")

    def update_category_name(self):
        category_list = self.get_categories()
        if not category_list:
            print("No categories available to update.")
            return
        
        print("Available categories:")
        for category in category_list:
            print(f"{category[0]}. {category[1]}")  
        try:
            category_id = int(input("Enter the ID of the category you want to update: ").strip())
            if category_id not in [cat[0] for cat in category_list]:
                print("Invalid category ID.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid category ID.")
            return

        new_category_name = input("Enter the new category name: ").strip()
        if not new_category_name:
            print("Category name cannot be empty.")
            return

        
        query = "UPDATE categories SET category_name = %s WHERE ca_ID = %s"
        self.db.execute_query(query, (new_category_name, category_id))
        print(f"Category ID {category_id} updated successfully to '{new_category_name}'.")

    def delete_category_by_id(self):
        category_list = self.get_categories()
        if not category_list:
            print("No categories available to delete.")
            return
        
        print("Available categories:")
        for category in category_list:
            print(f"{category[0]}. {category[1]}")  
        try:
            category_id = int(input("Enter the ID of the category you want to delete: ").strip())
            if category_id not in [cat[0] for cat in category_list]:
                print("Invalid category ID.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid category ID.")
            return

        confirm = input(f"Are you sure you want to delete category ID {category_id}? (yes/no): ").strip().lower()
        if confirm == 'yes':
            self.delete_category(category_id)
            print(f"Category ID {category_id} deleted successfully.")
        else:
            print("Category deletion canceled.")


