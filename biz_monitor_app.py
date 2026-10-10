import csv
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

def read_inventory(filename):
    inventory = {}
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                inventory[row['product_name']] = {
                    'cost_price': float(row['cost_price']),
                    'selling_price': float(row['selling_price']),
                    'quantity': int(row['quantity'])
                }
    except FileNotFoundError:
        messagebox.showerror("Error", f"{filename} not found")
    return inventory

def calculate_profit(cost, selling, quantity):
    return (selling - cost) * quantity

def format_naira(amount):
    return f"₦{amount:,.2f}"

def show_report():
    inventory = read_inventory("products.csv")
    if not inventory:
        return
    
    report_window = tk.Toplevel(root)
    report_window.title("Daily Report")
    report_window.geometry("500x400")
    
    text = tk.Text(report_window, font=("Consolas", 10))
    text.pack(fill="both", expand=True, padx=10, pady=10)
    
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    total = 0
    low_stock = []
    
    text.insert("end", f"BIZ MONITOR - {today}\n")
    text.insert("end", "="*45 + "\n")
    
    for name, d in inventory.items():
        profit = calculate_profit(d['cost_price'], d['selling_price'], d['quantity'])
        total += profit
        text.insert("end", f"{name}: Qty={d['quantity']} | Profit={format_naira(profit)}\n")
        if d['quantity'] <= 5:
            low_stock.append(name)
            
    text.insert("end", "-"*45 + "\n")
    text.insert("end", f"TOTAL PROFIT: {format_naira(total)}\n")
    text.insert("end", f"LOW STOCK: {', '.join(low_stock) if low_stock else 'All OK'}\n")

# Main App Window
root = tk.Tk()
root.title("Biz Monitor - My Shop")
root.geometry("400x300")

tk.Label(root, text="BIZ MONITOR", font=("Arial", 18, "bold")).pack(pady=20)
tk.Label(root, text="My Small Business Tracker", font=("Arial", 11)).pack()

ttk.Button(root, text="Show Daily Report", command=show_report).pack(pady=20, ipadx=20, ipady=10)
ttk.Button(root, text="Exit", command=root.quit).pack(pady=10)

tk.Label(root, text="© 2026 Your Business", font=("Arial", 8)).pack(side="bottom", pady=10)

root.mainloop()