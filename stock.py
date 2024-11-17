from database import DBhelper

class Stock:
    def __init__(self, db):
        self.db = db

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS stock (
            stock_id INT PRIMARY KEY AUTO_INCREMENT,
            item_name VARCHAR(50) UNIQUE,
            quantity FLOAT
        )
        """
        self.db.execute_query(query)

    def item_exists(self, item_name):
        query = "SELECT COUNT(*) FROM stock WHERE LOWER(item_name) = LOWER(%s)"
        result = self.db.fetch_one(query, (item_name,))
        return result[0] > 0 if result is not None else False

    def insert_stock_item(self, item_name, quantity):
        if not self.item_exists(item_name):
            query = "INSERT INTO stock (item_name, quantity) VALUES (%s, %s)"
            self.db.execute_query(query, (item_name, quantity))
        else:
            pass

    def retrieve_stock_items(self):
       
        query = "SELECT stock_id, item_name, quantity FROM stock"
        results = self.db.fetch_all(query)
        if results:
            for stock_id, item_name, quantity in results:
                print(f"ID: {stock_id}, Item: {item_name}, Quantity: {quantity} kg")
        else:
            print("No stock items available.")

    def update_stock_item(self, item_name, new_quantity):
        if self.item_exists(item_name):
            query = "UPDATE stock SET quantity = %s WHERE LOWER(item_name) = LOWER(%s)"
            self.db.execute_query(query, (new_quantity, item_name))
        else:
            pass

    def delete_stock_item(self, item_name):
        
        if self.item_exists(item_name):
            query = "DELETE FROM stock WHERE LOWER(item_name) = LOWER(%s)"
            self.db.execute_query(query, (item_name,))
        else:
            pass

    def insert_initial_stock(self):
        
        initial_items = [
            ('zinger_burger', 5.0),
            ('chicken_burger', 5.0),
            ('beef_burger', 5.0),
            ('chicken_karahi', 5.0),
            ('beef_karahi', 5.0),
            ('mutton_karahi', 5.0)
        ]
        for item_name, quantity in initial_items:
            if not self.item_exists(item_name):
                self.insert_stock_item(item_name, quantity)
        

    def check_stock(self, item_name, required_quantity):
        query = "SELECT quantity FROM stock WHERE LOWER(item_name) = LOWER(%s)"
        result = self.db.fetch_one(query, (item_name,))
        return result[0] >= required_quantity if result is not None else False

    def update_stock(self, item_name, used_quantity):
       
        query = """
        UPDATE stock 
        SET quantity = quantity - %s 
        WHERE LOWER(item_name) = LOWER(%s) AND quantity >= %s
        """
        self.db.execute_query(query, (used_quantity, item_name, used_quantity))
        
    def handle_order_stock(self, item_name, category_name, required_quantity):
        if category_name == "Fast Food":
            stock_deduction = 0.5  
            quantity = 1  
        else:
            stock_deduction = required_quantity 
            quantity = required_quantity

        if self.check_stock(item_name, stock_deduction):
            self.update_stock(item_name, stock_deduction)
            return item_name, quantity
        else:
            print(f"Insufficient stock for '{item_name}'. Required: {stock_deduction} kg.")
        return None
