from typing import Callable, NamedTuple, Any
from datetime import timedelta


from rx import operators as ops
from rx.core import Observable, typing
from rx.concurrency import timeout_scheduler

class TimeInterval(NamedTuple):
    value: Any
    interval: timedelta


def _time_interval(scheduler: typing.Scheduler = None) -> Callable[[Observable], Observable]:
    def time_interval(source: Observable) -> Observable:
        """Records the time interval between consecutive values in an
        observable sequence.

            >>> res = time_interval(source)

        Return:
            An observable sequence with time interval information on
            values.
        """

        def subscribe(observer, scheduler_):
            _scheduler = scheduler or scheduler_ or timeout_scheduler
            last = _scheduler.now

            def mapper(value):
                nonlocal last

                now = _scheduler.now
                span = now - last
                last = now
                return TimeInterval(value=value, interval=span)

            return source.pipe(ops.map(mapper)).subscribe(observer, scheduler_)
        return Observable(subscribe)
    return time_interval
