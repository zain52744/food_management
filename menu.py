from database import DBhelper

class Menu:
    def __init__(self):
        self.db = DBhelper()

    def create_table(self):
        """Create the menu table."""
        query = """
        CREATE TABLE IF NOT EXISTS menu (
            m_ID INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            category_id INT,
            FOREIGN KEY (category_id) REFERENCES categories(ca_ID)
        )
        """
        self.db.execute_query(query)

    def get_category_id(self, category_name):
        category_query = "SELECT ca_ID FROM categories WHERE category_name = %s"
        category = self.db.fetch_one(category_query, (category_name,))
        return category[0] if category else None

    def add_menu_items_from_dict(self, food_menu):
        
        for category_name, items in food_menu.items():
            
            category_id = self.get_category_id(category_name.capitalize())
            if category_id is None:
                print(f"Category '{category_name}' not found.")
                continue
            
            
            for item_name, price in items.items():
                query = "INSERT INTO menu (name, price, category_id) VALUES (%s, %s, %s)"
                values = (item_name, price, category_id)
                self.db.execute_query(query, values)
        print("Menu items added successfully.")

    def get_items_by_category(self, category_name):
        
        category_id = self.get_category_id(category_name)
        
        if not category_id:
            print(f"Category '{category_name}' not found.")
            return None

        query = "SELECT name, price FROM menu WHERE category_id = %s"
        results = self.db.fetch_all(query, (category_id,))
        
        if not results:
            print(f"No items found in the category '{category_name}'")
            return None

        return {item[0]: item[1] for item in results}
