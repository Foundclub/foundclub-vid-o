#!/usr/bin/env bash
# Recolle l'épisode à partir des 12 morceaux de a-monter/bourbier/ (coupés à 2 min pour passer sous les 100 Mo de GitHub).
# Usage : outils/recoller.sh   (depuis clips-bourbier/)
set -euo pipefail
mkdir -p source
for f in ../a-monter/bourbier/partie-*.mp4; do echo "file '$(realpath "$f")'"; done > source/liste.txt
ffmpeg -v error -y -f concat -safe 0 -i source/liste.txt -c copy source/episode.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 source/episode.mp4
