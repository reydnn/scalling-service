from http import HTTPStatus

from django.http import HttpRequest
from ninja import Path, Query
from ninja.errors import HttpError

from api.api_router import ApiRouter
from api.responses import ApiResponse, ListPaginatedResponse, PaginationOut
from core.exceptions import CommentNotFoundError, PostNotFoundError
from core.structures import DEFAULT_LIMIT, DEFAULT_PAGE, PaginationParams
from posts.schemas.comments import CommentIn, CommentOut, CommentUpdateIn
from posts.services.comments import CommentService

router = ApiRouter()


@router.post(
    "{post_id}/comments",
    response=ApiResponse[CommentOut],
)
def create_comment(
    request: HttpRequest,
    new_comment: CommentIn,
    post_id: str = Path(...),
) -> ApiResponse[CommentOut]:
    try:
        comment = CommentService(post_id=post_id).create_one(new_comment=new_comment)
    except PostNotFoundError as e:
        raise HttpError(
            status_code=HTTPStatus.NOT_FOUND,
            message=str(e),
        )

    return ApiResponse(data=comment)


@router.get(
    "{post_id}/comments",
    response=ApiResponse[ListPaginatedResponse[CommentOut]],
)
def get_comments(
    request: HttpRequest,
    post_id: str = Path(...),
    page: int = Query(default=DEFAULT_PAGE, ge=1),
    limit: int = Query(default=DEFAULT_LIMIT, ge=1),
) -> ApiResponse[ListPaginatedResponse[CommentOut]]:
    pagination_params = PaginationParams(
        page=page,
        limit=limit,
    )
    try:
        comments, count = CommentService(post_id=post_id).get_all(pagination=pagination_params)
    except PostNotFoundError as e:
        raise HttpError(
            status_code=HTTPStatus.NOT_FOUND,
            message=str(e),
        )

    return ApiResponse(
        data=ListPaginatedResponse(
            items=comments,
            pagination=PaginationOut(**pagination_params.dict(), total=count),
        ),
    )


@router.get(
    "{post_id}/comments/{id}",
    response=ApiResponse[CommentOut],
)
def get_comment_by_id(
    request: HttpRequest,
    post_id: str = Path(...),
    comment_id: str = Path(..., alias="id"),
) -> ApiResponse[CommentOut]:
    try:
        comment = CommentService(post_id=post_id).get_one(comment_id=comment_id)
    except (PostNotFoundError, CommentNotFoundError) as e:
        raise HttpError(
            status_code=HTTPStatus.NOT_FOUND,
            message=str(e),
        )

    return ApiResponse(data=comment)


@router.patch(
    "{post_id}/comments/{id}",
    response=ApiResponse[CommentOut],
)
def update_comment_by_id(
    request: HttpRequest,
    update_data: CommentUpdateIn,
    post_id: str = Path(...),
    comment_id: str = Path(..., alias="id"),
) -> ApiResponse[CommentOut]:
    try:
        comment = CommentService(post_id=post_id).update_one(comment_id=comment_id, update_data=update_data)
    except (PostNotFoundError, CommentNotFoundError) as e:
        raise HttpError(
            status_code=HTTPStatus.NOT_FOUND,
            message=str(e),
        )

    return ApiResponse(data=comment)


@router.delete(
    "{post_id}/comments/{id}",
    response=HTTPStatus.NO_CONTENT,
)
def delete_comment_by_id(
    request: HttpRequest,
    post_id: str = Path(...),
    comment_id: str = Path(..., alias="id"),
) -> HTTPStatus:
    try:
        CommentService(post_id=post_id).delete_one(comment_id=comment_id)
    except (PostNotFoundError, CommentNotFoundError) as e:
        raise HttpError(
            status_code=HTTPStatus.NOT_FOUND,
            message=str(e),
        )

    return HTTPStatus.NO_CONTENT
