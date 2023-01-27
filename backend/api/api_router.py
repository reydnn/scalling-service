from typing import Any, Callable

from ninja import Router
from ninja.types import TCallable


class ApiRouter(Router):
    def api_operation(self, *args: Any, **kwargs: Any) -> Callable[[TCallable], TCallable]:
        kwargs["by_alias"] = True
        return super().api_operation(*args, **kwargs)
