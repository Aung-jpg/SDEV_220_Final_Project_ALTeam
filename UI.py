import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from user import User


class ReservationGUI:
    def __init__(self, master):
        self.master = master
        master.title("Computer Reservation System")
        master.geometry("500x400")  # Increased window size for more space
        master.configure(bg="#e8f0fe")  # Light blue background

        # Title Label
        title_label = tk.Label(master, text="Library Computer Reservation", font=("Helvetica", 18, "bold"),
                               bg="#e8f0fe", fg="#3b5998")
        title_label.pack(pady=(20, 10))

        # Frame for Entry Fields
        entry_frame = tk.Frame(master, bg="#e8f0fe", bd=2, relief="groove")
        entry_frame.pack(pady=20, padx=20, fill="x")

        # Library Card Number
        self.label_card_number = tk.Label(entry_frame, text="Library Card Number (14 Digit): ", font=("Arial", 12), bg="#e8f0fe")
        self.label_card_number.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_card_number = tk.Entry(entry_frame, font=("Arial", 12), width=30)
        self.entry_card_number.grid(row=0, column=1, padx=10, pady=10)

        # Library Card Pin
        self.label_pin = tk.Label(entry_frame, text="Library Card Pin (4 Digit): ", font=("Arial", 12), bg="#e8f0fe")
        self.label_pin.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_pin = tk.Entry(entry_frame, font=("Arial", 12), width=30)
        self.entry_pin.grid(row=0, column=1, padx=10, pady=10)

        # Time Slot
        self.label_time_slot = tk.Label(entry_frame, text="Time Slot (MM/DD/YY 24HR):", font=("Arial", 12),
                                        bg="#e8f0fe")
        self.label_time_slot.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_time_slot = tk.Entry(entry_frame, font=("Arial", 12), width=30)
        self.entry_time_slot.grid(row=1, column=1, padx=10, pady=10)

        # Frame for Buttons
        button_frame = tk.Frame(master, bg="#e8f0fe", bd=2, relief="groove")
        button_frame.pack(pady=20, padx=20)

        # Button Styling Options
        button_options = {
            "font": ("Arial", 11),
            "width": 20,
            "height": 2,
            "bg": "#4CAF50",  # Green background
            "fg": "white",  # White text color
            "activebackground": "#388E3C",  # Darker green when pressed
            "activeforeground": "white"
        }

        # Buttons
        self.reserve_button = tk.Button(button_frame, text="Reserve Computer", command=self.reserve_computer,
                                        **button_options)
        self.reserve_button.grid(row=0, column=0, padx=10, pady=10)

        self.cancel_button = tk.Button(button_frame, text="Cancel Reservation", command=self.cancel_reservation,
                                       **button_options)
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10)

        self.list_button = tk.Button(button_frame, text="List Reservations", command=self.list_reservations,
                                     **button_options)
        self.list_button.grid(row=1, column=0, padx=10, pady=10)

        self.refresh_button = tk.Button(button_frame, text="Refresh Reservations", command=self.refresh_reservations,
                                        **button_options)
        self.refresh_button.grid(row=1, column=1, padx=10, pady=10)

    def validate_card_number(self, card_number):
        if len(card_number) != 14 or not card_number.isdigit():
            messagebox.showerror("Input Error", "Library Card Number must be exactly 14 digits.")
            return False
        return True

    def reserve_computer(self):
        card_number = self.entry_card_number.get()
        time_slot = self.entry_time_slot.get()

        if not self.validate_card_number(card_number):
            return

        if not time_slot:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        user = User(card_number)
        try:
            if len(user.list_reservations()) > 3:
                messagebox.showerror("Reservation Limit",
                                     "Reservation limit of three has been hit. Please cancel reservations or wait.")
                return
        except TypeError:
            pass

        reservation = user.reservation
        try:
            reservation.reserve_computer(time_slot)
            messagebox.showinfo("Reservation Successful", "You have successfully made a reservation.")
        except TypeError:
            messagebox.showerror("Input Error", "Invalid time slot format. Please use 'MM/DD/YY HH:00'.")
            return
        except ValueError:
            messagebox.showerror("Value Error",
                                 "Cannot reserve that time slot. The library is closed, it is already reserved, or it's in the past.")
            return

    def cancel_reservation(self):
        card_number = self.entry_card_number.get()
        time_slot = self.entry_time_slot.get()

        if not self.validate_card_number(card_number):
            return

        if not time_slot:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        user = User(card_number)
        reservation = user.reservation
        try:
            reservation.cancel_reservation(time_slot)
            messagebox.showinfo("Cancellation Successful", "Your reservation has been cancelled.")
        except ValueError:
            messagebox.showerror("Input Error", "No reservation found for this time slot.")
            return

    def list_reservations(self):
        card_number = self.entry_card_number.get()

        if not self.validate_card_number(card_number):
            return

        user = User(card_number)
        reservations = user.list_reservations()

        if reservations:
            dates = [date[0] for date in reservations]
            readable_string = ', '.join(dates)
            messagebox.showinfo("Your Reservations", readable_string)
        else:
            messagebox.showinfo("Your Reservations", "No reservations found.")

    def refresh_reservations(self):
        card_number = self.entry_card_number.get()

        if not self.validate_card_number(card_number):
            return

        user = User(card_number)
        user.reservation.remove_past_reservations()
        messagebox.showinfo("Refresh Reservations", "Your reservations have been refreshed.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ReservationGUI(root)
    root.mainloop()
