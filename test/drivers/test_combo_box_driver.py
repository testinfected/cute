# -*- coding: utf-8 -*-
import pytest
from PyQt5.QtWidgets import QComboBox
from hamcrest import equal_to
from pytest import raises

from cute.widgets import only_widget, QComboBoxDriver


@pytest.fixture()
def combo_box(viewer):
    combo = QComboBox()
    viewer.view(combo)
    return combo


@pytest.yield_fixture()
def driver(prober, automaton):
    driver = QComboBoxDriver(only_widget(QComboBox), prober, automaton)
    yield driver
    driver.close()


def test_asserts_combo_current_text(combo_box, driver):
    combo_box.addItems(["Bananas", "Oranges", "Apples"])
    combo_box.setCurrentIndex(1)

    driver.has_current_text("Oranges")

    with raises(AssertionError):
        driver.has_current_text(equal_to("Bananas"))


def test_selects_option_by_item_text(combo_box, driver):
    combo_box.addItems(["Bananas", "Oranges", "Apples"])

    driver.select_option("Oranges")
    driver.has_current_text("Oranges")


def test_asserts_presence_of_option(combo_box, driver):
    items = ["Bananas", "Oranges", "Apples"]
    combo_box.addItems(items)

    driver.has_options(*items)

    driver.has_no_option("Strawberry")
