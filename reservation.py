import sqlite3
from datetime import datetime


class ComputerReservation:
    def __init__(self, library_card_number):
        self.create_tables()
        self.library_card_number = library_card_number
        exists = self.user_exists()
        if not exists:
            self.add_self()
        
        
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
            cursor.execute('INSERT INTO all_members (library_card_number) VALUES (?)', (self.library_card_number,))
            conn.commit()


    def create_tables(self):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS all_members(
                    library_card_number TEXT PRIMARY KEY
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reservations(
                    time_slot TEXT PRIMARY KEY,
                    library_card_number TEXT,
                    FOREIGN KEY(library_card_number) REFERENCES all_members(library_card_number)
                )
            ''')
            conn.commit()


    def reserve_computer(self, time_slot: str):
        if not self.is_valid_time_slot(time_slot):
            return
        
        if self.is_past_time_slot(time_slot):
            print("Cannot reserve a time slot in the past.")
            return

        with self.get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT EXISTS(SELECT 1 FROM reservations WHERE time_slot = ?)", (time_slot,))
                if cursor.fetchone()[0]:
                    print("Time slot is already reserved.")
                    return

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
                    print("No reservation found for this time slot.")
            except sqlite3.Error as e:
                print(f"Failed to cancel reservation: {e}")


    def list_reservations(self):
        """List all reservations for the user."""
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT time_slot FROM reservations WHERE library_card_number = ?", (self.library_card_number,))
            reservations = cursor.fetchall()
            if reservations:
                print("Your reservations:")
                for reservation in reservations:
                    print(reservation[0])
            else:
                print("No reservations found.")


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

