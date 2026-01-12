from pathlib import Path
from visualasic.handlers import HandlerManager

def test_create_handler(tmp_path):
    root = tmp_path / "project"
    root.mkdir()
    hm = HandlerManager(root)
    p = hm.create_handler("btnOk_Click")
    assert p.exists()
    contents = p.read_text(encoding="utf-8")
    assert "Sub btnOk_Click" in contents


def test_inspector_opens_handler(tmp_path, qtbot):
    # Setup project root
    root = tmp_path / "project"
    root.mkdir()
    hm = HandlerManager(root)

    # Canvas + inspector
    from visualasic.ide.designer_widget import DesignerCanvas
    from visualasic.ide.property_inspector import PropertyInspector

    canvas = DesignerCanvas()
    inspector = PropertyInspector(canvas)

    btn = canvas.add_button(10,10, text='btnOk')
    btn.object_id = 'btnOk'

    qtbot.addWidget(canvas)
    qtbot.addWidget(inspector)

    # Select and refresh inspector
    btn.setSelected(True)
    canvas.scene.selectionChanged.emit()

    # Choose event and click open
    inspector.events.setCurrentText('Click')

    # wire inspector to handler manager
    inspector.open_handler.connect(lambda name: hm.create_handler(name))
    inspector.open_button.click()

    p = hm.handler_path('btnOk_Click')
    assert p.exists()
    assert 'Sub btnOk_Click' in p.read_text(encoding='utf-8')
