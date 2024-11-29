import pytest
from user import User
from initialize_users import initialize_users
# running "python -m pytest tests" in the terminal works

initialize_users()

def test_user_validation():
    # tests if user is in the database
    user = User("0"*14, "0000")
    assert user.validation == 0

def test_encryption():
    # tests if user's pin is encrypted correctly
    user = User("0"*14, "0000")
    assert user.pin == "9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0"
