#!/usr/bin/env bash
# Prépare les vidéos que lit la composition :
# - medias/video/source.mp4 : l'ouverture (3 s sur la première image d'ach10, sans voix, pour le mème « Moi le vendredi /
#   Moi le dimanche » qui n'a pas été tourné) puis les 5 prises d'a-monter/week-end-gache/, coupées au ras des silences ;
# - medias/enregistrement/enregistrement-30ips.mp4 : l'enregistrement d'écran des matchs amicaux (celui des vidéos 3 et 4).
set -euo pipefail
cd "$(dirname "$0")/.."
R=../a-monter/week-end-gache
# prise : début, fin (secondes de la prise), mesurés avec silencedetect (-35 dB, 0,15 s), 0,1 s de marge autour de la voix
PRISES=("IMG_2149 0.55 8.80" "IMG_2152 0.45 4.85" "IMG_2154 0.45 6.40" "IMG_2155 0.00 6.05" "IMG_2157 0.00 4.60")
ENTREES=(-loop 1 -t 3.0 -framerate 30 -i medias/video/ouverture.png -f lavfi -t 3.0 -i anullsrc=r=48000:cl=stereo)
ffmpeg -v error -y -ss 0.55 -i $R/IMG_2149.mp4 -frames:v 1 medias/video/ouverture.png
FILTRE="[0:v]fps=30,format=yuv420p,setsar=1[v0];[1:a]aformat=sample_rates=48000:channel_layouts=stereo[a0];"
LISTE="[v0][a0]"; i=1
for p in "${PRISES[@]}"; do
  set -- $p; ENTREES+=(-i "$R/$1.mp4"); k=$((i + 1))
  FILTRE+="[$k:v]trim=$2:$3,setpts=PTS-STARTPTS,fps=30,format=yuv420p,setsar=1[v$i];"
  FILTRE+="[$k:a]atrim=$2:$3,asetpts=PTS-STARTPTS,aresample=48000,aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.02,afade=t=out:st=$(python3 -c "print(round($3-$2-0.03,3))"):d=0.03[a$i];"
  LISTE+="[v$i][a$i]"; i=$((i + 1))
done
FILTRE+="${LISTE}concat=n=$i:v=1:a=1[v][a]"
ffmpeg -v error -y "${ENTREES[@]}" -filter_complex "$FILTRE" -map "[v]" -map "[a]" \
  -c:v libx264 -crf 16 -preset medium -g 30 -keyint_min 30 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart medias/video/source.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 medias/video/source.mp4
