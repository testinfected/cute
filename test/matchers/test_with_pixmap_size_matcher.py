# -*- coding: utf-8 -*-
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget
from hamcrest import assert_that
from hamcrest import is_

from cute import matchers


def test_matches_pixmaps_by_their_size(qt):
    matcher = matchers.with_pixmap_size(75, 50)

    assert_that(matcher.matches(QPixmap(75, 50)), is_(True), "right size")
    assert_that(matcher.matches(QPixmap(50, 75)), is_(False), "different size")
