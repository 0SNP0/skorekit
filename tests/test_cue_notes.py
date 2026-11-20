"""Regression test: selecting either of two generic cue episodes never shifts bars."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scorekit" / "scripts"))
from export import midi_events

SOURCE = r'''
\version "2.26.0"
\include "__CUE_HELPER__"
leader = {
  \time 3/4
  __LEADER_NOTES__
}
\addQuote "leader" { \leader }
receivingMusic = {
  \time 3/4
  R2.*2 |
  \scorekitCueAlternatives
    "leader" #UP "Leader" { R2.*2 | }
    #'(showFirst) #'(restFirst)
  R2. |
  \scorekitCueAlternatives
    "leader" #UP "Leader" { R2.*2 | }
    #'(showSecond) #'(restSecond)
  R2. |
  \barNumberCheck #9
  c''2. |
}
\score {
  \new Staff { \keepWithTag #'(__TAGS__) \receivingMusic }
  \layout { }
}
\score {
  \new Staff { \keepWithTag #'(restFirst restSecond) \receivingMusic }
  \midi { }
}
'''


@unittest.skipUnless(shutil.which("lilypond"), "LilyPond unavailable")
class CueNoteEngravingTests(unittest.TestCase):
    def test_two_independently_selected_cues_and_silent_midi(self):
        helper = (ROOT / "scorekit/lilypond/cue-notes.ily").as_posix()
        notes = " ".join(["c''4-. d''4( e''4) |"] * 9)
        for first in (True, False):
            for second in (True, False):
                with self.subTest(first=first, second=second):
                    tags = " ".join([
                        "showFirst" if first else "restFirst",
                        "showSecond" if second else "restSecond",
                    ])
                    source = (SOURCE.replace("__CUE_HELPER__", helper)
                              .replace("__LEADER_NOTES__", notes)
                              .replace("__TAGS__", tags))
                    with tempfile.TemporaryDirectory() as tmp:
                        path = Path(tmp)
                        file = path / "cue.ly"
                        file.write_text(source, encoding="utf-8")
                        result = subprocess.run(
                            ["lilypond", "-dno-point-and-click",
                             "-o", str(path / "cue"), str(file)],
                            cwd=ROOT, capture_output=True, text=True)
                        self.assertEqual(result.returncode, 0,
                                         result.stdout + result.stderr)
                        self.assertNotIn("barcheck failed", result.stderr.lower())
                        midi = path / "cue.midi"
                        self.assertTrue(midi.is_file(), result.stderr)
                        division, events = midi_events(midi)
                        notes_on = [
                            tick for tick, kind, track, data in events
                            if kind == "channel" and (data[0] & 0xF0) == 0x90
                            and len(data) > 2 and data[2] > 0
                        ]
                        self.assertEqual(notes_on, [24 * division])


if __name__ == "__main__":
    unittest.main()
