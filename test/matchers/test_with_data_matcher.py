# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QAction
from hamcrest import assert_that
from hamcrest import is_

from cute import matchers


def test_matches_actions_by_their_data(qt):
    action = QAction(None)
    action.setData("<data>")

    matcher = matchers.with_data("<data>")
    assert_that(matcher.matches(action), is_(True), "same data")

    action.setData("<other data>")
    assert_that(matcher.matches(action), is_(False), "different data")
