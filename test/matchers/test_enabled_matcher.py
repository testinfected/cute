# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel
from hamcrest import assert_that
from hamcrest import is_

from cute import matchers


def test_matches_enabled_widgets(qt):
    label = QLabel()
    label.setEnabled(True)

    matcher = matchers.enabled()
    assert_that(matcher.matches(label), is_(True), "enabled")

    label.setEnabled(False)
    assert_that(matcher.matches(label), is_(False), "disabled")
