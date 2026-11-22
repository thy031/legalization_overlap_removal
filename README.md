# Module 2 · Lesson 3: Overlap Removal (Legalization for EDA)

An interactive web-based lesson, animated video pipeline, and Python algorithm toolkit for **Overlap Removal** (detailed placement / legalization) in Electronic Design Automation (EDA).

---

## Directory Structure

```text
legalization_l5/
├── index.html                            # Main interactive course web page (video player, browser lab, game, quiz)
├── overlap_removal_lesson_animated.mp4   # Primary animated lesson video served to the web player
├── final.mp4                             # Rendered short-cut lesson video (middle lab/track sections trimmed)
├── final_full.mp4                        # Rendered full-length lesson video (all sections, 2:56)
├── quiz.json                             # Multiple-choice assessment questions, answers, and explanations
├── build_vtt_or.py                       # Script to generate English, Chinese, and bilingual .vtt captions
├── force_directed_place.py               # Python reference implementation for force-directed placement
├── render.py                             # Headless Chromium + FFmpeg frame renderer (short-cut timeline)
├── render_full.py                        # Headless Chromium + FFmpeg frame renderer (full timeline)
├── transcript_en.md                      # Timestamped English narration script
├── transcript_zh.md                      # Timestamped Chinese narration script
├── DESIGN.md                             # Lesson visual and instructional design notes
├── SCRIPT.md                             # Narration and storyboard timing script
├── video_course/                         # Animated SVG slide deck source and video build scripts
│   ├── index_overlap_removal.html        # SVG animation frames and timeline for the Overlap Removal lesson
│   ├── index_full.html                   # Full-length SVG animation template
│   ├── index_full_run.html               # Working copy of the HTML animation rendered by render_full.py
│   ├── build.sh                          # Shell script to build the trimmed video (final.mp4)
│   └── build_full.sh                     # Shell script to build the full video (final_full.mp4)
├── captions/                             # WebVTT subtitle tracks for the HTML5 video player
│   ├── or-short-en.vtt                   # English captions
│   ├── or-short-zh.vtt                   # Chinese captions
│   └── or-short-bilingual.vtt            # Bilingual (English + Chinese) captions
└── out/                                  # Intermediate video segments created during rendering
    ├── f1.mp4                            # First half of rendered video frames
    ├── f2.mp4                            # Second half of rendered video frames
    ├── full_only.mp4                     # Concatenated silent video frames before audio muxing
    └── listf.txt                         # FFmpeg concat file list
```

---

## File Explanations

### 1. Web Course Interface & Video Assets
* **`index.html`**  
  The main interactive learning page. Includes the HTML5 `<video>` player with multi-language subtitle tracks, an interactive SVG fallback player, a **Browser Tool** for testing snap-and-pack legalization, a **Game** tab (matching terms and layout missions), **Course Notes**, and an interactive **Quiz**.
* **`overlap_removal_lesson_animated.mp4`**  
  The primary H.264 (`avc1`) + AAC lesson video loaded by `index.html`.
* **`final.mp4`**  
  The trimmed build of the animated lesson (`~2:18`), where the browser-lab walkthrough section (`106.33s–143.70s`) is cut out for a shorter overview clip.
* **`final_full.mp4`**  
  The complete, unedited build of the animated lesson (`~2:56`, 5,286 frames at 30 fps) with synced narration audio.
* **`quiz.json`**  
  JSON data file containing the lesson's self-check quiz questions, choices, correct indices, and feedback explanations loaded dynamically by `index.html`.

### 2. Subtitles & Transcripts
* **`build_vtt_or.py`** *(also referenced as `built_vtt_or.py`)*  
  Parses `transcript_en.md` and `transcript_zh.md`, aligns English and Chinese sentences proportionally by word/character length, and outputs WebVTT files into `captions/` with responsive `::cue` font sizing.
* **`captions/or-short-en.vtt`**  
  English WebVTT subtitle track attached to the `<video>` player.
* **`captions/or-short-zh.vtt`**  
  Chinese (Simplified) WebVTT subtitle track attached to the `<video>` player.
* **`captions/or-short-bilingual.vtt`**  
  Combined two-line English and Chinese WebVTT subtitle track.
* **`transcript_en.md` / `transcript_zh.md`**  
  Source markdown transcripts containing section timestamps (`MM:SS — Title`) and narration paragraphs used by `build_vtt_or.py`.

### 3. Animated Video Source & Build Pipeline
* **`video_course/index_overlap_removal.html`**  
  Self-contained HTML + inline SVG + JavaScript animation engine that draws every frame of the Overlap Removal lesson at `1920×1080` via `frame(t)` (title card, two-phase snap & pack diagram, pseudocode, 5-step walkthrough, pitfalls, and summary).
* **`video_course/index_full.html` & `video_course/index_full_run.html`**  
  Full-timeline HTML animation source and the temporary working copy (`index_full_run.html`) read by `render_full.py` during batch rendering.
* **`render.py`**  
  Uses Python Playwright (headless Chromium) to capture screenshots of `frame(t)` at 30 fps for the short-cut timeline (skipping the `106.33s–143.7s` gap) and pipes MJPEG frames into FFmpeg to produce `out/q1.mp4` and `out/q2.mp4`.
* **`render_full.py`**  
  Renders the continuous full-length timeline from `index_full_run.html` at 30 fps (`1920×1080`, H.264 `yuv420p`) into `out/f1.mp4` and `out/f2.mp4`.
* **`video_course/build.sh` & `video_course/build_full.sh`**  
  Build automation scripts that run two parallel renderer workers, concatenate the video chunks via FFmpeg, and mux the narration audio track into `final.mp4` or `final_full.mp4`.

### 4. Algorithm Reference & Design Docs
* **`force_directed_place.py`**  
  Standalone Python reference implementation for Module 2's placement track (computing neighbor averages, center pull, damped updates, and Half-Perimeter Wirelength / HPWL).
* **`DESIGN.md` & `SCRIPT.md`**  
  Design specification and narration storyboard documenting scene timings, color palette, typography, and pedagogical structure.

---

## Quick Start

### 1. Run the Lesson Locally
Start a local HTTP server from the directory containing `index.html` (or its parent course root) so `fetch()` requests for `quiz.json`, `.vtt` captions, and `.mp4` video work properly:

```bash
python3 -m http.server 8001
```
Then open `http://localhost:8001/` in your browser.

### 2. Regenerate Caption Files
After editing `transcript_en.md` or `transcript_zh.md`, rebuild all three `.vtt` files in `captions/`:

```bash
python3 build_vtt_or.py
```

### 3. Rebuild the Animated Video
After modifying `video_course/index_overlap_removal.html`, re-render and mux with a narration audio source:

```bash
cd video_course
cp index_overlap_removal.html index_full.html
chmod +x build_full.sh
./build_full.sh /path/to/narration_source.mp4
```