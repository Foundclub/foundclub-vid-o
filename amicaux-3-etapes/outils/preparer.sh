#!/usr/bin/env bash
# Prépare les médias de la vidéo « Trouver un match amical en 3 étapes » (vendredi 30/10) :
# - medias/broll/ : 2 plans du tournage d'Adel et Clément (déjà recadrés en vertical pour la vidéo collectivités), en 30 i/s ;
# - medias/ecran/etape1.mp4 : l'enregistrement de l'assistant (recette, données fictives : Montrivage), 5 passages accélérés,
#   sans l'étape 2 ni l'étape 4 (leurs petites phrases promettent ce que l'app ne fait pas : captures/LISEZMOI.md §1) ;
# - medias/musique/fond.wav : « Race The Sun », Scott Buckley (CC BY 4.0, crédit obligatoire dans la description), prise à partir de
#   21,8 s : la montée tombe à 2,7 s, quand le téléphone arrive. (« Upbeat Acoustic » abandonnée le 29/10 : la vidéo compo s'en sert.)
set -euo pipefail
cd "$(dirname "$0")/.."
CAP=/d/App/fc-social/posts/amicaux/captures
BROLL=/d/App/video/collectivites/broll
for b in duel celebration; do
  ffmpeg -v error -y -i "$BROLL/v3-$b.mp4" -an -vf "fps=30,format=yuv420p" -c:v libx264 -crf 16 -g 15 "medias/broll/$b.mp4"
done
# passage : début, fin (s de l'enregistrement), durée à l'écran (s)
# Adel (29/10) : « ça va trop vite » ⇒ passages plus courts dans l'enregistrement, moins accélérés (×1,3 à ×3,2 au lieu de ×2 à ×10)
PASSAGES=("0.6 3.4 2.2" "6.5 12.1 3.0" "35.7 41.0 2.0" "46.1 51.2 1.6" "55.4 58.7 2.0")
F=""; L=""; i=0
for p in "${PASSAGES[@]}"; do
  set -- $p; v=$(python -c "print(round(($2-$1)/$3, 4))")
  F+="[0:v]trim=$1:$2,setpts=(PTS-STARTPTS)/$v,fps=30,trim=0:$3,setpts=PTS-STARTPTS[v$i];"; L+="[v$i]"; i=$((i+1))
done
ffmpeg -v error -y -i "$CAP/04-10_assistant_video_vitesse_reelle.mp4" -filter_complex "${F}${L}concat=n=$i:v=1:a=0,format=yuv420p[v]" \
  -map "[v]" -c:v libx264 -crf 16 -g 15 -an medias/ecran/etape1.mp4
ffmpeg -v error -y -ss 21.8 -t 31 -i /d/App/video/collectivites/assets/musique/candidates/U_race-the-sun_scott-buckley_2022.mp3 \
  -ar 48000 -ac 2 medias/musique/fond.wav
for f in medias/broll/*.mp4 medias/ecran/etape1.mp4 medias/musique/fond.wav; do echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)"; done
