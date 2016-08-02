# -*- coding: utf-8 -*-

from hamcrest.core.selfdescribing import SelfDescribing
from hamcrest.core.string_description import StringDescription

from . import event_loop
from cute.event_loop import Timeout

DEFAULT_POLL_DELAY = 25
DEFAULT_POLL_TIMEOUT = 1000


class Probe(SelfDescribing):
    def test(self):
        pass

    def is_satisfied(self):
        pass

    def describe_to(self, description):
        pass

    def describe_failure_to(self, description):
        pass


class Prober(object):
    def check(self, probe):
        pass


def _describe_failure_of(probe):
    description = StringDescription()
    description.append_text('\nTried to look for...\n  ')
    probe.describe_to(description)
    description.append_text('\nbut...\n  ')
    probe.describe_failure_to(description)
    return str(description)


class PollingProber(Prober):
    def __init__(self, poll_delay=DEFAULT_POLL_DELAY, timeout=DEFAULT_POLL_TIMEOUT):
        super(PollingProber, self).__init__()
        self._poll_delay = poll_delay
        self._poll_timeout = timeout

    def check(self, probe):
        if not self._poll(probe):
            raise AssertionError(_describe_failure_of(probe))

    def _poll(self, probe):
        timeout = Timeout(self._poll_timeout)

        while True:
            self._run_probe(probe)

            if probe.is_satisfied():
                return True
            if timeout.has_expired():
                return False
            self._wait_for(self._poll_delay)

    def _run_probe(self, probe):
        pass

    def _wait_for(self, duration):
        pass


class EventProcessingProber(PollingProber):
    def __init__(self, delay_in_ms=DEFAULT_POLL_DELAY, timeout_in_ms=DEFAULT_POLL_TIMEOUT):
        super(EventProcessingProber, self).__init__(delay_in_ms, timeout_in_ms, )

    def _run_probe(self, probe):
        probe.test()

    def _wait_for(self, ms):
        event_loop.process_events_for(ms)

