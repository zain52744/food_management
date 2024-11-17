from database import DBhelper

class Customer:
    def __init__(self, db):
        self.db = db

    def create_table(self):
        
        query = """
        CREATE TABLE IF NOT EXISTS customer (
            c_ID INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            info VARCHAR(100) NOT NULL
        )
        """
        if self.db.conn:
            self.db.execute_query(query)
        else:
            print("Database connection is not active.")

    def insert_customer(self, name, info):
        
        query = "INSERT INTO customer (name, info) VALUES (%s, %s)"
        values = (name, info)
        if self.db.conn:
            self.db.execute_query(query, values)
        else:
            print("Database connection is not active.")

    def get_all_customers(self):
       
        query = "SELECT c_ID, name, info FROM customer"
        if self.db.conn:
            customers = self.db.fetch_all(query)
            return customers
        else:
            print("Database connection is not active.")
            return []

    def get_customer_by_id(self, customer_id):
       
        query = "SELECT c_ID, name, info FROM customer WHERE c_ID = %s"
        if self.db.conn:
            customer = self.db.fetch_one(query, (customer_id,))
            return customer
        else:
            print("Database connection is not active.")
            return None

    def get_customer_id(self, name):
        
        query = "SELECT c_ID FROM customer WHERE name = %s"
        values = (name,)
        if self.db.conn:
            result = self.db.fetch_one(query, values)
            if result:
                return result[0]  
            else:
                print(f"No customer found with the name: {name}")
                return None
        else:
            print("Database connection is not active.")
            return None

    def update_customer(self, customer_id, new_name=None, new_info=None):
       
        updates = []
        values = []
        if new_name:
            updates.append("name = %s")
            values.append(new_name)
        if new_info:
            updates.append("info = %s")
            values.append(new_info)

        if not updates:
            print("No changes provided for update.")
            return

        query = f"UPDATE customer SET {', '.join(updates)} WHERE c_ID = %s"
        values.append(customer_id)

        if self.db.conn:
            self.db.execute_query(query, tuple(values))
        else:
            print("Database connection is not active.")

    def delete_customer(self, customer_id):
        
        query = "DELETE FROM customer WHERE c_ID = %s"
        if self.db.conn:
            self.db.execute_query(query, (customer_id,))
        else:
            print("Customer and associated orders deleted successfully!")



        
