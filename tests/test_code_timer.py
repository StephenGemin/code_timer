import re
import logging

import pytest

import code_timer as ct

logging.basicConfig(level=logging.DEBUG)
PACKAGE_LOGGER = "code_timer"
DEFAULT_TIMEIT_REPEATS = 10
DEFAULT_LOOPS = 10
ELAPSED_TIME_PREFIX = "Elapsed time:"
RE_TIMER_START = re.compile("Timer start: " + r"0\.\d{6}")
RE_TIMER_STOP = re.compile("Timer stop: " + r"0\.\d{6}")
RE_ELAPSED_TIME = re.compile(ELAPSED_TIME_PREFIX + r" 0\.\d{6} ms")


def timer_func(loop: int = DEFAULT_LOOPS):
    sum(n ** 2 for n in range(loop))


@ct.timer
def decorated_timer_no_brackets():
    timer_func()


@ct.timer()
def decorated_timer_with_brackets():
    timer_func()


@ct.timeit(num_repeats=DEFAULT_TIMEIT_REPEATS)
def decorated_timeit():
    timer_func()


class TestTimers:

    def test_timeit_decorator_info_level_logging(self, caplog):
        caplog.set_level(logging.INFO, logger=PACKAGE_LOGGER)
        decorated_timeit()
        assert len(caplog.records) == 1, "Contains more than one log output"
        assert caplog.records[0].levelname == "INFO", "Log level is not 'INFO'"
        assert all([rec for rec in caplog.records if rec.levelno <= 20]), \
            "Log record above 'INFO' level "

    def test_timeit_decorator_debug_level_logging(self, caplog):
        caplog.set_level(logging.DEBUG, logger=PACKAGE_LOGGER)
        decorated_timeit()
        assert len(caplog.records) >= DEFAULT_TIMEIT_REPEATS
        assert caplog.records[0].levelname == "DEBUG"
        assert caplog.records[-1].levelname == "INFO"

    def test_timer_class_as_context_manager(self, caplog):
        caplog.set_level(logging.DEBUG, logger=PACKAGE_LOGGER)
        with ct.Timer():
            timer_func()
        assert RE_TIMER_START.match(caplog.records[0].getMessage()), \
            f"Did not find text {str(RE_TIMER_START)} in first log"
        assert RE_TIMER_STOP.match(caplog.records[1].getMessage()), \
            f"Did not find text {str(RE_TIMER_STOP)} in first log"
        assert RE_ELAPSED_TIME.match(caplog.records[2].getMessage())

    def test_timer_error_if_stop_timer_when_not_running(self):
        t = ct.Timer()
        with pytest.raises(ct.TimerError):
            t.stop()

    def test_timer_error_if_start_timer_while_already_running(self):
        t = ct.Timer()
        t.start()
        with pytest.raises(ct.TimerError):
            t.start()

    def test_get_timer_info_when_name_not_passed(self):
        with ct.Timer() as t:
            timer_func()
        print(t.get_timer)
        assert isinstance(t.get_timer, dict), "get_timer did not return a " \
                                              "dictionary instance"
        assert t.get_timer == {None: 0}, \
            "get_timer did not return {None: 0} when a timer name was " \
            "not passed into the class instance"

    def test_elapsed_time_none_when_class_first_initialized(self):
        t = ct.Timer()
        assert t.elapsed_time is None

    def test_elapsed_time_returned_after_using_timer(self):
        with ct.Timer(name="my_timer") as t:
            timer_func()
        assert t.elapsed_time > 0
        assert isinstance(t.elapsed_time, float)
