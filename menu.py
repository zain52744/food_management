from database import DBhelper


class Menu:
    
    def __init__(self, db):
        self.db = db

    def create_table(self):
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
        items = self.db.fetch_all(query, (category_id,))
        return {item[0]: item[1] for item in items} if items else {}

    def add_menu_item(self, name, price, category_name):
        category_id = self.get_category_id(category_name)
        if not category_id:
            print(f"Category '{category_name}' not found.")
            return

        query = "INSERT INTO menu (name, price, category_id) VALUES (%s, %s, %s)"
        values = (name, price, category_id)
        self.db.execute_query(query, values)
        print(f"Item '{name}' added successfully.")

    def update_menu_item(self, menu_id, new_name=None, new_price=None, new_category_name=None):
        updates = []
        values = []
        if new_name:
            updates.append("name = %s")
            values.append(new_name)
        if new_price is not None:
            updates.append("price = %s")
            values.append(new_price)
        if new_category_name:
            new_category_id = self.get_category_id(new_category_name)
            if not new_category_id:
                print(f"Category '{new_category_name}' not found.")
                return
            updates.append("category_id = %s")
            values.append(new_category_id)
        if not updates:
            print("No changes provided.")
            return
        values.append(menu_id)
        query = f"UPDATE menu SET {', '.join(updates)} WHERE m_ID = %s"
        self.db.execute_query(query, values)
        print(f"Menu item with ID {menu_id} updated successfully.")

    def delete_menu_item(self, menu_id):
        query = "DELETE FROM menu WHERE m_ID = %s"
        self.db.execute_query(query, (menu_id,))
        print(f"Menu item with ID {menu_id} deleted successfully.")

    def retrieve_menu_items(self):
        query = "SELECT m_ID, name, price, category_id FROM menu"
        items = self.db.fetch_all(query)
        if not items:
            print("No menu items found.")
        else:
            for item in items:
                print(f"ID: {item[0]}, Name: {item[1]}, Price: Rs. {item[2]}, Category ID: {item[3]}")



