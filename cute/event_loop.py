# -*- coding: utf-8 -*-
import time

from PyQt5.QtCore import QCoreApplication, QEventLoop


ONE_SECOND_IN_MILLIS = 1000


class Timeout(object):
    def __init__(self, duration_in_ms):
        self._duration = duration_in_ms
        self._start_time = time.time()

    def has_expired(self):
        return self.elapsed_time(time.time()) >= self._duration

    def elapsed_time(self, now):
        return (now - self._start_time) * ONE_SECOND_IN_MILLIS


SLEEP_DELAY_IN_MILLIS = 10


def process_events_for(ms):
    timeout = Timeout(ms)
    while not timeout.has_expired():
        process_pending_events(ms)
        time.sleep(SLEEP_DELAY_IN_MILLIS / ONE_SECOND_IN_MILLIS)


def process_pending_events(for_ms=0):
    QCoreApplication.processEvents(QEventLoop.AllEvents, for_ms)
