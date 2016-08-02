# -*- coding: utf-8 -*-
from contextlib import contextmanager

import pytest
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QAbstractButton, QPushButton, QCheckBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from hamcrest import assert_that
from pytest import raises

from cute.matchers import has_dimensions
from cute.probes import ValueMatcherProbe
from cute.widgets import only_widget, QButtonDriver, QTabWidgetDriver


@pytest.fixture()
def tabs(viewer):
    tab_widget = QTabWidget()
    viewer.view(tab_widget)
    return tab_widget


@pytest.yield_fixture()
def driver(prober, automaton):
    driver = QTabWidgetDriver(only_widget(QTabWidget), prober, automaton)
    yield driver
    driver.close()


def test_selects_tab_by_text(tabs, driver):
    tabs.addTab(QWidget(), "tab1")
    tabs.addTab(QWidget(), "tab2")
    tabs.addTab(QWidget(), "tab3")

    driver.has_selected_tab(0)

    driver.select_tab("tab2")
    driver.has_selected_tab(1)
