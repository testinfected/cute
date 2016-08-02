import pytest
import time
from pytest import raises
from hamcrest import assert_that, contains_string

from cute.prober import EventProcessingProber, Probe


@pytest.fixture()
def prober(qt):
    return EventProcessingProber(50, 250)


def test_raises_assertion_if_probe_not_satisfied_within_timeout(prober):
    class FailingProbe(Probe):
        def is_satisfied(self):
            return False

        def describe_to(self, description):
            description.append_text("failure")

    with raises(AssertionError) as error:
        prober.check(FailingProbe())

    assert_that(str(error.value), contains_string("failure"), "error message")


def test_assertion_passes_if_probe_is_satisfied(prober):
    class SuccessfulProbe(Probe):
        def is_satisfied(self):
            return True

    prober.check(SuccessfulProbe())


def test_repeatedly_polls_probe_until_it_is_satisfied(prober):
    class EventuallySuccessfulProbe(Probe):
        def __init__(self):
            self._start_time = time.time()
            self._probe_time = self._start_time

        def test(self):
            self._probe_time = time.time()

        def is_satisfied(self):
            return self._probe_time > self._start_time + 0.1

        def describe_failure_to(self, description):
            description.append_text("probe never succeeded")

        def describe_to(self, description):
            description.append_text("probe to succeed after 100ms")

    prober.check(EventuallySuccessfulProbe())