# Combined instrumental staves

A score repository may print two performers on one staff while keeping **independent editable music sources** and separate extracted parts. ScoreKit does not decide whether players are unison, solo or independent: those are project-level engraving decisions.

## Musical and print layers

- Keep each player's notes, durations, ties, articulations, slurs and real dynamics in their own `music/<instrument>.ily`.
- Put combined-only voice mode, rest offsets, labels and duplicate-marking suppression in a project-owned `music/combined/<desk>.ily` (or equivalent print layer).
- Instantiate **the same combined print music and engraving settings** in `orchestra.ily` and `parts/combined/<desk>.ly`. A successful PDF compilation does not prove the two staves are equivalent.
- Do not duplicate large note sequences inside a separately maintained combined music copy. Factor out shared phrases and assemble print variants only where necessary.

## Engraving rules

Normally print **two separate voices**, with upward stems for the upper voice and downward stems for the lower voice when both are active. Even identical pitches do not authorize automatic unison merging.

Player labels (`I`, `II`, `I, II`, `a2`) are **manually placed** and only in combined print views. They do not automatically change voice modes. With an explicit solo `I` label, print only player I with natural stems (`\oneVoice`), replace II's silent duration with skips **in the combined print stream**, and restore separate voices when the solo mode ends. The corresponding behavior applies to a manual `II` solo passage.

When both players have a full-measure rest, show **one centered shared rest**. When only one rests and both voices are presented, retain its rest and adjust offsets just enough to avoid collisions. Do not change the individual player's rest placement as a shortcut.

Avoid automatic `\partCombine` when it changes stem directions, suppresses notes, invents unwanted labels or alters slurs. If a project intentionally uses it, inspect every affected passage and ensure the full score and extracted combined part still match.

## Required checks

Verify each player's rhythm and pitches across the full score, concert score, combined part, individual part and playback. Every mutually exclusive print branch must retain precisely the original duration; deleting a tagged rest shifts later notes. Inspect stems, rest collisions, shared full-measure rests, slurs, dynamics and manually placed labels in **both** printed contexts.

See [cue notes](CUE_NOTES.md), [code style](CODE_STYLE.md) and the [project guide](PROJECT_GUIDE.md).
