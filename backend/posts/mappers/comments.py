from posts.models import Comment
from posts.schemas.comments import CommentOut
from users.schemas.users import UserShort


class CommentToCommentOutMapper:
    @staticmethod
    def map(comment: Comment, post_id: int) -> CommentOut:
        return CommentOut(
            id=comment.pk,
            content=comment.content,
            post_id=post_id,
            author=UserShort(
                id=comment.author.pk,
                first_name=comment.author.first_name,
                last_name=comment.author.last_name,
            ),
            created_at=comment.created_at,
        )
