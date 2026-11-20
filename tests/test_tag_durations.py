"""Generic regression: final tag filters must preserve each voice's own time.

A simultaneous global spacer staff or a successful PDF compile cannot
establish whether an individual instrument lost its tagged silent measures.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scorekit" / "scripts"))
from export import midi_events  # noqa: E402

SOURCE = r'''
\version "2.26.0"
music = {
  \time 3/4
  c'4 r4 r4 |
  \tag #'(solo written concert playback) { R2.*3 | }
  \tag #'combined { R2. | R2.*2 | }
  \barNumberCheck #5
  d'4 r4 r4 |
}
\score {
  \new Staff \with { midiInstrument = "trombone" } {
    \keepWithTag #'(__VIEW__) { \tag #'__VIEW__ { \music } }
  }
  \midi { }
}
'''


@unittest.skipUnless(shutil.which("lilypond"), "LilyPond unavailable")
class TagDurationTests(unittest.TestCase):
    def test_all_final_views_preserve_note_onsets(self):
        for view in ("solo", "written", "concert", "playback", "combined"):
            with self.subTest(view=view), tempfile.TemporaryDirectory() as tmp:
                directory = Path(tmp)
                src = directory / "tags.ly"
                src.write_text(SOURCE.replace("__VIEW__", view), encoding="utf-8")
                process = subprocess.run(
                    ["lilypond", "-dno-print-pages", "-o",
                     str(directory / "tags"), str(src)],
                    cwd=ROOT, capture_output=True, text=True, check=False)
                self.assertEqual(process.returncode, 0,
                                 process.stdout + process.stderr)
                self.assertNotIn("barcheck failed", process.stderr.lower())
                division, events = midi_events(directory / "tags.midi")
                onsets = sorted({
                    tick for tick, kind, _track, data in events
                    if kind == "channel" and len(data) > 2
                    and (data[0] & 0xF0) == 0x90 and data[2] > 0
                })
                self.assertEqual(onsets, [0, 12 * division])


if __name__ == "__main__":
    unittest.main()
