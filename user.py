class User():
    """User class will interact with a ComputerReservation class to reverse a computer"""
    def __init__(self, data:dict) -> None:
        """data is a dict with data["library_card_number"] and data["pin"]"""
        self.library_card_number = data["library_card_number"]
        # eventually make pin more secure (maybe by hashing it) or getting it as an input from UI
        self.pin = data["pin"]
        # get other data (like name) by querying the user database
    
    def __str__(self) -> str:
        return f"Library User: {self.library_card_number}"