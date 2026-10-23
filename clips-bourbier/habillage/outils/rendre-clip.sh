#!/usr/bin/env bash
# Fabrique un clip vertical : recadrage (si besoin), assemblage, contrôle, rendu, bruitages, son à -14 LUFS.
# Usage : outils/rendre-clip.sh NN   (ex. outils/rendre-clip.sh 18) -> rendus/clip-NN-tiktok.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
: "${HYPERFRAMES_BROWSER_PATH:=$(ls /opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell 2>/dev/null | head -1 || true)}"
export HYPERFRAMES_BROWSER_PATH
NN=${1:?numero du clip, ex. 18}; CLIP=clips/$NN.json; CARRE=medias/video/clip-$NN-carre.mp4
if [ ! -f "$CARRE" ] || [ "$CLIP" -nt "$CARRE" ]; then python3 -I outils/recadrer.py "$CLIP"; fi
python3 -I outils/assembler.py "$CLIP"
npx hyperframes lint
npx hyperframes render -f 30 --crf 18 -o "rendus/clip-$NN-brut.mp4" --quiet
mkdir -p medias/sons
python3 -I outils/sons.py sons.json "medias/sons/sons-$NN.wav" "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "rendus/clip-$NN-brut.mp4")"
# limiteur suréchantillonné : loudnorm en mode linéaire peut laisser passer des crêtes (+1,7 dBFS mesurés sur le clip 15) ; -3 dB de marge, car l'encodage AAC fait remonter les crêtes ; fondu de 50 ms au début : la toute première trame claquait (+1,7 dBFS à 0 s)
LIMITEUR="afade=t=in:st=0:d=0.05,aresample=192000,alimiter=limit=0.708:attack=2:release=60:level=0:latency=1,aresample=48000"
MELANGE="[0:a][1:a]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.891:level=0:latency=1,"
MESURE=$(ffmpeg -hide_banner -i "rendus/clip-$NN-brut.mp4" -i "medias/sons/sons-$NN.wav" -filter_complex "${MELANGE}loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json" -vn -f null - 2>&1 \
  | python3 -c "import sys,json; t=sys.stdin.read(); d=json.loads(t[t.rindex('{'):t.rindex('}')+1]); print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -y -v error -i "rendus/clip-$NN-brut.mp4" -i "medias/sons/sons-$NN.wav" -filter_complex "${MELANGE}loudnorm=I=-14:TP=-1.5:LRA=11:$MESURE:linear=true,${LIMITEUR}[son]" \
  -map 0:v -map "[son]" -c:v copy -c:a aac -b:a 192k -ar 48000 -movflags +faststart "rendus/clip-$NN-tiktok.mp4"
ffprobe -v error -show_entries format=duration,size -of compact "rendus/clip-$NN-tiktok.mp4"
ffmpeg -hide_banner -i "rendus/clip-$NN-tiktok.mp4" -vn -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tr -s " " | tr "\n" " "; echo
