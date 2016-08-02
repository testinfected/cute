# -*- coding: utf-8 -*-
from PyQt5.QtCore import QPoint, QRect
from hamcrest import described_as, none, empty
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

from .prober import Probe


class WidgetAssertionProbe(Probe):
    def __init__(self, selector, assertion):
        super(WidgetAssertionProbe, self).__init__()
        self._selector = selector
        self._assertion = assertion
        self._assertion_met = False

    def test(self):
        self._selector.test()
        self._assertion_met = \
            self._selector.is_satisfied() and \
            self._assertion.matches(self._selector.widget())

    def is_satisfied(self):
        return self._assertion_met

    def describe_to(self, description):
        description.append_description_of(self._selector) \
            .append_text("\nand check that it ") \
            .append_description_of(self._assertion)

    def describe_failure_to(self, description):
        self._selector.describe_failure_to(description)
        if self._selector.is_satisfied():
            description.append_text("\n  it ")
            self._assertion.describe_mismatch(self._selector.widget(), description)


class WidgetPropertyAssertionProbe(Probe):
    def __init__(self, selector, query, matcher):
        super(WidgetPropertyAssertionProbe, self).__init__()
        self._selector = selector
        self._property_value_query = query
        self._property_value_matcher = wrap_matcher(matcher)
        self._property_value = None

    def test(self):
        self._selector.test()
        if self._selector.is_satisfied():
            self._property_value = self._property_value_query(self._selector.widget())

    def is_satisfied(self):
        return self._selector.is_satisfied() and self._property_value_matcher.matches(self._property_value)

    def describe_to(self, description):
        description.append_description_of(self._selector) \
            .append_text('\nand check that its ') \
            .append_description_of(self._property_value_query) \
            .append_text(' is ') \
            .append_description_of(self._property_value_matcher)

    def describe_failure_to(self, description):
        self._selector.describe_failure_to(description)
        if self._selector.is_satisfied():
            description.append_text('\n  its ') \
                .append_description_of(self._property_value_query) \
                .append_text(" ")
            self._property_value_matcher.describe_mismatch(self._property_value, description)


class WidgetManipulatorProbe(Probe):
    def __init__(self, finder, manipulation, description):
        super(WidgetManipulatorProbe, self).__init__()
        self._finder = finder
        self._manipulate = manipulation
        self._description = description

    def describe_to(self, description):
        self._finder.describe_to(description)
        description.append_text('\nand %s ' % self._description)

    def describe_failure_to(self, description):
        self._finder.describe_failure_to(description)

    def is_satisfied(self):
        return self._finder.is_satisfied()

    def test(self):
        self._finder.test()
        if self._finder.is_satisfied():
            for widget in self._finder.widgets():
                self._manipulate(widget)


class WidgetScreenBoundsProbe(Probe):
    def __init__(self, selector):
        super(WidgetScreenBoundsProbe, self).__init__()
        self._selector = selector
        self.bounds = None

    def describe_to(self, description):
        description.append_text('screen dimensions of ')
        description.append_description_of(self._selector)

    def describe_failure_to(self, description):
        self._selector.describe_failure_to(description)
        if self._selector.is_satisfied():
            description.append_text('\n  had no dimension')

    def is_satisfied(self):
        return self.bounds is not None and self.bounds.width() > 0 and self.bounds.height() > 0

    def test(self):
        self._selector.test()

        if not self._selector.is_satisfied():
            self.bounds = None
            return

        widget = self._selector.widget()
        if widget.isVisible():
            self.bounds = QRect(widget.mapToGlobal(QPoint(0, 0)), widget.size())
        else:
            self.bounds = None


def nothing():
    return described_as("nothing", none())


class ValueMatcherProbe(Probe):
    """
    A probe for callables that expect a single argument
    """

    def __init__(self, message, matcher=nothing()):
        super(ValueMatcherProbe, self).__init__()
        self._message = message
        self.expect(matcher)

    def expect(self, matcher):
        self._value_matcher = wrap_matcher(matcher)
        self._has_received_a_value = False
        self._received_value = None

    def test(self):
        pass

    def is_satisfied(self):
        return self._has_received_a_value and self._value_matcher.matches(self._received_value)

    def describe_to(self, description):
        description.append_text(self._message).append_text(" with ") \
            .append_description_of(self._value_matcher)

    def describe_failure_to(self, description):
        description.append_text(self._message).append_text(" ")
        if self._has_received_a_value:
            description.append_text('received ').append_value(self._received_value)
        else:
            description.append_text('was not received')

    def received(self, value=None):
        self._has_received_a_value = True
        self._received_value = value


class MultiValueMatcherProbe(Probe):
    """
    A probe for callables that expect multiple arguments. Use with collection matchers.
    """

    def __init__(self, message, matcher=empty()):
        super().__init__()
        self._message = message
        self.expect(matcher)

    def expect(self, matcher):
        self._value_matcher = matcher
        self._has_received_a_value = False
        self._received_values = []

    def test(self):
        pass

    def is_satisfied(self):
        return self._has_received_a_value and self._value_matcher.matches(self._received_values)

    def describe_to(self, description):
        description.append_text(self._message).append_text(" with ") \
            .append_description_of(self._value_matcher)

    def describe_failure_to(self, description):
        description.append_text(self._message).append_text(" ")
        if self._has_received_a_value:
            description.append_text('received ').append_list("values (", ", ", ")", self._received_values)
        else:
            description.append_text('was not received')

    def received(self, *values):
        self._has_received_a_value = True
        self._received_values.extend(values)


class KeywordsValueMatcherProbe(Probe):
    def __init__(self, message, matcher=empty()):
        super().__init__()
        self._message = message
        self.expect(matcher)

    def expect(self, matcher):
        self._value_matcher = matcher
        self._has_received_a_value = False
        self._received_values = {}

    def test(self):
        pass

    def is_satisfied(self):
        return self._has_received_a_value and self._value_matcher.matches(self._received_values)

    def describe_to(self, description):
        description.append_text(self._message).append_text(" with ") \
            .append_description_of(self._value_matcher)

    def describe_failure_to(self, description):
        description.append_text(self._message).append_text(" ")
        if self._has_received_a_value:
            description.append_text('received ').append_list("(", ", ", ")", self._received_values.items())
        else:
            description.append_text('was not received')

    def received(self, *_, **values):
        self._has_received_a_value = True
        self._received_values = dict(values)
