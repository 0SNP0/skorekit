"""Regression: cue-source includes do not make a musician a combined-desk member."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build


class PartOrderCueDependencyTests(unittest.TestCase):
    def test_combined_part_ignores_other_instruments_used_only_for_cues(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            def put(name, content):
                file = root / name
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(content, encoding="utf-8")

            put("orchestra.ily", r"""
orchestraScore = <<
  \new Staff { \flutesDeskPrint }
  \new Staff { \clarinetsDeskPrint }
>>
""")
            instruments = {
                "flute-1": "fluteOne",
                "flute-2": "fluteTwo",
                "clarinet-1": "clarinetOne",
                "clarinet-2": "clarinetTwo",
            }
            for filename, symbol in instruments.items():
                put(f"music/{filename}.ily",
                    f"{symbol}Music = {{ c'4 }}\n")
                put(f"parts/{filename}.ly",
                    r"\score { \new Staff { \compressEmptyMeasures "
                    + "\\" + symbol + "Music } \\partPrintLayout }\n")
            put("music/combined/flutes.ily",
                r"fluteOneMusicCombined = { c'4 }" + "\n"
                r"fluteTwoMusicCombined = { d'4 }" + "\n"
                r"flutesDeskPrint = << { \fluteOneMusicCombined } "
                r"{ \fluteTwoMusicCombined } >>")
            put("music/combined/clarinets.ily",
                r"clarinetOneMusicCombined = { c'4 }" + "\n"
                r"clarinetTwoMusicCombined = { d'4 }" + "\n"
                r"clarinetsDeskPrint = << { \clarinetOneMusicCombined } "
                r"{ \clarinetTwoMusicCombined } >>")
            for desk, sources in (
                ("flutes", ("flute-1", "flute-2", "clarinet-1")),
                ("clarinets", ("clarinet-1", "clarinet-2")),
            ):
                combined = "\n".join(
                    f'\\include "../../music/{name}.ily"'
                    for name in sources)
                combined += (f'\n\\include "../../music/combined/{desk}.ily"\n'
                             r"\score { \new Staff { \compressEmptyMeasures "
                             + "\\" + desk + "DeskPrint } \\partPrintLayout }\n")
                put(f"parts/combined/{desk}-1-2.ly", combined)

            build.part_order.cache_clear()
            try:
                with patch.object(build, "ROOT", root):
                    result = build.part_order()
            finally:
                build.part_order.cache_clear()
            self.assertEqual(result, [
                "combined/flutes-1-2", "flute-1", "flute-2",
                "combined/clarinets-1-2", "clarinet-1", "clarinet-2",
            ])


if __name__ == "__main__":
    unittest.main()
