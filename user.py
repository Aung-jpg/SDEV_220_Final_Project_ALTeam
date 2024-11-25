from reservation import ComputerReservation
import sqlite3
import hashlib

class User():
    """User class will interact with a ComputerReservation class to reverse a computer"""
    def __init__(self, library_card_number:str, pin:str) -> None:
        self.library_card_number = library_card_number
        self.pin = pin
        validation = self.validate_user()
        if validation == 0:
            self.reservation = ComputerReservation(self.library_card_number, self.pin)
        elif validation == -1:
            raise TypeError("Library Card Number doesn't exist")
        elif validation == 1:
            raise ValueError("Library Card Number and Pin don't go together")
    
    def list_reservations(self):
        """List all reservations for the user."""
        with self.reservation.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT time_slot FROM reservations WHERE library_card_number = ?", (self.library_card_number,))
            reservations = cursor.fetchall()
            if reservations:
                return reservations
            else:
                return
            
    def encrypt_pin(self, pin):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(pin.encode('utf-8'))
        return sha256_hash.hexdigest()
            
    def register_user_testing(self):
        res = ComputerReservation(self.library_card_number, self.pin)
        exists = res.user_exists()
        if not exists:
            res.add_self()
    
    def validate_user(self):
        conn = sqlite3.connect('LibraryMembers.db')
        cursor = conn.cursor()
        cursor.execute("SELECT library_card_number, pin FROM all_members WHERE library_card_number = ?", (self.library_card_number,))
        row = cursor.fetchone()  # Fetch the result
        if row == None:
            #lcn doesn't exist
            return -1
        if self.encrypt_pin(self.pin) == row[1]:
            # lcn and pin match
            return 0
        else:
            # lcn exists but pins don't match
            return 1


person = User("2222", "0000")
