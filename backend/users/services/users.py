from core.exceptions import UserNotFoundError
from core.strings import NOT_FOUND_USER_ERROR
from users.models import User


class UserService:
    def get_one(self, user_id: int) -> User:
        # TODO: Вынести в crud и отсюда отдавать данные с mapper'а
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise UserNotFoundError(NOT_FOUND_USER_ERROR.format(id=user_id))
        return user
