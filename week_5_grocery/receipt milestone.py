import csv

def read_dictionary(filename, key_column_index):
    dictionary = {}
    with open(filename, "r") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            key = row[key_column_index]
            dictionary[key] = row
    return dictionary

def main():
    products_dict = read_dictionary("products.csv", 0)
    print("All Products")
    print(products_dict)
    print()

    print("Requested Items")
    with open("request.csv", "r") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            product_key = row[0]
            quantity = row[1]
            product_info = products_dict[product_key]
            product_name = product_info[1]
            product_price = product_info[2]
            print(f"{product_name}: {quantity} @ {product_price}")

if __name__ == "__main__":
    main()