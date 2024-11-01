import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from reservation import ComputerReservation

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

    def reserve_computer(self):
        card_number = self.entry_card_number.get()
        time_slot = self.entry_time_slot.get()

        if not card_number or not time_slot:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        reservation = ComputerReservation(card_number)
        reservation.reserve_computer(time_slot)

    def cancel_reservation(self):
        card_number = self.entry_card_number.get()
        time_slot = self.entry_time_slot.get()

        if not card_number or not time_slot:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        reservation = ComputerReservation(card_number)
        reservation.cancel_reservation(time_slot)

    def list_reservations(self):
        card_number = self.entry_card_number.get()

        if not card_number:
            messagebox.showerror("Input Error", "Please enter your library card number.")
            return

        reservation = ComputerReservation(card_number)
        reservations = reservation.list_reservations()
        
        # TODO: make reservations show all the reservations in one messagebox
        if reservations:
            messagebox.showinfo("Your Reservations", "\n".join(reservations))
        else:
            messagebox.showinfo("Your Reservations", "No reservations found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReservationGUI(root)
    root.mainloop()