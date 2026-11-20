% Reusable single-player instrument switching.
% Change the visible staff name and its actual General MIDI timbre together.
% A player may invoke this command as often as needed, including after repeats.
switchInstrument = #(define-music-function
  (full-name short-name midi-name)
  (string? string? string?)
  #{
    \set Staff.instrumentName = #full-name
    \set Staff.shortInstrumentName = #short-name
    \set Staff.midiInstrument = #midi-name
  #})

% Piccolo sounds one octave above its conventional written notation.
% Tag filtering selects the correct representation for conductor scores,
% written player parts and concert-pitch playback from the SAME note events.
% The canonical notes are always the actual sounding pitches. Only the
% written piccolo part is displayed one octave lower. Concert and MIDI
% use those original sounding pitches without any pitch conversion.
scorekitPiccoloNotes = #(define-music-function (notes) (ly:music?)
  #{
    \tag #'written { \transpose c c, { $notes } }
    \tag #'concert { $notes }
    \tag #'playback { $notes }
  #})
