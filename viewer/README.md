# ScoreKit Viewer

ScoreKit provides the reusable **interactive score viewer**; each consumer score repository owns its music, metadata, releases, landing page and GitHub Pages deployment. A deployed site presents **one score repository's latest published release**, not a central directory of works or a browser for historic versions.

The engine lives in `viewer/portal/`. The Python programs in this directory build a per-project site, import a release's assets, and serve a local preview. Run the commands below from the **score repository root**, with ScoreKit checked out at `scorekit/`.

## Release and site lifecycle

A score repository builds PDF and media artifacts through ScoreKit's actions. When a published `v*` release has received all required PDF, audio and viewer assets, the release action dispatches `scorekit-viewer-update`. The **score repository's** Pages workflow builds its site:

```bash
python3 scorekit/viewer/build_site.py --output _site
python3 scorekit/viewer/publish_latest.py --output _site --repo OWNER/REPO
```

The first command copies `site/` (when present) and the viewer engine into `_site/`. The second uses `gh` to retrieve **only the latest published release** and extracts the viewer ZIP's SVG/JSON and the audio ZIP's MP3s under `_site/viewer/latest/`. It checks the manifest, page files and audio references, then creates `_site/viewer/latest.json` with the release tag, title and URL. The default site-size budget is **650 MiB**; exceeding it fails publication instead of silently omitting assets.

A project's Pages domain serves all notation and audio from the **same origin**; the browser does not download and unpack release ZIPs or require cross-origin access to GitHub assets. PDF documents and older versions remain downloadable in GitHub Releases. Pushing to `main` does not by itself update the published site.

The site workflow belongs at `.github/workflows/pages.yml` in the score repository; see the [site template](../site-template/README.md). The framework repository itself does not publish a composition's Pages site.

## Local preview

Build the score and audio/viewer resources first, then run:

```bash
python3 scorekit/scripts/build.py build --audio --soundfont /path/to/MS_Basic.sf3
python3 scorekit/viewer/serve.py
```

The preview uses local `dist/viewer/` and `dist/audio/` when available. To preview the latest published release instead:

```bash
python3 scorekit/viewer/serve.py --from-release
```

The release option needs Python 3 and GitHub CLI (`gh`) access to the score repository. You may add `--port 8080` or `--no-browser`. Open the local server's root URL (by default `http://127.0.0.1:8000/`); the default landing page forwards to `/viewer/` if the score has not provided its own `site/index.html`.

## Viewer features

- Select the full score, concert score, individual parts, or combined parts. The work and ensemble names come from the project's metadata.
- The highlighted printed measure follows the audio timeline. Click a visible measure to seek to its **first occurrence** in the performance route, including music with repeats or D.C. jumps.
- LilyPond SVG staff lines, barlines and printed measure numbers generate `measure_areas` and `page_viewboxes` in `manifest.json`. Multi-staff parts use a region spanning the complete printed system. A compressed multimeasure rest has one visible area with `last_printed_measure`, so the highlight persists throughout its span.
- SVG pages load on demand and support fit-to-view zoom and manual zoom controls. On narrow screens, the score remains scrollable and the audio controls stay accessible.
- The mixer offers a full-orchestra mix and selectable individual MP3 stems, independent per-track gain and a master volume. Selecting a combined part chooses its constituent tracks. Playback rate can be adjusted separately.
- The player waits for the chosen streams to buffer a common interval and keeps them aligned to a master clock on seek or speed changes; failure to load a selected track stops group playback rather than silently dropping it.
- The latest release's `README.md` appears beside the score with safe Markdown rendering. Relative links target the **published Git tag** in the score repository, not the Pages asset directory.

The site contains no older score versions, no manual repository picker, and no separate ZIP loader. Sound files are requested as needed rather than embedded in the HTML.

## Project-level configuration

**Catalog link:** ScoreKit reads the first non-comment URL from `scorekit/config/catalog-url.txt`. A project can override it with `site/catalog-url.txt`. Without a URL, the navigation control remains disabled. The catalog, if provided, is a separate website linking to independent score sites.

**Combined-part audio:** The exporter normally identifies constituent tracks from the combined part's source includes. Projects with unusual layouts can define `music/view-audio-map.json`; its keys are viewer view IDs and its values are arrays of audio track IDs. Missing referenced tracks are treated as an export error.

**MIDI timing:** Performance-to-print measure mapping comes from the generated MIDI timeline and optional project settings in `music/playback-map.json`. Metadata and measure geometry are generated, never guessed from page screenshots.

See [ScoreKit overview](../README.md), [project guide](../docs/PROJECT_GUIDE.md), and [playback markers](../docs/PLAYBACK_MARKERS.md).
