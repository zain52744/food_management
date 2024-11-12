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

    def get_customer_id(self, name):
        
        query = "SELECT c_ID FROM customer WHERE name = %s"
        result = None

        if self.db.conn:
            result = self.db.fetch_one(query, (name,))
        else:
            print("Database connection is not active.")
        
        if result:
            return result[0]
        else:
            print(f"Customer with name '{name}' not found.")
            return None  
    def get_customer_info(self, customer_id):
        
        query = "SELECT name, info FROM customer WHERE c_ID = %s"
        result = None

        if self.db.conn:
            result = self.db.fetch_one(query, (customer_id,))
        else:
            print("Database connection is not active.")
        
        if result:
            return result
        else:
            print(f"No customer found with ID {customer_id}.")
            return None 

