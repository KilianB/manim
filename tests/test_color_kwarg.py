import unittest

from manimlib.constants import BLUE, DEFAULT_LIGHT_COLOR, DEFAULT_MOBJECT_COLOR
from manimlib.constants import GREEN, GREY_B, GREY_D, LEFT, ORIGIN, RED, RIGHT
from manimlib.mobject.geometry import (
    AnnularSector,
    Annulus,
    Arrow,
    ArrowTip,
    Circle,
    Dot,
    SmallDot,
    Square,
    StrokeArrow,
)
from manimlib.mobject.probability import SampleSpace
from manimlib.mobject.shape_matchers import Cross


# Each class paired with the color channel that `color=` must reach.
# These all used to hard-code a default for that channel, which the
# VMobject constructor took as explicit and so silently ignored `color`.
CASES = [
    ("Circle", lambda **kw: Circle(**kw), "stroke"),
    ("Dot", lambda **kw: Dot(**kw), "fill"),
    ("SmallDot", lambda **kw: SmallDot(**kw), "fill"),
    ("AnnularSector", lambda **kw: AnnularSector(**kw), "fill"),
    ("Annulus", lambda **kw: Annulus(**kw), "fill"),
    ("StrokeArrow", lambda **kw: StrokeArrow(LEFT, RIGHT, **kw), "stroke"),
    ("Arrow", lambda **kw: Arrow(LEFT, RIGHT, **kw), "fill"),
    ("ArrowTip", lambda **kw: ArrowTip(**kw), "fill"),
    ("SampleSpace", lambda **kw: SampleSpace(**kw), "fill"),
    ("Cross", lambda **kw: Cross(Square(), **kw), "stroke"),
]


def get_channel(mob, channel):
    return mob.get_stroke_color() if channel == "stroke" else mob.get_fill_color()


class ColorKwargTest(unittest.TestCase):
    def test_color_kwarg_is_applied(self):
        for name, make, channel in CASES:
            with self.subTest(name):
                self.assertEqual(get_channel(make(color=BLUE), channel), BLUE)

    def test_explicit_channel_color_beats_color(self):
        for name, make, channel in CASES:
            with self.subTest(name):
                mob = make(color=BLUE, **{f"{channel}_color": GREEN})
                self.assertEqual(get_channel(mob, channel), GREEN)

    def test_defaults_unchanged(self):
        self.assertEqual(Circle().get_stroke_color(), RED)
        self.assertEqual(Dot().get_fill_color(), DEFAULT_MOBJECT_COLOR)
        self.assertEqual(Arrow(LEFT, RIGHT).get_fill_color(), DEFAULT_LIGHT_COLOR)
        self.assertEqual(SampleSpace().get_fill_color(), GREY_D)
        self.assertEqual(SampleSpace().get_stroke_color(), GREY_B)
        self.assertEqual(Cross(Square()).get_stroke_color(), RED)

    def test_positional_args_keep_their_meaning(self):
        # The new `color` parameter must not shift existing positional slots
        self.assertEqual(Dot(ORIGIN, 0.1, BLUE).get_stroke_color(), BLUE)
        self.assertEqual(Circle(0, GREEN).get_stroke_color(), GREEN)


if __name__ == "__main__":
    unittest.main()
