# Force-directed placement lesson — files
- `force_directed_place.py` — runnable reference implementation of the algorithm (`python3 force_directed_place.py`).
- `SCRIPT.md` — the lesson script / explanation, section by section.
- `video_source/index.html` — the whole animation as one HTML+SVG file. `frame(t)` draws any moment `t` (seconds of the
  original narration). Edit text/colours/timings in `SEC` (sections) and `SCH` (reveal times) at the top of the script.
- `video_source/render.py`, `video_source/build.sh` — render frames with Playwright/Chromium, then mux with the original narration
  (`./build.sh original_video.mp4` -> `final.mp4`). Requires python3, `pip install playwright && playwright install chromium`, ffmpeg.
  Fonts used: Poppins (Regular/Medium/Bold) and DejaVu Sans Mono Bold — edit the `@font-face` paths in index.html for your machine.
- Preview in a browser: open `index.html` and run `frame(60)` in the console (or add a slider).

- `DESIGN.md` — full UI/motion design spec (tokens, layers, per-scene layout, animation rules).
- `video_source/index_full.html` + `build_full.sh` — the FULL 2:56 version with all 14 sections (browser lab + implement track included).

## Overlap-removal lesson (second video)
- `video_source/index_overlap_removal.html` — same design system, new content (chip 12×6, cells A–F, snap → pack). Open it and run `frame(100)` in the console.
  Cut points: narration 133.53–174.67 s (browser lab + implement track) are skipped (`CUT` in the file). Render with the same `render.py`
  after changing its HTML file name, `CUT_START=133.53`, `GAP=41.14`, frames 0–4974; audio: keep 0–133.53 s and 174.67 s–end of the narration.
# legalization_overlap_removal
