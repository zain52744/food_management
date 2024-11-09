import mysql.connector

class DBhelper:
    def __init__(self):
        try:
            
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="F4d220190@",
                database="food_management",
            )
            self.conn.autocommit = False  
            print("Connected to database")
        except mysql.connector.Error as err:
            print(f"Connection error: {err}")
            self.conn = None

    def execute_query(self, query, values=None):
        
        if self.conn:
            cursor = self.conn.cursor()
            try:
                if values:
                    cursor.execute(query, values)
                else:
                    cursor.execute(query)
                self.conn.commit()
            except mysql.connector.Error as err:
                print(f"Query execution error: {err}")
                self.conn.rollback()
            finally:
                cursor.close()

    def execute_many(self, query, values):
        
        if self.conn:
            cursor = self.conn.cursor()
            try:
                cursor.executemany(query, values)
                self.conn.commit()
            except mysql.connector.Error as err:
                print(f"Batch execution error: {err}")
                self.conn.rollback()
            finally:
                cursor.close()

    def fetch_one(self, query, values=None):
        
        if self.conn:
            cursor = self.conn.cursor()
            try:
                cursor.execute(query, values)
                return cursor.fetchone()
            except mysql.connector.Error as err:
                print(f"Error fetching one record: {err}")
                return None
            finally:
                cursor.close()

    def fetch_all(self, query, values=None):
        
        if self.conn:
            cursor = self.conn.cursor()
            try:
                cursor.execute(query, values)
                return cursor.fetchall()
            except mysql.connector.Error as err:
                print(f"Error fetching all records: {err}")
                return None
            finally:
                cursor.close()

    def close_connection(self):
        
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("Database connection closed.")
