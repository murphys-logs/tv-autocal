"""Deterministic off-screen RGB8 buffers for the proposed diagnostic patterns.

Nothing here opens a window, enumerates displays, saves an image or contacts a
device. Codes describe application bytes, never demonstrated HDMI values or
light from a TV. A separately reviewed physical presenter is still required.
"""

from dataclasses import dataclass


WIDTH = 3840
HEIGHT = 2160
MAX_FRAME_BYTES = WIDTH * HEIGHT * 3
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
T003_RANGE_CODES = (255, 51, 26, 13, 5, 0)
T005_NEUTRAL_CODES = (0, 13, 26, 51, 102, 153, 204, 230, 242, 255)
T005_PRIMARY_CODES = (204, 230, 242, 255)


def _integer(value: int, minimum: int, maximum: int, name: str) -> None:
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(name + " must be an integer in the permitted range")


def _rgb(rgb: tuple[int, int, int]) -> None:
    if type(rgb) is not tuple or len(rgb) != 3:
        raise TypeError("RGB must be a tuple of three integer byte values")
    for value in rgb:
        _integer(value, 0, 255, "RGB component")


@dataclass(frozen=True)
class RGBFrame:
    """Immutable RGB bytes, top-left origin, row-major and no row padding."""

    width: int
    height: int
    pixels: bytes

    def __post_init__(self) -> None:
        _integer(self.width, 1, WIDTH, "Width")
        _integer(self.height, 1, HEIGHT, "Height")
        if type(self.pixels) is not bytes:
            raise TypeError("Frame pixels must be immutable bytes")
        if len(self.pixels) != self.width * self.height * 3:
            raise ValueError("RGB byte count does not match frame dimensions")

    def pixel(self, x: int, y: int) -> tuple[int, int, int]:
        _integer(x, 0, self.width - 1, "x")
        _integer(y, 0, self.height - 1, "y")
        offset = (y * self.width + x) * 3
        return tuple(self.pixels[offset : offset + 3])


@dataclass(frozen=True)
class Rectangle:
    """Integer pixel rectangle; the right and bottom edges are exclusive."""

    x: int
    y: int
    width: int
    height: int


@dataclass(frozen=True)
class Label:
    text: str
    x: int
    y: int
    scale: int = 1


@dataclass(frozen=True)
class PatternSpec:
    """Machine-readable definition; all coordinates refer to the native buffer."""

    name: str
    kind: str
    colours: tuple[tuple[int, int, int], ...]
    regions: tuple[Rectangle, ...]
    labels: tuple[Label, ...]


PATCH_RECTANGLE = Rectangle(1440, 810, 960, 540)

# Original, deliberately small 5x7 bitmap alphabet. Each set bit is one square
# pixel at scale=1; larger labels use exact integer replication, no smoothing.
_GLYPHS = {
    "0": (14, 17, 19, 21, 25, 17, 14),
    "1": (4, 12, 4, 4, 4, 4, 14),
    "2": (14, 17, 1, 2, 4, 8, 31),
    "3": (30, 1, 1, 14, 1, 1, 30),
    "4": (2, 6, 10, 18, 31, 2, 2),
    "5": (31, 16, 16, 30, 1, 1, 30),
    "6": (14, 16, 16, 30, 17, 17, 14),
    "7": (31, 1, 2, 4, 8, 8, 8),
    "8": (14, 17, 17, 14, 17, 17, 14),
    "9": (14, 17, 17, 15, 1, 1, 14),
    "B": (30, 17, 17, 30, 17, 17, 30),
    "G": (14, 17, 16, 23, 17, 17, 14),
    "L": (16, 16, 16, 16, 16, 16, 31),
    "R": (30, 17, 17, 30, 20, 18, 17),
    "T": (31, 4, 4, 4, 4, 4, 4),
    "W": (17, 17, 17, 21, 21, 21, 10),
    " ": (0, 0, 0, 0, 0, 0, 0),
}


