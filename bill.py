# from database import DBhelper

# class Bill:
#     def __init__(self, db):
#         self.db = db

#     def create_table(self):
#         """Create the bill table with the necessary foreign keys."""
#         query = """
#         CREATE TABLE IF NOT EXISTS bill (
#             bill_id INT PRIMARY KEY AUTO_INCREMENT,
#             c_id INT,
#             total_amount FLOAT,
#             FOREIGN KEY (c_id) REFERENCES customer(c_ID)
#         )
#         """
#         self.db.execute_query(query)
#         print("Bill table created successfully!")

#     def generate_bill(self, customer_id, order_ids):
#         """Generate bill by summing up total amount for all orders."""
#         total_amount = 0

#         # Loop over each order ID to calculate the total amount
#         for order_id in order_ids:
#             query = """
#             SELECT oi.item_name, oi.quantity, m.price
#             FROM order_items oi
#             JOIN menu m ON oi.item_name = m.name  -- Ensure item_name is joined with menu name
#             WHERE oi.order_id = %s
#             """
#             items = self.db.fetch_all(query, (order_id,))
            
#             if items:
#                 for item_name, quantity, price in items:
#                     total_amount += quantity * price

#         # Insert the total bill into the bill table
#         bill_query = """
#         INSERT INTO bill (c_id, total_amount) 
#         VALUES (%s, %s)
#         """
#         self.db.execute_query(bill_query, (customer_id, total_amount))
        
#         print(f"Bill generated for customer {customer_id} with total amount Rs. {total_amount:.2f}")
#         return total_amount
