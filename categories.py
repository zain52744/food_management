from database import DBhelper

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
