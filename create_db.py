from initialize_users import initialize_users

if __name__ == "__main__":
    instruction = """
create_db.py creates a database (meant for testing).
In the db there are five members that have library card numbers that are a number (0 through 4) repeated 14 times. 
They all have the same pin of 0000.
Example: library card number: 33333333333333 and pin: 0000
    """
    initialize_users()
    print(instruction)