from visualasic.ide.designer_widget import DesignerCanvas
from visualasic.handlers import HandlerManager
from pathlib import Path


def test_double_click_creates_handler(tmp_path, qtbot):
    root = tmp_path / "project"
    root.mkdir()
    hm = HandlerManager(root)

    canvas = DesignerCanvas()
    qtbot.addWidget(canvas)
    canvas.show()

    btn = canvas.add_button(10, 10, text='btnOk')
    btn.object_id = 'btnOk'

    # connect canvas double-click to handler creation
    canvas.control_double_clicked.connect(lambda name: hm.create_handler(name))

    # simulate double click at the button center
    center_scene = btn.mapToScene(btn.boundingRect().center())
    center_view = canvas.mapFromScene(center_scene)
    qtbot.mouseDClick(canvas.viewport(), qtbot.leftClick, pos=center_view)

    p = hm.handler_path('btnOk_Click')
    assert p.exists()
    assert 'Sub btnOk_Click' in p.read_text(encoding='utf-8')
