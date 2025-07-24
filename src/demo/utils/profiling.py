import functools
from collections.abc import Callable
from typing import Any


def profile[F: Callable[..., Any]](func: F) -> F:
    """No-op profiling decorator for production use.

    In development/profiling environments, this would be replaced
    with actual profiling instrumentation.

    Args:
        func: Function to decorate

    Returns:
        Original function unchanged
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return wrapper  # type: ignore[return-value]
