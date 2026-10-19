#!/usr/bin/env bash
# Prépare les vidéos que lit la composition :
# - medias/video/source.mp4 : la vidéo d'Adel (a-monter/matchs-amicaux-4.mp4, déjà en 1080x1920 à 30 i/s), une image clé par seconde ;
# - medias/enregistrement/enregistrement-30ips.mp4 : l'enregistrement d'écran de la première vidéo, à cadence fixe.
set -euo pipefail
cd "$(dirname "$0")/.."
ffmpeg -v error -y -i ../a-monter/matchs-amicaux-4.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30" \
  -c:v libx264 -crf 16 -preset medium -g 30 -keyint_min 30 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart medias/video/source.mp4
ffmpeg -v error -y -i ../matchs-amicaux/medias/enregistrement/enregistrement-ecran.mp4 -vf "fps=30,scale=1000:2166,setsar=1" -an \
  -c:v libx264 -crf 16 -preset medium -g 15 -keyint_min 15 -pix_fmt yuv420p medias/enregistrement/enregistrement-30ips.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 medias/video/source.mp4
