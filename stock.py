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
        print("Stock table created.")

    def item_exists(self, item_name):
        query = "SELECT COUNT(*) FROM stock WHERE LOWER(item_name) = LOWER(%s)"
        result = self.db.fetch_one(query, (item_name,))
        return result[0] > 0

    def insert_initial_stock(self):
        items = [
            ('zinger_burger', 5.0),
            ('chicken_burger', 5.0),
            ('beef_burger', 5.0),
            ('chicken_karahi', 5.0),
            ('beef_karahi', 5.0),
            ('mutton_karahi', 5.0)
        ]
        query = "INSERT INTO stock (item_name, quantity) VALUES (%s, %s)"
        for item in items:
            item_name, quantity = item
            if not self.item_exists(item_name):
                self.db.execute_query(query, (item_name, quantity))

    def check_stock(self, item_name, required_quantity):
        query = "SELECT quantity FROM stock WHERE LOWER(item_name) = LOWER(%s)"
        result = self.db.fetch_one(query, (item_name,))
        if result:
            current_quantity = result[0]
            return current_quantity >= required_quantity
        return False

    def update_stock(self, item_name, used_quantity):
        query = """
        UPDATE stock 
        SET quantity = quantity - %s 
        WHERE item_name = %s AND quantity >= %s
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
            print(f"Insufficient stock for {item_name}.")
            return None
