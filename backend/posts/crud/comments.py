import logging

from django.db.models import QuerySet

from core.exceptions import CommentNotFoundError
from core.strings import NOT_FOUND_COMMENT_ERROR
from core.structures import PaginationParams
from posts.models import Comment
from posts.schemas.comments import CommentIn, CommentUpdateIn
from posts.services.posts import PostService
from users.services.users import UserService

logger = logging.getLogger(__name__)


class CommentCRUD:
    def __init__(self, post_id: int) -> None:
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

        comments = (
            Comment.objects.select_related("author", "post")
            .filter(
                post__pk=self._post_id,
            )
            .order_by("-created_at")
        )

        paginated_comments = comments[pagination.start : pagination.end]
        self._log_query(query_set=comments)
        return paginated_comments, len(comments)

    def get_one(self, comment_id: int) -> Comment:
        """Получение комментария по id."""
        comment = Comment.objects.select_related("author", "post").filter(
            pk=comment_id,
            post__pk=self._post_id,
        )
        self._log_query(query_set=comment)
        if not comment.first():
            raise CommentNotFoundError(NOT_FOUND_COMMENT_ERROR.format(id=comment_id, post_id=self._post_id))

        return comment.first()

    def update_one(self, comment_id: int, update_data: CommentUpdateIn) -> Comment:
        """Обновление комментария по id."""
        comment = self.get_one(comment_id=comment_id)
        Comment.objects.filter(pk=comment.pk).update(**update_data.dict())
        return comment

    def delete_one(self, comment_id: int) -> None:
        """Удаление комментария по id."""
        comment = self.get_one(comment_id=comment_id)
        comment.delete()

    def _log_query(self, query_set: QuerySet) -> None:
        """Логирование запроса и Explain'а, который показывает из каких партиций взяты данные."""
        _query = str(query_set.query)
        explain = query_set.explain()
        logger.info(f"QUERY={_query} \n EXPLAIN={explain}")
