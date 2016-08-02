# -*- coding: utf-8 -*-
from contextlib import contextmanager

import pytest
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QAbstractButton, QPushButton, QCheckBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from pytest import raises

from cute.matchers import has_dimensions
from cute.probes import ValueMatcherProbe
from cute.widgets import only_widget, QButtonDriver


@pytest.fixture()
def button(viewer):
    button = QPushButton("button")
    viewer.view(button)
    return button


@pytest.fixture()
def checkbox(viewer):
    checkbox = QCheckBox()
    viewer.view(checkbox)
    return checkbox


@pytest.yield_fixture()
def driver(prober, automaton):
    driver = QButtonDriver(only_widget(QAbstractButton), prober, automaton)
    yield driver
    driver.close()


def test_clicks_button_with_the_mouse(button, driver):
    button_pressed_signal = ValueMatcherProbe("button press")

    button.clicked.connect(lambda: button_pressed_signal.received())
    driver.click()
    driver.check(button_pressed_signal)


def test_asserts_button_text(button, driver):
    button.setText("button text")

    driver.has_text("button text")

    with raises(AssertionError):
        driver.has_text("other text")


def test_asserts_button_is_checked(checkbox, driver):
    checkbox.setChecked(True)
    driver.is_checked()

    with raises(AssertionError):
        driver.is_unchecked()


def test_asserts_button_is_unchecked(checkbox, driver):
    checkbox.setChecked(False)
    driver.is_unchecked()

    with raises(AssertionError):
        driver.is_checked()


def test_asserts_button_icon_size(button, driver):
    button.setIconSize(QSize(24, 24))
    driver.has_icon_size(has_dimensions(24, 24))

    with raises(AssertionError):
        driver.has_icon_size(has_dimensions(48, 48))

