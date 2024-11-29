from user import User
import sqlite3

# initializes users in the database for testing. All with the same password
def initialize_users():
    people = ["0", "1", "2", "3", "4"]
    for person in people:
        try:
            User(person*14, "0000", 1)
        except sqlite3.IntegrityError:
            pass