def _bar_spec(name: str, codes: tuple[int, ...], channel: int | None) -> PatternSpec:
    colours = tuple(
        (code, code, code) if channel is None
        else tuple(code if index == channel else 0 for index in range(3))
        for code in codes
    )
    slot = 3200 // len(codes)
    regions = tuple(Rectangle(320 + index * slot, 540, slot - 32, 1080)
                    for index in range(len(codes)))
    labels = tuple(Label(str(code), region.x, 1750, 4)
                   for code, region in zip(codes, regions))
    return PatternSpec(name, "bars", colours, regions, labels)


_MANIFEST = (
    PatternSpec("geometry", "geometry", (WHITE,),
                (Rectangle(0, 0, WIDTH, 1), Rectangle(0, HEIGHT - 1, WIDTH, 1),
                 Rectangle(0, 1, 1, HEIGHT - 2), Rectangle(WIDTH - 1, 1, 1, HEIGHT - 2)),
                (Label("TL", 16, 16, 4), Label("TR", WIDTH - 60, 16, 4),
                 Label("BL", 16, HEIGHT - 44, 4), Label("BR", WIDTH - 60, HEIGHT - 44, 4))),
    _bar_spec("black", (0, 4, 8, 12, 16, 24, 32, 51), None),
    _bar_spec("white", (204, 230, 242, 250, 255), None),
    _bar_spec("red", T005_PRIMARY_CODES, 0),
    _bar_spec("green", T005_PRIMARY_CODES, 1),
    _bar_spec("blue", T005_PRIMARY_CODES, 2),
    PatternSpec("detail", "stripes", ((255, 0, 0), (0, 0, 255), BLACK, WHITE),
                (Rectangle(320, 540, 1536, 1080), Rectangle(1984, 540, 1536, 1080)),
                (Label("RGBW 0123456789", 320, 1750),)),
)


def pattern_manifest() -> tuple[PatternSpec, ...]:
    """Seven visual patterns, in T-005 order, with immutable native geometry.

    Labels belong only to visual patterns. Measurement patches are created by
    render_patch and contain no labels. The tuple is data, not a timed playlist.
    """
    return _MANIFEST


def _rectangle(buffer: bytearray, rectangle: Rectangle, rgb: tuple[int, int, int]) -> None:
    row = bytes(rgb) * rectangle.width
    stride = WIDTH * 3
    for y in range(rectangle.y, rectangle.y + rectangle.height):
        start = y * stride + rectangle.x * 3
        buffer[start : start + len(row)] = row


def _label(buffer: bytearray, label: Label) -> None:
    for index, character in enumerate(label.text):
        for y, bits in enumerate(_GLYPHS[character]):
            for x in range(5):
                if bits & (1 << (4 - x)):
                    _rectangle(buffer, Rectangle(label.x + (index * 6 + x) * label.scale,
                                                  label.y + y * label.scale,
                                                  label.scale, label.scale), WHITE)


def render_patch(rgb: tuple[int, int, int]) -> RGBFrame:
    """One centred 960x540 patch on black, without text or transformations."""
    _rgb(rgb)
    buffer = bytearray(MAX_FRAME_BYTES)
    _rectangle(buffer, PATCH_RECTANGLE, rgb)
    return RGBFrame(WIDTH, HEIGHT, bytes(buffer))


def render_pattern(name: str) -> RGBFrame:
    """Render one named visual pattern off-screen; never advances itself."""
    if type(name) is not str:
        raise TypeError("Pattern name must be a string")
    spec = next((item for item in _MANIFEST if item.name == name), None)
    if spec is None:
        raise ValueError("Unknown visual pattern")
    buffer = bytearray(MAX_FRAME_BYTES)
    if spec.kind == "geometry":
        for region in spec.regions:
            _rectangle(buffer, region, WHITE)
    elif spec.kind == "bars":
        for region, colour in zip(spec.regions, spec.colours):
            _rectangle(buffer, region, colour)
    else:
        for region, first, second in (
            (spec.regions[0], spec.colours[0], spec.colours[1]),
            (spec.regions[1], spec.colours[2], spec.colours[3]),
        ):
            row = (bytes(first) + bytes(second)) * (region.width // 2)
            for y in range(region.y, region.y + region.height):
                start = (y * WIDTH + region.x) * 3
                buffer[start : start + len(row)] = row
    for label in spec.labels:
        _label(buffer, label)
    return RGBFrame(WIDTH, HEIGHT, bytes(buffer))
