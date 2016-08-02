# -*- coding: utf-8 -*-
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget
from hamcrest import assert_that
from hamcrest import is_

from cute import matchers


def test_matches_widgets_by_their_text(qt):
    label = QLabel()
    label.setText("some text")

    matcher = matchers.with_text("some text")
    assert_that(matcher.matches(label), is_(True), "same text")

    label.setText("other text")
    assert_that(matcher.matches(label), is_(False), "other text")
