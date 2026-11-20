# ScoreKit

**Reusable LilyPond tooling for score editions.** ScoreKit provides engraving helpers, score/part builds, PDF and audio packaging, an interactive SVG viewer, and GitHub Actions integration. It does not contain a composition, instrumentation, or project-specific musical decisions.

ScoreKit has its own codebase and documentation. A **score repository** owns the notation, metadata, print configurations, release tags, and GitHub Pages website. Install ScoreKit inside each score repository at `scorekit/` (typically as a Git submodule); all commands below run from the **score repository root**, not from the ScoreKit checkout.

## What is included

| Directory | Purpose |
|---|---|
| [`lilypond/`](lilypond/) | Generic score/part layouts, printed Git version, cue, rest, transposition, instrument-switching, and playback helpers |
| [`scripts/`](scripts/) | LilyPond builds, PDF/MIDI validation, MP3 rendering, SVG and timeline export, print fingerprints and release packages |
| [`actions/`](actions/) | Reusable composite actions for PDF, media, releases, and a legacy LilyPond installer |
| [`viewer/`](viewer/README.md) | Interactive score viewer, Pages site builder, latest-release publisher, local server |
| [`site-template/`](site-template/README.md) | Example per-score website and Pages workflow |
| [`docs/`](docs/PROJECT_GUIDE.md) | Integration and engraving guides |
| [`tests/`](tests/) | Developer regression tests, separate from routine artifact-producing CI |
| [`config/`](config/) | Optional catalog URL and LilyPond version pin for the legacy installer |

## Integrate with a score repository

A typical **consumer project** looks like this:

```text
my-score/
├── .github/workflows/build.yml
├── .github/workflows/pages.yml
├── score.ly
├── concert-score.ly
├── orchestra.ily
├── metadata.ily
├── music/
├── parts/
├── site/                      # Optional custom Pages landing page
└── scorekit/                  # ScoreKit Git submodule
```

From the score repository root, configure the real ScoreKit clone URL and add or update the submodule:

```bash
# Set SCOREKIT_REPOSITORY_URL to your actual Git clone URL first.
git submodule add "$SCOREKIT_REPOSITORY_URL" scorekit
git submodule update --init --recursive
```

No ScoreKit remote URL is hard-coded in the framework documentation. The framework does **not** assume a particular GitHub owner/repository. The consumer's `score.ly`, `concert-score.ly`, `orchestra.ily`, `metadata.ily`, and music/part sources provide the input. Some optional project settings live in `music/playback-map.json` and `music/view-audio-map.json`.

The build scripts locate the score project as the parent of `scorekit/`. A standalone checkout of ScoreKit by itself cannot compile a score; place it in a consumer project before invoking the build commands. The consumer owns its workflows because GitHub does not load workflows from submodules.

## Build and preview

Run from `my-score/`:

```bash
python3 scorekit/scripts/check_music_structure.py
python3 scorekit/scripts/build.py build
python3 scorekit/scripts/build.py package
```

For audio, MIDI synchronization and the interactive SVG viewer, install FluidSynth, FFmpeg, a suitable SoundFont, and LilyPond, then run:

```bash
python3 scorekit/scripts/build.py build --audio --soundfont /path/to/MS_Basic.sf3
python3 scorekit/scripts/build.py package --full
python3 scorekit/viewer/serve.py
```

Output is written under `dist/`; temporary inputs and MIDI are kept under `build/`. The published media bundles contain MP3 and viewer data, not intermediate MIDI. For local production of PDF page checks, `pypdf` is recommended. See the [project guide](docs/PROJECT_GUIDE.md) for requirements, layouts and commands.

## CI, releases and Pages

A score repository's `.github/workflows/build.yml` invokes these local composite actions in order:

1. [`actions/build`](actions/build/action.yml) renders the full score, concert score, individual and combined-part PDFs, and an early PDF artifact.
2. [`actions/media`](actions/media/action.yml) reuses those PDFs and produces audio, viewer SVG/JSON, and release-ready archives.
3. [`actions/release`](actions/release/action.yml) attaches PDFs, MP3 and ZIP bundles when a `v*` GitHub Release is published. After uploading assets, it dispatches `scorekit-viewer-update` in the **score repository**.

The score repository's Pages workflow handles that event, downloads **only the latest published release**, and deploys an entirely same-origin static site. Ordinary pushes do **not** republish the public viewer. Each composition has its own website; an optional external catalog only links to those websites. See the [viewer](viewer/README.md) and [site template](site-template/README.md) guides.

**Normal CI uses a prepared, immutable container image pinned by digest in the score repository's workflow**, shared by PDF and media jobs. The image comes from a separate CI-image project and includes LilyPond, fonts, audio/PDF tools and the SoundFont. The consuming workflow must specify that digest: GitHub resolves the job container before checking out submodules. `config/lilypond-version.txt` is **only** the LilyPond version pin used by [the legacy Ubuntu installer](actions/install-lilypond/action.yml); changing it does not change the normal CI image.

Developer regression checks under `tests/` are not automatically added to the release-producing jobs. Avoid unnecessary CI work when adapting ScoreKit.

## Documentation

Start with the [project integration guide](docs/PROJECT_GUIDE.md) and [architecture](docs/ARCHITECTURE.md). For notation and timing, see [code style](docs/CODE_STYLE.md), [combined staves](docs/PART_COMBINING.md), [cue notes](docs/CUE_NOTES.md), [playback markers](docs/PLAYBACK_MARKERS.md), and [SoundFonts](docs/SOUNDFONTS.md).
