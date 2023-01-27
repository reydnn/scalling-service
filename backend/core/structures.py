from ninja import Field, Schema

DEFAULT_PAGE = 1
DEFAULT_LIMIT = 100


class PaginationParams(Schema):
    page: int = Field(DEFAULT_PAGE, ge=1)
    limit: int = Field(DEFAULT_LIMIT, ge=1)

    @property
    def offset(self):
        return (self.page - 1) * self.limit
