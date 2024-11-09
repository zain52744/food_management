from database import DBhelper

class Order:
    def __init__(self):
        self.db = DBhelper()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS orders (
            o_ID INT PRIMARY KEY AUTO_INCREMENT,
            customer_id INT,
            item_name VARCHAR(100),
            FOREIGN KEY (customer_id) REFERENCES customer(c_ID)
        )
        """
        self.db.execute_query(query)

    def insert_order(self, customer_id, order_items):
        
        if not order_items:
            print("No items to add to the order.")
            return

        for item in order_items:
            query = """
            INSERT INTO orders (customer_id, item_name) 
            VALUES (%s, %s)
            """
            values = (customer_id, item)
            self.db.execute_query(query, values)

        print("Order placed successfully!")
