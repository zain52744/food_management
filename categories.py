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
        for category_id, category_name in categories:
            print(f"{category_id}. {category_name}")

        category_id = input("Please enter the number of the category you would like to view: ").strip()
        if category_id.isdigit() and int(category_id) in [cat[0] for cat in categories]:
            return int(category_id)
        else:
            print("Invalid selection. Please try again.")
            return None

    def update_category_name(self):
        category_id = input("Enter the ID of the category you want to update: ").strip()
        new_name = input("Enter the new category name: ").strip()

        if category_id.isdigit():
            self.update_category(int(category_id), new_name)
            print(f"Category with ID {category_id} updated to '{new_name}'.")
        else:
            print("Invalid category ID.")

    def delete_category_by_id(self):
        category_id = input("Enter the ID of the category you want to delete: ").strip()

        if category_id.isdigit():
            self.delete_category(int(category_id))
            print(f"Category with ID {category_id} deleted.")
        else:
            print("Invalid category ID.")

    def add_category(self):
        category_name = input("Enter the name of the new category: ").strip()
        if category_name:
            query = "INSERT INTO categories (category_name) VALUES (%s)"
            self.db.execute_query(query, (category_name,))
            print(f"Category '{category_name}' added successfully.")
        else:
            print("Invalid category name. Please try again.")

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