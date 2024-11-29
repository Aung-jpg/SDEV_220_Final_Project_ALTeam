from user import User

# initializes users in the database for testing. All with the same password
people = ["0000", "1111", "2222", "3333", "4444"]
for person in people:
    User(person, "0000", 1)