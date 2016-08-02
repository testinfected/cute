# -*- coding: utf-8 -*-
import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from hamcrest import assert_that, same_instance
from pytest import raises

from cute import matchers
from cute.matchers import named
from cute.widgets import only_widget, QWidgetDriver


@pytest.fixture()
def widget(viewer):
    widget = QWidget()
    viewer.view(widget)
    return widget


@pytest.yield_fixture()
def driver(prober, automaton):
    driver = QWidgetDriver(only_widget(QWidget, named("widget under test")), prober, automaton)
    yield driver
    driver.close()


def test_asserts_presence_of_widget(widget, driver):
    driver.exists()
    assert_that(driver.widget(), same_instance(widget), "widget")

    with raises(AssertionError):
        QWidgetDriver.find_single(driver, QWidget, matchers.named("does not exist")).exists()


def test_asserts_widget_is_showing_on_screen(widget, driver):
    driver.is_showing_on_screen()

    widget.hide()
    with raises(AssertionError):
        driver.is_showing_on_screen()


def test_asserts_widget_is_hidden_from_view(widget, driver):
    with raises(AssertionError):
        driver.is_hidden()

    widget.hide()
    driver.is_hidden()


def test_asserts_widget_is_enabled(widget, driver):
    widget.setEnabled(True)
    driver.is_enabled()

    widget.setEnabled(False)
    with raises(AssertionError):
        driver.is_enabled()


def test_asserts_widget_is_disabled(widget, driver):
    widget.setDisabled(True)
    driver.is_disabled()

    widget.setDisabled(False)
    with raises(AssertionError):
        driver.is_disabled()


def test_asserts_widget_has_tooltip(widget, driver):
    widget.setToolTip("tooltip text")
    driver.has_tooltip("tooltip text")

    with raises(AssertionError):
        driver.has_tooltip("different tooltip text")


def test_asserts_widget_has_cursor_shape(widget, driver):
    widget.setCursor(Qt.ArrowCursor)
    driver.has_cursor_shape(Qt.ArrowCursor)

    with raises(AssertionError):
        driver.has_cursor_shape(Qt.PointingHandCursor)


def test_asserts_window_title_text(widget, driver):
    widget.setWindowTitle("title")
    driver.has_window_title("title")

    with raises(AssertionError):
        driver.has_window_title("different title")
