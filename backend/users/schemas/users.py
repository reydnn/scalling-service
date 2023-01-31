from ninja import Schema


class UserShort(Schema):
    id: str
    first_name: str
    last_name: str
