from reservation import ComputerReservation
class User():
    """User class will interact with a ComputerReservation class to reverse a computer"""
    def __init__(self, library_card_number:str) -> None:
        self.library_card_number = library_card_number
        self.reservation = ComputerReservation(self.library_card_number)
    
    def __str__(self) -> str:
        return f"Library User: {self.library_card_number}"
    
Jim = User("1234")
Jim.reservation.reserve_computer("11/2/24 9:00")