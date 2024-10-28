from user import User
class ComputerReservation:
    def __init__(self, library_card_number):
        self.reservations = {}
        self.user = library_card_number

    def reserve_computer(self, user: User, time_slot: str):
        """Reserve a computer for the user at a given time slot."""
        if time_slot in self.reservations:
            print("Time slot is already reserved.")
        else:
            self.reservations[time_slot] = user
            print(f"Computer reserved for {user.name} at {time_slot}.")

members = ("1234", "2345", "0000")