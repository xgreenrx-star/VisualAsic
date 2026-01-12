from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QBrush, QColor


class ButtonItem(QGraphicsRectItem):
    def __init__(self, x: float, y: float, w: float, h: float, text: str = "Button"):
        super().__init__(QRectF(0, 0, w, h))
        self.setPos(x, y)
        self.setBrush(QBrush(QColor("#008800")))
        self.setFlags(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable)
        self.text = QGraphicsTextItem(text, parent=self)
        # center text roughly
        tr = self.text.boundingRect()
        self.text.setPos((w - tr.width()) / 2, (h - tr.height()) / 2)


class DesignerCanvas(QGraphicsView):
    """A simple WYSIWYG canvas for placing and manipulating controls."""

    def __init__(self, parent=None, width: int = 320, height: int = 240):
        super().__init__(parent)
        self._scene = QGraphicsScene(0, 0, width, height)
        self.setScene(self._scene)
        self.setRenderHints(self.renderHints() | Qt.RenderHint.Antialiasing)
        self.setFixedSize(width + 2, height + 2)

    def add_button(self, x: float, y: float, w: float = 80, h: float = 30, text: str = "Button") -> ButtonItem:
        btn = ButtonItem(x, y, w, h, text)
        self._scene.addItem(btn)
        return btn

    def controls(self):
        return [it for it in self._scene.items() if isinstance(it, ButtonItem)]
