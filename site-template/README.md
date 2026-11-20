# Per-score GitHub Pages site template

This is an **example for a score repository**, not a website for the ScoreKit framework itself. Each score publishes its own latest release on its own Pages domain. No central ScoreKit catalog or cross-project version picker is required.

## Place the template in a score project

Copy `scorekit/site-template/site/index.html` to the consumer project's `site/index.html` if you want a custom landing page. Copy `scorekit/site-template/.github/workflows/pages.yml` to the consumer's `.github/workflows/pages.yml`. The paths below are relative to the **score repository root**:

```text
my-score/
├── .github/workflows/build.yml         # Project-owned build/release workflow
├── .github/workflows/pages.yml         # Project-owned Pages deployment
├── site/index.html                     # Optional project-specific landing page
├── score.ly, concert-score.ly, metadata.ily, orchestra.ily
├── music/, parts/
└── scorekit/                           # ScoreKit Git submodule
```

The provided landing page reads `viewer/latest.json` to display the work title, ensemble, tag and release download link; no repository name needs to be hard-coded. If `site/index.html` is absent, ScoreKit provides a minimal redirect to `/viewer/`. The project can also override the catalog URL with `site/catalog-url.txt`.

Enable GitHub Pages **GitHub Actions** deployment for the score repository and ensure its release and Pages workflows have the permissions specified in their YAML files. Checkout must initialize submodules.

## Publishing the latest release

The score project's release action uploads the finished PDF, audio and viewer assets to a published `v*` GitHub Release, then sends `repository_dispatch` with event type `scorekit-viewer-update`. The provided Pages workflow responds to **that event**; it does not publish unfinished assets on an ordinary push to `main`.

From the score repository root, the equivalent publishing commands are:

```bash
python3 scorekit/viewer/build_site.py --output _site
python3 scorekit/viewer/publish_latest.py --output _site --repo OWNER/REPO
```

`publish_latest.py` uses Python 3 and the GitHub CLI (`gh`) with access to the **score repository's** releases. In Actions, `GH_TOKEN` provides authentication and `GH_REPO` identifies that repository.

The publisher downloads the latest release's viewer and audio ZIP files, validates the assets, and writes `_site/viewer/latest.json` together with same-origin SVG/JSON and MP3 resources under `_site/viewer/latest/`. PDFs remain available in GitHub Releases. Older released versions are not copied into the Pages site.

## Local preview

After a local audio/viewer build, run:

```bash
python3 scorekit/viewer/serve.py
```

Use `--from-release` to preview the latest published release instead (requires `gh` authentication when necessary), or `--port 8080 --no-browser` for a custom port. The local web server uses a temporary directory, leaving the project files unchanged.

See [ScoreKit Viewer](../viewer/README.md) for playback, highlighting and mixer behavior.
