#!/usr/bin/env bash
# usage: ./build.sh narration_video.mp4   -> final.mp4 (animation + original narration, middle section cut, no sound effects)
set -e
SRC="$1"; N=4165; H=$((N/2))
python3 render.py 0 $H q1 & python3 render.py $H $N q2 & wait
printf "file out/q1.mp4\nfile out/q2.mp4\n" > out/list.txt
ffmpeg -y -f concat -i out/list.txt -c copy out/vid_only.mp4
ffmpeg -y -i out/vid_only.mp4 -i "$SRC" -filter_complex \
"[1:a]aresample=24000,asplit[x][y];[x]atrim=0:106.33,afade=t=out:st=106.2:d=0.12,asetpts=PTS-STARTPTS[a1];[y]atrim=143.7,afade=t=in:d=0.08,asetpts=PTS-STARTPTS[a2];[a1][a2]concat=n=2:v=0:a=1,apad[a]" \
-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 128k -t 138.83 final.mp4
