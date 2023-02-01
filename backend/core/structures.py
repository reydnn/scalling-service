from ninja import Field, Schema

DEFAULT_PAGE = 1
DEFAULT_LIMIT = 100


class PaginationParams(Schema):
    page: int = Field(DEFAULT_PAGE, ge=1)
    limit: int = Field(DEFAULT_LIMIT, ge=1)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit

    @property
    def start(self) -> int:
        return self.offset

    @property
    def end(self) -> int:
        return self.offset + self.limit
