import pytest
from PyQt6.QtWidgets import QWidget


def test_qt_smoke(qtbot):
    w = QWidget()
    w.setWindowTitle("qt_smoke")
    qtbot.addWidget(w)
    w.show()
    assert w.isVisible()
