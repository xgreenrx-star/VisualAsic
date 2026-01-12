from visualasic.ide.designer_widget import DesignerCanvas
from PyQt6.QtCore import Qt


def test_add_various_controls_and_snapping(qtbot):
    canvas = DesignerCanvas()
    qtbot.addWidget(canvas)
    canvas.show()

    # Add controls
    btn = canvas.add_button(13, 17, text='btn1', object_id='btn1')
    lbl = canvas.add_label(5, 7, text='lbl1', object_id='lbl1')
    tb = canvas.add_textbox(29, 44, text='')
    pb = canvas.add_picturebox(51, 73)

    # Check they are present
    items = canvas._scene.items()
    assert any(getattr(it, 'object_id', '') == 'btn1' for it in items)
    assert any(getattr(it, 'object_id', '') == 'lbl1' for it in items)

    # Snap behavior: move tb to a non-grid position then drag to trigger item change
    # grid size default is 8; snapping rounds to nearest grid multiple
    tb.setPos(29, 44)
    # after setting pos, itemChange should snap
    assert int(tb.x()) % canvas.grid_size == 0
    assert int(tb.y()) % canvas.grid_size == 0
    assert int(tb.x()) == round(29 / canvas.grid_size) * canvas.grid_size
    assert int(tb.y()) == round(44 / canvas.grid_size) * canvas.grid_size

    # Check grid visibility
    assert canvas.show_grid is True
    assert canvas.grid_size > 0
