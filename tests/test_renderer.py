"""Offline buffer checks using literal expected codes and pixel locations."""

from dataclasses import FrozenInstanceError
import unittest

from tv_autocal.renderer import RGBFrame, pattern_manifest, render_patch, render_pattern


class RendererTests(unittest.TestCase):
    def test_native_patch_has_exact_geometry_and_unmodified_channel_order(self):
        frame = render_patch((16, 128, 235))
        self.assertEqual((frame.width, frame.height, len(frame.pixels)),
                         (3840, 2160, 24883200))
        black_row = b"\0" * 11520
        patch_row = b"\0" * 4320 + b"\x10\x80\xeb" * 960 + b"\0" * 4320
        # Check every row, including every surround pixel, against independent
        # literal boundaries rather than the renderer's rectangle metadata.
        for y in range(2160):
            expected = patch_row if 810 <= y < 1350 else black_row
            self.assertEqual(frame.pixels[y * 11520 : (y + 1) * 11520], expected)
        self.assertEqual(frame.pixel(1440, 810), (16, 128, 235))
        self.assertEqual(frame.pixel(2399, 1349), (16, 128, 235))
        self.assertEqual(frame.pixel(2400, 1350), (0, 0, 0))

    def test_patch_zero_and_white_are_not_limited_range_encoded(self):
        black = render_patch((0, 0, 0))
        self.assertEqual(black.pixels, b"\0" * 24883200)
        white = render_patch((255, 255, 255))
        self.assertEqual(white.pixel(1920, 1080), (255, 255, 255))
        self.assertEqual(white.pixel(0, 0), (0, 0, 0))

    def test_bad_rgb_is_rejected_without_coercion(self):
        for rgb in ([1, 2, 3], b"\1\2\3", (1, 2), "red", None):
            with self.subTest(rgb=rgb), self.assertRaises(TypeError):
                render_patch(rgb)
        for rgb in ((True, 0, 0), (0, 1.0, 0), (-1, 0, 0), (256, 0, 0)):
            with self.subTest(rgb=rgb), self.assertRaises(ValueError):
                render_patch(rgb)

    def test_frame_is_immutable_and_pixel_addresses_are_strict(self):
        frame = RGBFrame(2, 2, b"\1\2\3\4\5\6\7\10\11\12\13\14")
        self.assertEqual(frame.pixel(1, 0), (4, 5, 6))
        self.assertEqual(frame.pixel(0, 1), (7, 8, 9))
        with self.assertRaises(FrozenInstanceError):
            frame.width = 8
        with self.assertRaises(TypeError):
            frame.pixels[0] = 7
        for x, y in ((-1, 0), (2, 0), (0, 2), (True, 0), (0, 0.0)):
            with self.subTest(x=x, y=y), self.assertRaises(ValueError):
                frame.pixel(x, y)

    def test_frame_rejects_malformed_sizes_and_mutable_buffers(self):
        for width, height in ((0, 1), (1, -1), (3841, 1), (1, 2161), (True, 1), (1, 1.0)):
            with self.subTest(width=width, height=height), self.assertRaises(ValueError):
                RGBFrame(width, height, b"")
        with self.assertRaises(ValueError):
            RGBFrame(1, 1, b"\0\0")
        with self.assertRaises(TypeError):
            RGBFrame(1, 1, bytearray(3))

    def test_manifest_is_stable_immutable_and_labels_are_separate(self):
        manifest = pattern_manifest()
        self.assertEqual(tuple(item.name for item in manifest),
                         ("geometry", "black", "white", "red", "green", "blue", "detail"))
        with self.assertRaises(FrozenInstanceError):
            manifest[0].name = "changed"
        self.assertEqual(manifest[1].colours, tuple((n, n, n) for n in (0, 4, 8, 12, 16, 24, 32, 51)))
        for spec in manifest[1:]:
            for label in spec.labels:
                self.assertEqual(label.y, 1750)
                self.assertGreater(label.y, max(r.y + r.height for r in spec.regions))

    def test_geometry_has_one_pixel_border_and_four_corner_labels(self):
        frame = render_pattern("geometry")
        self.assertEqual(frame.pixels[:11520], b"\xff" * 11520)
        self.assertEqual(frame.pixels[-11520:], b"\xff" * 11520)
        for y in range(1, 2159):
            self.assertEqual(frame.pixel(0, y), (255, 255, 255))
            self.assertEqual(frame.pixel(3839, y), (255, 255, 255))
        for point in ((1, 1), (3838, 2158), (1920, 1080), (1, 1080), (3838, 1080)):
            self.assertEqual(frame.pixel(*point), (0, 0, 0))
        self.assertEqual(tuple(label.text for label in pattern_manifest()[0].labels),
                         ("TL", "TR", "BL", "BR"))
        # Top stroke of each T/B is white; a gap between each pair stays black.
        for x, y in ((16, 16), (3780, 16), (16, 2116), (3780, 2116)):
            self.assertEqual(frame.pixel(x, y), (255, 255, 255))
            self.assertEqual(frame.pixel(x + 20, y), (0, 0, 0))

    def test_black_bars_have_literal_levels_gaps_and_limits(self):
        frame = render_pattern("black")
        for index, value in enumerate((0, 4, 8, 12, 16, 24, 32, 51)):
            x = 320 + index * 400
            self.assertEqual(frame.pixel(x, 540), (value,) * 3)
            self.assertEqual(frame.pixel(x + 367, 1619), (value,) * 3)
            self.assertEqual(frame.pixel(x + 368, 1000), (0, 0, 0))
            self.assertEqual(frame.pixel(x, 539), (0, 0, 0))
            self.assertEqual(frame.pixel(x, 1620), (0, 0, 0))

    def test_white_and_primary_bars_keep_exact_byte_values(self):
        frame = render_pattern("white")
        for index, value in enumerate((204, 230, 242, 250, 255)):
            self.assertEqual(frame.pixel(320 + index * 640, 1000), (value,) * 3)
        for name, expected in (
            ("red", ((204, 0, 0), (230, 0, 0), (242, 0, 0), (255, 0, 0))),
            ("green", ((0, 204, 0), (0, 230, 0), (0, 242, 0), (0, 255, 0))),
            ("blue", ((0, 0, 204), (0, 0, 230), (0, 0, 242), (0, 0, 255))),
        ):
            frame = render_pattern(name)
            for index, colour in enumerate(expected):
                self.assertEqual(frame.pixel(320 + index * 800, 1000), colour)
                self.assertEqual(frame.pixel(1088 + index * 800, 1000), (0, 0, 0))

    def test_detail_stripes_are_single_pixels_and_text_is_unfiltered(self):
        frame = render_pattern("detail")
        row_start = 540 * 11520
        self.assertEqual(frame.pixels[row_start + 960 : row_start + 5568],
                         b"\xff\0\0\0\0\xff" * 768)
        self.assertEqual(frame.pixels[row_start + 5952 : row_start + 10560],
                         b"\0\0\0\xff\xff\xff" * 768)
        self.assertEqual(frame.pixel(1856, 1000), (0, 0, 0))
        self.assertEqual(frame.pixel(1983, 1000), (0, 0, 0))
        # R's first glyph row is four white pixels, one black, then spacing.
        self.assertEqual(tuple(frame.pixel(x, 1750) for x in range(320, 326)),
                         ((255, 255, 255),) * 4 + ((0, 0, 0),) * 2)

    def test_rendering_is_repeatable_and_unknown_names_fail(self):
        self.assertEqual(render_patch((13, 26, 51)), render_patch((13, 26, 51)))
        self.assertEqual(render_pattern("detail"), render_pattern("detail"))
        for name in ("", "BLACK", "display", "../../other"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                render_pattern(name)
        for name in (None, 1, b"black"):
            with self.subTest(name=name), self.assertRaises(TypeError):
                render_pattern(name)


if __name__ == "__main__":
    unittest.main()
