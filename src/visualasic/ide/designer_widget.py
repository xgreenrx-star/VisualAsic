from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt6.QtCore import Qt, QRectF, pyqtSignal, QPointF
from PyQt6.QtGui import QBrush, QColor, QPainter
from PyQt6.QtWidgets import QGraphicsItem


class BaseControlItem(QGraphicsRectItem):
    """Base class for simple rectangular controls with basic movement and snapping support."""
    def __init__(self, x: float, y: float, w: float, h: float, text: str = "", object_id: str = None):
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
        sc = self.scene()
        try:
            for v in sc.views():
                if hasattr(v, 'on_item_double_clicked'):
                    v.on_item_double_clicked(self)
        except Exception:
            pass

    def itemChange(self, change, value):
        # Handle position snapping if moved
        try:
            if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
                new_pos = value
                sc = self.scene()
                if sc is None:
                    return super().itemChange(change, value)
                # get first view and read grid/snap settings
                views = sc.views()
                if not views:
                    return super().itemChange(change, value)
                v = views[0]
                if getattr(v, 'snap_to_grid', False):
                    gs = getattr(v, 'grid_size', 8)
                    # round to nearest grid
                    nx = round(new_pos.x() / gs) * gs
                    ny = round(new_pos.y() / gs) * gs
                    return QPointF(float(nx), float(ny))
        except Exception:
            pass
        return super().itemChange(change, value)

    def setPos(self, *args):
        # Snap programmatic setPos calls as well
        try:
            if len(args) == 1:
                p = args[0]
                x, y = p.x(), p.y()
            else:
                x, y = float(args[0]), float(args[1])
            sc = self.scene()
            if sc:
                views = sc.views()
                if views:
                    v = views[0]
                    if getattr(v, 'snap_to_grid', False):
                        gs = getattr(v, 'grid_size', 8)
                        nx = round(x / gs) * gs
                        ny = round(y / gs) * gs
                        return super().setPos(float(nx), float(ny))
        except Exception:
            pass
        return super().setPos(*args)


class ButtonItem(BaseControlItem):
    def __init__(self, x: float, y: float, w: float, h: float, text: str = "Button", object_id: str = None):
        super().__init__(x, y, w, h, text, object_id)


class LabelItem(BaseControlItem):
    def __init__(self, x: float, y: float, text: str = "Label", object_id: str = None):
        # estimate text width/height default
        w, h = 80, 20
        super().__init__(x, y, w, h, text, object_id)


class TextBoxItem(BaseControlItem):
    def __init__(self, x: float, y: float, w: float = 120, h: float = 24, text: str = "", object_id: str = None):
        super().__init__(x, y, w, h, text, object_id)


class PictureBoxItem(BaseControlItem):
    def __init__(self, x: float, y: float, w: float = 100, h: float = 80, object_id: str = None):
        super().__init__(x, y, w, h, "", object_id)
        # PictureBox will display a placeholder background
        self.setBrush(QBrush(QColor("#CCCCCC")))


class DesignerCanvas(QGraphicsView):
    """A simple WYSIWYG canvas for placing and manipulating controls with grid/snapping."""

    # Emits handler name, e.g. 'btnOk_Click' when a control is double-clicked
    control_double_clicked = pyqtSignal(str)

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

        # grid settings
        self.show_grid = True
        self.grid_size = 8
        self.snap_to_grid = True

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        if not self.show_grid:
            return
        gs = self.grid_size
        painter.setPen(QColor(220, 220, 220))
        left = int(rect.left()) - (int(rect.left()) % gs)
        top = int(rect.top()) - (int(rect.top()) % gs)
        x = left
        while x < rect.right():
            painter.drawLine(QPointF(float(x), float(rect.top())), QPointF(float(x), float(rect.bottom())))
            x += gs
        y = top
        while y < rect.bottom():
            painter.drawLine(QPointF(float(rect.left()), float(y)), QPointF(float(rect.right()), float(y)))
            y += gs

    @property
    def scene(self):
        """Expose the underlying QGraphicsScene (helper for tests & inspector)."""
        return self._scene

    # Emits handler name, e.g. 'btnOk_Click' when a control is double-clicked
    control_double_clicked = pyqtSignal(str)

    def add_button(self, x: float, y: float, w: float = 80, h: float = 30, text: str = "Button", object_id: str = None) -> ButtonItem:
        btn = ButtonItem(x, y, w, h, text, object_id)
        self._scene.addItem(btn)
        return btn

    def add_label(self, x: float, y: float, text: str = "Label", object_id: str = None) -> LabelItem:
        lbl = LabelItem(x, y, text, object_id)
        self._scene.addItem(lbl)
        return lbl

    def add_textbox(self, x: float, y: float, w: float = 120, h: float = 24, text: str = "", object_id: str = None) -> TextBoxItem:
        tb = TextBoxItem(x, y, w, h, text, object_id)
        self._scene.addItem(tb)
        return tb

    def add_picturebox(self, x: float, y: float, w: float = 100, h: float = 80, object_id: str = None) -> PictureBoxItem:
        pb = PictureBoxItem(x, y, w, h, object_id)
        self._scene.addItem(pb)
        return pb

    def on_item_double_clicked(self, item: ButtonItem):
        # Emit a standard handler name {object_id}_Click
        obj_id = getattr(item, 'object_id', None) or getattr(item, 'id', None)
        if obj_id:
            handler_name = f"{obj_id}_Click"
            self.control_double_clicked.emit(handler_name)

    def controls(self):
        return [it for it in self._scene.items() if isinstance(it, ButtonItem)]
