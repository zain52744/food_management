def create_tables(cursor):
    
    cursor.execute("CREATE DATABASE IF NOT EXISTS food_management")
    cursor.execute("USE food_management")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(50),
            item_name VARCHAR(50),
            price INT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(50),
            item_name VARCHAR(50),
            quantity INT
        )
    """)
