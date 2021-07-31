import re
import logging

import pytest

import code_timer.timer as ct

logging.basicConfig(level=logging.DEBUG)
PACKAGE_LOGGER = "code_timer"

DEFAULT_TIMEIT_REPEATS = 10
DEFAULT_LOOPS = 100
RE_TIMER_START = re.compile("timer start: " + r"0\.\d{6}")
RE_TIMER_STOP = re.compile("timer stop: " + r"0\.\d{6}")
RE_ELAPSED_TIME = re.compile("elapsed time: " + r"0\.\d{6} ms")
TIMER_NAME = "my_timer"
TIMER_NAME_LOG = f"using custom timer: timer (name='{TIMER_NAME}'"
RE_TIMER_NAME_LOG = re.compile("acc_time=" + r"0\.\d{6} ms")
TIMEIT_LOG = f"best 3 of {DEFAULT_TIMEIT_REPEATS} for "


def timer_func(loop: int = DEFAULT_LOOPS):
    sum(n ** 2 for n in range(loop))
    return 3


@pytest.fixture(autouse=True)
def propogate_package_logger():
    """
    Adding propogation before each test, then removing in the cleanup for
    each test.

    The caplog doesn't register any logs if propogate=False.  However,
    if propogate=True it registers the logs, but there are double logs
    output to the console. When I tried outputting the logs to a file,
    only 1 set of logs were output.
    """
    logger = logging.getLogger(PACKAGE_LOGGER)
    logger.propagate = True

    yield

    logger.propagate = False


class TestTimerClass:
    def test_timer_init(self):
        t = ct.Timer(name="my_name")
        assert t.elapsed_time is None
        assert "my_name" in t.timers

    def test_timer_class_as_context_manager(self):
        with ct.Timer() as t:
            timer_func()
        assert t.elapsed_time is not None and t.elapsed_time >= 0

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
        assert isinstance(t.timers, dict), (
            "get_timer did not return a " "dictionary instance"
        )
        assert "default" in t.timers.keys(), (
            "get_timer did not return {None: 0} when a timer name was "
            "not passed into the class instance"
        )

    def test_elapsed_time_returned_after_using_timer(self):
        with ct.Timer(name="my_timer") as t:
            timer_func()
        assert t.elapsed_time > 0
        assert isinstance(t.elapsed_time, float)

    def test_clear_all_timers(self):
        with ct.Timer() as t:
            timer_func()
            t.clear()
        assert t.timers == {t.DEFAULT_TIMER: 0}


@ct.timeit(num_repeats=DEFAULT_TIMEIT_REPEATS, name="my_timer")
def dec_timing():
    return 3


class TestTimerDecorators:
    def test_deco_timer_with_kwargs(self):
        @ct.timer(name="my_timer")
        def timing():
            return 3

        assert timing() == 3

    def test_timer_with_brackets_defaults(self):
        @ct.timer()
        def timing():
            return 3

        assert timing() == 3

    def test_timer_no_brackets(self):
        @ct.timer
        def timing():
            return 3

        assert timing() == 3

    def test_timeit_log_output(self, caplog):
        caplog.set_level(logging.INFO, logger=PACKAGE_LOGGER)
        dec_timing()
        assert len(caplog.records) == 1, "Contains more than one log output"
        assert caplog.records[0].levelname == "INFO", "Log level is not 'INFO'"
        assert all(
            [rec for rec in caplog.records if rec.levelno <= 20]
        ), "Log record above 'INFO' level "

    def test_timeit_with_kwargs(self):
        assert dec_timing() == 3

    def test_timeit_with_brackets_defaults(self):
        @ct.timeit()
        def timing():
            return 3

        assert timing() == 3

    def test_timeit_no_brackets(self):
        @ct.timeit
        def timing():
            return 3

        assert timing() == 3

    def test_recursive_timer(self):
        @ct.recursive_timer
        def fib(n):
            if n <= 0:
                return 0
            elif n == 1:
                return 1
            return fib(n-2) + fib(n-1)
        fib(25)

