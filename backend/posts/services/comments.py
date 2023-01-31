from core.exceptions import CommentNotFoundError, PostNotFoundError, UserNotFoundError
from core.strings import NOT_FOUND_COMMENT_ERROR, NOT_FOUND_POST_ERROR, NOT_FOUND_USER_ERROR
from core.structures import PaginationParams
from posts.models import Comment, Post
from posts.schemas.comments import CommentIn, CommentOut, CommentUpdateIn
from users.models import User
from users.schemas.users import UserShort


class CommentService:
    def __init__(self, post_id: str) -> None:
        self._post_id = post_id

    def create_one(self, new_comment: CommentIn) -> CommentOut:
        """Создание нового комментария для поста."""
        user = self._get_user(new_comment.author_id)

        try:
            comment = Comment(
                content=new_comment.content,
                post=self._post_id,
                author=user.pk,
            )
            comment.full_clean()
            comment.save()
        except Post.DoesNotExist:
            raise PostNotFoundError(NOT_FOUND_POST_ERROR.format(id=self._post_id))

        return CommentOut(
            id=comment.pk,
            content=comment.content,
            post_id=self._post_id,
            author=UserShort(
                id=user.pk,
                first_name=user.first_name,
                last_name=user.last_name,
            ),
            created_at=comment.created_at,
        )

    def get_all(self, pagination: PaginationParams) -> tuple[list[CommentOut], int]:
        """Получение всех комментариев для поста."""

        comments = Comment.objects.all()
        paginated_comments = comments[pagination.offset : pagination.limit]

        mapped_comments = [
            CommentOut(
                id=comment.pk,
                content=comment.content,
                post_id=comment.post.pk,
                author=UserShort(
                    id=comment.author.pk,
                    first_name=comment.author.first_name,
                    last_name=comment.author.last_name,
                ),
                created_at=comment.created_at,
            )
            for comment in paginated_comments
        ]
        return mapped_comments, len(comments)

    def get_one(self, comment_id: str) -> CommentOut:
        """Получение комментария по id."""
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise CommentNotFoundError(NOT_FOUND_COMMENT_ERROR.format(id=comment_id))
        return CommentOut(
            id=comment.pk,
            content=comment.content,
            post_id=comment.post.pk,
            author=UserShort(
                id=comment.author.pk,
                first_name=comment.author.first_name,
                last_name=comment.author.last_name,
            ),
            created_at=comment.created_at,
        )

    def update_one(self, comment_id: str, update_data: CommentUpdateIn) -> CommentOut:
        """Обновление комментария по id."""
        pass

    def delete_one(self, comment_id: str) -> None:
        """Удаление комментария по id."""
        pass

    def _get_user(self, pk: str) -> User:
        # TODO: Вынести в сервис пользователя
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise UserNotFoundError(NOT_FOUND_USER_ERROR.format(id=pk))
        return user
