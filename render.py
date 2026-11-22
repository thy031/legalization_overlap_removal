"""Render the animation (index.html) to MP4 frames. Needs: python3, playwright+chromium, ffmpeg.
usage: python3 render.py START_FRAME END_FRAME NAME      (30 fps; frames are OUTPUT time)
The sections 'browser lab' (106.33-143.7 s of the narration) are skipped by the time mapping below.
"""
import sys, os, subprocess, pathlib
from playwright.sync_api import sync_playwright
a, b, name = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
FPS, CUT_START, GAP = 30, 106.33, 37.37
os.makedirs('out', exist_ok=True)
ff = subprocess.Popen(['ffmpeg','-v','error','-y','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-',
                       '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',f'out/{name}.mp4'], stdin=subprocess.PIPE)
url = pathlib.Path('index.html').resolve().as_uri()
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width':1920,'height':1080})
    pg.goto(url); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
    for f in range(a, b):
        t = f / FPS
        pg.evaluate(f'frame({t if t < CUT_START else t + GAP})')   # frame(t) draws the scene for narration time t
        ff.stdin.write(pg.screenshot(type='jpeg', quality=93))
    ff.stdin.close(); ff.wait(); br.close()
