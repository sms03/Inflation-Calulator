import tkinter as tk
from tkinter import messagebox

# Example currency exchange rates (from Base Currency to Target Currency)
exchange_rates = {
    "USD": {"USD": 1, "EUR": 0.85, "JPY": 110, "INR": 74, "GBP": 0.75, "CNY": 6.45},
    "EUR": {"USD": 1.18, "EUR": 1, "JPY": 129.53, "INR": 87.19, "GBP": 0.88, "CNY": 7.58},
    "JPY": {"USD": 0.0091, "EUR": 0.0077, "JPY": 1, "INR": 0.67, "GBP": 0.0068, "CNY": 0.059},
    "INR": {"USD": 0.013, "EUR": 0.0115, "JPY": 1.49, "INR": 1, "GBP": 0.011, "CNY": 0.087},
    "GBP": {"USD": 1.33, "EUR": 1.14, "JPY": 147.18, "INR": 90.12, "GBP": 1, "CNY": 8.65},
    "CNY": {"USD": 0.155, "EUR": 0.132, "JPY": 16.84, "INR": 11.53, "GBP": 0.116, "CNY": 1},
}

def calculate_inflation():
    try:
        # Debugging print statement
        print("Calculate Inflation button clicked.")

        # Get input values from the entries
        old_price = float(old_price_entry.get())
        new_price = float(new_price_entry.get())
        old_year = int(old_year_entry.get())
        new_year = int(new_year_entry.get())
        base_currency = base_currency_var.get()
        target_currency = target_currency_var.get()
        
        # Convert prices if currencies are different
        if base_currency != target_currency:
            # Convert old price to target currency
            old_price_converted = old_price * exchange_rates[base_currency][target_currency]
        else:
            old_price_converted = old_price
        
        # Calculate inflation rate
        inflation_rate = ((new_price - old_price_converted) / old_price_converted) * 100

        # Define symbols for various currencies
        currency_symbols = {
            "USD": "$",
            "EUR": "€",
            "JPY": "¥",
            "INR": "₹",
            "GBP": "£",
            "CNY": "¥",
        }

        # Get the correct symbol or default to an empty string if currency not found
        symbol = currency_symbols.get(target_currency, "")
        
        # Display the result
        result_text = (f"Inflation rate from {old_year} to {new_year} is {inflation_rate:.2f}%.\n"
                       f"The price increased from {symbol}{old_price_converted:.2f} in {old_year} "
                       f"(in {target_currency}) to {symbol}{new_price:.2f} in {new_year} (in {target_currency}).")
        
        result_label.config(text=result_text)
        print("Calculation successful.")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for prices and years.")
    except ZeroDivisionError:
        messagebox.showerror("Invalid Input", "Old price cannot be zero.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        print(f"An error occurred: {e}")

# Initialize the main window
root = tk.Tk()
root.title("Inflation Calculator")
root.geometry("500x500")

# Labels and entries for user input
tk.Label(root, text="Old Price:").pack(pady=5)
old_price_entry = tk.Entry(root)
old_price_entry.pack(pady=5)

tk.Label(root, text="New Price:").pack(pady=5)
new_price_entry = tk.Entry(root)
new_price_entry.pack(pady=5)

tk.Label(root, text="Old Year:").pack(pady=5)
old_year_entry = tk.Entry(root)
old_year_entry.pack(pady=5)

tk.Label(root, text="New Year:").pack(pady=5)
new_year_entry = tk.Entry(root)
new_year_entry.pack(pady=5)

# Dropdown for base currency (old price currency) and target currency (new price currency)
tk.Label(root, text="Base Currency (Old Price):").pack(pady=5)
base_currency_var = tk.StringVar(root)
base_currency_var.set("USD")  # Default value
base_currency_menu = tk.OptionMenu(root, base_currency_var, "USD", "EUR", "JPY", "INR", "GBP", "CNY")
base_currency_menu.pack(pady=5)

tk.Label(root, text="Target Currency (New Price):").pack(pady=5)
target_currency_var = tk.StringVar(root)
target_currency_var.set("USD")  # Default value
target_currency_menu = tk.OptionMenu(root, target_currency_var, "USD", "EUR", "JPY", "INR", "GBP", "CNY")
target_currency_menu.pack(pady=5)

# Button to calculate inflation
calculate_button = tk.Button(root, text="Calculate Inflation", command=calculate_inflation)
calculate_button.pack(pady=10)

# Label to display the result
result_label = tk.Label(root, text="", wraplength=400, justify="center", font=("Arial", 10))
result_label.pack(pady=20)

# Start the GUI event loop
root.mainloop()
