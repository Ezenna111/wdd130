# CSE 111 - Milestone for Biz Monitor
# Student: [Eze Chinecherem]
# 
# What I have completed so far:
# - Created products.csv with 5 products
# - Completed read_inventory() - reads CSV into dictionary
# - Completed calculate_profit() - calculates profit
# - Completed format_naira() - formats with ₦
#
# What is left to do:
# - calculate_total_profit()
# - get_low_stock()
# - print_daily_report()
# - test file
#
# Challenges: Formatting Naira and FileNotFoundError


# CSE 111 - Final Project - Biz Monitor
# Student: [PUT YOUR REAL NAME HERE]

import csv
from datetime import datetime

def read_inventory(filename):
    """Reads products.csv into dictionary {name: {cost, selling, quantity}}"""
    inventory = {}
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['product_name']
                inventory[name] = {
                    'cost_price': float(row['cost_price']),
                    'selling_price': float(row['selling_price']),
                    'quantity': int(row['quantity'])
                }
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return {}
    except Exception as e:
        print(f"Error reading file: {e}")
        return {}
    return inventory

def calculate_profit(cost, selling, quantity):
    """Calculates profit for one product: (selling - cost) * quantity"""
    return (selling - cost) * quantity

def format_naira(amount):
    """Formats amount as Naira: ₦6,000.00"""
    return f"₦{amount:,.2f}"

def calculate_total_profit(inventory):
    """Calculates total profit for all products"""
    total = 0
    for details in inventory.values():
        profit = calculate_profit(
            details['cost_price'],
            details['selling_price'],
            details['quantity']
        )
        total += profit
    return total

def get_low_stock(inventory, limit=5):
    """Returns list of products where quantity <= limit"""
    low_items = []
    for name, details in inventory.items():
        if details['quantity'] <= limit:
            low_items.append(name)
    return low_items

def print_daily_report(inventory):
    """Prints daily report with date, all products, total profit, low stock"""
    today = datetime.now()
    print("=" * 50)
    print(f"BIZ MONITOR - DAILY REPORT")
    print(f"Date: {today.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    for name, details in inventory.items():
        profit = calculate_profit(details['cost_price'], details['selling_price'], details['quantity'])
        print(f"{name}: Qty={details['quantity']} | Profit={format_naira(profit)}")

    print("-" * 50)
    total_profit = calculate_total_profit(inventory)
    print(f"TOTAL PROFIT: {format_naira(total_profit)}")

    low_stock = get_low_stock(inventory, 5)
    if low_stock:
        print(f"LOW STOCK ALERT (<=5): {', '.join(low_stock)}")
    else:
        print("All products have enough stock.")
    print("=" * 50)

def main():
    try:
        inventory = read_inventory("products.csv")
        if not inventory:
            print("No inventory to display.")
            return
        print_daily_report(inventory)
    except Exception as e:
        print(f"An unexpected error happened: {e}")

if __name__ == "__main__":
    main()