from core.exceptions import CommentNotFoundError
from core.strings import NOT_FOUND_COMMENT_ERROR
from core.structures import PaginationParams
from posts.models import Comment
from posts.schemas.comments import CommentIn, CommentUpdateIn
from posts.services.posts import PostService
from users.services.users import UserService


class CommentCRUD:
    def __init__(self, post_id: str) -> None:
        self._post_id = post_id

    def create_one(self, new_comment: CommentIn) -> Comment:
        """Создание нового комментария для поста."""
        user = UserService().get_one(user_id=new_comment.author_id)
        post = PostService().get_one(post_id=self._post_id)

        comment = Comment(
            content=new_comment.content,
            post=post,
            author=user,
        )
        comment.full_clean()
        comment.save()
        return comment

    def get_all(self, pagination: PaginationParams) -> tuple[list[Comment], int]:
        """Получение всех комментариев для поста."""

        comments = Comment.objects.select_related("author").filter(post__pk=self._post_id).order_by("-created_at")
        paginated_comments = comments[pagination.start : pagination.end]
        return paginated_comments, len(comments)

    def get_one(self, comment_id: str) -> Comment:
        """Получение комментария по id."""
        comment = (
            Comment.objects.select_related("author")
            .filter(
                pk=comment_id,
                post__pk=self._post_id,
            )
            .first()
        )
        if not comment:
            raise CommentNotFoundError(NOT_FOUND_COMMENT_ERROR.format(id=comment_id, post_id=self._post_id))
        return comment

    def update_one(self, comment_id: str, update_data: CommentUpdateIn) -> Comment:
        """Обновление комментария по id."""
        comment = self.get_one(comment_id=comment_id)
        Comment.objects.filter(pk=comment.pk).update(**update_data.dict())
        return comment

    def delete_one(self, comment_id: str) -> None:
        """Удаление комментария по id."""
        comment = self.get_one(comment_id=comment_id)
        comment.delete()
