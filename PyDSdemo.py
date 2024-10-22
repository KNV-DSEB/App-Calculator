import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import math
import statistics as sts
import requests

# Define Font and Color Constants
LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"

# Main application class
class CalculatorApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("600x667")
        self.window.resizable(0, 0)
        self.window.title("Calculator")

        # Create a notebook for tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill='both')

        # Create tabs
        self.basic_calculator = Calculate(self.notebook)
        self.currency_converter = CurrencyConverter(self.notebook)
        self.unit_converter = UnitConverter(self.notebook)
        self.statistics_calculator = Statistics(self.notebook)

    def run(self):
        self.window.mainloop()

# Basic Calculator functionality
class Calculate:
    def __init__(self, notebook):
        self.window = tk.Frame(notebook)
        notebook.add(self.window, text='Basic Calculator')

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))

            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

# Currency Converter functionality
class CurrencyConverter:
    def __init__(self, notebook):
        self.window = tk.Frame(notebook)
        notebook.add(self.window, text='Currency Converter')

        # Currency conversion UI
        self.create_currency_converter()

    def create_currency_converter(self):
        tk.Label(self.window, text="Currency Converter", font=DEFAULT_FONT_STYLE).pack(pady=20)

        # Amount input
        tk.Label(self.window, text="Amount", font=DEFAULT_FONT_STYLE).pack(pady=10)
        self.amount_entry = tk.Entry(self.window, font=DEFAULT_FONT_STYLE)
        self.amount_entry.pack(pady=10)

        # From currency dropdown
        tk.Label(self.window, text="From", font=DEFAULT_FONT_STYLE).pack(pady=10)
        self.from_currency = ttk.Combobox(self.window, values=["USD", "EUR", "JPY", "VND"], font=DEFAULT_FONT_STYLE)
        self.from_currency.pack(pady=10)

        # To currency dropdown
        tk.Label(self.window, text="To", font=DEFAULT_FONT_STYLE).pack(pady=10)
        self.to_currency = ttk.Combobox(self.window, values=["USD", "EUR", "JPY", "VND"], font=DEFAULT_FONT_STYLE)
        self.to_currency.pack(pady=10)

        # Convert button
        self.result_label = tk.Label(self.window, text="", font=DEFAULT_FONT_STYLE)
        ttk.Button(self.window, text="Convert", command=self.convert_currency).pack(pady=10)
        self.result_label.pack(pady=10)

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_currency = self.from_currency.get()
            to_currency = self.to_currency.get()

            url = f"https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/{from_currency}"
            response = requests.get(url)
            response.raise_for_status()  # Raise an error if the request failed

            rate = response.json()['rates'].get(to_currency)
            if rate:
                result = amount * rate
                self.result_label.config(text=f'{amount} {from_currency} = {result:.2f} {to_currency}')
            else:
                messagebox.showerror("Error", "Conversion rate not found")
        except Exception:
            messagebox.showerror("Error", "Conversion error")

# Unit Converter functionality
class UnitConverter:
    def __init__(self, notebook):
        self.window = tk.Frame(notebook)
        notebook.add(self.window, text='Unit Converter')

        self.create_unit_converter()

    def create_unit_converter(self):
        tk.Label(self.window, text="Unit Converter", font=DEFAULT_FONT_STYLE).pack(pady=20)

        tk.Label(self.window, text="Value", font=DEFAULT_FONT_STYLE).pack(pady=10)
        self.value_entry = tk.Entry(self.window, font=DEFAULT_FONT_STYLE)
        self.value_entry.pack(pady=10)

        tk.Label(self.window, text="From", font=DEFAULT_FONT_STYLE).pack(pady=10)
        self.from_unit = ttk.Combobox(self.window, values=["m", "km", "cm"], font=DEFAULT_FONT_STYLE)
        self.from_unit.pack(pady=10)

        tk.Label(self.window, text="To", font=DEFAULT_FONT_STYLE).pack(pady=10)
        self.to_unit = ttk.Combobox(self.window, values=["m", "km", "cm"], font=DEFAULT_FONT_STYLE)
        self.to_unit.pack(pady=10)

        self.result_label = tk.Label(self.window, text="", font=DEFAULT_FONT_STYLE)
        ttk.Button(self.window, text="Convert", command=self.convert_units).pack(pady=10)
        self.result_label.pack(pady=10)

    def convert_units(self):
        try:
            value = float(self.value_entry.get())
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()

            conversion_factors = {"m": 1, "km": 0.001, "cm": 100}
            result = value * conversion_factors[to_unit] / conversion_factors[from_unit]
            self.result_label.config(text=f'{value} {from_unit} = {result:.4f} {to_unit}')
        except ValueError:
            messagebox.showerror("Error", "Invalid input")

