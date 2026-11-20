# LilyPond source guidelines

These are reusable conventions for **score projects consuming ScoreKit**, not definitions of a particular composition.

- Keep each instrument's sounding music in a canonical `music/<instrument>.ily` source. Define the full score's staff organization and measure/rehearsal timeline in project-owned `orchestra.ily` and `music/global.ily`.
- `parts/*.ly` should be wrappers for the original music, score transposition, layout and output settings—not second copies of the score. Keep combined score/part engraving in project-owned `music/combined/` and `parts/combined/`, sharing the **same resolved combined print definition** between the full score and extracted combined part.
- Do not assume automatic `\partCombine` is appropriate. Distinct players usually require independent voices and explicit voice-mode changes; manual player labels, rest displacement and duplicate-marking suppression must remain in the combined print layer.
- Comments naming printed measures must match real timing; `R2.*N` can express full-measure rests, but every tag or cue selection must preserve the duration of all consuming views. Use `\barNumberCheck` near important print-only alternatives.
- Choose written, concert and playback transpositions deliberately; a doubling musician's instrument changes must update printed names and MIDI program without timing drift.
- Keep genuine dynamics, ties, articulations and expression text with the notes. Put score-specific print overrides at the appropriate project-local level; reserve `scorekit/lilypond/` for generic helpers.
- Define credits, titles and a compact filename slug in project-owned `metadata.ily`; Git-derived version and common layout helpers belong in ScoreKit.
- Validate individual parts, combined parts and corresponding score staves visually and compare timing, pitches and playback whenever notation changes.
