import pytest

from core.exceptions import UserNotFoundError
from core.strings import NOT_FOUND_USER_ERROR
from users.services.users import UserService


@pytest.mark.django_db
class TestUserService:
    def test_get_one(self, user):
        _user = UserService().get_one(user_id=user.pk)

        assert _user
        assert _user.pk == user.pk
        assert _user.first_name == user.first_name
        assert _user.last_name == user.last_name
        assert _user.birthday == user.birthday.date()
        assert _user.city == user.city
        assert _user.gender == user.gender
        assert _user.email == user.email

    def test_get_one_not_found(self):
        _id = 123

        with pytest.raises(UserNotFoundError) as e:
            UserService().get_one(user_id=_id)
            assert str(e) == NOT_FOUND_USER_ERROR.format(id=_id)