# Statistics functionality
class Statistics:
    def __init__(self, notebook):
        self.window = tk.Frame(notebook)
        notebook.add(self.window, text='Statistics')

        # Radio buttons to choose 1-variable or 2-variables
        self.mode = tk.StringVar(value="1-Variable")
        self.radio_1_variable = ttk.Radiobutton(
            self.window, text="1-Variable", variable=self.mode, value="1-Variable", command=self.show_option)
        self.radio_1_variable.pack(anchor='w', padx=10, pady=5)

        self.radio_2_variables = ttk.Radiobutton(
            self.window, text="2-Variables", variable=self.mode, value="2-Variables", command=self.show_option)
        self.radio_2_variables.pack(anchor='w', padx=10, pady=5)

        # Frame to display content
        self.content_frame = tk.Frame(self.window)
        self.content_frame.pack(expand=True, fill='both')

        # Instances of the 1-variable and 2-variable classes
        self.one_var_stat = OneVariableStatistics(self.content_frame)
        self.two_var_stat = TwoVariableStatistics(self.content_frame)

        self.show_option()  # Display the default option

    def show_option(self):
        # Clear the content frame before showing the new option
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Show 1-variable or 2-variables functionality based on selection
        if self.mode.get() == "1-Variable":
            self.one_var_stat.display()
        else:
            self.two_var_stat.display()

class OneVariableStatistics:
    def __init__(self, parent):
        self.parent = parent
        self.x_values = []
        self.x_entries = []
        self.x_entry_widgets = []

    def display(self):
        # Create the table for 1-variable statistics
        self.table_frame = tk.Frame(self.parent)
        self.table_frame.pack(pady=10)

        tk.Label(self.table_frame, text="", font=DEFAULT_FONT_STYLE, width=5).grid(row=0, column=0)
        tk.Label(self.table_frame, text="x", font=DEFAULT_FONT_STYLE, width=10).grid(row=0, column=1)

        self.create_row(1)
        self.create_row(2)
        self.create_row(3)
        self.create_row(4)

    def create_row(self, index):
        # Create a label for the index in the first column
        tk.Label(self.table_frame, text=str(index), font=DEFAULT_FONT_STYLE, width=5).grid(row=index, column=0)

        x_var = tk.StringVar()
        x_entry = ttk.Entry(self.table_frame, textvariable=x_var, font=DEFAULT_FONT_STYLE, width=10)

        if index > 1:
            x_entry.config(state='disabled')

        self.x_entries.append(x_var)
        self.x_entry_widgets.append(x_entry)

        x_entry.grid(row=index, column=1)

        # Detect when user fills in the current row
        x_var.trace_add("write", lambda *args, row=index: self.check_add_row(row))

    def check_add_row(self, row):
        if self.x_entries[row - 1].get():
            # Enable the next row's entry if it exists
            if row < len(self.x_entry_widgets):
                self.x_entry_widgets[row].config(state='normal')
            else:
                # Create a new row if necessary
                self.create_row(row + 1)
                self.x_entry_widgets[row].config(state='normal')

        # Update x_values with the current inputs
        self.update_values()

    def update_values(self):
        self.x_values = [x_var.get() for x_var in self.x_entries if x_var.get()]


class TwoVariableStatistics:
    def __init__(self, parent):
        self.parent = parent
        self.x_values = []
        self.y_values = []
        self.x_entries = []
        self.y_entries = []
        self.x_entry_widgets = []
        self.y_entry_widgets = []

    def display(self):
        # Create the table for 2-variable statistics
        self.table_frame = tk.Frame(self.parent)
        self.table_frame.pack(pady=10)

        tk.Label(self.table_frame, text="", font=DEFAULT_FONT_STYLE, width=5).grid(row=0, column=0)
        tk.Label(self.table_frame, text="x", font=DEFAULT_FONT_STYLE, width=10).grid(row=0, column=1)
        tk.Label(self.table_frame, text="y", font=DEFAULT_FONT_STYLE, width=10).grid(row=0, column=2)

        self.create_row(1)
        self.create_row(2)
        self.create_row(3)
        self.create_row(4)

    def create_row(self, index):
        tk.Label(self.table_frame, text=str(index), font=DEFAULT_FONT_STYLE, width=5).grid(row=index, column=0)

        x_var = tk.StringVar()
        y_var = tk.StringVar()

        x_entry = ttk.Entry(self.table_frame, textvariable=x_var, font=DEFAULT_FONT_STYLE, state='disabled', width=10)
        y_entry = ttk.Entry(self.table_frame, textvariable=y_var, font=DEFAULT_FONT_STYLE, state='disabled', width=10)

        # Enable input for the first row initially
        if index == 1:
            x_entry.config(state='normal')
            y_entry.config(state='normal')

        self.x_entries.append(x_var)
        self.y_entries.append(y_var)
        self.x_entry_widgets.append(x_entry)
        self.y_entry_widgets.append(y_entry)

        x_entry.grid(row=index, column=1)
        y_entry.grid(row=index, column=2)

        # Detect when user fills in the current row
        x_var.trace_add("write", lambda *args, row=index: self.check_add_row(row))
        y_var.trace_add("write", lambda *args, row=index: self.check_add_row(row))

    def check_add_row(self, row):
        if self.x_entries[row - 1].get() and self.y_entries[row - 1].get():
            # Enable the next row's entries if they exist
            if row < len(self.x_entry_widgets):
                self.x_entry_widgets[row].config(state='normal')
                self.y_entry_widgets[row].config(state='normal')
            else:
                # Create a new row if necessary
                self.create_row(row + 1)
                self.x_entry_widgets[row].config(state='normal')
                self.y_entry_widgets[row].config(state='normal')

        # Update x_values and y_values with the current inputs
        self.update_values()

    def update_values(self):
        self.x_values = [x_var.get() for x_var in self.x_entries if x_var.get()]
        self.y_values = [y_var.get() for y_var in self.y_entries if y_var.get()]


if __name__ == "__main__":
    app = CalculatorApp()
    app.run()
