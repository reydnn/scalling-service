from core.structures import PaginationParams
from posts.crud.comments import CommentCRUD
from posts.mappers.comments import CommentToCommentOutMapper
from posts.schemas.comments import CommentIn, CommentOut, CommentUpdateIn


class CommentService:
    def __init__(self, post_id: int) -> None:
        self._post_id = post_id
        self._mapper = CommentToCommentOutMapper
        self._crud = CommentCRUD(post_id=self._post_id)

    def create_one(self, new_comment: CommentIn) -> CommentOut:
        """Создание нового комментария для поста."""
        comment = self._crud.create_one(new_comment=new_comment)
        return self._mapper.map(comment, self._post_id)

    def get_all(self, pagination: PaginationParams) -> tuple[list[CommentOut], int]:
        """Получение всех комментариев для поста."""
        comments, count = self._crud.get_all(pagination=pagination)
        mapped_comments = [self._mapper.map(comment=comment, post_id=self._post_id) for comment in comments]
        return mapped_comments, count

    def get_one(self, comment_id: int) -> CommentOut:
        """Получение комментария по id."""
        comment = self._crud.get_one(comment_id=comment_id)
        return self._mapper.map(comment=comment, post_id=self._post_id)

    def update_one(self, comment_id: int, update_data: CommentUpdateIn) -> CommentOut:
        """Обновление комментария по id."""
        comment = self._crud.update_one(comment_id=comment_id, update_data=update_data)
        mapped_comment = self._mapper.map(comment=comment, post_id=self._post_id)
        return mapped_comment.copy(update=update_data.dict(exclude_unset=True))

    def delete_one(self, comment_id: int) -> None:
        """Удаление комментария по id."""
        return self._crud.delete_one(comment_id=comment_id)
