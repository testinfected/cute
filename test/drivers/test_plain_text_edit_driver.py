# -*- coding: utf-8 -*-
import pytest
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPlainTextEdit
from hamcrest import not_, equal_to
from pytest import raises

from cute import gestures
from cute.probes import ValueMatcherProbe
from cute.widgets import only_widget, QPlainTextEditDriver


@pytest.fixture()
def text_edit(viewer):
    edit = QPlainTextEdit()
    viewer.view(edit)
    return edit


@pytest.yield_fixture()
def driver(prober, automaton):
    driver = QPlainTextEditDriver(only_widget(QPlainTextEdit), prober, automaton)
    yield driver
    driver.close()


def test_asserts_text_edit_content(text_edit, driver):
    text_edit.setPlainText("some text\nspanning\nmultiple lines")

    driver.has_plain_text("some text\nspanning\nmultiple lines")

    with raises(AssertionError):
        driver.has_plain_text(not_(equal_to("some text\nspanning\nmultiple lines")))


def test_enters_a_single_line_of_text_in_an_empty_text_edit(text_edit, driver):
    driver.focus_with_mouse()
    driver.type_text("lorem ipsum")

    driver.has_plain_text("lorem ipsum")


def test_enters_multiple_lines_of_text_in_an_empty_text_edit(text_edit, driver):
    driver.focus_with_mouse()
    driver.type_text("some text")
    driver.add_line("spanning")
    driver.add_line("multiple lines")

    driver.has_plain_text("some text\nspanning\nmultiple lines")


def test_clears_text_edit(text_edit, driver):
    text_edit.setPlainText("some text\nspanning\nmultiple lines")

    driver.focus_with_mouse()
    driver.clear_all_text()

    driver.has_plain_text("")


def test_replaces_all_line_edit_text(text_edit, driver):
    text_edit.setPlainText("some text\nspanning\nmultiple lines")

    driver.replace_all_text("replacement text")
    driver.has_plain_text("replacement text")
