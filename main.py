import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import requests
import matplotlib.pyplot as plt

# Main window
root = tk.Tk()
root.title("Calculator Application")
root.geometry("600x600")
root['bg'] = '#f5f5f5'  # Light grey background for a softer look

# Define new color scheme
btn_bg = "#4CAF50"  # Green background for buttons
btn_fg = "#ffffff"  # White text on buttons
entry_bg = "#ffffff"  # White background for entry
entry_fg = "#000000"  # Black text for entry

# Styles for ttk buttons
style = ttk.Style()
style.configure("TButton", font=("Arial", 18), padding=10)
style.configure("TFrame", background="#f5f5f5")  # Apply background to frames
style.configure("TLabel", background="#f5f5f5", font=("Arial", 14))  # Consistent label style

# Notebook tabs
tab_control = ttk.Notebook(root)
calc_tab = ttk.Frame(tab_control)
currency_tab = ttk.Frame(tab_control)
converter_tab = ttk.Frame(tab_control)
stats_tab = ttk.Frame(tab_control)

tab_control.add(calc_tab, text='Basic Calculator')
tab_control.add(currency_tab, text='Currency Converter')
tab_control.add(converter_tab, text='Unit Converter')
tab_control.add(stats_tab, text='Statistics')

tab_control.pack(expand=1, fill="both")

# ========== Basic Calculator Functionality ==========

calc_history = []  # History list

def clear_display():
    display.set("")

def evaluate_expression():
    try:
        expression = display.get()
        result = eval(expression)
        display.set(result)
        calc_history.append(f'{expression} = {result}')
    except Exception as e:
        messagebox.showerror("Error", "Invalid input!")

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Calculation History")
    history_list = tk.Listbox(history_window)
    history_list.pack(fill=tk.BOTH, expand=True)
    for item in calc_history:
        history_list.insert(tk.END, item)

def append_to_expression(value):
    current_expr = display.get()
    if current_expr and current_expr[-1] in '+-*/' and value in '+-*/':
        return
    if not current_expr and value in '+-*/':
        return
    display.set(current_expr + value)

# Display entry
display = tk.StringVar()
calc_entry = tk.Entry(calc_tab, textvariable=display, font=('Arial', 24), bd=10, insertwidth=4, width=14, borderwidth=4, bg=entry_bg, fg=entry_fg, justify='right')
calc_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# ========== Calculator Buttons ==========

buttons = [
    '7', '8', '9', '/', 
    '4', '5', '6', '*', 
    '1', '2', '3', '-', 
    '0', '.', '=', '+'
]

row_val, col_val = 1, 0
for button in buttons:
    if button == '=':
        action = evaluate_expression
    else:
        action = lambda x=button: append_to_expression(x)
    
    ttk.Button(calc_tab, text=button, command=action, width=10).grid(row=row_val, column=col_val, padx=5, pady=5)
    
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# Clear (AC) button and history button
ttk.Button(calc_tab, text='AC', command=clear_display, width=10).grid(row=5, column=0, columnspan=2, padx=5, pady=5)
ttk.Button(calc_tab, text='History', command=show_history, width=10).grid(row=5, column=2, columnspan=2, padx=5, pady=5)
