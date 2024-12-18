import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize the main application window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("600x500")

# List to store expenses
expenses = []

# Function to add a new expense
def add_expense():
    category = category_var.get()
    amount = amount_var.get()
    description = description_var.get()

    if not category or not amount or not description:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showwarning("Input Error", "Amount must be a number!")
        return

    # Add expense to the list
    expenses.append({"Category": category, "Amount": amount, "Description": description})
    update_expense_list()
    amount_var.set("")
    description_var.set("")

# Function to update the listbox with current expenses
def update_expense_list():
    expense_listbox.delete(0, tk.END)
    for expense in expenses:
        expense_listbox.insert(
            tk.END, f"{expense['Category']} - {expense['Amount']} - {expense['Description']}"
        )

# Function to calculate the total expenses
def calculate_total():
    total = sum(expense["Amount"] for expense in expenses)
    messagebox.showinfo("Total Expenses", f"Total Expenses: ₹{total:.2f}")

# Function to generate a pie chart of expenses by category
def show_pie_chart():
    if not expenses:
        messagebox.showwarning("No Data", "No expenses to display in the pie chart!")
        return

    # Calculate total expenses by category
    category_totals = {}
    for expense in expenses:
        category = expense["Category"]
        category_totals[category] = category_totals.get(category, 0) + expense["Amount"]

    # Create a pie chart
    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    figure = Figure(figsize=(6, 4), dpi=100)
    subplot = figure.add_subplot(111)
    subplot.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
    subplot.set_title("Expenses by Category")

    # Display the pie chart in a new window
    chart_window = tk.Toplevel(root)
    chart_window.title("Expense Pie Chart")
    canvas = FigureCanvasTkAgg(figure, chart_window)
    canvas.get_tk_widget().pack()
    canvas.draw()

# Layout and Input Fields
category_label = tk.Label(root, text="Category:")
category_label.pack(pady=5)
category_var = tk.StringVar()
category_combobox = ttk.Combobox(root, textvariable=category_var, values=["Food", "Transport", "Utilities", "Others"])
category_combobox.pack(pady=5)

amount_label = tk.Label(root, text="Amount (₹):")
amount_label.pack(pady=5)
amount_var = tk.StringVar()
amount_entry = tk.Entry(root, textvariable=amount_var)
amount_entry.pack(pady=5)

description_label = tk.Label(root, text="Description:")
description_label.pack(pady=5)
description_var = tk.StringVar()
description_entry = tk.Entry(root, textvariable=description_var)
description_entry.pack(pady=5)

add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.pack(pady=10)

# Listbox to display expenses
expense_listbox = tk.Listbox(root, width=50)
expense_listbox.pack(pady=10)

total_button = tk.Button(root, text="Calculate Total", command=calculate_total)
total_button.pack(pady=10)

chart_button = tk.Button(root, text="Show Pie Chart", command=show_pie_chart)
chart_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
