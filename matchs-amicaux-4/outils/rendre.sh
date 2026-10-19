#!/usr/bin/env bash
# Assemble index.html, rend la video, ajoute les bruitages (sons.json), puis regle le son a -14 LUFS (niveau des reseaux sociaux).
# Usage : outils/rendre.sh <nom-de-sortie> [qualite CRF, defaut 18]
set -euo pipefail
cd "$(dirname "$0")/.."
# En session cloud, le navigateur de rendu est deja installe dans /opt/pw-browsers
: "${HYPERFRAMES_BROWSER_PATH:=$(ls /opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell 2>/dev/null | head -1 || true)}"
export HYPERFRAMES_BROWSER_PATH
NOM=${1:?nom de sortie, ex. ach10-final}; CRF=${2:-18}
python3 -I outils/assembler.py
npx hyperframes lint   # bloque sur une erreur de composition (les chevauchements de la scène 2 sont voulus)
npx hyperframes render -f 30 --crf "$CRF" -o "rendus/$NOM-brut.mp4" --quiet
# Sound design : si sons.json existe, la piste de bruitages est fabriquée puis mélangée sous la voix
# avant le réglage du son à -14 LUFS.
ENTREES=(-i "rendus/$NOM-brut.mp4"); MELANGE="[0:a]"
if [ -f sons.json ]; then
  mkdir -p medias/sons
  python3 -I outils/sons.py sons.json medias/sons/sons.wav "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "rendus/$NOM-brut.mp4")"
  ENTREES+=(-i medias/sons/sons.wav)
  MELANGE="[0:a][1:a]amix=inputs=2:normalize=0:duration=first,"
fi
# Réglage du son à -14 LUFS par un gain FIXE puis un limiteur doux à -3 dBFS, suréchantillonné x4 (crêtes entre échantillons).
# Pourquoi pas loudnorm : la voix de cette vidéo est enregistrée bas (-18,8 LUFS), loudnorm ne peut pas monter de +4,8 dB
# d'un bloc et passe en mode dynamique ; il écrase alors les « p » d'ach10 en créneaux que l'encodeur AAC fait déborder
# (mesuré sur apercu-v3 : -2,0 dBFS avant AAC, +1,4 dBFS après, à 6,42 s). Deux passes : le gain est corrigé de ce que
# le limiteur retire.
CHAINE="aresample=192000,alimiter=limit=0.708:attack=2:release=60:level=0:latency=1,aresample=48000"
mesurer() { ffmpeg -hide_banner "${ENTREES[@]}" -filter_complex "${MELANGE}volume=${1}dB,$CHAINE,ebur128" -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}'; }
G=$(python3 -c "print(round(-14 - ($(mesurer 0)), 2))")
G=$(python3 -c "print(round($G - 14 - ($(mesurer "$G")), 2))")
echo "gain du réglage final : +$G dB"
ffmpeg -y -v error "${ENTREES[@]}" -filter_complex "${MELANGE}volume=${G}dB,$CHAINE[son]" \
  -map 0:v -map "[son]" -c:v copy -c:a aac -b:a 192k -ar 48000 -movflags +faststart "rendus/$NOM.mp4"
ffprobe -v error -show_entries format=duration,size -of compact "rendus/$NOM.mp4"
ffmpeg -hide_banner -i "rendus/$NOM.mp4" -vn -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2
