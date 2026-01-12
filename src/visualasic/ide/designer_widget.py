from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QBrush, QColor, QPainter


class ButtonItem(QGraphicsRectItem):
    def __init__(self, x: float, y: float, w: float, h: float, text: str = "Button", object_id: str = None):
        super().__init__(QRectF(0, 0, w, h))
        self.setPos(x, y)
        self._color = "#008800"
        self.setBrush(QBrush(QColor(self._color)))
        self.setFlags(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable)
        self.text = QGraphicsTextItem(text, parent=self)
        # store id for inspector/event mapping
        self.object_id = object_id or text
        # center text roughly
        tr = self.text.boundingRect()
        self.text.setPos((w - tr.width()) / 2, (h - tr.height()) / 2)

    def mouseDoubleClickEvent(self, event):
        # bubble up to the scene/view; the canvas will handle event opening
        super().mouseDoubleClickEvent(event)
        # no-op here; canvas can inspect double-clicked item via scene event


class DesignerCanvas(QGraphicsView):
    """A simple WYSIWYG canvas for placing and manipulating controls."""

    def __init__(self, parent=None, width: int = 320, height: int = 240):
        super().__init__(parent)
        self._scene = QGraphicsScene(0, 0, width, height)
        self.setScene(self._scene)
        # Enable antialiasing for nicer visuals
        try:
            self.setRenderHints(self.renderHints() | QPainter.RenderHint.Antialiasing)
        except Exception:
            # Fallback if enum naming differs
            self.setRenderHints(self.renderHints())
        self.setFixedSize(width + 2, height + 2)

    @property
    def scene(self):
        """Expose the underlying QGraphicsScene (helper for tests & inspector)."""
        return self._scene

    def add_button(self, x: float, y: float, w: float = 80, h: float = 30, text: str = "Button") -> ButtonItem:
        btn = ButtonItem(x, y, w, h, text)
        self._scene.addItem(btn)
        return btn

    def controls(self):
        return [it for it in self._scene.items() if isinstance(it, ButtonItem)]
