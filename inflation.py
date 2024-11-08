import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize customtkinter and configure appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Set up the API endpoint and key (Replace 'YOUR_API_KEY' with your actual API key)
API_URL = "https://openexchangerates.org/api/latest.json"
API_KEY = "YOUR_API_KEY"

# Function to get real-time exchange rates
def get_exchange_rate(base_currency, target_currency):
    try:
        response = requests.get(f"{API_URL}?app_id={API_KEY}&base={base_currency}")
        data = response.json()
        if response.status_code != 200 or 'error' in data:
            raise ValueError("Error fetching exchange rates.")
        # Get the target currency rate relative to the base currency
        rate = data['rates'][target_currency]
        return rate
    except Exception as e:
        messagebox.showerror("Error", f"Could not retrieve exchange rate: {e}")
        return None

# Function to calculate inflation
def calculate_inflation():
    try:
        # Get inputs from GUI
        old_price = float(old_price_entry.get())
        new_price = float(new_price_entry.get())
        old_year = int(old_year_entry.get())
        new_year = int(new_year_entry.get())
        base_currency = base_currency_var.get()
        target_currency = target_currency_var.get()

        # Calculate years difference
        years_difference = new_year - old_year
        if years_difference <= 0:
            messagebox.showerror("Invalid Input", "New year must be greater than old year.")
            return

        # Fetch real-time exchange rate
        if base_currency != target_currency:
            exchange_rate = get_exchange_rate(base_currency, target_currency)
            if exchange_rate is None:
                return  # Exit if we couldn't fetch the rate
            old_price_converted = old_price * exchange_rate
        else:
            old_price_converted = old_price

        # Calculate inflation
        inflation_rate_total = ((new_price - old_price_converted) / old_price_converted) * 100
        average_annual_inflation = (((new_price / old_price_converted) ** (1 / years_difference)) - 1) * 100

        # Display results and show pie chart
        show_result(inflation_rate_total, average_annual_inflation, old_price_converted, new_price, old_year, new_year, target_currency)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for prices and years.")
    except ZeroDivisionError:
        messagebox.showerror("Invalid Input", "Old price cannot be zero.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to display results and pie chart
def show_result(inflation_rate_total, average_annual_inflation, old_price, new_price, old_year, new_year, currency):
    # Prepare result text
    result_text = (f"Inflation from {old_year} to {new_year} is {inflation_rate_total:.2f}%.\n"
                   f"Average Annual Inflation Rate: {average_annual_inflation:.2f}%\n"
                   f"Price increased from {currency}{old_price:.2f} to {currency}{new_price:.2f}.")

    # Update result text box
    result_text_box.delete("1.0", tk.END)  # Clear existing text
    result_text_box.insert(tk.END, result_text)  # Insert new result text

    # Create and display pie chart
    if hasattr(show_result, 'pie_canvas'):
        show_result.pie_canvas.get_tk_widget().destroy()  # Destroy the previous pie chart if it exists

    fig, ax = plt.subplots(figsize=(3, 3), dpi=100)
    ax.pie([old_price, new_price], labels=[f"{currency} {old_price}", f"{currency} {new_price}"],
           colors=['#4CAF50', '#FF5722'], autopct='%1.1f%%')
    ax.set_title("Price Comparison")

    # Embed pie chart in the GUI
    show_result.pie_canvas = FigureCanvasTkAgg(fig, master=result_frame)
    show_result.pie_canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)
    show_result.pie_canvas.draw()

# Initialize main window
root = ctk.CTk()
root.title("Real-Time Inflation Calculator")
root.geometry("650x500")

# Frame to hold inputs
input_frame = ctk.CTkFrame(root, width=600, height=250)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Input fields
ctk.CTkLabel(input_frame, text="Old Price").grid(row=0, column=0, padx=10, pady=5, sticky="w")
old_price_entry = ctk.CTkEntry(input_frame, width=200)
old_price_entry.grid(row=0, column=1, padx=10, pady=5)

ctk.CTkLabel(input_frame, text="New Price").grid(row=1, column=0, padx=10, pady=5, sticky="w")
new_price_entry = ctk.CTkEntry(input_frame, width=200)
new_price_entry.grid(row=1, column=1, padx=10, pady=5)

ctk.CTkLabel(input_frame, text="Old Year").grid(row=2, column=0, padx=10, pady=5, sticky="w")
old_year_entry = ctk.CTkEntry(input_frame, width=200)
old_year_entry.grid(row=2, column=1, padx=10, pady=5)

ctk.CTkLabel(input_frame, text="New Year").grid(row=3, column=0, padx=10, pady=5, sticky="w")
new_year_entry = ctk.CTkEntry(input_frame, width=200)
new_year_entry.grid(row=3, column=1, padx=10, pady=5)

ctk.CTkLabel(input_frame, text="Base Currency").grid(row=4, column=0, padx=10, pady=5, sticky="w")
base_currency_var = tk.StringVar(value="USD")
base_currency_menu = ctk.CTkOptionMenu(input_frame, variable=base_currency_var, values=["USD", "EUR", "JPY", "INR", "GBP", "CNY"])
base_currency_menu.grid(row=4, column=1, padx=10, pady=5)

ctk.CTkLabel(input_frame, text="Target Currency").grid(row=5, column=0, padx=10, pady=5, sticky="w")
target_currency_var = tk.StringVar(value="USD")
target_currency_menu = ctk.CTkOptionMenu(input_frame, variable=target_currency_var, values=["USD", "EUR", "JPY", "INR", "GBP", "CNY"])
target_currency_menu.grid(row=5, column=1, padx=10, pady=5)

calculate_button = ctk.CTkButton(input_frame, text="Calculate Inflation", command=calculate_inflation)
calculate_button.grid(row=6, column=0, columnspan=2, pady=10)

# Frame to hold results (Text Explanation and Pie Chart)
result_frame = ctk.CTkFrame(root, width=600, height=250)
result_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Result text box (scrollable)
result_text_box = tk.Text(result_frame, wrap="word", height=5, width=30, font=("Arial", 10))
result_text_box.grid(row=0, column=0, padx=10, pady=10)
result_text_box.config(state="normal")  # Set to read-only when needed

# Configure root grid layout to allow dynamic resizing
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Start GUI event loop
root.mainloop()
