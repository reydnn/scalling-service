from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from ninja.errors import ValidationError

api = NinjaAPI()


@api.exception_handler(ValidationError)
def validation_errors(request: HttpRequest, exc: ValidationError) -> HttpResponse:
    errors = {}
    for err in exc.errors:
        msg = err["msg"]
        ctx = err.get("ctx")
        if ctx:
            msg = msg.format(**ctx)
        errors[err["loc"][-1]] = msg

    return api.create_response(request, {"field_errors": errors}, status=422)
