from ninja import Schema


class UserShort(Schema):
    id: int
    first_name: str
    last_name: str
