# timer.py

import time
import logging
import functools

# Setup logging
logger = logging.getLogger("code_timer")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter(
    fmt="%(asctime)s: %(name)s.%(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)


class TimerError(Exception):
    """Custom exception for Timer class."""


def timer(*dargs, **dkwargs):
    """
    Apply Timer as decorator.  Benefit of this is you can use @timer or
    @timer()

    :param dargs: positional arguments passed to Timer object
    :param dkwargs: keyword arguments passed to Timer object
    """
    # support both @timer and @timer() as valid syntax
    if len(dargs) == 1 and callable(dargs[0]):
        def wrap_simple(f):
            @functools.wraps(f)
            def wrapped_f(*args, **kwargs):
                with Timer():
                    return f(*args, **kwargs)
            return wrapped_f
        return wrap_simple(dargs[0])
    else:
        def wrap(f):
            @functools.wraps(f)
            def wrapped_f(*args, **kwargs):
                with Timer(*dargs, **dkwargs):
                    return f(*args, **kwargs)
            return wrapped_f
        return wrap


def timeit(*, num_repeats: int = 10000):
    # support both @timeit and @timeit() as valid syntax
    def wrap(f):
        @functools.wraps(f)
        def wrapped_f(*args, **kwargs):
            repeats = [0] * num_repeats
            for i in range(num_repeats):
                with Timer() as t:
                    temp = f(*args, **kwargs)
                repeats[i] = t.elapsed_time
            repeats.sort()
            logger.info(f"Best 3 of {num_repeats} "
                        f"for {f.__name__}: "
                        f"{repeats[0]:0.4f} ms; "
                        f"{repeats[1]:0.4f} ms; "
                        f"{repeats[2]:0.4f} ms; ")
            return temp
        return wrapped_f
    return wrap


class Timer:
    timers = dict()

    def __init__(self, name: str = None):
        """
        :param name: can pass in a specific name of a timer.  This is
            helpful if you want to time multiple events, and accumulate the
            result with one total time.  The timer name is the dictionary
            key and the accumulated time is the dictionary value.
        """
        self.__name = name
        self.__start_time = None
        self.__elapsed_time = None

        # Add new name to dictionary of timers
        self.timers.setdefault(name, 0)

    @property
    def get_timer(self) -> dict:
        """
        Get timer name and associated time value

        :return: dictionary of the timer name and run time for that timer name
        """
        return self.timers

    @property
    def elapsed_time(self):
        return self.__elapsed_time

    def start(self) -> None:
        """Start timer"""
        if self.__start_time is not None:
            raise TimerError("Timer is running. "
                             "Use .stop() to stop it")
        self.__start_time = time.perf_counter()
        logger.debug(f"Timer start: {self.__start_time}")

    def stop(self) -> float:
        """
        Stop timer, and reset value of start time to None

        :return: elapsed time (aka delta) since starting the timer
        """
        if self.__start_time is None:
            raise TimerError("Timer not started. "
                             "Use .start() to start it.")
        end_time = time.perf_counter()
        self.__elapsed_time = (end_time - self.__start_time) * 1000  # in ms
        self.__start_time = None

        if self.__name:
            # Accumulating time for timers with the same name
            self.timers[self.__name] += self.__elapsed_time
            logger.info(f"Using custom timer: {self.__repr__()}")

        logger.debug(f"Timer stop: {end_time}")
        logger.debug(f"Elapsed time: {self.__elapsed_time:0.6f} ms")
        return self.__elapsed_time

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
        return f"{Timer.__name__} " \
            f"(name='{self.__name}'; " \
            f"acc_time={self.get_timer[self.__name]:0.4f} ms)"
