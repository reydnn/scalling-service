import pytest

from core.exceptions import CommentNotFoundError
from core.strings import NOT_FOUND_COMMENT_ERROR
from core.structures import PaginationParams
from posts.models import Comment
from posts.schemas.comments import CommentIn, CommentUpdateIn
from posts.services.comments import CommentService


@pytest.mark.django_db
class TestCommentService:
    def test_create_one(self, post, user):
        new_comment_in = CommentIn(
            content="Test",
            author_id=user.pk,
        )
        new_comment = CommentService(post_id=post.pk).create_one(new_comment_in)

        assert new_comment

        new_comment_from_db = Comment.objects.get(pk=new_comment.id)

        assert new_comment_from_db.pk == new_comment.id
        assert new_comment_from_db.content == new_comment.content == new_comment_in.content
        assert new_comment_from_db.post.pk == new_comment.post_id == post.pk
        assert new_comment_from_db.author.pk == new_comment.author.id == post.user.pk
        assert new_comment_from_db.created_at

    def test_read_one(self, user, post, comment):
        test_comment = comment
        _comment = CommentService(post_id=post.pk).get_one(comment_id=test_comment.pk)

        assert _comment
        assert _comment.id == test_comment.pk
        assert _comment.content == test_comment.content
        assert _comment.post_id == test_comment.post.pk
        assert _comment.author.id == test_comment.author.pk
        assert _comment.created_at

    def test_read_one_not_found(self, post):
        _id = 123
        with pytest.raises(CommentNotFoundError) as e:
            CommentService(post_id=post.pk).get_one(comment_id=_id)
            assert str(e) == NOT_FOUND_COMMENT_ERROR.format(id=_id, post_id=post.pk)

    def test_read_many(self, post, user):
        test_count = 5
        test_comments = []
        for i in range(test_count):
            comment = Comment.objects.create(
                content=f"SomeContent{i}",
                post=post,
                author=user,
            )
            test_comments.append(comment)

        comments, count = CommentService(post_id=post.pk).get_all(pagination=PaginationParams())

        assert count == test_count

    def test_update_one(self, post, user, comment):
        test_comment = comment
        update_data = CommentUpdateIn(content="TestContent")

        CommentService(post_id=post.pk).update_one(
            comment_id=test_comment.pk,
            update_data=update_data,
        )
        updated_comment = Comment.objects.get(pk=test_comment.pk)

        assert updated_comment.content == update_data.content

    def test_delete_one(self, post, user, comment):
        test_comment = comment

        assert Comment.objects.get(pk=test_comment.pk)
        CommentService(post_id=post.pk).delete_one(comment_id=test_comment.pk)

        with pytest.raises(Comment.DoesNotExist):
            Comment.objects.get(pk=test_comment.pk)
