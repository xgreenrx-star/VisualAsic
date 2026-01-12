from visualasic.ide.designer_widget import DesignerCanvas
from visualasic.handlers import HandlerManager
from pathlib import Path


def test_picturebox_load_image(tmp_path, qtbot):
    canvas = DesignerCanvas()
    qtbot.addWidget(canvas)
    canvas.show()

    pb = canvas.add_picturebox(0,0,50,50,object_id='pic1')
    # create a tiny PNG
    img = tmp_path / 'img.png'
    from PIL import Image
    im = Image.new('RGBA', (10, 10), color=(255,0,0,255))
    im.save(img)

    pb.load_image(str(img))
    assert pb.image_path() == str(img)
    # pixmap child exists
    assert any(type(ch).__name__ == 'QGraphicsPixmapItem' for ch in pb.childItems())


def test_textbox_set_text_and_trigger(qtbot):
    canvas = DesignerCanvas()
    qtbot.addWidget(canvas)
    tb = canvas.add_textbox(0,0, object_id='txt1')

    events = []
    canvas.control_event.connect(lambda cid, ev: events.append((cid, ev)))

    tb.set_text('hello')
    tb.trigger_on_enter()

    assert events == [('txt1', 'OnEnter')]
