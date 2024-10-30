def calculate_bill(ordered_items):
    total = sum(price for item, price in ordered_items)
    print("\n----- Bill Summary -----")
    for item, price in ordered_items:
        print(f"{item.replace('_', ' ').title()}: {price} PKR")
    print(f"Total: {total} PKR")
    print("------------------------")