from visualasic.ide.designer_widget import DesignerCanvas
from visualasic.ide.property_inspector import PropertyInspector
from PyQt6.QtCore import Qt


def test_property_updates_control(qtbot):
    canvas = DesignerCanvas()
    qtbot.addWidget(canvas)
    canvas.show()

    btn = canvas.add_button(10, 10, w=80, h=30, text="btnOk")
    btn.object_id = "btnOk"

    inspector = PropertyInspector(canvas)
    qtbot.addWidget(inspector)

    # select the button in the scene
    btn.setSelected(True)
    # signal loop to update inspector
    canvas.scene.selectionChanged.emit()

    # ensure inspector shows text
    assert inspector.txt_text.text() == 'btnOk'

    # change text via inspector and trigger editingFinished
    inspector.txt_text.setText('NewText')
    inspector.txt_text.editingFinished.emit()

    # verify the button text changed
    assert any(ch.toPlainText() == 'NewText' for ch in btn.childItems())

    # change geometry
    inspector.spin_x.setValue(50)
    inspector.spin_y.setValue(40)

    # verify position applied
    assert int(btn.x()) == 50
    assert int(btn.y()) == 40

    # change color
    inspector.txt_color.setText('#FF0000')
    inspector.txt_color.editingFinished.emit()
    assert getattr(btn, '_color', '') == '#FF0000'
