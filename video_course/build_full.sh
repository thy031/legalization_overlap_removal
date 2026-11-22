#!/usr/bin/env bash
# FULL-length version (all 14 sections, 2:56). usage: ./build_full.sh narration_video.mp4 -> final_full.mp4
# Uses index_full.html. Optional sound effects are NOT added (the original SFX were a separate pop track; omit them).
set -e
SRC="$1"; N=5286; H=$((N/2)); mkdir -p out
cp index_overlap_removal.html index_full_run.html
cat > render_full.py <<'PY'
import sys,os,subprocess,pathlib
from playwright.sync_api import sync_playwright
a,b,name=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]
ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',f'out/{name}.mp4'],stdin=subprocess.PIPE)
url=pathlib.Path('index_full_run.html').resolve().as_uri()
with sync_playwright() as p:
    br=p.chromium.launch();pg=br.new_page(viewport={'width':1920,'height':1080});pg.goto(url);pg.evaluate('document.fonts.ready');pg.wait_for_timeout(500)
    for f in range(a,b):
        pg.evaluate(f'frame({f/30})');ff.stdin.write(pg.screenshot(type='jpeg',quality=93))
    ff.stdin.close();ff.wait();br.close()
PY
python3 render_full.py 0 $H f1 & python3 render_full.py $H $N f2 & wait
printf "file f1.mp4\nfile f2.mp4\n" > out/listf.txt
ffmpeg -y -f concat -i out/listf.txt -c copy out/full_only.mp4
ffmpeg -y -i out/full_only.mp4 -i "$SRC" -filter_complex "[1:a]aresample=24000,apad[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 128k -t 176.2 final_full.mp4
