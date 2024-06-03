from functools import wraps
from multiprocessing.pool import ThreadPool


class Result:
    def __init__(self, success: bool, output: str | None = None) -> None:
        self.success = success
        self.output = output


class Colors:
    def __init__(self) -> None:
        self.standard = "\033[0;0m"
        self.error = "\033[1;31m"
        self.success = "\033[1;32m"
        self.neutral = "\033[1;33m"


def timeout(max_timeout: int):
    """Timeout decorator, parameter in seconds."""

    def timeout_decorator(fn: callable):
        @wraps(fn)
        def func_wrapper(*args, **kwargs):
            """Closes function if execution exceeds max_timeout."""
            pool = ThreadPool(processes=1)
            async_result = pool.apply_async(fn, args, kwargs)
            return async_result.get(max_timeout)

        return func_wrapper

    return timeout_decorator
