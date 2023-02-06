import pytest

from core.structures import PaginationParams
from posts.crud.comments import CommentCRUD
from posts.models import Comment
from posts.schemas.comments import CommentIn, CommentUpdateIn


@pytest.mark.django_db
class TestCommentsCRUD:
    def test_create_one(self, post, user):
        new_comment_in = CommentIn(
            content="Test",
            author_id=user.pk,
        )
        new_comment = CommentCRUD(post_id=post.pk).create_one(new_comment_in)

        assert new_comment

        new_comment_from_db = Comment.objects.get(pk=new_comment.pk)
        assert new_comment_from_db.pk == new_comment.pk
        assert new_comment_from_db.content == new_comment.content == new_comment_in.content
        assert new_comment_from_db.post.pk == post.pk
        assert new_comment_from_db.author.pk == post.user.pk
        assert new_comment_from_db.created_at

    def test_read_one(self, user, post, comment):
        test_comment = comment
        _comment = CommentCRUD(post_id=post.pk).get_one(comment_id=test_comment.pk)

        assert _comment
        assert _comment.pk == test_comment.pk
        assert _comment.content == test_comment.content
        assert _comment.post.pk == test_comment.post.pk
        assert _comment.author.pk == test_comment.author.pk
        assert _comment.created_at

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

        comments, count = CommentCRUD(post_id=post.pk).get_all(pagination=PaginationParams())

        assert count == test_count

        for comment in comments:
            assert comment in test_comments

    def test_update_one(self, post, user, comment):
        test_comment = comment
        update_data = CommentUpdateIn(content="TestContent")

        CommentCRUD(post_id=post.pk).update_one(
            comment_id=test_comment.pk,
            update_data=update_data,
        )
        updated_comment = Comment.objects.get(pk=test_comment.pk)

        assert updated_comment.content == update_data.content

    def test_delete_one(self, post, user, comment):
        test_comment = comment

        assert Comment.objects.get(pk=test_comment.pk)
        CommentCRUD(post_id=post.pk).delete_one(comment_id=test_comment.pk)

        with pytest.raises(Comment.DoesNotExist):
            Comment.objects.get(pk=test_comment.pk)
