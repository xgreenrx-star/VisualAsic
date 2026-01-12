from visualasic.ide.designer_widget import DesignerCanvas
from visualasic.ide.property_inspector import PropertyInspector


def test_snap_toggle_and_grid_size(qtbot):
    canvas = DesignerCanvas()
    qtbot.addWidget(canvas)
    canvas.show()

    inspector = PropertyInspector(canvas)
    qtbot.addWidget(inspector)

    # default is snap on, grid 8
    assert canvas.snap_to_grid is True
    assert canvas.grid_size == 8

    # turn snapping off via inspector
    inspector.cb_snap.setCurrentText('Off')
    assert canvas.snap_to_grid is False

    # change grid size
    inspector.spin_grid.setValue(16)
    assert canvas.grid_size == 16

    # turning snap back on
    inspector.cb_snap.setCurrentText('On')
    assert canvas.snap_to_grid is True

    # verify snapping uses new grid size
    tb = canvas.add_textbox(10, 10)
    tb.setPos(5, 5)
    # nearest multiple of 16 for 5 is 0
    assert int(tb.x()) % canvas.grid_size == 0
    assert int(tb.y()) % canvas.grid_size == 0
