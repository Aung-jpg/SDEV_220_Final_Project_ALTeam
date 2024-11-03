from reservation import ComputerReservation
class User():
    """User class will interact with a ComputerReservation class to reverse a computer"""
    def __init__(self, library_card_number:str) -> None:
        self.library_card_number = library_card_number
        self.reservation = ComputerReservation(self.library_card_number)
    
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

person = User("1234")
print(person.list_reservations())