import pytest
from user import User
from initialize_users import initialize_users
# running "python -m pytest tests" in the terminal works

initialize_users()

def test_valid_time_slot():
    # tests if time slot is valid (aka is the library open)
    user = User("0"*14, "0000")
    value = user.reservation.is_valid_time_slot("12/14/23 12:00")
    assert value == 1

def test_invalid_time_slot():
    # tests if time slot is valid (aka is the library open)
    user = User("0"*14, "0000")
    value = user.reservation.is_valid_time_slot("11/17/24 18:00")
    assert value == 0

def test_past_time_slot():
    # tests if time slot is in the past
    user = User("0"*14, "0000")
    value = user.reservation.is_past_time_slot("11/29/20 12:00")
    assert value == 1