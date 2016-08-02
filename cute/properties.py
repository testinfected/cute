# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QObject, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QLineEdit, QDateTimeEdit, QComboBox, QAbstractButton, QAction
from hamcrest.core.selfdescribing import SelfDescribing


def name():
    return PropertyQuery("name", QObject.objectName)


def text():
    return PropertyQuery("text", lambda w: w.text())


def data():
    return PropertyQuery("data", QAction.data)


def icon_size():
    return PropertyQuery("icon size", QAbstractButton.iconSize)


def size_height():
    return PropertyQuery("height", QSize.height)


def size_width():
    return PropertyQuery("width", QSize.width)


def label_pixmap():
    return PropertyQuery("pixmap", QLabel.pixmap)


def pixmap_size():
    return PropertyQuery("size", QPixmap.size)


def label_buddy():
    return PropertyQuery("buddy", QLabel.buddy)


def input_text():
    return PropertyQuery("display text", QLineEdit.displayText)


def plain_text():
    return PropertyQuery("plain text", lambda w: w.toPlainText())


def current_text():
    return PropertyQuery("current text", QComboBox.currentText)


def item_text():
    return PropertyQuery("item text", lambda item: item.data(Qt.DisplayRole))


def time():
    return PropertyQuery("time", QDateTimeEdit.time)


def date():
    return PropertyQuery("date", QDateTimeEdit.date)


def title():
    return PropertyQuery("title", lambda w: w.title())


def window_title():
    return PropertyQuery("window title", lambda w: w.windowTitle())


def cursor_shape():
    return PropertyQuery("cursor shape", lambda w: w.cursor().shape())


def count():
    return PropertyQuery("options count", lambda w: w.count())


def tooltip():
    return PropertyQuery("tooltip", lambda w: w.toolTip())


def has_option_text(index):
    return PropertyQuery("option {0}".format(index), lambda combo_box: combo_box.itemText(index))


def current_directory():
    return PropertyQuery("current directory", lambda dialog: dialog.directory().absolutePath())


class Query(SelfDescribing):
    def __call__(self, arg):
        pass


class PropertyQuery(Query):
    def __init__(self, name, query):
        super().__init__()
        self._property_name = name
        self._query = query

    def __call__(self, arg):
        return self._query(arg)

    def describe_to(self, description):
        description.append_text(self._property_name)
