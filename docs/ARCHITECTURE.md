# Architecture: ScoreKit and score editions

ScoreKit is a **reusable framework repository**. A composition lives in a **separate score repository** and brings ScoreKit into its checkout at `scorekit/`, normally as a Git submodule. The boundary is intentional: ScoreKit can be updated independently without collecting scores, composers, instrument lists or project-specific engraving decisions.

## Score repository owns

- `score.ly`, `concert-score.ly`, `orchestra.ily` and `metadata.ily`.
- `music/`: each instrument's canonical notes and performance markings, plus optional `playback-map.json` and `view-audio-map.json`.
- `parts/` and `parts/combined/`: instrument print wrappers and manually controlled combined-staff presentation.
- `site/`: optional project website, custom landing page and catalog URL.
- `.github/workflows/`: triggers, the immutable CI image digest, releases and Pages deployment.
- Git tags, GitHub Releases and the musician-facing Pages domain.

## ScoreKit repository owns

- `scripts/`: generic compilation, verification, audio and SVG export, archive preparation.
- `lilypond/`: shared engraving layouts and reusable music helpers.
- `actions/`: local composite actions for PDF, media, release and legacy tool installation.
- `viewer/portal/`: browser-based score/player UI.
- `viewer/build_site.py`, `viewer/publish_latest.py`, `viewer/serve.py`: site construction, import of latest release, local preview.
- `site-template/`: examples copied into score repositories; never a centrally hosted catalog.
- `docs/` and `tests/`: reusable reference material and opt-in developer checks.

Both scripts and project workflow references assume the dependency path `scorekit/`, directly under the score repository root. A ScoreKit-only checkout does not supply the musical inputs required to build or publish a score. Submodule permissions must be configured if the dependency is private.

## Publishing model

The consumer's PDF job builds all printable editions. The media job reuses those PDFs and creates audio, SVG/JSON and packages. For a published release tag, the release action attaches the assets and sends the `scorekit-viewer-update` event. The **consumer's** Pages workflow responds to that event and extracts the latest release directly into same-origin static resources. An ordinary push is not a request to deploy new published music.

The normal CI environment is pinned by immutable image digest **in the score repository workflow**. `config/lilypond-version.txt` is a version pin for the legacy Ubuntu installer only, not a second source of truth for normal CI.

Each score has its own Pages site; an optional catalog is external and contains links rather than copies of the scores' media.
