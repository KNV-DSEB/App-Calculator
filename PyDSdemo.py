import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import math
import statistics as sts
import requests
import scipy.stats as scs

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
def is_number(value):
    try:
        float(value)
        return True
    except:
        return False

class Statistics:
    def __init__(self, notebook):
        self.window = tk.Frame(notebook)
        notebook.add(self.window, text='Statistics')

        # 1-Variable and 2-Variable Modes
        self.one_var_mode = OneVariableStatistics(self.window)
        self.two_var_mode = TwoVariableStatistics(self.window)

        # Buttons for switching between modes
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(pady=10)

        one_var_button = ttk.Button(self.button_frame, text="1-Variable", command=self.show_one_var_mode)
        one_var_button.pack(side="left", padx=10)

        two_var_button = ttk.Button(self.button_frame, text="2-Variables", command=self.show_two_var_mode)
        two_var_button.pack(side="left", padx=10)

        # Show 1-variable mode by default
        self.show_one_var_mode()
    
    def show_one_var_mode(self):
        self.two_var_mode.hide()
        self.one_var_mode.show()

    def show_two_var_mode(self):
        self.one_var_mode.hide()
        self.two_var_mode.show()

    def run(self):
        self.window.mainloop()


class OneVariableStatistics:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.x_values = []
        self.x_entries = []
        self.x_entry_widgets = []

        self.create_widgets() 
    
    def create_widgets(self):
        self.table_frame = tk.Frame(self.frame)
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
        x_entry.grid(row=index, column=1)

        if index > 1:
            x_entry.config(state='disabled')
        
        self.x_entry_widgets.append(x_entry)
        self.x_entries.append(x_var)

        # Detect when user fills in the current row
        x_var.trace_add("write", lambda *args, row=index: self.check_add_row(row))

    def check_add_row(self, row):
        x_value = self.x_entries[row - 1].get()
        # Check if x_value is numeric:
        if is_number(x_value):
            # Enable the next row's entry if it exists
            if row < len(self.x_entries):
                self.x_entry_widgets[row].config(state='normal')
            else:
                # Create a new row if necessary
                self.create_row(row + 1)
                self.x_entry_widgets[row].config(state='normal')

            self.update_values()
        else:
            #self.x_entry_widgets[row-1].delete(0,tk.END) # clear invalid input
            self.x_entry_widgets[row-1].delete(0,tk.END)
            ###
            #  add error message
            ###

        # Update x_values with the current inputs

    def update_values(self):
        self.x_values = [float(x_var.get()) for x_var in self.x_entries if x_var.get()]
        
    def show(self):
        self.frame.pack(expand=True, fill='both')

    def hide(self):
        self.frame.pack_forget()


class TwoVariableStatistics:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)

        self.x_values = []
        self.y_values = []

        self.x_entries = []
        self.y_entries = []

        self.x_entry_widgets = []
        self.y_entry_widgets = []

        self.create_widgets()
    
    def create_widgets(self):
        self.table_frame = tk.Frame(self.frame)
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
        x_entry.grid(row=index, column=1)

        y_entry = ttk.Entry(self.table_frame, textvariable=y_var, font=DEFAULT_FONT_STYLE, state='disabled', width=10)
        y_entry.grid(row=index, column=2)

        # Enable input for the first row initially
        if index == 1:
            x_entry.config(state='normal')
            y_entry.config(state='normal')

        self.x_entry_widgets.append(x_entry)
        self.y_entry_widgets.append(y_entry)

        self.x_entries.append(x_var)
        self.y_entries.append(y_var)

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
        self.x_values = []  # Reset the x_values list
        self.y_values = []  # Reset the y_values list
    
        for i in range(len(self.x_entries)):
            x_value = self.x_entries[i].get()
            y_value = self.y_entries[i].get()
            
            # Only add valid x and y values
            if is_number(x_value) and is_number(y_value):
                self.x_values.append(float(x_value))
                self.y_values.append(float(y_value))
    
    def show(self):
        self.frame.pack(expand=True, fill='both')

    def hide(self):
        self.frame.pack_forget()

class StatisticsCalc:
    def __init__(self, x_values, y_values = None):
        self.inputX = np.array(x_values)
        self.inputY = np.array(y_values) if y_values is not None else []

    def n(self):
        return len(self.inputX) 

    def meanX(self):
        return np.mean(self.inputX)
    def meanY(self):
        return np.mean(self.inputY)

    def medianX(self):
        return np.median(self.inputX)
    def medianY(self):
        return np.median(self.inputY)
    
    def minX(self):
        return np.amin(self.inputX)
    def minY(self):
        return np.amin(self.inputY)
    
    def maxX(self):
        return np.amax(self.inputX)
    def maxY(self):
        return np.amax(self.inputY)

    def modeX(self):
        return sts.multimode(self.inputX)
    def modeY(self):
        return sts.multimode(self.inputY)
    
    def sumX(self):
        return np.sum(self.inputX)
    def sumY(self):
        return np.sum(self.inputY)

    def sum_squareX(self):
        return np.sum(np.square(self.inputX))
    def sum_squareY(self):
        return np.sum(np.square(self.inputY))
    
    def sum_XY(self):
        return np.sum(np.multiply(self.inputX, self.inputY))
    
    def sum_cubeX(self):
        return np.sum(np.multiply(np.square(self.inputX)), self.inputX)
    
    def sum_X_to_fourth(self):
        return np.sum(np.square(np.square(self.inputX)))
    

    def Q1_X(self):
        return np.percentile(self.inputX, 25)
    def Q1_Y(self):
        return np.percentile(self.inputY, 25)
    
    def Q3_X(self):
        return np.percentile(self.inputX, 75)
    def Q3_Y(self):
        return np.percentile(self.inputY, 75)
    
    def skewnessX(self):
        return scs.skew(self.inputX, bias = False)
    def skewnessY(self):
        return scs.skew(self.inputY, bias = False)

    # variablility
    def sample_varianceX(self):
        return sts.variance(self.inputX)
    def sample_varianceY(self):
        return sts.variance(self.inputY)
    
    def population_varianceX(self):
        return sts.pvariance(self.inputX)
    def population_varianceY(self):
        return sts.pvariance(self.inputY)

    def sample_std_dev_X(self):
        return sts.stdev(self.inputX)
    def sample_std_dev_Y(self):
        return sts.stdev(self.inputY)
    
    def population_std_dev_X(self):
        return sts.pstdev(self.inputX)
    def population_std_dev_Y(self):
        return sts.pstdev(self.inputY)
    
    #relation between two inputs
    def covariance(self):
        return sts.covariance(self.inputX, self.inputY)
    
    def correlation(self):
        return sts.correlation(self.inputX, self.inputY)
    
    def linear_reg(self, i = -1): ## corresponding display
        '''
            Y = a + bX
            0 = slope = b
            1 = intercept = a
            2 = r value = Pearson correlation coefficient  
            3 = p value
            4 = std error  = std error of the estimated slope
            5 = intercept error 
        '''
        if i == -1: # display all 6 values
            return scs.linregress(self.inputX, self.inputY)
        else: # display the chosen value only
            return scs.linregress(self.inputX, self.inputY)[i]


if __name__ == "__main__":
    app = CalculatorApp()
    app.run()
