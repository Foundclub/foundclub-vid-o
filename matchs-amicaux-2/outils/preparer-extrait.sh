#!/usr/bin/env bash
# Prépare medias/reference/extrait.mp4 : le passage de la vidéo de référence (« Embrouille Entraîneur et Joueur —
# Dimanche prochain je vais jouer », envoyée par Adel le 17/10/2026) de 30,50 à 34,23 s :
# « Et dimanche prochain, je vais jouer ! Je vais jouer, la tête de ma mère, que je vais jouer ! »
# Début et fin dans les silences (mesurés), avant « Maintenant vous allez voir ».
# La vidéo est horizontale (854x480) : elle est posée en pleine largeur au milieu de l'écran vertical,
# sur un fond fait d'elle-même, floutée et assombrie. Son baissé de 4 dB : il est enregistré à -13,9 LUFS,
# la voix d'ach10 à -17,7 LUFS sur le même genre de passage.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p medias/reference
DEBUT=30.50; DUREE=3.7333        # 112 images à 30 i/s
ffmpeg -v error -y -ss "$DEBUT" -i ../a-monter/reference-dimanche-prochain-je-vais-jouer.mp4 -t "$DUREE" -filter_complex \
  "[0:v:0]fps=30,split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=40:2,eq=brightness=-0.06:saturation=0.9[fond];\
[b]scale=1080:608:flags=lanczos,unsharp=5:5:0.5[devant];[fond][devant]overlay=0:656,format=yuv420p[v];\
[0:a:0]aresample=48000,volume=-4dB,afade=t=in:d=0.03,afade=t=out:st=$(python3 -c "print($DUREE-0.06)"):d=0.06[son]" \
  -map "[v]" -map "[son]" -c:v libx264 -crf 16 -preset medium -g 30 -pix_fmt yuv420p -c:a aac -b:a 192k -ac 2 -t "$DUREE" \
  -movflags +faststart medias/reference/extrait.mp4
ffprobe -v error -show_entries stream=codec_type,duration,nb_frames -of compact medias/reference/extrait.mp4
