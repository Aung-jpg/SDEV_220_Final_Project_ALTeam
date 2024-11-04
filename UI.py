import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from user import User

# Assume the ComputerReservation class code is already defined here...

class ReservationGUI:
    def __init__(self, master):
        self.master = master
        master.title("Computer Reservation System")

        self.label_card_number = tk.Label(master, text="Library Card Number:")
        self.label_card_number.pack()

        self.entry_card_number = tk.Entry(master)
        self.entry_card_number.pack()

        self.label_time_slot = tk.Label(master, text="Time Slot (MM/DD/YY HH:00):")
        self.label_time_slot.pack()

        self.entry_time_slot = tk.Entry(master)
        self.entry_time_slot.pack()

        self.reserve_button = tk.Button(master, text="Reserve Computer", command=self.reserve_computer)
        self.reserve_button.pack()

        self.cancel_button = tk.Button(master, text="Cancel Reservation", command=self.cancel_reservation)
        self.cancel_button.pack()

        self.list_button = tk.Button(master, text="List Reservations", command=self.list_reservations)
        self.list_button.pack()

        self.list_button = tk.Button(master, text="Refresh Reservations", command=self.refresh_reservations)
        self.list_button.pack()

    def reserve_computer(self):
        card_number = self.entry_card_number.get()
        time_slot = self.entry_time_slot.get()

        if not card_number or not time_slot:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        user = User(card_number)
        try:
            if len(user.list_reservations()) > 3:
                messagebox.showerror("Reservation Limit", "Reservation limit of three has been hit. Please cancel reservations or wait.")
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
            messagebox.showerror("Value Error", "Cannot reserve that time slot. The library is closed, it is already reserved, or it's in the past.")
            return


    def cancel_reservation(self):
        card_number = self.entry_card_number.get()
        time_slot = self.entry_time_slot.get()

        if not card_number or not time_slot:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        user = User(card_number)
        reservation = user.reservation
        try:
            reservation.cancel_reservation(time_slot)
        except ValueError:
            messagebox.showerror("Input Error", "No reservation found for this time slot.")
            return

    def list_reservations(self):
        card_number = self.entry_card_number.get()

        if not card_number:
            messagebox.showerror("Input Error", "Please enter your library card number.")
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
        if not card_number:
            messagebox.showerror("Input Error", "Please enter your library card number.")
            return
        user = User(card_number)
        user.reservation.remove_past_reservations()
        messagebox.showinfo("Refresh Reservations", "Your reservations have been refreshed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReservationGUI(root)
    root.mainloop()