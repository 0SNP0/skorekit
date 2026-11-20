"""Regression coverage for multi-staff SVG measure hit regions."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from export import (_svg_measure_regions, _svg_measure_systems,
                    annotate_measure_spans, coalesce_svg_measure_regions)


def staff(top):
    return (top, top + 4, 10.0, 90.0)


class MultiStaffRegionsTests(unittest.TestCase):
    def test_two_staff_part_highlights_both_staves(self):
        staves = [staff(10), staff(20), staff(40), staff(50)]
        labels = [(1, 10, 10), (2, 50, 10),
                  (3, 10, 40), (4, 50, 40)]
        bars = [(x, y) for y in (10, 20, 40, 50) for x in (10, 50, 90)]
        systems = _svg_measure_systems(staves, labels, "individual")
        self.assertEqual(len(systems), 2)
        self.assertEqual((systems[0][0][0], systems[0][0][1]), (10, 24))
        self.assertEqual((systems[1][0][0], systems[1][0][1]), (40, 54))
        regions, carry = _svg_measure_regions(
            staves, bars, labels, "individual", 1)
        self.assertIsNone(carry)
        self.assertEqual([r["measure_id"] for r in regions],
                         [f"measure-{n:04d}" for n in (1, 2, 3, 4)])
        self.assertEqual([(r["y"], r["height"]) for r in regions],
                         [(9.6, 14.8), (9.6, 14.8),
                          (39.6, 14.8), (39.6, 14.8)])

    def test_duplicate_labels_on_both_staves_are_one_measure(self):
        staves = [staff(10), staff(20)]
        labels = [(1, 10, 10), (2, 50, 10),
                  (1, 10, 20), (2, 50, 20)]
        bars = [(x, y) for y in (10, 20) for x in (10, 50, 90)]
        regions, carry = _svg_measure_regions(
            staves, bars, labels, "individual", 1)
        self.assertIsNone(carry)
        merged = coalesce_svg_measure_regions(regions)
        annotate_measure_spans(merged, 2)
        self.assertEqual(len(merged), 2)
        self.assertTrue(all(r["height"] == 14.8 for r in merged))

    def test_next_page_carries_number_into_entire_two_staff_system(self):
        staves = [staff(10), staff(20)]
        bars = [(x, y) for y in (10, 20) for x in (10, 50, 90)]
        regions, carry = _svg_measure_regions(
            staves, bars, [(2, 90, 10)], "individual", 1)
        self.assertEqual(regions, [])
        self.assertEqual(carry, 2)
        regions, carry = _svg_measure_regions(
            staves, bars, [(3, 50, 10)], "individual", 2, carry)
        self.assertIsNone(carry)
        self.assertEqual([r["measure_id"] for r in regions],
                         ["measure-0002", "measure-0003"])
        self.assertTrue(all(r["y"] == 9.6 and r["height"] == 14.8
                            for r in regions))

    def test_score_geometry_is_unchanged(self):
        systems = _svg_measure_systems(
            [staff(10), staff(20), staff(40)],
            [(1, 10, 10)], "score")
        self.assertEqual(systems, [((10, 44, 10.0, 90.0), [(1, 10, 10)])])


if __name__ == "__main__":
    unittest.main()
