#!/usr/bin/env bash
# Prépare les médias de la vidéo « Trouver un match amical en 3 étapes » (vendredi 30/10) :
# - medias/broll/ : 2 plans du tournage d'Adel et Clément (déjà recadrés en vertical pour la vidéo collectivités), en 30 i/s ;
# - medias/ecran/etape1.mp4 : l'enregistrement de l'assistant (recette, données fictives : Montrivage), 5 passages accélérés,
#   sans l'étape 2 ni l'étape 4 (leurs petites phrases promettent ce que l'app ne fait pas : captures/LISEZMOI.md §1) ;
# - medias/musique/fond.wav : « Upbeat Acoustic », Stockaudios (Pixabay), prise à partir de 16 s, là où elle monte.
set -euo pipefail
cd "$(dirname "$0")/.."
CAP=/d/App/fc-social/posts/amicaux/captures
BROLL=/d/App/video/collectivites/broll
for b in duel celebration; do
  ffmpeg -v error -y -i "$BROLL/v3-$b.mp4" -an -vf "fps=30,format=yuv420p" -c:v libx264 -crf 16 -g 15 "medias/broll/$b.mp4"
done
# passage : début, fin (s de l'enregistrement), durée à l'écran (s)
PASSAGES=("0.6 3.4 1.4" "6.5 31.9 2.6" "35.7 45.9 1.4" "46.1 55.3 1.0" "55.4 58.7 1.4")
F=""; L=""; i=0
for p in "${PASSAGES[@]}"; do
  set -- $p; v=$(python -c "print(round(($2-$1)/$3, 4))")
  F+="[0:v]trim=$1:$2,setpts=(PTS-STARTPTS)/$v,fps=30,trim=0:$3,setpts=PTS-STARTPTS[v$i];"; L+="[v$i]"; i=$((i+1))
done
ffmpeg -v error -y -i "$CAP/04-10_assistant_video_vitesse_reelle.mp4" -filter_complex "${F}${L}concat=n=$i:v=1:a=0,format=yuv420p[v]" \
  -map "[v]" -c:v libx264 -crf 16 -g 15 -an medias/ecran/etape1.mp4
ffmpeg -v error -y -ss 16 -t 26 -i /d/App/video/complexes/assets/musique/candidates/L_upbeat-acoustic_stockaudios_113986.mp3 \
  -ar 48000 -ac 2 medias/musique/fond.wav
for f in medias/broll/*.mp4 medias/ecran/etape1.mp4 medias/musique/fond.wav; do echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)"; done
