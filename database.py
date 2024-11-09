import mysql.connector
# import mysql.connector.locales.eng.client_error

class DBhelper:
    def __init__(self):
        try:
            # Establish connection with necessary parameters, removed locale
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="F4d220190@",
                database="food_management",
                
            )
        

            self.conn.autocommit = False  # Transactions need to be committed manually
            print("Connected to database")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(f"Connection error: {err}")
            self.conn = None

    def execute_query(self, query, values=None):
        """Execute a single query with optional values."""
        if self.conn:
            cursor = self.conn.cursor()  # Create a new cursor
            try:
                if values:
                    cursor.execute(query, values)
                else:
                    cursor.execute(query)
                self.conn.commit()  # Commit transaction
            except mysql.connector.Error as err:
                print(f"Query execution error: {err}")
                self.conn.rollback()  # Rollback on error
            finally:
                cursor.close()  # Ensure cursor is always closed

    def execute_many(self, query, values):
        """Execute a batch of queries with provided values."""
        if self.conn:
            cursor = self.conn.cursor()
            try:
                cursor.executemany(query, values)
                self.conn.commit()  # Commit transaction
            except mysql.connector.Error as err:
                print(f"Batch execution error: {err}")
                self.conn.rollback()  # Rollback on error
            finally:
                cursor.close()  # Ensure cursor is always closed

    def fetch_one(self, query, values=None):
        """Fetch a single result."""
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
        """Fetch all results."""
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

    # def __del__(self):
    #     """Ensure the database connection is properly closed when object is deleted."""
    #     try:
    #         if self.conn and self.conn.is_connected():
    #             self.conn.close()
    #             print("Database connection closed.")
    #     except AttributeError:
    #         # Handle case where self.conn is None
    #         pass
    #     except mysql.connector.Error as err:
    #         print(f"Error closing connection: {err}")
