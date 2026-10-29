#!/usr/bin/env bash
# Assemble, rend l'image, fabrique le son (musique + bruitages), règle à -14 LUFS, mesure APRÈS l'encodage, décode en entier.
# Usage : outils/rendre.sh <nom-de-sortie> [CRF, défaut 18]   SANS_RENDU=1 : reprendre le son sur l'image déjà rendue
set -euo pipefail
cd "$(dirname "$0")/.."
NOM=${1:?nom de sortie}; CRF=${2:-18}
python outils/assembler.py
npx hyperframes lint
[ -n "${SANS_RENDU:-}" ] || npx hyperframes render -f 30 --crf "$CRF" -o "rendus/$NOM-brut.mp4" --quiet --frames-cache-dir "/d/App/video/rushs/cache-hyperframes"
DUREE=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "rendus/$NOM-brut.mp4")
mkdir -p medias/sons
python outils/mixer.py "$DUREE" medias/sons/piste.wav
ENTREES=(-i "rendus/$NOM-brut.mp4" -i medias/sons/piste.wav)
CHAINE="afade=t=in:st=0:d=0.05,aresample=192000,alimiter=limit=0.708:attack=2:release=60:level=0:latency=1,aresample=48000"
mesurer() { ffmpeg -hide_banner "${ENTREES[@]}" -filter_complex "[1:a]volume=${1}dB,$CHAINE,ebur128" -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}'; }
G=$(python -c "print(round(-14 - ($(mesurer 0)), 2))")
G=$(python -c "print(round($G - 14 - ($(mesurer "$G")), 2))")
echo "gain du réglage final : $G dB"
ffmpeg -y -v error "${ENTREES[@]}" -filter_complex "[1:a]volume=${G}dB,$CHAINE[son]" -map 0:v -map "[son]" -shortest \
  -c:v copy -c:a aac -b:a 192k -ar 48000 -movflags +faststart "rendus/$NOM.mp4"
ffprobe -v error -show_entries format=duration,size -of compact "rendus/$NOM.mp4"
ffmpeg -hide_banner -i "rendus/$NOM.mp4" -vn -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2
ffmpeg -v error -i "rendus/$NOM.mp4" -f null - && echo "décodage complet : 0 erreur"
