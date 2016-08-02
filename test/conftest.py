import pytest
import sip

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

from cute.animatron import Animatron
from cute.prober import EventProcessingProber


@pytest.yield_fixture()
def qt():
    application = QApplication([])
    yield application
    application.exit()
    # If we don't force deletion of the C++ wrapped object, it causes the test suite to eventually crash
    # Never ever remove this!!
    sip.delete(application)


@pytest.fixture()
def prober():
    return EventProcessingProber()


# The animatron requires a running qt event loop
@pytest.fixture()
def automaton(qt):
    return Animatron()


class WidgetViewer(QMainWindow):
    def view(self, widget):
        widget.setObjectName("widget under test")
        self.setCentralWidget(widget)
        self.adjustSize()
        self.show()


@pytest.fixture()
def viewer(qt):
    return WidgetViewer()

