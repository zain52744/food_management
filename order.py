from database import DBhelper
import mysql

class Order:
    def __init__(self, db):
        self.db = db

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS orders (
            o_ID INT PRIMARY KEY AUTO_INCREMENT,
            customer_id INT,
            item_name VARCHAR(100),
            quantity FLOAT,
            FOREIGN KEY (customer_id) REFERENCES customer(c_ID) ON DELETE CASCADE
        )
        """
        self.db.execute_query(query)

    def insert_order(self, customer_id, order_items):
        if not order_items:
            print("No items to add to the order.")
            return

        for item_name, quantity in order_items:
            query = """
            INSERT INTO orders (customer_id, item_name, quantity) 
            VALUES (%s, %s, %s)
            """
            values = (customer_id, item_name, quantity)
            self.db.execute_query(query, values)

        print("Order placed successfully!")

    def retrieve_order(self, order_id):
        query = "SELECT * FROM orders WHERE o_ID = %s"
        cursor = self.db.conn.cursor(buffered=True)
        try:
            cursor.execute(query, (order_id,))
            result = cursor.fetchone()
            if result:
                print(f"Order ID: {result[0]}, Customer ID: {result[1]}, Item: {result[2]}, Quantity: {result[3]}")
            else:
                print("No order found with the given ID.")
        except mysql.connector.Error as err:
            print(f"Error retrieving order: {err}")
        finally:
         cursor.close()
    
    def delete_order(self, order_id):
        query = "DELETE FROM orders WHERE o_ID = %s"
        self.db.execute_query(query, (order_id,))
        print("Order deleted successfully.")

    def update_order(self, order_id, new_item_name, new_quantity=None):
        if new_quantity is None:
            query = "UPDATE orders SET item_name = %s WHERE o_ID = %s"
            values = (new_item_name, order_id)
        else:
            query = "UPDATE orders SET item_name = %s, quantity = %s WHERE o_ID = %s"
            values = (new_item_name, new_quantity, order_id)

        self.db.execute_query(query, values)
        print("Order updated successfully.")

    def view_all_orders(self):
        query = "SELECT * FROM orders"
        cursor = self.db.conn.cursor(buffered=True)
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                print("All Orders:")
                for row in results:
                    print(f"Order ID: {row[0]}, Customer ID: {row[1]}, Item: {row[2]}, Quantity: {row[3]}")
            else:
                print("No orders found.")
        except mysql.connector.Error as err:
            print(f"Error retrieving orders: {err}")
        finally:
            cursor.close()
