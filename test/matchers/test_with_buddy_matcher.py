# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget
from hamcrest import assert_that
from hamcrest import is_

from cute import matchers


def test_matches_labels_by_their_buddy(qt):
    label = QLabel()
    buddy = QLineEdit()
    label.setBuddy(buddy)

    matcher = matchers.with_buddy(buddy)
    assert_that(matcher.matches(label), is_(True), "same buddy")

    label.setBuddy(QWidget())
    assert_that(matcher.matches(label), is_(False), "other buddy")


