from thumbor.ext.filters import _round_corner


def test_transparent_round_corner_edge_is_not_darkened_when_opaque():
    width, height = 60, 60
    buffer = bytes([255] * (width * height * 4))

    result = _round_corner.apply(
        1, "RGBA", 20, 20, 255, 255, 255, width, height, buffer, 1
    )

    pixels = bytearray(result)
    dark_opaque = []
    for i in range(0, len(pixels), 4):
        r, g, b, a = pixels[i : i + 4]
        if a == 255 and (r, g, b) != (255, 255, 255):
            dark_opaque.append((i // 4, (r, g, b, a)))

    assert dark_opaque == [], (
        "edge pixels stayed opaque and were darkened: "
        f"{len(dark_opaque)} found, e.g. {dark_opaque[:3]}"
    )
