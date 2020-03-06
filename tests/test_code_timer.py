import time
import logging

import pytest

from code_timer import timer, timeit

logging.basicConfig(level=logging.DEBUG)
PACKAGE_LOGGER = "code_timer"
DEFAULT_TIMEIT_REPEATS = 10
DEFAULT_LOOPS = 10


@timer
def decorated_timer_no_brackets(*, loop: int):
    sum(n ** 2 for n in range(loop))


@timer()
def decorated_timer_with_brackets(*, loop: int):
    sum(n ** 2 for n in range(loop))


@timeit(num_repeats=DEFAULT_TIMEIT_REPEATS)
def decorated_timeit(*, loop: int):
    sum(n ** 2 for n in range(loop))


def test_timeit_decorator_info_level_logging(caplog):
    caplog.set_level(logging.INFO, logger=PACKAGE_LOGGER)
    decorated_timeit(loop=DEFAULT_LOOPS)
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "INFO"


def test_timeit_decorator_debug_level_logging(caplog):
    caplog.set_level(logging.DEBUG, logger=PACKAGE_LOGGER)
    decorated_timeit(loop=DEFAULT_LOOPS)
    assert len(caplog.records) >= DEFAULT_TIMEIT_REPEATS
    assert caplog.records[0].levelname == "DEBUG"
    assert caplog.records[-1].levelname == "INFO"

