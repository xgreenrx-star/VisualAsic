from visualasic.ide.designer_widget import DesignerCanvas
from PyQt6.QtCore import QPoint


def test_add_button_and_drag(qtbot):
    canvas = DesignerCanvas()
    qtbot.addWidget(canvas)
    canvas.show()

    btn = canvas.add_button(10, 10, w=80, h=30, text="btnOk")
    # initial position
    x0, y0 = btn.x(), btn.y()
    assert (x0, y0) == (10, 10)

    # Map the center of the button to widget coords
    center_scene = btn.mapToScene(btn.boundingRect().center())
    center_view = canvas.mapFromScene(center_scene)

    # Simulate press and drag
    qtbot.mousePress(canvas.viewport(), Qt.MouseButton.LeftButton, pos=center_view)
    # drag to offset +40,+30
    new_view_pos = center_view + QPoint(40, 30)
    qtbot.mouseMove(canvas.viewport(), pos=new_view_pos)
    qtbot.mouseRelease(canvas.viewport(), Qt.MouseButton.LeftButton, pos=new_view_pos)

    # After move the item position should have changed
    x1, y1 = btn.x(), btn.y()
    assert (x1, y1) != (x0, y0)
    # Rough check for expected movement (allowing for scene/view coordinate differences)
    assert abs(x1 - x0) >= 30
    assert abs(y1 - y0) >= 20
