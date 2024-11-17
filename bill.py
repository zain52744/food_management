from decimal import Decimal

class Bill:
    def __init__(self, db):
        self.db = db

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS bill (
            bill_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            item_name VARCHAR(255),
            quantity DECIMAL(5,2),
            total_price DECIMAL(10,2),
            FOREIGN KEY (customer_id) REFERENCES customer(c_id) ON DELETE CASCADE
        )
        """
        self.db.execute_query(query)

    def generate_bill(self, customer_id, order_items):
        total_amount = Decimal(0.0)
        print("Generating Consolidated Bill for Customer ID:", customer_id)
        print("-" * 50)
        print("Item Name | Quantity | Price | Total")
        print("-" * 50)

        for item_name, quantity in order_items:
            query = "SELECT price FROM menu WHERE name = %s"
            price = self.db.fetch_one(query, (item_name,))

            if price:
                price = Decimal(price[0])
                quantity = Decimal(quantity)
                total_price = price * quantity
                total_amount += total_price

                insert_query = """
                INSERT INTO bill (customer_id, item_name, quantity, total_price)
                VALUES (%s, %s, %s, %s)
                """
                self.db.execute_query(insert_query, (customer_id, item_name, quantity, total_price))
                print(f"{item_name} | {quantity} | Rs. {price} | Rs. {total_price}")
            else:
                print(f"Error: Price not found for {item_name}")

        print("-" * 50)
        print(f"Total Bill Amount: Rs. {total_amount}")
        return total_amount

    def get_all_bills(self):
        query = "SELECT * FROM bill"
        return self.db.fetch_all(query)

    def get_bill_by_id(self, bill_id):
        query = "SELECT * FROM bill WHERE bill_id = %s"
        return self.db.fetch_one(query, (bill_id,))

    def update_bill(self, bill_id, item_name=None, quantity=None, total_price=None):
        query = "UPDATE bill SET "
        updates = []
        params = []

        if item_name:
            updates.append("item_name = %s")
            params.append(item_name)
        if quantity:
            updates.append("quantity = %s")
            params.append(quantity)
        if total_price:
            updates.append("total_price = %s")
            params.append(total_price)

        query += ", ".join(updates) + " WHERE bill_id = %s"
        params.append(bill_id)
        
        self.db.execute_query(query, tuple(params))

    def delete_bill(self, bill_id):
        query = "DELETE FROM bill WHERE bill_id = %s"
        self.db.execute_query(query, (bill_id,))
