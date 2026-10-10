#!/usr/bin/env bash
# Prepare medias/video/source.mp4 : la video de l'orateur SANS la prise en double
# (24,433 -> 28,067 s de l'original : « ...pour disputer le Mondial » redit juste apres),
# 1080x1920, 30 i/s, une image cle par seconde, son -> AAC.
set -euo pipefail
cd "$(dirname "$0")/.."
ffmpeg -v error -y -i ../a-monter/world-cup.mp4 -filter_complex \
 "[0:v]trim=0:24.433,setpts=PTS-STARTPTS[v1];[0:a]atrim=0:24.433,asetpts=PTS-STARTPTS[a1];\
  [0:v]trim=28.067,setpts=PTS-STARTPTS[v2];[0:a]atrim=28.067,asetpts=PTS-STARTPTS[a2];\
  [v1][a1][v2][a2]concat=n=2:v=1:a=1[v][a];[v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30[vv]" \
 -map "[vv]" -map "[a]" -c:v libx264 -crf 16 -preset medium -g 30 -keyint_min 30 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart medias/video/source.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 medias/video/source.mp4
