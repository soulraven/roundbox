#  -*- coding: utf-8 -*-

# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.
# https://github.com/home-assistant/core/blob/dev/LICENSE.md

import asyncio
import threading
from collections.abc import Callable, Coroutine
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, TypeVar

from .dt import utcnow


class Throttle:
    """A class for throttling the execution of tasks.
    This method decorator adds a cooldown to a method to prevent it from being
    called more than 1 time within the timedelta interval `min_time` after it
    returned its result.
    Calling a method a second time during the interval will return None.
    Pass keyword argument `no_throttle=True` to the wrapped method to make
    the call not throttled.
    Decorator takes in an optional second timedelta interval to throttle the
    'no_throttle' calls.
    Adds a datetime attribute `last_call` to the method.
    """

    def __init__(
        self, min_time: timedelta, limit_no_throttle: timedelta | None = None
    ) -> None:
        """Initialize the throttle.

        :param min_time:
        :param limit_no_throttle:
        """
        self.min_time = min_time
        self.limit_no_throttle = limit_no_throttle

    def __call__(self, method: Callable) -> Callable:
        """Caller for the throttle.

        :param method:
        :return:
        """
        # Make sure we return a coroutine if the method is async.
        if asyncio.iscoroutinefunction(method):

            async def throttled_value() -> None:
                """Stand-in function for when real func is being throttled."""
                return None

        else:

            def throttled_value() -> None:  # type: ignore[misc]
                """Stand-in function for when real func is being throttled."""
                return None

        if self.limit_no_throttle is not None:
            method = Throttle(self.limit_no_throttle)(method)

        # Different methods that can be passed in:
        #  - a function
        #  - an unbound function on a class
        #  - a method (bound function on a class)

        # We want to be able to differentiate between function and unbound
        # methods (which are considered functions).
        # All methods have the classname in their qualname separated by a '.'
        # Functions have a '.' in their qualname if defined inline, but will
        # be prefixed by '.<locals>.' so we strip that out.
        is_func = (
            not hasattr(method, "__self__")
            and "." not in method.__qualname__.split(".<locals>.")[-1]
        )

        @wraps(method)
        def wrapper(*args: Any, **kwargs: Any) -> Callable | Coroutine:
            """Wrap that allows wrapped to be called only once per min_time.
            If we cannot acquire the lock, it is running so return None.

            :param args:
            :param kwargs:
            :return:
            """
            if hasattr(method, "__self__"):
                host = getattr(method, "__self__")
            elif is_func:
                host = wrapper
            else:
                host = args[0] if args else wrapper

            # pylint: disable=protected-access # to _throttle
            if not hasattr(host, "_throttle"):
                host._throttle = {}

            if id(self) not in host._throttle:
                host._throttle[id(self)] = [threading.Lock(), None]
            throttle = host._throttle[id(self)]
            # pylint: enable=protected-access

            if not throttle[0].acquire(False):
                return throttled_value()

            # Check if method is never called or no_throttle is given
            force = kwargs.pop("no_throttle", False) or not throttle[1]

            try:
                if force or utcnow() - throttle[1] > self.min_time:
                    result = method(*args, **kwargs)
                    throttle[1] = utcnow()
                    return result  # type: ignore[no-any-return]

                return throttled_value()
            finally:
                throttle[0].release()

        return wrapper
