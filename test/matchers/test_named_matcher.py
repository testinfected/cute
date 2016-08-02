# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel
from hamcrest import assert_that
from hamcrest import is_

from cute import matchers


def test_matches_widgets_by_their_object_name(qt):
    label = QLabel()
    label.setObjectName("label")

    matcher = matchers.named("label")
    assert_that(matcher.matches(label), is_(True), "same name")

    label.setObjectName("other")
    assert_that(matcher.matches(label), is_(False), "other name")
