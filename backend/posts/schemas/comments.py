from datetime import datetime

from ninja import Schema

from users.schemas.users import UserShort


class CommentIn(Schema):
    content: str
    author_id: str


class CommentOut(Schema):
    id: str
    content: str
    post_id: str
    author: UserShort
    created_at: datetime


class CommentUpdateIn(Schema):
    content: str
