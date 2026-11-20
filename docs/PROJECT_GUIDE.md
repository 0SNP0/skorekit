# ScoreKit project integration guide

ScoreKit is a reusable LilyPond framework consumed by an **independent score repository**. The score repository contains musical sources and owns the release; the toolkit supplies building, verification, engraving helpers and a viewer. Install the dependency at `scorekit/` underneath the score root. This guide's commands are run from that root.

## Required project layout

```text
score-repository/
├── score.ly                     # Written/transposed full score
├── concert-score.ly             # Concert-pitch score
├── orchestra.ily                # Printed staff organization
├── metadata.ily                 # Work metadata and printable credits
├── music/                       # Canonical music and optional JSON maps
├── parts/                       # Separate musician parts
│   └── combined/               # Optional combined-print parts
├── site/                         # Optional project-owned Pages home page
├── .github/workflows/           # Project-owned triggers and image digest
└── scorekit/                    # ScoreKit Git submodule
```

Engraving/layout templates live under `scorekit/lilypond/`. Each instrument should have a single authoritative source of notes, rhythm, articulation, slurs and genuine dynamics. Combined-specific stems, voice labels, rest positions and duplicate-dynamic suppression belong in a **combined print layer**, not in an individual instrument's music. Keep the rendered combined staff equivalent in the full score and extracted combined part.

Optional settings: `music/playback-map.json` for performance-route assertions; `music/view-audio-map.json` for exceptional mappings between combined parts and audio stems.

## Local build

You need Python 3, LilyPond (the toolkit's legacy install pin is currently `2.26.0`), and the fonts required by your score. For MIDI rendering and the interactive viewer, install FluidSynth, FFmpeg and an appropriate SoundFont (plus `pypdf` for PDF page checks).

```bash
python3 scorekit/scripts/check_music_structure.py
python3 scorekit/scripts/build.py build
python3 scorekit/scripts/build.py package
```

The build creates A4 PDF scores and parts under `dist/pdf/`, with a Git-derived revision in printed metadata. The package step writes release-ready ZIP bundles to `dist/packages/`.

```bash
python3 scorekit/scripts/build.py build --audio --soundfont /path/to/MS_Basic.sf3
python3 scorekit/scripts/build.py package --full
python3 scorekit/viewer/serve.py
```

These additional steps render the performance MIDI, individual and mixed MP3 tracks, SVG score pages, a measure-synchronized viewer manifest and timeline. Intermediate MIDI remains under `build/` and is not published. The audio mix is normalized with **one constant gain**, not dynamic-range compression.

The print pipeline separately records `music_hash` (music content), `print_hash` (printed notation/layout fingerprint) and `pdf_sha256` (exact PDF bytes, including revision-dependent footer). See [playback markers](PLAYBACK_MARKERS.md) for repeat/D.C. route tracking and [cue notes](CUE_NOTES.md) for duration-safe quotation.

## GitHub Actions and releases

GitHub workflows belong in the **score repository**; workflows placed in a Git submodule are not loaded as GitHub Actions. The typical build workflow invokes `scorekit/actions/build` for PDFs and then `scorekit/actions/media` for the MIDI/audio/viewer stage. The second job downloads and reuses the PDFs instead of reprinting them:

```bash
# PDF stage:
python3 scorekit/scripts/build.py build
python3 scorekit/scripts/build.py package

# Media stage, after restoring the PDF artifact:
python3 scorekit/scripts/build.py build --audio --reuse-pdf
python3 scorekit/scripts/build.py package --full
```

Only a published `v*` release triggers `scorekit/actions/release` to attach printable PDFs, the orchestra MP3 and PDF/audio/viewer ZIP bundles. Once the upload is complete it dispatches `scorekit-viewer-update`, which the score repository's Pages workflow uses to deploy **only the latest release**. A push to `main` does not publish the viewer. See [site template](../site-template/README.md) and [viewer guide](../viewer/README.md).

Routine CI should build delivery artifacts promptly; keep developer regression checks under `scorekit/tests/` outside normal workflows unless a score project explicitly opts in.

## Version pinning

For regular CI the consumer's workflow pins **one immutable container image digest**, reused by the PDF and media jobs. The prepared image supplies LilyPond, fonts, FluidSynth, FFmpeg, PDF dependencies and SoundFont. GitHub must choose this image before checking out the ScoreKit submodule.

The separate `scorekit/config/lilypond-version.txt` pin controls **only** the fallback installer at `scorekit/actions/install-lilypond` on legacy/non-container Ubuntu workflows. Updating that file alone does **not** upgrade the regular CI environment; a verified new image digest must be published and explicitly pinned in the score repository workflow.

## Further reading

- [Architecture](ARCHITECTURE.md) and [code style](CODE_STYLE.md)
- [Combined staves](PART_COMBINING.md) and [cue notes](CUE_NOTES.md)
- [Playback markers](PLAYBACK_MARKERS.md), [SoundFonts](SOUNDFONTS.md)
- [Importing MuseScore material](IMPORT_FROM_MUSESCORE.md)
