from datetime import datetime

import pytest

from users.models import Gender, User


@pytest.fixture
def user():
    return User.objects.create(
        first_name="Test",
        last_name="Testov",
        city="Moscow",
        gender=Gender.MALE,
        birthday=datetime.today(),
        mobile_phone="79991234567",
    )
