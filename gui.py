import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from user import User

class GUI:
    """
    A GUI-based system for a computer reservation system.
    """
    def __init__(self, root) -> None:
        """
        Initialize the GUI application with the root window, setting up
        the title, geometry, and default login screen.

        Args:
            root (tk.Tk): The root window for the application.
        """
        self.root = root
        root.title("Computer Reservation System")
        root.geometry("800x600")
        root.configure(bg="#ffffff")
        self.large_font = ('Helvetica', 20)

        self.create_login_screen()

    def create_login_screen(self):
        """
        Create and display the login screen with input fields for library card number and pin.
        """
        self.clear_screen()
        tk.Label(self.root, text="Library Card Number", font=self.large_font).pack(pady=10)
        self.lcn_entry = tk.Entry(self.root, font=self.large_font)
        self.lcn_entry.pack()
        tk.Label(self.root, text="Pin", font=self.large_font).pack(pady=5)
        self.pin_entry = tk.Entry(self.root, show="*", font=self.large_font)
        self.pin_entry.pack()

        tk.Button(self.root, text="Login", command=self.login, font=self.large_font).pack(pady=10)

    def login(self):
        """
        Handle the login process by validating input and authenticating the user.

        Raises appropriate error messages for invalid input or authentication failures.
        """
        lcn = self.lcn_entry.get()
        pin = self.pin_entry.get()
        if lcn == "" or pin == "":
            messagebox.showerror("Input Error", "Input Error: there is no input in one or more entries")
            return
        try:
            self.user = User(lcn, pin)

        except TypeError as e:
            # library card number doesn't exist
            messagebox.showerror("Error", f"{e}")
            return

        except ValueError as e:
            # wrong pin
            messagebox.showerror("Error", f"{e}")
            return
        
        else:
            self.create_main_screen()
    
    def create_main_screen(self):
        """
        Display the main screen with options to manage reservations.
        """
        self.clear_screen()
        self.user.reservation.remove_past_reservations()
        
        tk.Label(self.root, text=f"Logged in as Library Card Number: {self.user.library_card_number}", font=self.large_font).pack(pady=5)

        self.reserve_computer_button = tk.Button(self.root, text="Reserve Computer", command=self.create_reserve_computer_screen, font=self.large_font).pack(pady=5)
        self.cancel_reservation_button = tk.Button(self.root, text="Cancel Computer Reservation", command=self.cancel_computer_reservation_screen, font=self.large_font).pack(pady=5)
        self.list_reservations_button = tk.Button(self.root, text="List Reservations", command=self.list_reservations_screen, font=self.large_font).pack(pady=5)
        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout, font=self.large_font).pack(pady=5)

    def create_reserve_computer_screen(self):
        """
        Create and display the screen for reserving a computer.
        Allows the user to select a date and time for the reservation.
        """
        self.clear_screen()

        tk.Label(self.root, text="Reserve Computer", font=self.large_font).pack(pady=5)
        self.cal = Calendar(root, selectmode='day', date_pattern='mm/dd/yy')
        self.cal.pack(pady=10)

        tk.Label(root, text="Select Time:").pack()
        time_options = [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in range(0, 60, 60)]  
        self.time_combobox = ttk.Combobox(root, values=time_options, state="readonly")
        self.time_combobox.set("12:00") # default
        self.time_combobox.pack(pady=5)
        tk.Button(root, text="Create Reservation", command=self.create_reservation).pack(pady=5)

        tk.Button(root, text="Back", command=self.create_main_screen).pack(pady=5)
    
    def create_reservation(self):
        """
        Attempt to create a reservation for a selected date and time.

        Handles errors for invalid reservations (e.g., past times, already reserved).
        """
        selected_date = self.cal.get_date()  # Get selected date from calendar
        selected_time = self.time_combobox.get()  # Get selected time from combobox
        date_time_string = selected_date + " " + selected_time
        current_reservations = len(self.user.list_reservations())

        if current_reservations >= 3:
            messagebox.showerror("Error", f"You have {current_reservations}, you can't have any more")
            return
        
        try:
            self.user.reservation.reserve_computer(date_time_string)

        except TypeError as e:
            # Library isn't open
            messagebox.showerror("Error", f"{e}")
            return

        except ValueError as e:
            # time slot is in the past
            messagebox.showerror("Error", f"{e}")
            return
        
        except IndexError as e:
            # time slot is already reserved
            messagebox.showerror("Error", f"{e}")
            return
        
        else:
            messagebox.showinfo("Reservation Success", f"Reservation for {date_time_string} successful!")
            self.create_main_screen()
    
    def cancel_computer_reservation_screen(self):
        """
        Display the screen for canceling an existing computer reservation.
        """
        self.clear_screen()

        tk.Label(self.root, text="Cancel Reservation", font=self.large_font).pack(pady=5)
        reservations = self.user.list_reservations()
        reservations = [r[0] for r in reservations]
        tk.Label(root, text="Select Reservation:").pack()
        self.reservation_combobox = ttk.Combobox(root, values=reservations, state="readonly")
        self.reservation_combobox.pack(pady=5)

        tk.Button(root, text="Cancel Reservation", command=self.cancel_reservation).pack(pady=5)

        tk.Button(root, text="Back", command=self.create_main_screen).pack(pady=5)

    def cancel_reservation(self):
        """
        Cancel the selected reservation.
        
        Raises error messages if the reservation cannot be canceled.
        """
        reservation = self.reservation_combobox.get()
        try:
            self.user.reservation.cancel_reservation(reservation)  
        except ValueError as e:
            # reservation doesn't exist
            messagebox.showerror("Error", f"{e}")
            return
        else:
            messagebox.showinfo("Cancelation Success", f"Canceled reservation for {reservation}!")
            self.create_main_screen()

    def list_reservations_screen(self):
        """
        Display a list of current reservations made by the user.
        """
        self.clear_screen()
        tk.Label(self.root, text="Reservations:", font=self.large_font).pack(pady=5)
        reservations = self.user.list_reservations()
        for reservation in reservations:
            tk.Label(self.root, text=f"{reservation[0]}").pack(pady=5)
        tk.Button(root, text="Back", command=self.create_main_screen).pack(pady=5)

    def logout(self):
        """
        Log out the current user and return to the login screen.
        """
        self.user = None
        self.create_login_screen()

    def clear_screen(self):
        """
        Clear all widgets from the root window.
        """
        for widget in self.root.winfo_children():
            widget.destroy()
    

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()