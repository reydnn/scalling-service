import pytest

from posts.mappers.comments import CommentToCommentOutMapper
from posts.models import Comment


@pytest.mark.django_db
class TestCommentToCommentOutMapper:
    def test_map_success(self, post, user):
        comment = Comment(
            pk=1,
            content="SomeContent",
            post=post,
            author=user,
        )

        mapped_data = CommentToCommentOutMapper.map(comment=comment, post_id=post.pk)

        assert mapped_data
        assert mapped_data.id == comment.pk
        assert mapped_data.content == comment.content
        assert mapped_data.post_id == post.pk
        assert mapped_data.created_at == comment.created_at
        assert mapped_data.author.id == user.pk
        assert mapped_data.author.first_name == user.first_name
        assert mapped_data.author.last_name == user.last_name
