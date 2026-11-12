from io import BytesIO

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine


def make_transparent_palette_gif():
    # Palette GIF: index 0 is the transparent background, index 1 is blue.
    img = Image.new("P", (40, 40), 0)
    img.putpalette([0, 0, 0, 0, 0, 255] + [0, 0, 0] * 254)
    for x in range(10, 30):
        for y in range(10, 30):
            img.putpixel((x, y), 1)
    buffer = BytesIO()
    img.save(buffer, "GIF", transparency=0)
    return buffer.getvalue()


def test_resized_palette_gif_keeps_transparent_background():
    config = Config(PILLOW_PRESERVE_INDEXED_MODE=True)
    context = Context(config=config)
    engine = Engine(context)
    engine.load(make_transparent_palette_gif(), ".gif")
    engine.resize(80, 80)

    result = engine.read(".gif")
    out = Image.open(BytesIO(result)).convert("RGBA")

    # The corner was transparent in the source and must stay transparent.
    assert out.getpixel((0, 0))[3] == 0
    # The blue disc in the middle must stay opaque.
    assert out.getpixel((40, 40))[3] == 255
