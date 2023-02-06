from core.exceptions import PostNotFoundError
from core.strings import NOT_FOUND_POST_ERROR
from posts.models import Post


class PostService:
    def get_one(self, post_id: int) -> Post:
        # TODO: Вынести в Crud и здесь отдавать данные с mapper'а
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise PostNotFoundError(NOT_FOUND_POST_ERROR.format(id=post_id))
        return post
