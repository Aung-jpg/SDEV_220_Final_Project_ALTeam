import sqlite3
from datetime import datetime
import hashlib


class ComputerReservation:
    def __init__(self, library_card_number, pin):
        self.create_tables()
        self.library_card_number = library_card_number
        self.pin = pin
        
        
    @staticmethod
    def get_db():
        conn = sqlite3.connect('LibraryMembers.db')
        return conn
    

    def user_exists(self):
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM all_members WHERE library_card_number = ?)", (self.library_card_number,))
        exists = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return exists
    

    def add_self(self):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO all_members (library_card_number, pin) VALUES (?, ?)', (self.library_card_number, self.encrypt_pin(self.pin,)))
            conn.commit()


    def encrypt_pin(self, pin):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(pin.encode('utf-8'))
        return sha256_hash.hexdigest()


    def create_tables(self):
        with self.get_db() as conn:
            cursor = conn.cursor()
            
            # Enable foreign key constraints for this session
            cursor.execute('PRAGMA foreign_keys = ON;')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS all_members (
                    library_card_number TEXT PRIMARY KEY,
                    pin TEXT NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reservations (
                    time_slot TEXT PRIMARY KEY,
                    library_card_number TEXT,
                    FOREIGN KEY(library_card_number) REFERENCES all_members(library_card_number)
                )
            ''')
            conn.commit()


    def reserve_computer(self, time_slot: str):
        if not self.is_valid_time_slot(time_slot):
            raise TypeError("Invalid time slot format. Please use 'MM/DD/YY HH:00'.")
        
        if self.is_past_time_slot(time_slot):
            raise ValueError("Cannot reserve a time slot in the past.")

        with self.get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT EXISTS(SELECT 1 FROM reservations WHERE time_slot = ?)", (time_slot,))
                if cursor.fetchone()[0]:
                    raise ValueError("Time slot is already reserved.")

                cursor.execute("INSERT INTO reservations (time_slot, library_card_number) VALUES (?, ?)", (time_slot, self.library_card_number))
                conn.commit()
                print(f"Computer reserved for {self.library_card_number} at {time_slot}.")
            except sqlite3.Error as e:
                print(f"Failed to reserve computer: {e}")


    def cancel_reservation(self, time_slot: str):
        """Cancel a reservation for the specified time slot."""
        with self.get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM reservations WHERE time_slot = ? AND library_card_number = ?",
                               (time_slot, self.library_card_number))
                conn.commit()
                if cursor.rowcount > 0:
                    print(f"Reservation for {time_slot} cancelled.")
                else:
                    raise ValueError("No reservation found for this time slot.")
            except sqlite3.Error as e:
                print(f"Failed to cancel reservation: {e}")


    @staticmethod
    def is_valid_time_slot(time_slot):
        try:
            dt = datetime.strptime(time_slot, '%m/%d/%y %H:%M')
            # Ensure the time is on the hour
            if dt.minute != 0:
                return False
            weekday = dt.weekday()
            if weekday == 6:
                print("Invalid time slot: closed on Sunday")
                return False
            if weekday in [4, 5]:
                # Friday and Saturday closed hours
                if dt.hour in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 18, 19, 20, 21, 22, 23, 24]:
                    print("Invalid time slot: open between 10am-6pm")
                    return False
            if weekday in [0, 1, 2, 3]:
                # regular days closed hours
                if dt.hour in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24]:
                    print("Invalid time slot: open between 10am-9pm")
                    return False
            return True
        except ValueError:
            print("Invalid time slot format. Please use 'MM/DD/YY HH:00'.")
            return False
        
    
    @staticmethod
    def is_past_time_slot(time_slot):
        """Check if the time slot is in the past."""
        dt = datetime.strptime(time_slot, '%m/%d/%y %H:%M')
        return dt < datetime.now()


    def remove_past_reservations(self):
        """Remove all reservations that have already passed."""
        now = datetime.now()
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reservations WHERE time_slot < ?", (now.strftime('%m/%d/%y %H:%M'),))
            conn.commit()
            print("Past reservations removed.")