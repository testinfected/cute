# -*- coding: utf-8 -*-
import time

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from . import event_loop
from .gestures import Automaton, MIN_TIME_TO_AVOID_DOUBLE_CLICK

ONE_SECOND_IN_MILLIS = 1000


class KeyboardLayout:
    MODIFIER_MAP = {
        'ctrl': Qt.ControlModifier,
        'command': Qt.ControlModifier
    }

    KEY_MAP = {
        'backspace': Qt.Key_Backspace,
        'escape': Qt.Key_Escape,
        'return': Qt.Key_Return,
        'f4': Qt.Key_F4,
    }

    @staticmethod
    def modifier_code(key):
        return KeyboardLayout.MODIFIER_MAP.get(key, key)

    @staticmethod
    def is_modifier(key):
        return key in KeyboardLayout.MODIFIER_MAP

    @staticmethod
    def key_code(key):
        return KeyboardLayout.KEY_MAP.get(key, key)


class MouseLayout:
    BUTTON_MAP = {
        'left': Qt.LeftButton,
        'right': Qt.RightButton,
    }

    @staticmethod
    def button_code(button):
        return MouseLayout.BUTTON_MAP.get(button, button)


def current_time():
    return time.perf_counter()


class Robot(Automaton):
    """
    A robotic automaton that simulates human gestures. It is very fast, but has limitations.

    The known limitations are:
        - no mouse drag and drop
        - no right clicks on Mac
    """
    MOUSE_MOVE_DELAY = 10  # in ms

    # For detecting double clicks
    _last_button_clicked = -1
    _last_click_time = 0
    _last_click_position = (-1, -1)

    def __init__(self):
        self._modifiers = Qt.NoModifier

    @property
    def mouse_position(self):
        current_position = QCursor.pos()
        return current_position.x(), current_position.y()

    def press_key(self, key):
        if KeyboardLayout.is_modifier(key):
            self._modifiers |= KeyboardLayout.modifier_code(key)
        else:
            QTest.keyPress(self._widget_under_cursor(), KeyboardLayout.key_code(key), self._modifiers)

    def release_key(self, key):
        if KeyboardLayout.is_modifier(key):
            self._modifiers &= ~KeyboardLayout.modifier_code(key)
        else:
            QTest.keyRelease(self._widget_under_cursor(), KeyboardLayout.key_code(key), self._modifiers)

    def type(self, key):
        QTest.keyClick(self._widget_under_cursor(), KeyboardLayout.key_code(key), self._modifiers)

    def move_mouse(self, x, y):
        QCursor.setPos(x, y)
        self.delay(self.MOUSE_MOVE_DELAY)

    def press_mouse(self, button):
        mouse_action = QTest.mouseDClick if self._double_click_detected(button) else QTest.mousePress
        self._at_cursor_position(mouse_action, MouseLayout.button_code(button))

        # for detecting double clicks
        self._last_click_time = current_time()
        self._last_button_clicked = button
        self._last_click_position = self.mouse_position

    def _double_click_detected(self, button_clicked):
        current_position = self.mouse_position
        elapsed_time_in_ms = (current_time() - self._last_click_time) * ONE_SECOND_IN_MILLIS

        return (button_clicked == self._last_button_clicked) and \
               (current_position == self._last_click_position) and \
               (elapsed_time_in_ms <= MIN_TIME_TO_AVOID_DOUBLE_CLICK)

    def release_mouse(self, button):
        self._at_cursor_position(QTest.mouseRelease, MouseLayout.button_code(button))

    def double_click_mouse(self, button):
        self._at_cursor_position(QTest.mouseDClick, MouseLayout.button_code(button))

    def delay(self, ms):
        event_loop.process_events_for(ms)

    def _at_cursor_position(self, mouse_action, button):
        # By default QTest will operate mouse at the center of the widget,
        # but we want the action to occur at the current cursor position
        mouse_action(self._widget_under_cursor(), button, self._modifiers,
                     self._relative_position_to_widget_under_cursor())

    def _widget_under_cursor(self):
        return _widget_at(*self.mouse_position)

    def _relative_position_to_widget_under_cursor(self):
        return _compute_relative_position(self._widget_under_cursor(), *self.mouse_position)


def _widget_at(x, y):
    widget = QApplication.widgetAt(x, y)
    if not widget:
        raise AssertionError('No widget at screen position (%d, %d)!'
                             ' Have you moved the mouse while running the tests?' % (x, y))
    return widget


def _compute_relative_position(widget, x, y):
    return widget.mapFromGlobal(QPoint(x, y))

