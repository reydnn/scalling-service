import pytest

from core.exceptions import PostNotFoundError
from core.strings import NOT_FOUND_POST_ERROR
from posts.services.posts import PostService


@pytest.mark.django_db
class TestPostService:
    def test_get_one(self, post):
        _post = PostService().get_one(post_id=post.pk)

        assert _post
        assert _post.pk == post.pk
        assert _post.content == post.content
        assert _post.user == post.user
        assert _post.likes == post.likes

    def test_get_one_not_found(self):
        with pytest.raises(PostNotFoundError) as e:
            _id = 123
            PostService().get_one(post_id=_id)
            assert str(e) == NOT_FOUND_POST_ERROR.format(id=_id)
