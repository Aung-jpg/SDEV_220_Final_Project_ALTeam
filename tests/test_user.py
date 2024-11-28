import pytest
from user import User
# running "python -m pytest tests" in the terminal works

def test_user_validation():
    user = User("1234", "0000", 1)
    assert user.validation == 0

def test_encryption():
    user = User("1234", "0000")
    assert user.pin == "9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0"
