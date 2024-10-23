class User():
    """User calss will interact with a Computer_reservation class to reverse a computer"""
    def __init__(self, library_card_number, pin) -> None:
        self.library_card_number = library_card_number
        # eventually make pin more secure (maybe by hashing it)
        self.pin = pin
        # get other data (like name) by querying the user database
    
    def __str__(self) -> str:
        return f"Library User: {self.library_card_number}"