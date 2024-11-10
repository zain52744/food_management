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

    def insert_initial_stock(self):
        """Insert initial stock data into the database."""
        items = [
            ('zinger_burger', 5.0),
            ('chicken_burger', 5.0),
            ('beef_burger', 5.0),
            ('chicken_karahi', 5.0),
            ('beef_karahi', 5.0),
            ('mutton_karahi', 5.0)
        ]
        query = "INSERT INTO stock (item_name, quantity) VALUES (%s, %s)"
        self.db.execute_many(query, items)
        print("Initial stock inserted.")

    def check_stock(self, item_name, required_quantity):
        """Check if there is enough stock for the required quantity."""
        query = "SELECT quantity FROM stock WHERE LOWER(item_name) = LOWER(%s)"
        result = self.db.fetch_one(query, (item_name,))
        
        if result:
            current_quantity = result[0]
            if current_quantity >= required_quantity:
                return True
            else:
                print(f"Insufficient stock for {item_name}. Available: {current_quantity} kg, Required: {required_quantity} kg.")
        else:
            print(f"Item {item_name} not found in stock.")
        return False

    def update_stock(self, item_name, used_quantity):
        """Reduce the stock by the specified quantity."""
        query = """
        UPDATE stock 
        SET quantity = quantity - %s 
        WHERE item_name = %s AND quantity >= %s
        """
        self.db.execute_query(query, (used_quantity, item_name, used_quantity))
        print(f"Stock updated for {item_name}, reduced by {used_quantity} kg.")
