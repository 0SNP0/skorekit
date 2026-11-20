% Output-only notation transforms. Instrument music is stored at concert
% (sounding) pitch, without \transpose in the project musical sources.
% Examples: \scorekitNotatedAt d { \clarinetOneMusic } for B-flat,
% \scorekitNotatedAt a { \altoSaxMusic } for E-flat, or
% \scorekitNotatedAt c' { \contrabassesMusic } for octave notation.
% Never apply these notation-only transforms to MIDI playback.
scorekitNotatedAt = #(define-music-function (written-c music)
  (ly:pitch? ly:music?)
  #{
    \transpose c #written-c { $music }
  #})
