import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

# Mock data for simplicity
valid_pin = "1234"  # Replace this with a secure PIN storage method in real applications

# Availability data (branch, date, time) -> available computers
availability_data = {
    "Central Library": {
        "2024-10-30": {"9:00 AM": 3, "10:00 AM": 2, "11:00 AM": 0, "12:00 PM": 1},
        "2024-10-31": {"9:00 AM": 4, "10:00 AM": 1, "11:00 AM": 2, "12:00 PM": 3}
    },
    "East Branch": {
        "2024-10-30": {"9:00 AM": 1, "10:00 AM": 0, "11:00 AM": 1, "12:00 PM": 2},
        "2024-10-31": {"9:00 AM": 0, "10:00 AM": 1, "11:00 AM": 2, "12:00 PM": 1}
    }
}


# Function to check availability
def check_availability():
    branch = branch_var.get()
    date = date_var.get()
    time = time_var.get()

    if branch and date and time:
        available_computers = availability_data.get(branch, {}).get(date, {}).get(time, 0)
        if available_computers > 0:
            result_label.config(text=f"{available_computers} computers available at {branch} on {date} at {time}")
        else:
            result_label.config(text="No computers available for the selected branch, date, and time.")
    else:
        result_label.config(text="Please select all options to check availability.")


# Function to handle reservation
def reserve_computer():
    branch = branch_var.get()
    date = date_var.get()
    time = time_var.get()

    if branch and date and time:
        available_computers = availability_data.get(branch, {}).get(date, {}).get(time, 0)
        if available_computers > 0:
            # Update availability
            availability_data[branch][date][time] -= 1
            result_label.config(text=f"Computer reserved at {branch} on {date} at {time}")
        else:
            result_label.config(text="Sorry, no computers are available for the selected time.")
    else:
        result_label.config(text="Please fill all fields to reserve a computer.")


# Function to verify login PIN
def verify_pin():
    entered_pin = pin_entry.get()
    if entered_pin == valid_pin:
        login_frame.pack_forget()  # Hide login frame
        main_frame.pack()  # Show main reservation frame
    else:
        login_result_label.config(text="Incorrect PIN. Please try again.")


# Set up the main application window
root = tk.Tk()
root.title("Library Computer Reservation System")
root.geometry("400x400")

# Login Frame
login_frame = tk.Frame(root)
login_label = tk.Label(login_frame, text="Enter 4-digit PIN:")
login_label.pack(pady=10)
pin_entry = tk.Entry(login_frame, show="*", width=4)
pin_entry.pack()
login_button = tk.Button(login_frame, text="Login", command=verify_pin)
login_button.pack(pady=5)
login_result_label = tk.Label(login_frame, text="", fg="red")
login_result_label.pack()
login_frame.pack()

# Main Reservation Frame (hidden initially)
main_frame = tk.Frame(root)

# Branch selection
branch_label = tk.Label(main_frame, text="Select Library Branch:")
branch_label.pack()
branch_var = tk.StringVar()
branch_dropdown = ttk.Combobox(main_frame, textvariable=branch_var)
branch_dropdown['values'] = list(availability_data.keys())
branch_dropdown.pack()

# Date selection
date_label = tk.Label(main_frame, text="Select Date:")
date_label.pack()
date_var = tk.StringVar()
date_dropdown = ttk.Combobox(main_frame, textvariable=date_var)

# Generate dates for the next 7 days
today = datetime.today()
dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
date_dropdown['values'] = dates
date_dropdown.pack()

# Time selection
time_label = tk.Label(main_frame, text="Select Time:")
time_label.pack()
time_var = tk.StringVar()
time_dropdown = ttk.Combobox(main_frame, textvariable=time_var)
time_dropdown['values'] = (
"9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM")
time_dropdown.pack()

# Check availability button
check_button = tk.Button(main_frame, text="Check Availability", command=check_availability)
check_button.pack(pady=5)

# Reserve button
reserve_button = tk.Button(main_frame, text="Reserve Computer", command=reserve_computer)
reserve_button.pack(pady=5)

# Result label
result_label = tk.Label(main_frame, text="", fg="green")
result_label.pack()

root.mainloop()
