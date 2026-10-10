#!/usr/bin/env bash
# Prepare les deux videos que lit la composition :
# - medias/video/source.mp4 : la video de l'orateur (1080x1920, 30 i/s, une image cle par seconde) ;
# - medias/enregistrement/enregistrement-30ips.mp4 : l'enregistrement d'ecran a cadence fixe (il etait a cadence variable).
set -euo pipefail
cd "$(dirname "$0")/.."
ffmpeg -v error -y -i ../a-monter/matchs-amicaux.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30" \
  -c:v libx264 -crf 16 -preset medium -g 30 -keyint_min 30 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart medias/video/source.mp4
ffmpeg -v error -y -i medias/enregistrement/enregistrement-ecran.mp4 -vf "fps=30,scale=1000:2166,setsar=1" -an \
  -c:v libx264 -crf 16 -preset medium -g 15 -keyint_min 15 -pix_fmt yuv420p medias/enregistrement/enregistrement-30ips.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 medias/video/source.mp4
