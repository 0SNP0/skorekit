% Generic, duration-safe orchestral cue notes (LilyPond 2.26).
%
% The receiving player's real music is passed once as the duration source.
% When printing a cue, \skip hides that material while preserving its time;
% when hidden (including MIDI), the original material is returned unchanged.
%
% Register source music with \addQuote in the score project. Never put
% project-specific instruments, labels or measure counts in this helper.

scorekitCueOrRest =
#(define-music-function (show-cue? source direction label receiving-music)
   (boolean? string? ly:dir? string? ly:music?)
   (if show-cue?
       #{
         % Keep phrasing and articulations, not the source's dynamics.
         \set Score.quotedCueEventTypes =
           #'(note-event rest-event tie-event beam-event tuplet-span-event
              articulation-event slur-event)
         <>^\markup \tiny #label
         \cueDuring #source #direction { \skip $receiving-music }
       #}
       receiving-music))

% Tags provide independent choices for each cue episode and each output.
% Select EXACTLY ONE tag from either list, using ONE outer \keepWithTag
% expression per final score/part. Do not nest keepWithTag calls.
scorekitCueAlternatives =
#(define-music-function
   (source direction label receiving-music show-tags rest-tags)
   (string? ly:dir? string? ly:music? list? list?)
   #{
     \tag #show-tags {
       \scorekitCueOrRest ##t #source #direction #label $receiving-music
     }
     \tag #rest-tags {
       \scorekitCueOrRest ##f #source #direction #label $receiving-music
     }
   #})

% For a cue on an octave-transposing written staff, alter the quoted
% pitches in the print source (not the performing instrument's notes).
scorekitCueOctaveUp = #(define-music-function (music) (ly:music?)
  #{ \transpose c c' { $music } #})
