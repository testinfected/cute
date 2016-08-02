# -*- coding: utf-8 -*-
import pytest
from PyQt5.QtGui import QPixmap
from hamcrest import not_, equal_to
from pytest import raises
from PyQt5.QtWidgets import QLabel

from cute import matchers
from cute.widgets import QLabelDriver, only_widget


@pytest.fixture()
def label(viewer):
    label = QLabel()
    viewer.view(label)
    return label


@pytest.yield_fixture()
def driver(prober, automaton):
    driver = QLabelDriver(only_widget(QLabel), prober, automaton)
    yield driver
    driver.close()


def test_asserts_label_text(label, driver):
    label.setText("text")

    driver.has_text("text")

    with raises(AssertionError):
        driver.has_text(not_(equal_to("text")))


def test_asserts_label_pixmap(label, driver):
    label.setPixmap(QPixmap(20, 30))

    driver.has_pixmap(matchers.with_pixmap_size(20, 30))

    with raises(AssertionError):
        driver.has_pixmap(matchers.with_pixmap_size(0, 0))

