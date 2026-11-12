from io import BytesIO

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context, RequestParameters
from thumbor.engines.pil import Engine
from thumbor.transformer import Transformer


def make_opaque_square_png():
    img = Image.new("RGBA", (16, 16), (255, 0, 0, 255))
    buffer = BytesIO()
    img.save(buffer, "PNG")
    return buffer.getvalue()


def test_resize_to_wide_strip_keeps_picture():
    config = Config()
    context = Context(config=config)
    engine = Engine(context)
    engine.load(make_opaque_square_png(), ".png")
    context.request = RequestParameters(width=800, height=20)
    context.request.engine = engine

    Transformer(context).img_operation_worker()

    out = Image.open(BytesIO(engine.read(".png"))).convert("RGBA")
    assert out.size == (800, 20)
    # The source is opaque red, so the strip must be opaque red too.
    assert out.getpixel((400, 10)) == (255, 0, 0, 255)
