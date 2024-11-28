import tkinter as tk
from tkinter import messagebox
from user import User

class GUI:
    def __init__(self, root) -> None:
        self.root = root
        root.title("Computer Reservation System")
        root.geometry("1000x600")
        root.configure(bg="#ffffff")
        self.large_font = ('Helvetica', 20)

        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Library Card Number", font=self.large_font).grid(row=0, column=0)
        tk.Label(self.root, text="Pin", font=self.large_font).grid(row=1, column=0)
        self.lcn_entry = tk.Entry(self.root, font=self.large_font)
        self.pin_entry = tk.Entry(self.root, show="*", font=self.large_font)

        self.lcn_entry.grid(row=0, column=1)
        self.pin_entry.grid(row=1, column=1)

        tk.Button(self.root, text="Login", command=self.login, font=self.large_font).grid(row=2, column=0, columnspan=2)

    def login(self):
        lcn = self.lcn_entry.get()
        pin = self.pin_entry.get()
        if lcn == "" or pin == "":
            messagebox.showerror("Input Error", "Input Error: there is no input in one or more entries")
            return
        try:
            self.user = User(lcn, pin)

        except TypeError as e:
            # lcn doesn't exist
            messagebox.showerror("Error", f"{e}")
            return

        except ValueError as e:
            # wrong pin
            messagebox.showerror("Error", f"{e}")
            return
        
        else:
            self.create_main_screen()
    
    def create_main_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text=f"Logged in as Library Card Number: {self.user.library_card_number}", font=self.large_font).pack()

        self.reserve_computer_button = tk.Button(self.root, text="Reserve Computer", command=self.create_reserve_computer_screen, font=self.large_font).pack()

    def create_reserve_computer_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Reserve Computer", font=self.large_font).pack()
        

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