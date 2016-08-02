from PyQt5.QtCore import QPoint, QMargins


def center_right(rect):
    return QPoint(rect.right(), rect.center().y())


def center_left(rect):
    return QPoint(rect.left(), rect.center().y())


def top_center(rect):
    return QPoint(rect.center().x(), rect.top())


def bottom_center(rect):
    return QPoint(rect.center().x(), rect.bottom())


def inside_bounds(rect, left=0, top=0, right=0, bottom=0):
    return rect.marginsRemoved(QMargins(left, top, right, bottom))