from user import User

# initializes users in the database for testing. All with the same password
people = ["0", "1", "2", "3", "4"]
for person in people:
    User(person*14, "0000", 1)