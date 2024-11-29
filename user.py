from reservation import ComputerReservation
import sqlite3
import hashlib

class User:
    """
    Represents a user interacting with a ComputerReservation class to reserve a computer.
    Utilizes the user's Library Card Number (LCN) and PIN for authentication.
    """

    def __init__(self, library_card_number: str, pin: str, testing: int = 0) -> None:
        """
        Initializes a User object and validates the user's credentials.

        Args:
            library_card_number (str): The user's library card number.
            pin (str): The user's PIN, used for authentication.
            testing (int, optional): Determines whether the user is in testing mode (default: 0). 
                - 0: Normal mode (raises an error if user does not exist).
                - 1: Testing mode (adds the user to the database if not found).

        Raises:
            TypeError: If the library card number does not exist (in non-testing mode).
            ValueError: If the library card number exists but the PIN is incorrect.
        """
        self.library_card_number = library_card_number
        self.pin = self.encrypt_pin(pin)  # Encrypt the PIN for security.

        # edge case where no tables exist yet
        if testing == 1:
            self.register_user_testing()

        self.validation = self.validate_user()
        if self.validation == 0:
            # Library card number exists, and the PIN is correct.
            self.reservation = ComputerReservation(self.library_card_number, self.pin)
            print("ComputerReservation class enabled")
        elif self.validation == -1 and testing == 0:
            # Library card number doesn't exist (non-testing mode).
            raise TypeError("Library Card Number doesn't exist")
        elif self.validation == 1:
            # Library card number exists, but the PIN is incorrect.
            raise ValueError("Incorrect Pin")
    

    def list_reservations(self):
        """
        Lists all reservations for the current user.

        Returns:
            list or str: A list of reservation time slots if any exist, 
                         or [] if none are found.
        """
        with self.reservation.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT time_slot FROM reservations WHERE library_card_number = ?", (self.library_card_number,))
            reservations = cursor.fetchall()
            return reservations if reservations else []
            

    def encrypt_pin(self, pin: str) -> str:
        """
        Encrypts the user's PIN for secure storage.

        Args:
            pin (str): The plaintext PIN to be encrypted.

        Returns:
            str: The encrypted (hashed) PIN.
        """
        sha256_hash = hashlib.sha256()
        sha256_hash.update(pin.encode('utf-8'))
        return sha256_hash.hexdigest()
            

    def register_user_testing(self):
        """
        Adds the user to the database (for testing purposes only).
        Uses the `add_self` method from the ComputerReservation class.

        Raises:
            sqlite3.IntegrityError: If the user already exists in the database.
        """
        res = ComputerReservation(self.library_card_number, self.pin)
        exists = res.user_exists()
        if not exists:
            res.add_self()
        else:
            raise sqlite3.IntegrityError(f"{self.library_card_number} is already in the all_members table: UNIQUE constraint failed")
    

    def validate_user(self) -> int:
        """
        Validates if the library card number (LCN) and PIN match the database records.

        Returns:
            int: 
                - -1 if the library card number does not exist.
                - 0 if the library card number exists and the PIN is correct.
                - 1 if the library card number exists but the PIN is incorrect.
        """
        conn = sqlite3.connect('LibraryMembers.db')
        cursor = conn.cursor()
        cursor.execute("SELECT library_card_number, pin FROM all_members WHERE library_card_number = ?", (self.library_card_number,))
        row = cursor.fetchone()
        if row is None:
            # Library card number doesn't exist.
            return -1
        if self.pin == row[1]:
            # Library card number and PIN match.
            return 0
        else:
            # Library card number exists, but PIN is incorrect.
            return 1
