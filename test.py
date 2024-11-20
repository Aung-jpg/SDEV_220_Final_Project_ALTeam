import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import datetime

def show_selected_date_time():
    selected_date = cal.get_date()  # Get selected date from calendar
    selected_time = time_combobox.get()  # Get selected time from combobox
    result_label.config(text=f"Selected Date and Time: {selected_date} {selected_time}")

# Create the main window
root = tk.Tk()
root.title("Calendar with Time Selection")

# Create a Calendar widget
cal = Calendar(root, selectmode='day', date_pattern='yyyy-mm-dd')
cal.pack(pady=20)

# Create a Label for Time Selection
time_label = tk.Label(root, text="Select Time:")
time_label.pack()

# Create a Combobox for Time selection (24-hour format)
time_options = [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in range(0, 60, 30)]  # Time options every 30 minutes
time_combobox = ttk.Combobox(root, values=time_options, state="readonly")
time_combobox.set("12:00")  # Default time
time_combobox.pack(pady=10)

# Button to show the selected date and time
select_button = tk.Button(root, text="Show Selected Date & Time", command=show_selected_date_time)
select_button.pack(pady=10)

# Label to display the selected date and time
result_label = tk.Label(root, text="")
result_label.pack(pady=20)

# Run the application
root.mainloop()
