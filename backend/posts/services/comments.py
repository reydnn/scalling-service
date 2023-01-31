from core.structures import PaginationParams
from posts.schemas.comments import CommentIn, CommentOut, CommentUpdateIn


class CommentService:
    def __init__(self, post_id: str) -> None:
        self._post_id = post_id

    def create_one(self, new_comment: CommentIn) -> CommentOut:
        """Создание нового комментария для поста."""
        pass

    def get_all(self, pagination: PaginationParams) -> list[CommentOut]:
        """Получение всех комментариев для поста."""
        pass

    def get_one(self, comment_id: str) -> CommentOut:
        """Получение комментария по id."""
        pass

    def update_one(self, comment_id: str, update_data: CommentUpdateIn) -> CommentOut:
        """Обновление комментария по id."""
        pass

    def delete_one(self, comment_id: str) -> None:
        """Удаление комментария по id."""
        pass
