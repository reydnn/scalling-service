from datetime import datetime

import pytest

from posts.models import Comment, Post
from users.models import Gender, User


@pytest.fixture
def user():
    return User.objects.create(
        first_name="Test",
        last_name="Testov",
        city="Moscow",
        gender=Gender.MALE,
        birthday=datetime.today(),
        mobile_phone="79991234567",
    )


@pytest.fixture
def post(user):
    return Post.objects.create(
        title="test_title",
        content="some_content",
        user=user,
    )


@pytest.fixture
def comment(post, user):
    return Comment.objects.create(
        content="SomeContent",
        post=post,
        author=user,
    )
