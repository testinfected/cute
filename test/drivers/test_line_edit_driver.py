# -*- coding: utf-8 -*-
import pytest
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLineEdit
from hamcrest import not_, equal_to
from pytest import raises

from cute import matchers
from cute.probes import ValueMatcherProbe
from cute.widgets import only_widget, QLineEditDriver


@pytest.fixture()
def line_edit(viewer):
    edit = QLineEdit()
    viewer.view(edit)
    return edit


@pytest.yield_fixture()
def driver(prober, automaton):
    driver = QLineEditDriver(only_widget(QLineEdit), prober, automaton)
    yield driver
    driver.close()


def test_asserts_line_edit_text(line_edit, driver):
    line_edit.setText("text")

    driver.has_text("text")

    with raises(AssertionError):
        driver.has_text(not_(equal_to("text")))


def test_enters_text_in_an_empty_line_edit(line_edit, driver):
    driver.focus_with_mouse()
    driver.type_text("lorem ipsum")
    driver.has_text("lorem ipsum")


def test_replaces_line_edit_current_text(line_edit, driver):
    line_edit.setText("existing text")

    driver.change_text("replacement text")
    driver.has_text("replacement text")


def test_clears_line_edit_current_text(line_edit, driver):
    line_edit.setText("lorem ipsum")

    driver.focus_with_mouse()
    driver.clear_all_text()
    driver.has_text("")

