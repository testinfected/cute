# -*- coding: utf-8 -*-
from .prober import Probe


class WidgetFinder(Probe):
    def widgets(self):
        pass


class WidgetSelector(WidgetFinder):
    def widget(self):
        return self.widgets()[0] if self.widgets() else None


class RecursiveWidgetFinder(WidgetFinder):
    def __init__(self, widget_type, criteria, parent_finder):
        super(RecursiveWidgetFinder, self).__init__()
        self._widget_type = widget_type
        self._criteria = criteria
        self._parent_finder = parent_finder
        self._found = set()

    def is_satisfied(self):
        return self._parent_finder.is_satisfied()

    def widgets(self):
        return tuple(self._found)

    def test(self):
        self._parent_finder.test()
        self._found.clear()
        self._search(self._parent_finder.widgets())

    def describe_to(self, description):
        description.append_text(self._widget_type.__name__) \
            .append_text(" ") \
            .append_description_of(self._criteria) \
            .append_text("\n  in ") \
            .append_description_of(self._parent_finder)

    def describe_failure_to(self, description):
        self._parent_finder.describe_failure_to(description)

    def _search(self, widgets):
        for widget in widgets:
            self._search_within(widget)

    def _search_within(self, widget):
        if isinstance(widget, self._widget_type) and self._criteria.matches(widget):
            self._found.add(widget)
        else:
            self._search(widget.findChildren(self._widget_type))


class TopLevelWidgetsFinder(WidgetFinder):
    def __init__(self, app):
        super(TopLevelWidgetsFinder, self).__init__()
        self._app = app

    def is_satisfied(self):
        return True

    def widgets(self):
        return tuple(self._root_windows)

    def test(self):
        self._root_windows = set()
        for top_level_widget in self._app.topLevelWidgets():
            self._root_windows.add(self._root_parent(top_level_widget))

    def describe_to(self, description):
        description.append_text('all top level widgets')

    def describe_failure_to(self, description):
        self.describe_to(description)

    def _root_parent(self, widget):
        return widget if not widget.parent() else self._root_parent(widget.parent())


class SingleWidgetFinder(WidgetSelector):
    def __init__(self, finder):
        super(SingleWidgetFinder, self).__init__()
        self._finder = finder

    def is_satisfied(self):
        return self._finder.is_satisfied() & self._is_single()

    def test(self):
        self._finder.test()

    def widgets(self):
        return self._finder.widgets()

    def describe_to(self, description):
        description.append_text('the unique ').append_description_of(self._finder)

    def describe_failure_to(self, description):
        if not self._finder.is_satisfied():
            self._finder.describe_failure_to(description)
        else:
            description.append_text("found ")
            if self._widget_count() > 0:
                description.append_description_of(self._widget_count())
            else:
                description.append_text("no")

            description.append_text(" ")
            self._finder.describe_to(description)

    def _is_single(self):
        return self._widget_count() == 1

    def _widget_count(self):
        return len(self.widgets())


class MissingWidgetFinder(WidgetFinder):
    def __init__(self, finder):
        super().__init__()
        self._finder = finder

    def is_satisfied(self):
        return self._finder.is_satisfied() and self._is_missing()

    def test(self):
        self._finder.test()

    def widgets(self):
        return self._finder.widgets()

    def describe_to(self, description):
        description.append_text('no ').append_description_of(self._finder)

    def describe_failure_to(self, description):
        self._finder.describe_failure_to(description)

    def _is_missing(self):
        return len(self.widgets()) == 0


class WidgetIdentity(WidgetSelector):
    def __init__(self, widget, description=None):
        self._widget = widget
        self._description = description

    def test(self):
        pass

    def widgets(self):
        return self._widget,

    def is_satisfied(self):
        return True

    def describe_to(self, description):
        description.append_text('the exact ') \
            .append_text(type(self._widget).__name__) \
            .append_text(" '{0}'".format(self._description or self._widget.objectName()))

    def describe_failure_to(self, description):
        pass


class NthWidgetFinder(WidgetSelector):
    def __init__(self, finder, index):
        super(NthWidgetFinder, self).__init__()
        self._finder = finder
        self._index = index

    def widgets(self):
        widgets = self._finder.widgets()
        if widgets:
            return widgets[self._index],
        else:
            return ()

    def describe_failure_to(self, description):
        self._finder.describe_failure_to(description)
        if self.is_satisfied():
            description.append_text('\n  the ')
            description.append_description_of(self._index + 1)
            description.append_text('th widget')

    def describe_to(self, description):
        description.append_text('the ')
        description.append_description_of(self._index + 1)
        description.append_text('th widget from those matching ')
        description.append_description_of(self._finder)

    def is_satisfied(self):
        return self._finder.is_satisfied() and len(self._finder.widgets()) > self._index

    def test(self):
        self._finder.test()
