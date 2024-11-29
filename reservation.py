import sqlite3
from datetime import datetime


class ComputerReservation:
    """
    Manages computer reservations for library users. Handles user registration, 
    database setup, and time slot reservations.
    """

    def __init__(self, library_card_number: str, pin: str):
        """
        Initializes a ComputerReservation instance.

        Args:
            library_card_number (str): The library card number of the user.
            pin (str): The user's encrypted PIN.
        """
        self.create_tables()
        self.library_card_number = library_card_number
        self.pin = pin

    @staticmethod
    def get_db():
        """
        Creates a connection to the database.

        Returns:
            sqlite3.Connection: A connection object for the SQLite database.
        """
        conn = sqlite3.connect('LibraryMembers.db')
        return conn

    def user_exists(self) -> int:
        """
        Checks if the user exists in the database using their library card number.

        Returns:
            int: 1 if the user exists, 0 otherwise.
        """
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM all_members WHERE library_card_number = ?)", (self.library_card_number,))
        exists = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return exists

    def add_self(self):
        """
        Adds the current user to the database. Primarily for testing purposes.

        Raises:
            sqlite3.IntegrityError: If the library card number already exists in the database.
        """
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO all_members (library_card_number, pin) VALUES (?, ?)', (self.library_card_number, self.pin))
            conn.commit()

    def create_tables(self):
        """
        Sets up the database tables if they do not already exist:
        - `all_members`: Stores library card numbers and encrypted PINs.
        - `reservations`: Stores time slot reservations and associated library card numbers.
        """
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
        """
        Reserves a computer for the user at the specified time slot.

        Args:
            time_slot (str): The desired time slot in 'MM/DD/YY HH:00' format.

        Raises:
            TypeError: If the time slot format is invalid.
            ValueError: If the time slot is in the past.
            IndexError: If the time slot is already reserved.
        """
        if not self.is_valid_time_slot(time_slot):
            raise TypeError("Library is not open that day and time.")

        if self.is_past_time_slot(time_slot):
            raise ValueError("Cannot reserve a time slot in the past.")

        with self.get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT EXISTS(SELECT 1 FROM reservations WHERE time_slot = ?)", (time_slot,))
                if cursor.fetchone()[0]:
                    raise IndexError("Time slot is already reserved.")

                cursor.execute("INSERT INTO reservations (time_slot, library_card_number) VALUES (?, ?)", (time_slot, self.library_card_number))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Failed to reserve computer: {e}")

    def cancel_reservation(self, time_slot: str):
        """
        Cancels a reservation for the specified time slot.

        Args:
            time_slot (str): The time slot to cancel in 'MM/DD/YY HH:00' format.

        Raises:
            ValueError: If no reservation exists for the given time slot.
        """
        with self.get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM reservations WHERE time_slot = ? AND library_card_number = ?",
                               (time_slot, self.library_card_number))
                conn.commit()
                if cursor.rowcount > 0:
                    return
                else:
                    raise ValueError("No reservation found for this time slot.")
            except sqlite3.Error as e:
                print(f"Failed to cancel reservation: {e}")

    @staticmethod
    def is_valid_time_slot(time_slot: str) -> bool:
        """
        Validates if the time slot is within the library's working hours.

        Args:
            time_slot (str): The desired time slot in 'MM/DD/YY HH:00' format.

        Returns:
            bool: True if the time slot is valid, False otherwise.
        """
        try:
            dt = datetime.strptime(time_slot, '%m/%d/%y %H:%M')
            # Ensure the time is on the hour
            if dt.minute != 0:
                return False
            weekday = dt.weekday()
            if weekday == 6:  # Sunday
                print("Invalid time slot: closed on Sunday")
                return False
            if weekday in [4, 5]:  # Friday and Saturday
                if dt.hour < 10 or dt.hour > 17:  # Open 10 AM - 6 PM
                    print("Invalid time slot: open between 10 AM-6 PM")
                    return False
            if weekday in [0, 1, 2, 3]:  # Monday - Thursday
                if dt.hour < 10 or dt.hour > 20:  # Open 10 AM - 9 PM
                    print("Invalid time slot: open between 10 AM-9 PM")
                    return False
            return True
        except ValueError:
            print("Invalid time slot format. Please use 'MM/DD/YY HH:00'.")
            return False

    @staticmethod
    def is_past_time_slot(time_slot: str) -> bool:
        """
        Checks if the time slot is in the past.

        Args:
            time_slot (str): The time slot in 'MM/DD/YY HH:00' format.

        Returns:
            bool: True if the time slot is in the past, False otherwise.
        """
        dt = datetime.strptime(time_slot, '%m/%d/%y %H:%M')
        return dt < datetime.now()

    def remove_past_reservations(self):
        """
        Removes all reservations that have already passed.
        """
        now = datetime.now()
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT time_slot FROM reservations")
            reservations = cursor.fetchall()
            for reservation in reservations:
                reservation = datetime.strptime(reservation[0], '%m/%d/%y %H:%M')
                if reservation < now:
                    cursor.execute("DELETE FROM reservations WHERE time_slot = ?", (reservation,))
            conn.commit()
