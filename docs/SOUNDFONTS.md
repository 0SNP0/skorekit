# SoundFonts and audio rendering

ScoreKit renders MIDI through **FluidSynth** using a General MIDI SoundFont (SF2 or SF3), then encodes MP3 through FFmpeg. MuseSounds/MuseSampler libraries are not FluidSynth SoundFonts.

**Normal GitHub Actions builds** use a prepared, digest-pinned CI image containing LilyPond, audio tools and **MS Basic.sf3**. The score project's workflow pins the container image; ScoreKit does **not** download a SoundFont on every normal job.

For local builds, provide a compatible file and pass its absolute path or set `SOUNDFONT`:

```bash
python3 scorekit/scripts/build.py build --audio --soundfont /path/to/MS_Basic.sf3
```

A separate, non-container fallback workflow can download MS Basic.sf3 from the [MuseScore source](https://github.com/musescore/MuseScore/tree/0e44d8e1dd7e0cad1fac85915330c5225bd7882e/share/sound) when it is not already available. The project should not commit large SoundFont binaries to ScoreKit.

For licensing information, refer to the [MS Basic SoundFont license](https://github.com/musescore/MuseScore/blob/main/share/sound/MS%20Basic_License.md).
