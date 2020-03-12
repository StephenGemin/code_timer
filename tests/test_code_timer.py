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


@ct.timer
def decorated_timer_no_brackets():
    timer_func()


@ct.timer()
def decorated_timer_with_brackets():
    timer_func()


@ct.timer(name=TIMER_NAME)
def decorated_timer_name_passed():
    timer_func()


@ct.timeit(num_repeats=DEFAULT_TIMEIT_REPEATS)
def decorated_timeit_num_repeats():
    timer_func()


@ct.timeit(num_repeats=DEFAULT_TIMEIT_REPEATS, name=TIMER_NAME)
def decorated_timeit_num_repeats_and_name():
    timer_func()


@ct.timeit()
def decorated_timeit_with_brackets_no_arguments():
    timer_func()


@ct.timeit
def decorated_timeit_no_brackets():
    timer_func()


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
    def test_timer_class_as_context_manager(self, caplog):
        caplog.set_level(logging.DEBUG, logger=PACKAGE_LOGGER)
        with ct.Timer():
            timer_func()
        log = caplog.records[-1].getMessage().lower()
        assert RE_ELAPSED_TIME.match(log), \
            f"Did not find text {str(RE_ELAPSED_TIME)} in log: {log}"

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


class TestTimerDec:
    def test_deco_timer_with_brackets(self, caplog):
        caplog.set_level(logging.DEBUG, logger=PACKAGE_LOGGER)
        decorated_timer_with_brackets()
        log = caplog.records[-1].getMessage().lower()
        assert RE_ELAPSED_TIME.match(log), \
            f"Did not find text {str(RE_ELAPSED_TIME)} in log: {log}"

    def test_deco_timer_without_brackets(self, caplog):
        caplog.set_level(logging.DEBUG, logger=PACKAGE_LOGGER)
        decorated_timer_no_brackets()
        log = caplog.records[-1].getMessage().lower()
        assert RE_ELAPSED_TIME.match(log), \
            f"Did not find text {str(RE_ELAPSED_TIME)} in log: {log}"

    def test_deco_timer_name_passed(self, caplog):
        caplog.set_level(logging.DEBUG, logger=PACKAGE_LOGGER)
        decorated_timer_name_passed()
        log1 = caplog.records[-1].getMessage().lower()
        log2 = caplog.records[1].getMessage().lower()
        assert RE_ELAPSED_TIME.match(log1), \
            f"Did not find text {str(RE_ELAPSED_TIME)} in log: {log1}"
        assert TIMER_NAME_LOG in log2, \
            f"Did not find text {TIMER_NAME_LOG} in log: {log2}"
        assert re.search(RE_TIMER_NAME_LOG, log2), \
            f"Did not find text {RE_TIMER_NAME_LOG} in log: {log2}"


class TestTimeitDec:

    def test_deco_timeit_info_level_logging(self, caplog):
        caplog.set_level(logging.INFO, logger=PACKAGE_LOGGER)
        decorated_timeit_num_repeats()
        assert len(caplog.records) == 1, "Contains more than one log output"
        assert caplog.records[0].levelname == "INFO", "Log level is not 'INFO'"
        assert all([rec for rec in caplog.records if rec.levelno <= 20]), \
            "Log record above 'INFO' level "

    def test_deco_timeit_debug_level_logging(self, caplog):
        caplog.set_level(logging.DEBUG, logger=PACKAGE_LOGGER)
        decorated_timeit_num_repeats()
        assert len(caplog.records) >= DEFAULT_TIMEIT_REPEATS
        assert caplog.records[0].levelname == "DEBUG"
        assert caplog.records[-1].levelname == "INFO"

    def test_deco_timeit_empty_brackets(self, caplog):
        caplog.set_level(logging.INFO, logger=PACKAGE_LOGGER)
        decorated_timeit_with_brackets_no_arguments()
        assert len(caplog.records) == 1, "Contains more than one log output"
        assert caplog.records[0].levelname == "INFO", "Log level is not 'INFO'"
        assert all([rec for rec in caplog.records if rec.levelno <= 20]), \
            "Log record above 'INFO' level "

    def test_deco_timeit_no_brackets(self, caplog):
        caplog.set_level(logging.INFO, logger=PACKAGE_LOGGER)
        decorated_timeit_no_brackets()
        assert len(caplog.records) == 1, "Does not contain one " \
                                         "single 'INFO' level log"
        assert caplog.records[0].levelname == "INFO", "Log level is not 'INFO'"
        assert all([rec for rec in caplog.records if rec.levelno <= 20]), \
            "Log record above 'INFO' level "

    def test_deco_timeit_name_passed(self, caplog):
        caplog.set_level(logging.DEBUG, logger=PACKAGE_LOGGER)
        func = decorated_timeit_num_repeats_and_name
        func()
        log1 = caplog.records[-1].getMessage().lower()
        log2 = caplog.records[1].getMessage().lower()
        assert TIMEIT_LOG + func.__name__ + ":" in log1
        assert TIMER_NAME_LOG in log2, \
            f"Did not find text {TIMER_NAME_LOG} in log: {log2}"
        assert re.search(RE_TIMER_NAME_LOG, log2), \
            f"Did not find text {RE_TIMER_NAME_LOG} in log: {log2}"
