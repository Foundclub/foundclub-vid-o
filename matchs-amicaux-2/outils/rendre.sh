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
# (limiteur à -1 dBFS, sans retard), avant le réglage du son à -14 LUFS.
ENTREES=(-i "rendus/$NOM-brut.mp4"); MELANGE="[0:a]"
if [ -f sons.json ]; then
  mkdir -p medias/sons
  python3 -I outils/sons.py sons.json medias/sons/sons.wav "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "rendus/$NOM-brut.mp4")"
  ENTREES+=(-i medias/sons/sons.wav)
  MELANGE="[0:a][1:a]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.891:level=0:latency=1,"
fi
MESURE=$(ffmpeg -hide_banner "${ENTREES[@]}" -filter_complex "${MELANGE}loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json" -vn -f null - 2>&1 \
  | python3 -c "import sys,json; t=sys.stdin.read(); d=json.loads(t[t.rindex('{'):t.rindex('}')+1]); print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
# La voix de cette vidéo est enregistrée bas (-18,8 LUFS) : loudnorm ne peut pas monter de +4,8 dB d'un bloc et passe en
# mode dynamique, qui laisse passer des crêtes à -0,1 dBFS (mesuré sur apercu-v2). Un limiteur à -2 dBFS les rattrape après coup.
ffmpeg -y -v error "${ENTREES[@]}" -filter_complex "${MELANGE}loudnorm=I=-14:TP=-1.5:LRA=11:$MESURE:linear=true,aresample=48000,alimiter=limit=0.794:level=0:latency=1[son]" \
  -map 0:v -map "[son]" -c:v copy -c:a aac -b:a 192k -ar 48000 -movflags +faststart "rendus/$NOM.mp4"
ffprobe -v error -show_entries format=duration,size -of compact "rendus/$NOM.mp4"
ffmpeg -hide_banner -i "rendus/$NOM.mp4" -vn -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1
