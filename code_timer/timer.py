# timer.py

import time
import logging
import functools

# Setup logging
logger = logging.getLogger("code_timer")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter(
    fmt="%(asctime)s: %(name)s.%(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.propagate = False


class TimerError(Exception):
    """Custom exception for Timer class."""


def timer(f=None, *, name: str = None):
    """
    Apply Timer as decorator.  Benefit of this is you can use @timer or
    @timer()

    :param f: function being wrapped
    :param name: custom timer name passed to Timer class
    """
    # support both @timer and @timer() as valid syntax
    if f is None:
        return functools.partial(timer, name=name)

    @functools.wraps(f)
    def wrapped_f(*args, **kwargs):
        with Timer(name=name):
            return f(*args, **kwargs)

    return wrapped_f


def timeit(f=None, *, num_repeats: int = 10000, name: str = None):
    """
    Repeat a function a number of times and outputs a log line indicating
    the three lowest

    :param f: function being wrapped
    :param name: custom timer name passed to Timer class
    :param num_repeats: Number of times to repeat the function being timed
    """
    # support both @timeit and @timeit() as valid syntax
    if f is None:
        return functools.partial(timeit, num_repeats=num_repeats, name=name)

    @functools.wraps(f)
    def wrapped_f(*args, **kwargs):
        repeats = [0] * num_repeats
        for i in range(num_repeats):
            with Timer(name=name) as t:
                temp = f(*args, **kwargs)
            repeats[i] = t.elapsed_time
        repeats.sort()
        logger.info(
            f"Best 3 of {num_repeats} "
            f"for {f.__name__}: "
            f"{repeats[0]:0.4f} ms; "
            f"{repeats[1]:0.4f} ms; "
            f"{repeats[2]:0.4f} ms; "
        )
        return temp

    return wrapped_f


def recursive_timer(f):
    """Timer specifically for recursive calls"""
    is_evaluating = False
    timer = Timer()

    # support passing keyword to @recursive_timer(stdout=False) or @recursive_timer()
    if f is None:
        return functools.partial(recursive_timer)

    @functools.wraps(f)
    def wrapped_func(*args, **kwargs):
        nonlocal is_evaluating, timer

        if is_evaluating:
            return f(*args, **kwargs)

        timer.start()
        is_evaluating = True
        try:
            value = f(*args, **kwargs)
        finally:
            timer.update_name(f"{f.__name__}{args, kwargs}")
            is_evaluating = False
        timer.stop()
        logger.debug(timer)
        logger.info(
            f"Elapsed time '{f.__name__}{args, kwargs}': "
            f"{timer.elapsed_time:0.6f} ms"
        )
        return value

    return wrapped_func


class Timer:
    timers = dict()
    DEFAULT_TIMER = "default"

    def __init__(self, name: str = None):
        """
        :param name: can pass in a specific name of a timer.  This is
            helpful if you want to time multiple events, and accumulate the
            result with one total time.  The timer name is the dictionary
            key and the accumulated time is the dictionary value.
        """
        self.__name = name or self.DEFAULT_TIMER
        self.__start_time = None
        self.__elapsed_time = None

        # Add new name to dictionary of timers
        self.timers.setdefault(self.__name, 0)

    @property
    def elapsed_time(self):
        return self.__elapsed_time

    def start(self) -> None:
        """Start timer"""
        if self.__start_time is not None:
            raise TimerError("Timer is running. Use .stop() to stop it")
        self.__start_time = time.perf_counter()
        # logger.debug(f"Timer start: {self.__start_time}")

    def stop(self) -> float:
        """
        Stop timer, and reset value of start time to None

        :return: elapsed time (aka delta) since starting the timer
        """
        if self.__start_time is None:
            raise TimerError("Timer not started. Use .start() to start it.")
        end_time = time.perf_counter()
        self.__elapsed_time = (end_time - self.__start_time) * 1000  # in ms
        self.__start_time = None

        if self.__name:
            # Accumulating time for timers with the same name
            try:
                self.timers[self.__name] += self.__elapsed_time
            except KeyError:
                self.timers[self.__name] = 0
        logger.debug(repr(self))

        # logger.debug(f"Timer stop: {end_time}")
        # logger.debug(f"Elapsed time: {self.__elapsed_time:0.6f} ms")
        return self.__elapsed_time

    def update_name(self, name: str):
        self.timers[name] = self.timers.pop(self.__name)
        self.__name = name

    def __call__(self, func):
        """Support using Timer as a decorator"""

        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper_timer

    # Adding ability to use Timer as a context manager
    def __enter__(self):
        """Start new timer using Timer context manager"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Stop timer using Timer context manager

        For the moment, this class does not yet do any error handling.
        It just uses the default error handling when calling .__exit__()
        """
        self.stop()

    def __repr__(self) -> str:
        return (
            f"{Timer.__name__} "
            f"(name='{self.__name}', "
            f"elapsed={self.__elapsed_time:0.6f} ms, "
            f"acc_time={self.timers.get(self.__name):0.6f} ms)"
        )
