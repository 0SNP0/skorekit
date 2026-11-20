% Derive a percussion playback voice from a single canonical Drum Kit
% music expression. Each note exists exactly once in the source.
% EventChord is rewritten to contain only the requested drum type.
% Empty chords and rests become invisible duration-preserving skips.
#(define (scorekit-only-drum drum source)
  (music-map
    (lambda (event)
      (if (eq? (ly:music-property event 'name) 'EventChord)
        (let* ((events (ly:music-property event 'elements))
               (selected (filter
                 (lambda (e)
                   (and (eq? (ly:music-property e 'name) 'NoteEvent)
                        (eq? (ly:music-property e 'drum-type) drum)))
                 events))
               (rhythmic (find
                 (lambda (e)
                   (memq (ly:music-property e 'name)
                         '(NoteEvent RestEvent SkipEvent)))
                 events))
               (non-rhythmic (filter
                 (lambda (e)
                   (not (memq (ly:music-property e 'name)
                              '(NoteEvent RestEvent SkipEvent))))
                 events)))
          (if (null? selected)
            (if rhythmic
              (make-music 'SkipEvent
                'duration (ly:music-property rhythmic 'duration))
              event)
            (begin
              (ly:music-set-property! event 'elements
                (append selected non-rhythmic))
              event)))
        event))
    (ly:music-deep-copy source)))
scorekitDrumStem =
#(define-music-function (drum source) (symbol? ly:music?)
  (scorekit-only-drum drum source))
