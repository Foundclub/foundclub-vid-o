#!/usr/bin/env bash
# Assemble index.html, rend la video, puis regle le son a -14 LUFS (niveau des reseaux sociaux).
# Usage : outils/rendre.sh <nom-de-sortie> [qualite CRF, defaut 18]
set -euo pipefail
cd "$(dirname "$0")/.."
NOM=${1:?nom de sortie, ex. ach10-final}; CRF=${2:-18}
python3 -I outils/assembler.py
npx hyperframes lint   # bloque sur une erreur de composition (les chevauchements de la scène 2 sont voulus)
npx hyperframes render -f 30 --crf "$CRF" -o "rendus/$NOM-brut.mp4" --quiet
MESURE=$(ffmpeg -hide_banner -i "rendus/$NOM-brut.mp4" -vn -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 \
  | python3 -c "import sys,json; t=sys.stdin.read(); d=json.loads(t[t.rindex('{'):t.rindex('}')+1]); print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -y -v error -i "rendus/$NOM-brut.mp4" -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11:$MESURE:linear=true" \
  -c:a aac -b:a 192k -ar 48000 -movflags +faststart "rendus/$NOM.mp4"
ffprobe -v error -show_entries format=duration,size -of compact "rendus/$NOM.mp4"
ffmpeg -hide_banner -i "rendus/$NOM.mp4" -vn -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1
