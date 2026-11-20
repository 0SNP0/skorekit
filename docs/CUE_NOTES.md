# Cue notes in ScoreKit

The reusable engraving helpers are in \`scorekit/lilypond/cue-notes.ily\`.
Register source music with \`\addQuote\` in the project, never copy the cue
melody, and pass the receiver's original music as the duration source:

\`\`\`lilypond
\include "scorekit/lilypond/cue-notes.ily"
\addQuote "guide" { \guideMusic }
\scorekitCueAlternatives
  "guide" #UP "Guide" { R2.*3 | }
  #'(cuePart cueScore cueConcert cueCombined)
  #'(cueRest)
\`\`\`

\`scorekitCueOrRest\` with \`##t\` displays cue notes on invisible skips
of matching duration. With \`##f\`, it returns the receiver's original
music (typically rests). Its duration must never change with visibility.

Select exactly ONE of each episode's tags, in ONE outer \`\keepWithTag\`
per edition. For example, \`#'(written cueScore)\` in the full score,
\`#'(concert cueConcert)\` in the concert score,
\`#'(written cuePart)\` in the part, and \`#'(playback cueRest)\` in MIDI.
To hide an episode in one edition, choose its rest tag instead.
Nested \`\keepWithTag\` calls can remove the entire cue/rest duration.

Quote canonical source music, preserving slurs and articulations.
Quoted dynamics are excluded. Do not print a second layer of receiver
rests below the quote. MIDI must select the original music, never the cue.
Combined staves show a cue only where it does not duplicate the other
printed player's notes and must match the corresponding score staff.

Test with \`python3 -m unittest discover -s scorekit/tests -p 'test_cue_notes.py'\`
under the pinned LilyPond version; also inspect rendered PDFs and MIDI.
