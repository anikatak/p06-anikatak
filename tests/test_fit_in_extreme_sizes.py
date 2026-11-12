from io import BytesIO

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context, RequestParameters
from thumbor.engines.pil import Engine
from thumbor.transformer import Transformer


def make_wide_png():
    img = Image.new("RGBA", (940, 2), (255, 0, 0, 255))
    buffer = BytesIO()
    img.save(buffer, "PNG")
    return buffer.getvalue()


def run_fit_in(width, height):
    config = Config()
    context = Context(config=config)
    engine = Engine(context)
    engine.load(make_wide_png(), ".png")
    context.request = RequestParameters(width=width, height=height)
    context.request.fit_in = True
    context.request.engine = engine

    Transformer(context).img_operation_worker()

    return Image.open(BytesIO(engine.read(".png"))).convert("RGBA")


def test_fit_in_1x1_returns_1x1_image():
    out = run_fit_in(1, 1)
    assert out.size == (1, 1)


def test_fit_in_width_only_100x0_returns_100x1_image():
    out = run_fit_in(100, 0)
    assert out.size == (100, 1)
