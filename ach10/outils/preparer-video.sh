#!/usr/bin/env bash
# Prepare medias/video/ach10-source.mp4, la video que lit la composition :
# 1080x1920, 30 images/s, une image cle par seconde (sinon le rendu fige l'image au saut),
# couleurs HDR d'iPhone ramenees en SDR. Part de l'original s'il est la, sinon de la version legere.
# Le son : la voix d'origine, sauf « Cette application, c'est FoundClub » (16,7-18,9 s), repris de la
# prise refaite a-monter/ach10-foundclub.mov (FoundClub prononce a l'anglaise). PRISE=1|2|3, defaut 1.
# Les deux autres FoundClub (vers 34 et 48 s) recoivent le FoundClub de la prise 1 (greffes).
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=medias/video/ach10-original.mov
[ -f "$SRC" ] || SRC=medias/video/ach10-leger.mp4
FILTRE="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30"
TRANSFERT=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of csv=p=0 "$SRC")
if [[ "$TRANSFERT" =~ arib|2084 ]]; then
  FILTRE="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,$FILTRE"
fi
echo "source : $SRC (transfert : ${TRANSFERT:-inconnu})"
python3 -I outils/remplacer-foundclub.py "$SRC" ../a-monter/ach10-foundclub.mov medias/video/ach10-voix.wav "${PRISE:-1}"
ffmpeg -y -i "$SRC" -i medias/video/ach10-voix.wav -map 0:v:0 -map 1:a:0 -vf "$FILTRE" -c:v libx264 -crf 16 -preset medium -g 30 -keyint_min 30 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart medias/video/ach10-source.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 medias/video/ach10-source.mp4
