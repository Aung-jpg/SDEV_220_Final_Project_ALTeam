class ComputerReservation():
    def __init__(self, library_card_num:str) -> None:
        if library_card_num not in []: # not in database for library card nums
            raise "ERROR: number is not in system"
        self.card_number = library_card_num
        # get other data by querying database

    def check_open_times():
        pass