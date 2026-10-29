#!/usr/bin/env bash
# Assemble index.html pour un carrousel, rend la vidéo, fabrique la musique et les bruitages, puis règle le son à -14 LUFS.
# Usage : outils/rendre.sh <carrousel> <nom-de-sortie> [qualité CRF, défaut 18]     ex. outils/rendre.sh car-b car-b-v1
# APERCU=5 outils/rendre.sh car-b apercu : seulement les 5 premières secondes
set -euo pipefail
cd "$(dirname "$0")/.."
CAR=${1:?carrousel, ex. car-b}; NOM=${2:?nom de sortie}; CRF=${3:-18}
python outils/assembler.py "$CAR"
npx hyperframes lint
mkdir -p medias/sons
# le cache d'images va sur D: (C: est juste)
[ -n "${SANS_RENDU:-}" ] || npx hyperframes render -f 30 --crf "$CRF" -o "rendus/$NOM-brut.mp4" --quiet --frames-cache-dir "/d/App/video/rushs/cache-hyperframes"
DUREE=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "rendus/$NOM-brut.mp4")
python outils/musique.py musique.json medias/sons/musique.wav
python outils/sons.py sons.json medias/sons/sons.wav "$DUREE"
ENTREES=(-i "rendus/$NOM-brut.mp4" -i medias/sons/musique.wav -i medias/sons/sons.wav)
MELANGE="[1:a][2:a]amix=inputs=2:normalize=0:duration=first,atrim=0:${APERCU:-$DUREE},"
# Chaîne de la méthode (§4) : gain fixe en deux passes, puis limiteur suréchantillonné ; fondu de 50 ms contre le claquement
CHAINE="afade=t=in:st=0:d=0.05,aresample=192000,alimiter=limit=0.708:attack=2:release=60:level=0:latency=1,aresample=48000"
mesurer() { ffmpeg -hide_banner "${ENTREES[@]}" -filter_complex "${MELANGE}volume=${1}dB,$CHAINE,ebur128" -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}'; }
G=$(python -c "print(round(-14 - ($(mesurer 0)), 2))")
G=$(python -c "print(round($G - 14 - ($(mesurer "$G")), 2))")
echo "gain du réglage final : $G dB"
ffmpeg -y -v error "${ENTREES[@]}" -filter_complex "${MELANGE}volume=${G}dB,$CHAINE[son]" \
  -map 0:v -map "[son]" ${APERCU:+-t $APERCU} -c:v copy -c:a aac -b:a 192k -ar 48000 -movflags +faststart "rendus/$NOM.mp4"
ffprobe -v error -show_entries format=duration,size -of compact "rendus/$NOM.mp4"
# Mesure APRÈS l'encodage (méthode §4) et décodage complet
ffmpeg -hide_banner -i "rendus/$NOM.mp4" -vn -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2
ffmpeg -v error -i "rendus/$NOM.mp4" -f null - && echo "décodage complet : 0 erreur"
