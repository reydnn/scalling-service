from datetime import datetime

from ninja import Schema

from users.schemas.users import UserShort


class CommentOut(Schema):
    id: str
    content: str
    post_id: str
    author: UserShort
    created_at: datetime
