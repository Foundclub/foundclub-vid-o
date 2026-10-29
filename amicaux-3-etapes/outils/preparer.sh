#!/usr/bin/env bash
# Prépare les médias de la vidéo « Trouver un match amical en 3 étapes » (vendredi 30/10) :
# - medias/broll/ : 2 plans du tournage d'Adel et Clément (déjà recadrés en vertical pour la vidéo collectivités), en 30 i/s ;
# - medias/ecran/etape1.mp4 : l'enregistrement de l'assistant (recette, données fictives : Montrivage), 5 passages accélérés,
#   sans l'étape 2 ni l'étape 4 (leurs petites phrases promettent ce que l'app ne fait pas : captures/LISEZMOI.md §1) ;
# - medias/musique/fond.wav : « Groovy Upbeat Drums and Percussions », SOFRA (Pixabay, pas de Content ID, choisie par Adel le 30/09
#   pour les collectivités), prise à partir de 31,78 s : sa grosse relance (34,23 s) tombe quand le téléphone arrive (2,45 s).
#   Abandonnées le 29/10 : « Upbeat Acoustic » (déjà dans la vidéo compo), « Race The Sun » (Adel : « change la musique »).
set -euo pipefail
cd "$(dirname "$0")/.."
CAP=/d/App/fc-social/posts/amicaux/captures
BROLL=/d/App/video/collectivites/broll
# le plan du duel commence flou (la mise au point se fait) : on le prend à 0,9 s
for b in "duel 0.9" "celebration 0"; do
  set -- $b
  ffmpeg -v error -y -ss $2 -i "$BROLL/v3-$1.mp4" -an -vf "fps=30,format=yuv420p" -c:v libx264 -crf 16 -g 15 "medias/broll/$1.mp4"
done
# passage : début, fin (s de l'enregistrement), durée à l'écran (s)
# Adel (29/10) : « ça va trop vite » ⇒ passages plus courts dans l'enregistrement, moins accélérés (×1,3 à ×3,2 au lieu de ×2 à ×10)
PASSAGES=("0.8 3.4 1.6" "6.5 12.1 2.4" "35.7 41.0 1.8" "55.4 58.7 1.8")
F=""; L=""; i=0
for p in "${PASSAGES[@]}"; do
  set -- $p; v=$(python -c "print(round(($2-$1)/$3, 4))")
  F+="[0:v]trim=$1:$2,setpts=(PTS-STARTPTS)/$v,fps=30,trim=0:$3,setpts=PTS-STARTPTS[v$i];"; L+="[v$i]"; i=$((i+1))
done
ffmpeg -v error -y -i "$CAP/04-10_assistant_video_vitesse_reelle.mp4" -filter_complex "${F}${L}concat=n=$i:v=1:a=0,format=yuv420p[v]" \
  -map "[v]" -c:v libx264 -crf 16 -g 15 -an medias/ecran/etape1.mp4
# - medias/ecran/filtres.mp4 : l'enregistrement d'Adel sur son iPhone (29/10), SEULEMENT le panneau « Filtres » (4,4 -> 16,0 s) :
#   on n'y voit aucun club. Avant et après, sa liste montre de vrais clubs : on montre la liste de recette (02_liste.png).
#   La barre d'état (heure, point rouge d'enregistrement) est coupée.
# - medias/ecran/accueil.mp4 : le même enregistrement, de 0,5 s (la carte « Cotisations impayées » est déjà sortie de l'écran)
#   à 2,85 s (la liste s'ouvre, encore vide : ses vrais clubs n'apparaissent qu'après).
# Les deux sont recadrés au format des captures (1080 × 2424), barre d'état coupée.
REC="/c/Users/adelf/Downloads/ScreenRecording_10-29-2026 17-33-46_1.mp4"
CADRE="crop=1085:2436:47:120,scale=1080:2424,setsar=1"
ffmpeg -v error -y -ss 0.5 -t 2.35 -i "$REC" -an -vf "$CADRE,setpts=PTS/1.1,fps=30,format=yuv420p" -t 2.1 -c:v libx264 -crf 16 -g 15 medias/ecran/accueil.mp4
ffmpeg -v error -y -ss 4.4 -t 11.6 -i "$REC" -an -vf "$CADRE,setpts=PTS/3.6,fps=30,format=yuv420p" -t 3.2 -c:v libx264 -crf 16 -g 15 medias/ecran/filtres.mp4
ffmpeg -v error -y -ss 31.78 -t 31 -i /d/App/video/collectivites/assets/musique/sofra-groovy-upbeat-drums-and-percussions-130592.mp3 \
  -ar 48000 -ac 2 medias/musique/fond.wav
for f in medias/broll/*.mp4 medias/ecran/*.mp4 medias/musique/fond.wav; do echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)"; done
