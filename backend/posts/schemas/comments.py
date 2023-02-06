from datetime import datetime

from ninja import Schema

from users.schemas.users import UserShort


class CommentIn(Schema):
    content: str
    author_id: str


class CommentOut(Schema):
    id: int
    content: str
    post_id: int
    author: UserShort
    created_at: datetime


class CommentUpdateIn(Schema):
    content: str
