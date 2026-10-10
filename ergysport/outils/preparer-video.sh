#!/usr/bin/env bash
# Prepare medias/video/source.mp4 a partir de l'original (a-monter/ach10-ergysport.mov, deja monte par ach10 :
# loupe d'ouverture, logo Ergysport incruste vers 10 s) : 1080x1920, 30 i/s, une image cle par seconde, son AAC.
set -euo pipefail
cd "$(dirname "$0")/.."
ffmpeg -v error -y -i ../a-monter/ach10-ergysport.mov -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30" \
  -c:v libx264 -crf 16 -preset medium -g 30 -keyint_min 30 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart medias/video/source.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 medias/video/source.mp4
