import ctypes
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import pandas as pd

# Set DPI awareness to prevent scaling issues on Windows
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# Configure CustomTkinter appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# Function to calculate inflation
def calculate_inflation(*args):
    try:
        old_price = float(old_price_entry.get())
        new_price = float(new_price_entry.get())
        old_year = int(old_year_entry.get())
        new_year = int(new_year_entry.get())
        conversion_rate = float(conversion_rate_entry.get())

        years_difference = new_year - old_year
        if years_difference <= 0:
            messagebox.showerror("Invalid Input", "New year must be greater than old year.")
            return

        old_price_converted = old_price * conversion_rate  # This step is only needed if conversion rate is for currency
        
        # Inflation rate calculation (check for price decrease)
        inflation_rate_total = ((new_price - old_price_converted) / old_price_converted) * 100
        # Annual inflation calculation (compounding effect)
        if years_difference > 0:
            average_annual_inflation = (((new_price / old_price_converted) ** (1 / years_difference)) - 1) * 100
        else:
            average_annual_inflation = 0

        # Ensure that the inflation rate and annual inflation are rounded
        inflation_rate_total = round(inflation_rate_total, 2)
        average_annual_inflation = round(average_annual_inflation, 2)

        # Check for negative inflation and adjust accordingly (avoid display issues)
        if inflation_rate_total < 0:
            inflation_rate_total = abs(inflation_rate_total)  # Display as positive if it's negative (deflation)
        if average_annual_inflation < 0:
            average_annual_inflation = abs(average_annual_inflation)  # Display as positive

        display_result(inflation_rate_total, average_annual_inflation, old_price, new_price, old_year, new_year, old_price_converted)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for prices and years.")
    except ZeroDivisionError:
        messagebox.showerror("Invalid Input", "Old price cannot be zero.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Display result and draw chart based on selected chart type
def display_result(inflation_rate_total, average_annual_inflation, old_price, new_price, old_year, new_year, old_price_converted):
    result_text = (f"Inflation from {old_year} to {new_year} is {inflation_rate_total:.2f}%.\n"
                   f"Average Annual Inflation Rate: {average_annual_inflation:.2f}%\n"
                   f"Price increased from {old_price:.2f} to {new_price:.2f}.\n"
                   f"Old price converted to current currency: {old_price_converted:.2f}")
    result_text_box.delete("1.0", tk.END)
    result_text_box.insert(tk.END, result_text)

    # Clear previous chart if it exists
    for widget in result_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
    sns.set_theme(style="whitegrid", palette="pastel")
    years = pd.Series(range(old_year, new_year + 1))
    inflation_over_time = pd.Series([(1 + average_annual_inflation / 100) ** i for i in range(len(years))])

    chart_type = chart_type_var.get()
    if chart_type == "Pie Chart":
        labels = [f"Old Price: {old_price:.2f}", f"New Price: {new_price:.2f}"]
        sizes = [old_price, new_price]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
        ax.axis('equal')
    elif chart_type == "Histogram":
        sns.histplot(inflation_over_time, kde=True, ax=ax)
        ax.set_title("Inflation Distribution Over Time")
        ax.set_xlabel("Inflation Growth Factor")
    elif chart_type == "Box Plot":
        sns.boxplot(data=inflation_over_time, ax=ax)
        ax.set_title("Box Plot of Inflation Over Time")
        ax.set_ylabel("Inflation Growth Factor")
    elif chart_type == "Violin Plot":
        sns.violinplot(data=inflation_over_time, ax=ax)
        ax.set_title("Violin Plot of Inflation Over Time")
        ax.set_ylabel("Inflation Growth Factor")
    elif chart_type == "Bar Plot":
        sns.barplot(x=years, y=inflation_over_time, ax=ax)
        ax.set_title("Bar Plot of Inflation Growth Over Time")
        ax.set_xlabel("Year")
        ax.set_ylabel("Growth Factor")
    elif chart_type == "Scatter Plot":
        sns.scatterplot(x=years, y=inflation_over_time, ax=ax)
        ax.set_title("Scatter Plot of Inflation Growth Over Time")
        ax.set_xlabel("Year")
        ax.set_ylabel("Growth Factor")
    else:
        sns.lineplot(x=years, y=inflation_over_time, ax=ax)
        ax.set_title("Inflation Growth Over Time")
        ax.set_xlabel("Year")
        ax.set_ylabel("Price Growth Factor")

    chart_canvas = FigureCanvasTkAgg(fig, master=result_frame)
    chart_canvas.get_tk_widget().pack()
    chart_canvas.draw()

root = ctk.CTk()
root.title("Inflation Calculator")
root.geometry("850x700")
root.eval('tk::PlaceWindow . center')

input_frame = ctk.CTkFrame(root, width=700, height=250, corner_radius=10)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Input Fields
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

ctk.CTkLabel(input_frame, text="Conversion Rate").grid(row=4, column=0, padx=10, pady=5, sticky="w")
conversion_rate_entry = ctk.CTkEntry(input_frame, width=200)
conversion_rate_entry.grid(row=4, column=1, padx=10, pady=5)

ctk.CTkLabel(input_frame, text="Currency").grid(row=5, column=0, padx=10, pady=5, sticky="w")
currency_var = tk.StringVar(value="USD")
currency_menu = ctk.CTkOptionMenu(input_frame, variable=currency_var, values=["USD", "EUR", "JPY", "INR", "GBP", "CNY"])
currency_menu.grid(row=5, column=1, padx=10, pady=5)

ctk.CTkLabel(input_frame, text="Chart Type").grid(row=6, column=0, padx=10, pady=5, sticky="w")
chart_type_var = tk.StringVar(value="Line Chart")
chart_type_menu = ctk.CTkOptionMenu(input_frame, variable=chart_type_var, values=["Line Chart", "Pie Chart", "Histogram", "Box Plot", "Violin Plot", "Bar Plot", "Scatter Plot"])
chart_type_menu.grid(row=6, column=1, padx=10, pady=5)

calculate_button = ctk.CTkButton(input_frame, text="Calculate Inflation", command=calculate_inflation, fg_color="#A8DADC")
calculate_button.grid(row=7, column=0, columnspan=2, pady=10)

# Result Frame
result_frame = ctk.CTkFrame(root, width=700, height=300, corner_radius=10)
result_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Text Box for result
result_text_box = tk.Text(root, wrap="word", height=5, width=80, font=("Arial", 12), bg="#F1FAEE", fg="#1D3557")
result_text_box.grid(row=2, column=0, padx=10, pady=(5, 15))

root.mainloop()
