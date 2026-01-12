from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QSpinBox, QLabel, QPushButton, QComboBox
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor, QBrush

class PropertyInspector(QWidget):
    # signal emitted when user requests to open/create an event handler
    open_handler = pyqtSignal(str)  # handler name

    def __init__(self, canvas, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.id_label = QLabel("")
        self.txt_text = QLineEdit()
        self.spin_x = QSpinBox()
        self.spin_y = QSpinBox()
        self.spin_w = QSpinBox()
        self.spin_h = QSpinBox()
        self.txt_color = QLineEdit()
        self.events = QComboBox()
        self.open_button = QPushButton("Open/Create Handler")

        self.layout.addRow("ID", self.id_label)
        self.layout.addRow("Text", self.txt_text)
        self.layout.addRow("X", self.spin_x)
        self.layout.addRow("Y", self.spin_y)
        self.layout.addRow("W", self.spin_w)
        self.layout.addRow("H", self.spin_h)
        self.layout.addRow("Color", self.txt_color)
        self.layout.addRow("Events", self.events)
        self.layout.addRow(self.open_button)

        # limits
        self.spin_x.setRange(-10000, 10000)
        self.spin_y.setRange(-10000, 10000)
        self.spin_w.setRange(1, 10000)
        self.spin_h.setRange(1, 10000)

        # hooks
        self.canvas.scene.selectionChanged.connect(self._on_selection_changed)
        self.txt_text.editingFinished.connect(self._apply_text)
        self.spin_x.valueChanged.connect(self._apply_geometry)
        self.spin_y.valueChanged.connect(self._apply_geometry)
        self.spin_w.valueChanged.connect(self._apply_geometry)
        self.spin_h.valueChanged.connect(self._apply_geometry)
        self.txt_color.editingFinished.connect(self._apply_color)
        self.open_button.clicked.connect(self._open_event_handler)

    def _on_selection_changed(self):
        items = [it for it in self.canvas.scene.items() if it.isSelected()]
        if not items:
            self._clear()
            return
        item = items[0]
        # populate
        self.id_label.setText(getattr(item, 'object_id', ''))
        # text
        text = ''
        for ch in item.childItems():
            if hasattr(ch, 'toPlainText'):
                text = ch.toPlainText()
                break
        self.txt_text.setText(text)
        # geometry
        self.spin_x.setValue(int(item.x()))
        self.spin_y.setValue(int(item.y()))
        self.spin_w.setValue(int(item.rect().width()))
        self.spin_h.setValue(int(item.rect().height()))
        # color
        brush = getattr(item, 'brush', None)
        self.txt_color.setText(getattr(item, '_color', ''))
        # events
        self._populate_events_for(item)

    def _populate_events_for(self, item):
        self.events.clear()
        # Basic events based on type
        if type(item).__name__ == 'ButtonItem':
            self.events.addItem('Click')
            self.events.addItem('Right_Click')
            self.events.addItem('Double_Click')
        elif type(item).__name__ == 'TextBoxItem':
            self.events.addItem('OnEnter')
            self.events.addItem('Change')
        else:
            self.events.addItem('Click')

    def _apply_text(self):
        items = [it for it in self.canvas.scene.items() if it.isSelected()]
        if not items:
            return
        item = items[0]
        for ch in item.childItems():
            if hasattr(ch, 'setPlainText'):
                ch.setPlainText(self.txt_text.text())
                break

    def _apply_geometry(self):
        items = [it for it in self.canvas.scene.items() if it.isSelected()]
        if not items:
            return
        item = items[0]
        x = self.spin_x.value()
        y = self.spin_y.value()
        w = self.spin_w.value()
        h = self.spin_h.value()
        item.setRect(0, 0, w, h)
        item.setPos(x, y)

    def _apply_color(self):
        items = [it for it in self.canvas.scene.items() if it.isSelected()]
        if not items:
            return
        item = items[0]
        c = self.txt_color.text()
        try:
            item.setBrush(QBrush(QColor(c)))
            item._color = c
        except Exception:
            pass

    def _open_event_handler(self):
        # Signal the requested handler name for the selected item and selected event
        items = [it for it in self.canvas.scene.items() if it.isSelected()]
        if not items:
            return
        item = items[0]
        control_id = getattr(item, 'object_id', '') or getattr(item, 'id', '')
        event = self.events.currentText()
        handler_name = f"{control_id}_{event}"
        self.open_handler.emit(handler_name)

    def _clear(self):
        self.id_label.setText("")
        self.txt_text.setText("")
        self.spin_x.setValue(0)
        self.spin_y.setValue(0)
        self.spin_w.setValue(0)
        self.spin_h.setValue(0)
        self.txt_color.setText("")
        self.events.clear()
