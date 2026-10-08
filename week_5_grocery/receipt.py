# Exceeding Requirements:
# 1. Days until New Years Sale (Jan 1)
# 2. Return by date - 30 days at 9:00 PM
# 3. Buy One Get One 50% off for D083 (yogurt)
# 4. Prints coupon for a product ordered

import csv
from datetime import datetime, timedelta
import random

def read_dictionary(filename, key_column_index):
    dictionary = {}
    with open(filename, "r") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            if len(row)!=0:
                key = row[key_column_index]
                dictionary[key] = row
    return dictionary

def main():
    try:
        products_dict = read_dictionary("products.csv", 0)
        print("Inkom Emporium")
        print()

        total_items = 0
        subtotal = 0.0
        ordered_products = []

        with open("request.csv", "r") as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                product_number = row[0]
                quantity = int(row[1])

                product_data = products_dict[product_number]
                product_name = product_data[1]
                product_price = float(product_data[2])

                ordered_products.append(product_name)

                # --- BOGO 50% off for D083 ---
                line_total = 0
                if product_number == "D083":
                    # every 2nd item half price
                    full_price_count = (quantity + 1) // 2
                    half_price_count = quantity // 2
                    line_total = full_price_count * product_price + half_price_count * (product_price * 0.5)
                    print(f"{product_name}: {quantity} @ {product_price:.2f} = {line_total:.2f} (BOGO 50% off)")
                else:
                    line_total = quantity * product_price
                    print(f"{product_name}: {quantity} @ {product_price:.2f}")

                total_items += quantity
                subtotal += line_total

        print()
        print(f"Number of Items: {total_items}")
        print(f"Subtotal: {subtotal:.2f}")

        sales_tax = subtotal * 0.06
        total = subtotal + sales_tax

        print(f"Sales Tax: {sales_tax:.2f}")
        print(f"Total: {total:.2f}")
        print()
        print("Thank you for shopping at the Inkom Emporium.")

        current_date_and_time = datetime.now()
        print(f"{current_date_and_time:%a %b %d %I:%M:%S %Y}")
        print()

        # --- Exceeding: Days until New Years ---
        today = datetime.now()
        next_new_year = datetime(today.year + 1, 1, 1)
        days_until = (next_new_year - today).days
        print(f"New Years Sale starts in {days_until} days! (Jan 1)")

        # --- Exceeding: Return by date ---
        return_date = today + timedelta(days=30)
        return_date = return_date.replace(hour=21, minute=0, second=0)
        print(f"Return by: {return_date:%a %b %d %I:%M %p %Y}")

        # --- Exceeding: Coupon ---
        if ordered_products:
            coupon_item = random.choice(ordered_products)
            print(f"Coupon: 10% off {coupon_item} next time!")

    except FileNotFoundError as err:
        print(f"Error: missing file\n{err}")
    except KeyError as err:
        print(f"Error: unknown product ID in the request.csv file\n{err}")

if __name__ == "__main__":
    main()