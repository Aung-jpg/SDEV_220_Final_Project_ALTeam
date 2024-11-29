import pytest
from user import User
from initialize_users import initialize_users
# running "python -m pytest tests" in the terminal works

initialize_users()

@pytest.mark.run(order=1)
def test_user_not_in_database():
    with pytest.raises(TypeError):
        # this user isn't in the database and should raise a type error
        person = User("01234550098374", "0000")

@pytest.mark.run(order=2)
def test_reserve_computer():
    person = User("0"*14, "0000")
    # WILL NOT WORK ONCE THIS DATE IS PASSED
    reservation_date = "12/14/24 15:00"
    person.reservation.reserve_computer(reservation_date)
    assert person.list_reservations()[0][0] == "12/14/24 15:00"

@pytest.mark.run(order=3)
def test_cancel_reservation():
    person = User("0"*14, "0000")
    # IF THE PREVIOUS TEST FAILED THEN THIS ONE WON'T WORK
    reservation_date = "12/14/24 15:00"
    person.reservation.cancel_reservation(reservation_date)
    assert person.list_reservations() == []